# app/auth.py

from datetime import datetime, timedelta
from fastapi import HTTPException, status
from passlib.context import CryptContext
from app.utils import measure_execution_time, format_response
from app.jwt import create_token_response  # Importar función para generar tokens JWT
import json
import os

# Configuración de encriptación con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

# Simulación de almacenamiento en memoria
# En un entorno de producción, esto debería ser una base de datos persistente
login_attempts = {}
USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                data = f.read().strip()
                if not data:
                    return {}
                return json.loads(data)
        except Exception as e:
            print(f"[ERROR] No se pudo cargar users.json: {e}")
            return {}
    return {}

def save_users():
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users_db, f, default=str, indent=2)

# Cargar usuarios al iniciar
users_db = load_users()

# Constantes de configuración de seguridad
MAX_ATTEMPTS = 5  # REQ-SEC-001: 5 intentos fallidos
BLOCK_DURATION = timedelta(minutes=15)

class AuthService:
    """Servicio de autenticación que gestiona login, registro e intentos fallidos."""
    
    @staticmethod
    def get_password_hash(password):
        """Genera un hash seguro de la contraseña utilizando bcrypt."""

        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password, hashed_password):
        """Verifica si la contraseña coincide con el hash almacenado."""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def register_login_attempt(username, success):
        """
        Registra un intento de inicio de sesión y bloquea la cuenta si es necesario.
        
        Args:
            username: Nombre de usuario
            success: True si el intento fue exitoso, False en caso contrario
        
        Returns:
            Dict con información del intento y estado de bloqueo
        """
        now = datetime.now()
        
        # Si es la primera vez que vemos este usuario o fue un intento exitoso
        if username not in login_attempts or success:
            if success:
                # Resetear intentos si el login fue exitoso
                login_attempts[username] = {
                    "attempts": 0,
                    "last_attempt": now,
                    "blocked_until": None
                }
            else:
                # Primer intento fallido
                login_attempts[username] = {
                    "attempts": 1,
                    "last_attempt": now,
                    "blocked_until": None
                }
        else:
            # Ya existe un registro para este usuario
            user_data = login_attempts[username]
            
            # Verificar si está bloqueado
            if user_data["blocked_until"] and user_data["blocked_until"] > now:
                # Actualizar intentos pero mantener el bloqueo
                user_data["attempts"] += 1
                user_data["last_attempt"] = now
            else:
                # No está bloqueado o el bloqueo ha expirado
                user_data["attempts"] += 1
                user_data["last_attempt"] = now
                
                # Bloquear después del máximo de intentos
                if user_data["attempts"] >= MAX_ATTEMPTS:
                    user_data["blocked_until"] = now + BLOCK_DURATION
        
        return login_attempts[username]
    
    @classmethod
    @measure_execution_time
    def register_user(cls, username, password):
        """
        Registra un nuevo usuario en el sistema.
        
        Args:
            username: Nombre de usuario
            password: Contraseña en texto plano
        
        Returns:
            Dict con información del usuario registrado
        
        Raises:
            HTTPException: Si el usuario ya existe
        """
        if username in users_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya existe"
            )
        
        # Generar hash de la contraseña
        hashed_password = cls.get_password_hash(password)
        
        # Guardar usuario en la base de datos
        users_db[username] = {
            "username": username,
            "hashed_password": hashed_password,
            "disabled": False,
            "created_at": datetime.now().isoformat()
        }
        save_users()  # <--- Guarda los usuarios cada vez que se registra uno
        return users_db[username]
    
    @classmethod
    @measure_execution_time
    def login(cls, username, password):
        print(f"[DEBUG] Intentando login para usuario: {username}")
        """
        Realiza el proceso de login y maneja los intentos fallidos.
        
        Args:
            username: Nombre de usuario
            password: Contraseña en texto plano
        
        Returns:
            Dict con información del usuario autenticado y token JWT
        
        Raises:
            HTTPException: Si las credenciales son inválidas o el usuario está bloqueado
        """
        # Verificar si el usuario existe
        if username not in users_db:
            print(f"[DEBUG] Usuario '{username}' NO encontrado en users_db. users_db actual: {list(users_db.keys())}")
            # Registrar intento fallido
            attempt_info = cls.register_login_attempt(username, False)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas"
            )
        
        # Obtener información del usuario
        user = users_db[username]
        print(f"[DEBUG] Usuario encontrado: {user}")
        
        # Verificar si la cuenta está bloqueada
        if username in login_attempts and login_attempts[username].get("blocked_until"):
            blocked_until = login_attempts[username]["blocked_until"]
            if blocked_until and blocked_until > datetime.now():
                print(f"[DEBUG] Cuenta bloqueada hasta: {blocked_until}")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Cuenta bloqueada hasta {blocked_until}"
                )
        
        # Verificar contraseña
        password_ok = cls.verify_password(password, user["hashed_password"])
        print(f"[DEBUG] Verificando contraseña: plain='{password}' hash='{user['hashed_password']}' resultado={password_ok}")
        if not password_ok:
            # Registrar intento fallido
            attempt_info = cls.register_login_attempt(username, False)
            print(f"[DEBUG] Intento fallido. attempt_info: {attempt_info}")
            # Verificar si la cuenta ahora está bloqueada
            if attempt_info.get("blocked_until"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Cuenta bloqueada hasta {attempt_info['blocked_until']} después de {MAX_ATTEMPTS} intentos fallidos"
                )
            else:
                attempts_left = MAX_ATTEMPTS - attempt_info["attempts"]
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Credenciales incorrectas. Intentos restantes antes de bloqueo: {attempts_left}"
                )
        
        # Login exitoso, resetear contadores de intentos
        cls.register_login_attempt(username, True)
        print(f"[DEBUG] Login exitoso para usuario: {username}")
        
        # Generar y devolver el token JWT
        token_data = create_token_response(username)
        print(f"[DEBUG] Token generado: {token_data}")
        return {
            "user": user,
            "token": token_data
        }


# Inicializar usuarios de demostración
def initialize_demo_users():
    """
    Inicializa algunos usuarios de demostración.
    """
    if not users_db:
        # Crear usuario de prueba
        AuthService.register_user("testuser", "secret")
        AuthService.register_user("admin", "admin123")
        AuthService.register_user("pedrot", "admin123")
        save_users()

# Inicializar usuarios de demostración al cargar el módulo
initialize_demo_users()

# Funciones de exportación para mantener compatibilidad con código existente
def get_password_hash(password):
    return AuthService.get_password_hash(password)

def verify_password(plain_password, hashed_password):
    return AuthService.verify_password(plain_password, hashed_password)

def register_user(username, password):
    return AuthService.register_user(username, password)

def is_user_blocked(username):
    return AuthService.is_user_blocked(username)

def register_login_attempt(username, success):
    return AuthService.register_login_attempt(username, success)

def login(username, password):
    return AuthService.login(username, password)