from pydantic import BaseModel, constr, validator, Field

class LoginRequest(BaseModel):
    """Modelo para solicitudes de login."""
    username: str = Field(description="Nombre de usuario")
    password: str = Field(description="Contraseña del usuario")

class RegisterRequest(BaseModel):
    """Modelo para solicitudes de registro de nuevos usuarios."""
    username: str = Field(description="Nombre de usuario")
    password: str = Field(description="Contraseña del usuario")
    confirm_password: str = Field(None, description="Confirmación de contraseña")
    
    @validator('username')
    def username_validator(cls, v):
        """Valida que el nombre de usuario cumpla con los requisitos."""
        if not v:
            raise ValueError("El nombre de usuario no puede estar vacío")
        
        if len(v) < 3:
            raise ValueError("El nombre de usuario debe tener al menos 3 caracteres")
        
        if len(v) > 30:
            raise ValueError("El nombre de usuario debe tener máximo 30 caracteres")
        
        import re
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError("El nombre de usuario solo puede contener letras, números y guiones bajos")
        
        return v
    
    @validator('password')
    def password_validator(cls, v):
        """Valida que la contraseña cumpla con los requisitos de seguridad."""
        if not v:
            raise ValueError("La contraseña no puede estar vacía")
        
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        
        # Verificar presencia de al menos una letra mayúscula
        if not any(c.isupper() for c in v):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula")
        
        # Verificar presencia de al menos una letra minúscula
        if not any(c.islower() for c in v):
            raise ValueError("La contraseña debe contener al menos una letra minúscula")
        
        # Verificar presencia de al menos un número
        if not any(c.isdigit() for c in v):
            raise ValueError("La contraseña debe contener al menos un número")
        
        # Verificar presencia de al menos un carácter especial
        special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?/"
        if not any(c in special_chars for c in v):
            raise ValueError("La contraseña debe contener al menos un carácter especial")
        
        return v
    
    @validator('confirm_password')
    def confirm_password_validator(cls, v, values):
        """Valida que la confirmación de contraseña coincida con la contraseña."""
        if v is None:
            return v
        if 'password' in values and v != values['password']:
            raise ValueError("Las contraseñas no coinciden")
        return v

class AuthResponse(BaseModel):
    """Modelo para respuestas de autenticación."""
    success: bool = Field(description="Indica si la autenticación fue exitosa")
    message: str = Field(description="Mensaje descriptivo")
    token: dict = Field(None, description="Token de autenticación (JWT)")
    user: dict = Field(None, description="Información del usuario")

class UserInfoResponse(BaseModel):
    """Modelo para respuestas con información de usuario."""
    username: str = Field(description="Nombre de usuario")
    disabled: bool = Field(False, description="Indica si la cuenta está deshabilitada")
    created_at: str = Field(None, description="Fecha de creación de la cuenta")

class TokenResponse(BaseModel):
    """Modelo para respuestas con token JWT."""
    access_token: str = Field(description="Token de acceso JWT")
    token_type: str = Field(description="Tipo de token")
    
class PasswordValidationResult(BaseModel):
    """Modelo para resultados de validación de contraseñas."""
    valid: bool = Field(description="Indica si la contraseña es válida")
    errors: list = Field(default_factory=list, description="Lista de errores de validación")

# Simple dictionaries to replace Pydantic models
def create_login_request(username, password):
    return {
        "username": username, 
        "password": password
    }

def create_register_request(username, password, confirm_password=None):
    return {
        "username": username,
        "password": password,
        "confirm_password": confirm_password
    }

def create_auth_response(success, message, token=None, user=None):
    response = {
        "success": success,
        "message": message
    }
    if token:
        response["token"] = token
    if user:
        response["user"] = user
    return response

def create_user_info_response(username, disabled=False, created_at=None):
    return {
        "username": username,
        "disabled": disabled,
        "created_at": created_at
    }

def create_token_response(access_token, token_type="bearer"):
    return {
        "access_token": access_token,
        "token_type": token_type
    }

def create_password_validation_result(valid=True, errors=None):
    if errors is None:
        errors = []
    return {
        "valid": valid,
        "errors": errors
    }
