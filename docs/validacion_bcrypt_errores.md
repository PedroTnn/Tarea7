# Validación de Uso Correcto de bcrypt y Manejo de Errores

## Fecha de Revisión: 24/05/2025
## Revisor: Equipo de Seguridad

## 1. Análisis del Uso de bcrypt

### 1.1 Configuración de bcrypt

```python
# Configuración de encriptación con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

**Evaluación**: ✅ CORRECTO
- Se utiliza `passlib.context.CryptContext` que es una biblioteca recomendada para manejo seguro de contraseñas
- Se especifica bcrypt como el esquema de hashing, que es actualmente considerado seguro
- La opción `deprecated="auto"` garantiza que se usen automáticamente los algoritmos más recientes si bcrypt queda obsoleto

### 1.2 Generación de Hash para Contraseñas

```python
def get_password_hash(password: str) -> str:
    """
    Genera un hash seguro para la contraseña utilizando bcrypt.
    """
    return pwd_context.hash(password)
```

**Evaluación**: ✅ CORRECTO
- Se utiliza la función `hash()` de CryptContext que aplica automáticamente:
  - Generación de salt aleatorio
  - Número de rondas adecuado para bcrypt
  - Formato de almacenamiento seguro que incluye el salt
- La función está correctamente documentada

### 1.3 Verificación de Contraseñas

```python
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica que la contraseña coincida con el hash almacenado.
    """
    return pwd_context.verify(plain_password, hashed_password)
```

**Evaluación**: ✅ CORRECTO
- Se utiliza la función `verify()` de CryptContext que:
  - Extrae el salt del hash almacenado
  - Realiza la comparación de manera segura contra ataques de tiempo
  - Maneja automáticamente diferentes formatos de hash
- La función está correctamente documentada

### 1.4 Uso en el Registro de Usuarios

```python
def register_user(username: str, password: str) -> Dict:
    """
    Registra un nuevo usuario con contraseña encriptada.
    """
    if username in users_db:
        raise HTTPException(status_code=400, detail="El usuario ya existe.")
    
    hashed_password = get_password_hash(password)
    users_db[username] = hashed_password
    
    return {"msg": "Usuario registrado exitosamente"}
```

**Evaluación**: ✅ CORRECTO
- Las contraseñas se hashean antes de almacenarse
- No se almacena la contraseña en texto plano en ningún momento
- Se genera un nuevo hash para cada usuario, garantizando salts únicos

### 1.5 Uso en la Autenticación

```python
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
```

**Evaluación**: ✅ CORRECTO
- Se utiliza la función `verify_password()` para comparar de manera segura
- No se expone información sobre si el usuario existe o la contraseña es incorrecta (misma respuesta en ambos casos)
- La verificación se realiza en tiempo constante (a través de `pwd_context.verify()`)

## 2. Análisis del Manejo de Errores

### 2.1 Validación de Usuarios Existentes

```python
def register_user(username: str, password: str) -> Dict:
    if username in users_db:
        raise HTTPException(status_code=400, detail="El usuario ya existe.")
    
    # Resto del código...
```

**Evaluación**: ✅ CORRECTO
- Se verifica la existencia del usuario antes de registrarlo
- Se utiliza un código HTTP apropiado (400 Bad Request)
- El mensaje de error es informativo pero no expone información sensible

### 2.2 Bloqueo de Cuentas

```python
def login(username: str, password: str):
    if is_user_blocked(username):
        raise HTTPException(status_code=403, detail="Usuario bloqueado temporalmente.")
    
    # Resto del código...
```

**Evaluación**: ✅ CORRECTO
- Se verifica el estado de bloqueo antes de intentar autenticar
- Se utiliza un código HTTP apropiado (403 Forbidden)
- El mensaje de error es informativo pero no proporciona información sobre cuándo se desbloqueará la cuenta

### 2.3 Manejo de Credenciales Inválidas

```python
def login(username: str, password: str):
    # Código anterior...
    
    if not success:
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")
    
    return {"msg": "Login exitoso"}
```

**Evaluación**: ✅ CORRECTO
- Se utiliza un código HTTP apropiado (401 Unauthorized)
- El mensaje de error no diferencia entre usuario inexistente y contraseña incorrecta, lo que es una buena práctica de seguridad
- Se registra el intento fallido antes de mostrar el error (mediante `register_login_attempt`)

### 2.4 Función `is_user_blocked`

```python
def is_user_blocked(username: str) -> bool:
    user_data = login_attempts.get(username, {"attempts": 0, "blocked_until": None})
    if user_data["blocked_until"] and datetime.now() < user_data["blocked_until"]:
        return True
    return False
```

**Evaluación**: ✅ CORRECTO
- Utiliza `.get()` con valor predeterminado para manejar usuarios no existentes
- Verifica explícitamente que `blocked_until` no sea None antes de comparar con la fecha actual
- Retorna un valor booleano claro

### 2.5 Registro de Intentos de Login

```python
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
```

**Evaluación**: ✅ CORRECTO
- Utiliza `.get()` con valor predeterminado para manejar usuarios no existentes
- Maneja correctamente tanto intentos exitosos como fallidos
- Implementa correctamente la lógica de bloqueo después de MAX_ATTEMPTS intentos fallidos

## 3. Mejores Prácticas Implementadas

1. ✅ **Uso de biblioteca establecida**: Utiliza passlib/bcrypt en lugar de implementar algoritmos criptográficos propios
2. ✅ **Hashing + Salting**: bcrypt genera automáticamente un salt único para cada contraseña
3. ✅ **Comparación en tiempo constante**: Previene ataques de temporización mediante pwd_context.verify()
4. ✅ **Mensajes de error genéricos**: No revela si un usuario existe o si la contraseña es incorrecta
5. ✅ **Bloqueo temporal**: Protege contra ataques de fuerza bruta
6. ✅ **Manejo de valores null/None**: Evita errores al usar .get() con valores predeterminados
7. ✅ **Tipado**: Incluye anotaciones de tipo para mejorar la claridad

## 4. Recomendaciones Adicionales

1. **Validación de fortaleza de contraseñas**: Implementar validación para rechazar contraseñas débiles en el registro
2. **Parámetros configurables**: Hacer que MAX_ATTEMPTS y BLOCK_DURATION sean configurables desde un archivo de configuración
3. **Logging de seguridad**: Agregar logging detallado para intentos fallidos (sin incluir contraseñas)
4. **Alarmas de seguridad**: Implementar notificaciones para múltiples intentos fallidos desde la misma IP
5. **Recaptcha**: Para mayor seguridad, considerar implementar recaptcha después de 2-3 intentos fallidos

## 5. Conclusión

El uso de bcrypt y el manejo de errores en este código sigue las mejores prácticas de seguridad actuales. La implementación es robusta contra:

- Ataques de fuerza bruta (mediante bloqueo temporal)
- Ataques de temporización (mediante comparación en tiempo constante)
- Exposición de contraseñas (mediante hashing seguro)
- Enumeración de usuarios (mediante mensajes de error genéricos)

**Veredicto Final**: ✅ IMPLEMENTACIÓN SEGURA
