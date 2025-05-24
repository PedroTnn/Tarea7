# app/main.py

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.auth import login as auth_login, register_user
from app.utils import validate_username, log_login_attempt
from pydantic import BaseModel

class UserCredentials(BaseModel):
    username: str
    password: str

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

@app.get("/register")
async def register_form():
    """
    Proporciona información sobre cómo registrar un usuario.
    Redirecciona a la documentación de la API.
    """
    from fastapi.responses import HTMLResponse, RedirectResponse
    
    # Opción 1: Redireccionar a la documentación
    return RedirectResponse(url="/docs#/default/register_route_register_post")
    
    # Opción 2: Un formulario HTML simple (descomentar para usar)
    # html_content = """
    # <!DOCTYPE html>
    # <html>
    # <head>
    #     <title>Registro de Usuario</title>
    #     <style>
    #         body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
    #         .container { max-width: 500px; margin: 0 auto; }
    #         input, button { padding: 8px; margin: 5px 0; width: 100%; }
    #         button { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
    #     </style>
    # </head>
    # <body>
    #     <div class="container">
    #         <h1>Registro de Usuario</h1>
    #         <form id="registerForm">
    #             <input type="text" id="username" placeholder="Nombre de usuario" required>
    #             <input type="password" id="password" placeholder="Contraseña" required>
    #             <button type="submit">Registrar</button>
    #         </form>
    #         <p>Para probar la API, utilice la <a href="/docs">documentación interactiva</a>.</p>
    #         <div id="result"></div>
    #     </div>
    #     <script>
    #         document.getElementById('registerForm').addEventListener('submit', async (e) => {
    #             e.preventDefault();
    #             const username = document.getElementById('username').value;
    #             const password = document.getElementById('password').value;
    #             
    #             try {
    #                 const response = await fetch('/register', {
    #                     method: 'POST',
    #                     headers: { 'Content-Type': 'application/json' },
    #                     body: JSON.stringify({ username, password })
    #                 });
    #                 

    #                 const data = await response.json();
    #                 document.getElementById('result').innerHTML = 
    #                     `<p style="color: ${response.ok ? 'green' : 'red'}">
    #                         ${response.ok ? data.msg : data.detail}
    #                     </p>`;
    #             } catch (error) {
    #                 document.getElementById('result').innerHTML = 
    #                     `<p style="color: red">Error: ${error.message}</p>`;
    #             }
    #         });
    #     </script>
    # </body>
    # </html>
    # """
    # return HTMLResponse(content=html_content)

@app.get("/test-client")
async def test_client():
    """
    Proporciona una interfaz HTML para probar la API de autenticación.
    """
    with open("test_client.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.post("/login")
async def login_route(request: Request, user: UserCredentials):
    ip = request.client.host
    username = user.username
    password = user.password

    if not validate_username(username):
        log_login_attempt(ip, username, "invalid format")
        raise HTTPException(status_code=400, detail="Nombre de usuario inválido")

    try:
        result = auth_login(username, password)
        log_login_attempt(ip, username, "success")
        return result
    except HTTPException as e:
        log_login_attempt(ip, username, "failed")
        raise e

@app.post("/register")
async def register_route(request: Request, user: UserCredentials):
    """
    Registra un nuevo usuario con contraseña cifrada.
    """
    ip = request.client.host
    username = user.username
    password = user.password

    if not validate_username(username):
        log_login_attempt(ip, username, "register_invalid_format")
        raise HTTPException(status_code=400, detail="Nombre de usuario inválido")

    try:
        result = register_user(username, password)
        log_login_attempt(ip, username, "register_success")
        return result
    except HTTPException as e:
        log_login_attempt(ip, username, "register_failed")
        raise e