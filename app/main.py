# app/main.py

from fastapi import FastAPI, HTTPException, Request, status, Depends, Body
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import AuthService
from app.utils import validate_username, validate_password, log_login_attempt, measure_execution_time
from app.jwt import get_current_user, oauth2_scheme
from app.models import create_auth_response

app = FastAPI(
    title="Servicio de Autenticación Segura",
    description="Microservicio que gestiona autenticación segura con bloqueo por intentos fallidos.",
    version="1.0.0"
)

# Configurar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, cambiar a orígenes específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """
    Endpoint raíz que proporciona la interfaz de usuario.
    """
    return RedirectResponse(url="/static/index.html")

@app.get("/register", response_class=HTMLResponse)
async def register_form():
    """
    Proporciona información sobre cómo registrar un usuario.
    Redirecciona a la documentación de la API.
    """
    # Redireccionar a la documentación
    return RedirectResponse(url="/docs#/default/register_route_register_post")

@app.get("/test-client", response_class=HTMLResponse)
async def test_client():
    """
    Proporciona una interfaz HTML para probar la API de autenticación.
    """
    with open("test_client.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.post("/login")
@measure_execution_time
async def login_route(
    request: Request,
    username: str = Body(...),
    password: str = Body(...)
):
    """
    Endpoint para iniciar sesión.
    
    Args:
        request: Objeto Request de FastAPI
        username: Nombre de usuario
        password: Contraseña
        
    Returns:
        Dict: Respuesta con mensaje de éxito y token
    """
    ip = request.client.host

    if not validate_username(username):
        log_login_attempt(ip, username, "invalid format")
        return create_auth_response(
            success=False,
            message="Formato de nombre de usuario inválido"
        )

    try:
        result = AuthService.login(username, password)
        log_login_attempt(ip, username, "success")
        return {
            "success": True,
            "message": "Login exitoso",
            "token": result["token"],  # dict con access_token y token_type
            "user": result["user"]     # <-- Cambiado de "user_info" a "user"
        }
    except HTTPException as e:
        log_login_attempt(ip, username, f"failed: {e.detail}")
        return create_auth_response(
            success=False,
            message=e.detail
        )

@app.post("/login/form")
@measure_execution_time
async def login_form(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Endpoint alternativo para iniciar sesión usando formulario OAuth2.
    Útil para integración con otros sistemas.
    """
    ip = request.client.host
    username = form_data.username
    password = form_data.password

    if not validate_username(username):
        log_login_attempt(ip, username, "invalid format")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Nombre de usuario inválido"
        )

    try:
        result = AuthService.login(username, password)
        log_login_attempt(ip, username, "success")
        return result
    except HTTPException as e:
        log_login_attempt(ip, username, f"failed: {e.detail}")
        raise e

@app.post("/login/token")
@measure_execution_time
async def login_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Endpoint especializado para autenticación OAuth2 que devuelve un token JWT.
    Compatible con el flujo estándar de OAuth2 password flow.
    
    Args:
        request: Objeto Request de FastAPI
        form_data: Formulario con username y password
        
    Returns:
        Dict: Respuesta con token JWT
    """
    ip = request.client.host
    username = form_data.username
    password = form_data.password

    if not validate_username(username):
        log_login_attempt(ip, username, "invalid format")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Nombre de usuario inválido"
        )

    try:
        result = AuthService.login(username, password)
        log_login_attempt(ip, username, "success")
        return result
    except HTTPException as e:
        log_login_attempt(ip, username, f"failed: {e.detail}")
        raise e

@app.get("/me")
@measure_execution_time
async def get_current_user_info(username: str = Depends(get_current_user)):
    """
    Endpoint protegido que requiere autenticación JWT.
    Devuelve información del usuario autenticado.
    
    Args:
        username: Nombre de usuario obtenido del token JWT
        
    Returns:
        Dict: Respuesta con información del usuario
    """
    return {
        "success": True,
        "message": "Usuario autenticado",
        "data": {
            "username": username
        }
    }

@app.post("/register")
@measure_execution_time
async def register_route(
    request: Request,
    username: str = Body(...),
    password: str = Body(...),
    confirm_password: str = Body(None)
):
    """
    Registra un nuevo usuario con contraseña cifrada.
    
    Args:
        request: Objeto Request de FastAPI
        username: Nombre de usuario
        password: Contraseña
        confirm_password: Confirmación de contraseña (opcional)
        
    Returns:
        Dict: Respuesta con mensaje de éxito
    """
    ip = request.client.host
    
    # Manual validation
    if not username or len(username) < 3:
        return create_auth_response(
            success=False,
            message="Nombre de usuario inválido. Debe tener al menos 3 caracteres."
        )
    
    if not validate_username(username):
        return create_auth_response(
            success=False,
            message="Formato de nombre de usuario inválido. Solo letras, números y guiones bajos."
        )
    
    # Validate password using the utility function
    password_validation = validate_password(password)
    if not password_validation["valid"]:
        return create_auth_response(
            success=False,
            message="Contraseña inválida: " + " ".join(password_validation["errors"])
        )
    
    # Check if passwords match
    if confirm_password is not None and password != confirm_password:
        return create_auth_response(
            success=False,
            message="Las contraseñas no coinciden"
        )

    try:
        result = AuthService.register_user(username, password)
        log_login_attempt(ip, username, "register_success")
        return create_auth_response(
            success=True,
            message="Usuario registrado correctamente",
            user={"username": result["username"], "created_at": str(result["created_at"])}
        )
    except HTTPException as e:
        log_login_attempt(ip, username, f"register_failed: {e.detail}")
        return create_auth_response(
            success=False,
            message=e.detail
        )