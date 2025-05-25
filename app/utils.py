# app/utils.py

import re
import logging
import time
import os
import json
from datetime import datetime, timedelta
from functools import wraps

# Configuración de logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Configurar también el logging a archivo si es necesario
if os.environ.get("LOG_TO_FILE", "false").lower() == "true":
    file_handler = logging.FileHandler("security.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def validate_username(username):
    """
    Valida que el nombre de usuario cumpla con los requisitos de seguridad.
    
    Args:
        username: Nombre de usuario a validar
    
    Returns:
        True si el nombre de usuario es válido, False en caso contrario
    """
    # Solo permitir letras, números y guiones bajos
    pattern = r'^[a-zA-Z0-9_]+$'
    if not re.match(pattern, username):
        return False
    
    # Longitud entre 3 y 30 caracteres
    if len(username) < 3 or len(username) > 30:
        return False
    
    return True

def validate_password(password):
    """
    Valida que la contraseña cumpla con los requisitos de seguridad.
    
    Args:
        password: Contraseña a validar
    
    Returns:
        Dict con resultado de validación y mensajes
    """
    results = {
        "valid": True,
        "errors": []
    }
    
    # Verificar longitud mínima
    if len(password) < 8:
        results["valid"] = False
        results["errors"].append("La contraseña debe tener al menos 8 caracteres.")
    
    # Verificar presencia de al menos una letra mayúscula
    if not any(c.isupper() for c in password):
        results["valid"] = False
        results["errors"].append("La contraseña debe contener al menos una letra mayúscula.")
    
    # Verificar presencia de al menos una letra minúscula
    if not any(c.islower() for c in password):
        results["valid"] = False
        results["errors"].append("La contraseña debe contener al menos una letra minúscula.")
    
    # Verificar presencia de al menos un número
    if not any(c.isdigit() for c in password):
        results["valid"] = False
        results["errors"].append("La contraseña debe contener al menos un número.")
    
    # Verificar presencia de al menos un carácter especial
    special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?/"
    if not any(c in special_chars for c in password):
        results["valid"] = False
        results["errors"].append("La contraseña debe contener al menos un carácter especial.")
    
    return results

def log_login_attempt(ip: str, username: str, status: str):
    """
    Registra intentos de inicio de sesión.
    
    Args:        ip: Dirección IP desde donde se realiza el intento
        username: Nombre de usuario utilizado
        status: Estado del intento (success, failed, blocked, etc.)
    """
    logger.info(f"Login attempt - IP: {ip} | User: {username} | Status: {status}")

def log_security_event(event_type, description, severity="INFO", user=None):
    """
    Registra eventos de seguridad para auditoría.
    
    Args:
        event_type: Tipo de evento (login, logout, blocked, etc.)
        description: Descripción detallada del evento
        severity: Nivel de severidad (INFO, WARNING, ERROR, CRITICAL)
        user: Usuario relacionado con el evento (opcional)
    """
    log_method = getattr(logger, severity.lower(), logger.info)
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "description": description,
        "user": user
    }
    log_method(f"SECURITY_EVENT: {json.dumps(log_data)}")

def measure_execution_time(func):
    """
    Decorador que mide el tiempo de ejecución de una función.
    
    Args:
        func: Función a medir
    
    Returns:
        Wrapper que mide el tiempo y llama a la función
    """
    import asyncio
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # en milisegundos
        logger.debug(f"Función {func.__name__} ejecutada en {execution_time:.2f} ms")
        return result

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # en milisegundos
        logger.debug(f"Función {func.__name__} ejecutada en {execution_time:.2f} ms")
        return result

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper

def format_response(success, message, error=None, data=None):
    """
    Formatea una respuesta estándar para la API.
    
    Args:
        success: Indica si la operación fue exitosa        message: Mensaje descriptivo del resultado
        error: Mensaje de error en caso de fallo (opcional)
        data: Datos adicionales a incluir en la respuesta (opcional)
        
    Returns:
        Diccionario con la respuesta formateada
    """
    response = {
        "success": success,
        "message": message,
    }
    if error:
        response["error"] = error
    if data:
        response["data"] = data
    return response

def rate_limit(max_calls: int, period: int = 60):
    """
    Decorador para implementar limitación de tasa en endpoints.
    Ayuda a prevenir ataques de fuerza bruta (REQ-SEC-001).
    
    Args:
        max_calls: Número máximo de llamadas permitidas en el periodo
        period: Periodo en segundos para resetear el contador
        
    Returns:
        Decorador que limita la tasa de llamadas
    """
    # Diccionario para almacenar las llamadas por IP
    calls = {}
    
    def decorator(func):
        @wraps(func)
        async def wrapper(request, *args, **kwargs):
            ip = request.client.host
            now = time.time()
            
            # Inicializar o actualizar registro para esta IP
            call_record = calls.get(ip, {"count": 0, "reset_time": now + period})
            
            # Resetear contador si ya pasó el periodo
            if now > call_record["reset_time"]:
                call_record = {"count": 0, "reset_time": now + period}
            
            # Verificar límite
            if call_record["count"] >= max_calls:
                log_security_event(
                    "RATE_LIMIT_EXCEEDED", 
                    f"IP {ip} excedió el límite de tasa ({max_calls} llamadas en {period}s)",
                    "WARNING"
                )
                return format_response(
                    success=False,
                    message="Demasiadas solicitudes",
                    error="Has excedido el límite de solicitudes. Intenta más tarde."
                )
            
            # Incrementar contador
            call_record["count"] += 1
            calls[ip] = call_record
            
            # Ejecutar función original
            return await func(request, *args, **kwargs)
        
        return wrapper
    
    return decorator

def sanitize_input(data: str) -> str:
    """
    Sanitiza entradas de texto para prevenir inyección.
    
    Args:
        data: Texto a sanitizar
        
    Returns:
        str: Texto sanitizado
    """
    # Implementación básica para eliminar caracteres potencialmente peligrosos
    # En un entorno de producción, considerar una librería especializada
    sanitized = re.sub(r"[<>\"'%;()&]", "", data)
    return sanitized

def check_account_lockout(username, login_attempts):
    """
    Verifica si una cuenta está bloqueada por demasiados intentos fallidos.
    
    Args:
        username: Nombre de usuario a verificar
        login_attempts: Diccionario con los intentos de login
    
    Returns:
        Tuple (bool, datetime) - (True si está bloqueada, tiempo hasta desbloqueo)
    
    Ayuda a prevenir ataques de fuerza bruta ("REQ-SEC-001").
    """
    if username not in login_attempts:
        return False, None
    
    user_data = login_attempts[username]
    
    # Verificar si está bloqueada y el bloqueo no ha expirado
    if user_data.get("blocked_until") and user_data["blocked_until"] > datetime.now():
        return True, user_data["blocked_until"]
    
    return False, None

# Otras funciones útiles
def generate_secure_token(length=32):
    """
    Genera un token seguro para uso en operaciones que requieren alta seguridad.
    
    Args:
        length: Longitud del token en bytes
    
    Returns:
        String con el token generado
    """
    import secrets
    return secrets.token_hex(length)
