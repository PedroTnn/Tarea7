# app/jwt.py

from datetime import datetime, timedelta

from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from app.utils import log_security_event, format_response

# Configuración para JWT
# En un entorno de producción, estos valores deberían estar en variables de entorno
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # Clave secreta para firmar tokens
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # REQ-SEC-002: Tiempo de expiración del token

# Configuración para el mecanismo OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class JWTService:
    """Servicio para gestionar la creación y validación de tokens JWT."""
    
    @staticmethod
    def create_access_token(data, expires_delta=None):
        """
        Crea un token JWT con los datos proporcionados y tiempo de expiración.
        
        Args:
            data: Dict con los datos a incluir en el token
            expires_delta: Duración de validez del token (opcional)
        
        Returns:
            Token JWT como string
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return encoded_jwt
    
    @staticmethod
    def decode_token(token):
        """
        Decodifica y verifica un token JWT.
        
        Args:
            token: Token JWT a decodificar
        
        Returns:
            Dict con los datos contenidos en el token
        
        Raises:
            HTTPException: Si el token es inválido o ha expirado
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError as e:
            log_security_event("TOKEN_ERROR", f"Error al decodificar token JWT: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No se pudo validar las credenciales",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    @staticmethod
    def get_current_user(token):
        """
        Obtiene el usuario actual a partir de un token JWT.
        
        Args:
            token: Token JWT
        
        Returns:
            Dict con la información del usuario
        """
        payload = JWTService.decode_token(token)
        username = payload.get("sub")
        
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No se pudo validar las credenciales",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return {"username": username}

# Función para verificar token y obtener usuario actual como dependencia
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Verifica el token JWT y obtiene el usuario actual.
    Se utiliza como dependencia en endpoints protegidos.
    
    Args:
        token: Token JWT proporcionado en la solicitud
    
    Returns:
        Dict con información del usuario actual
    """
    return JWTService.get_current_user(token)

def create_token_response(username):
    """
    Crea un token JWT para un usuario y devuelve la respuesta formateada.
    
    Args:
        username: Nombre de usuario para el que se crea el token
    
    Returns:
        Dict con token de acceso y tipo
    """
    access_token = JWTService.create_access_token(
        data={"sub": username}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
