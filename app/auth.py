# app/auth.py

from datetime import datetime, timedelta
from fastapi import HTTPException
from passlib.context import CryptContext
import os
from typing import Dict, Optional, Tuple

# Configuración de encriptación con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Simulación de almacenamiento en memoria
login_attempts = {}
users_db = {}  # Simulación de base de datos de usuarios
MAX_ATTEMPTS = 5
BLOCK_DURATION = timedelta(minutes=15)

def get_password_hash(password: str) -> str:
    """
    Genera un hash seguro para la contraseña utilizando bcrypt.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica que la contraseña coincida con el hash almacenado.
    """
    return pwd_context.verify(plain_password, hashed_password)

def register_user(username: str, password: str) -> Dict:
    """
    Registra un nuevo usuario con contraseña encriptada.
    """
    if username in users_db:
        raise HTTPException(status_code=400, detail="El usuario ya existe.")
    
    hashed_password = get_password_hash(password)
    users_db[username] = hashed_password
    
    return {"msg": "Usuario registrado exitosamente"}

def initialize_demo_users():
    """
    Inicializa algunos usuarios de demostración.
    """
    if not users_db:
        # Crear usuario de prueba
        register_user("testuser", "secret")
        register_user("admin", "admin123")

# Inicializar usuarios de demostración
initialize_demo_users()

def is_user_blocked(username: str) -> bool:
    user_data = login_attempts.get(username, {"attempts": 0, "blocked_until": None})
    if user_data["blocked_until"] and datetime.now() < user_data["blocked_until"]:
        return True
    return False

def register_login_attempt(username: str, success: bool):
    user_data = login_attempts.get(username, {"attempts": 0, "blocked_until": None})
    if success:
        user_data["attempts"] = 0
        user_data["blocked_until"] = None
    else:
        user_data["attempts"] += 1
        if user_data["attempts"] >= MAX_ATTEMPTS:
            user_data["blocked_until"] = datetime.now() + BLOCK_DURATION
    login_attempts[username] = user_data

def login(username: str, password: str):
    """
    Realiza un login seguro con bloqueo tras múltiples intentos.
    Verifica la contraseña utilizando bcrypt.
    """
    if is_user_blocked(username):
        raise HTTPException(status_code=403, detail="Usuario bloqueado temporalmente.")

    # Verificación de contraseña con bcrypt
    hashed_password = users_db.get(username)
    success = False
    
    if hashed_password:
        success = verify_password(password, hashed_password)
    
    register_login_attempt(username, success)

    if not success:
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")

    return {"msg": "Login exitoso"}