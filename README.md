# Aplicación de Autenticación

Servicio de autenticación con funcionalidades de seguridad como bloqueo de cuentas después de múltiples intentos fallidos.

## Características

- Registro de usuarios con contraseñas encriptadas usando bcrypt
- Login seguro con manejo de sesiones
- Bloqueo de cuentas después de 5 intentos fallidos
- Desbloqueo automático después de un período de tiempo

## Requerimientos

- Python 3.8+
- FastAPI
- Dependencias en `requirements.txt`

## Instalación

```bash
# Clonar repositorio
git clone <url-del-repositorio>
cd auth-service

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

```bash
# Iniciar el servidor
python run.py
```

El servidor estará disponible en http://127.0.0.1:8000

## Tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests específicos
pytest tests/test_auth.py

# Ejecutar tests con reporte de cobertura
.\run_tests_with_coverage.bat
```

Los reportes de cobertura se generan en formato HTML en el directorio `htmlcov/`.

### Casos de prueba para flujos críticos

El proyecto incluye casos de prueba específicos para los flujos más críticos:

1. **Bloqueo de cuentas**: Verifica que una cuenta se bloquee después de 5 intentos fallidos
2. **Autenticación**: Prueba el proceso completo de registro e inicio de sesión
3. **Desbloqueo automático**: Verifica que las cuentas se desbloqueen después del tiempo establecido

Ejemplo de prueba para el mecanismo de bloqueo:

```python
def test_login_fails_and_blocks():
    username = "testuser"
    
    # 5 intentos fallidos
    for _ in range(5):
        with pytest.raises(Exception) as e:
            login(username, "wrong")
        assert "Credenciales inválidas" in str(e.value.detail)
    
    # El 6to intento debe mostrar que la cuenta está bloqueada
    with pytest.raises(Exception) as e:
        login(username, "wrong")
    assert "Usuario bloqueado" in str(e.value.detail)
```

## QA – Process Quality Assurance

Este proyecto sigue las buenas prácticas de OWASP y PEP8. El código es verificado con Bandit para seguridad y Flake8 para estilo.

### Verificaciones realizadas

| Fecha      | Herramientas | Resultado | Observaciones |
|------------|--------------|-----------|---------------|
| 23/05/2025 | Bandit, Flake8 | Exitoso  | No se encontraron problemas de seguridad ni estilo en el código. Proyecto cumple con estándares OWASP y PEP8. |

### Matriz de trazabilidad: Controles de calidad ↔ Componentes

| Control de calidad | Componente | Herramienta | Estado |
|--------------------|------------|-------------|--------|
| Validación de entrada | app/utils.py (validate_username) | Bandit, Revisión manual | Implementado |
| Logging seguro | app/utils.py (log_login_attempt) | Bandit | Implementado |
| Almacenamiento seguro de contraseñas | app/auth.py | Bandit | Implementado |
| Bloqueo de cuentas | app/auth.py | Pruebas unitarias | Implementado |
| Estilo de código PEP8 | Todos los archivos .py | Flake8 | Cumple |

### Hallazgos de auditoría de calidad

| ID | Fecha | Componente | Descripción | Severidad | Estado |
|----|-------|------------|-------------|-----------|--------|
| QA001 | 23/05/2025 | app/* | Verificación completa de código: sin problemas de seguridad | Informativo | Cerrado |
| QA002 | 23/05/2025 | app/* | Verificación de estilo PEP8: sin problemas | Informativo | Cerrado |

### Integración en CI

Los análisis de calidad están integrados en el proceso de CI a través de los siguientes mecanismos:

1. **Pre-commit hooks**: Ejecutan Flake8 antes de cada commit
2. **Pipeline de CI**: Las verificaciones de Bandit y Flake8 se ejecutan automáticamente en cada pull request
3. **Reportes automáticos**: Los resultados se registran y están disponibles en el dashboard del proyecto

Para ejecutar manualmente las verificaciones:

```bash
# Windows
.\run_qa.bat

# Linux/Mac
./run_qa.sh
```

### Ejemplos de código verificado

El módulo `app/utils.py` implementa validaciones de seguridad y logging:

```python
import re
import logging

logger = logging.getLogger(__name__)

def validate_username(username: str) -> bool:
    """Valida que el nombre de usuario sea alfanumérico (3-30 caracteres)."""
    pattern = r"^[a-zA-Z0-9_]{3,30}$"
    return bool(re.match(pattern, username))

def log_login_attempt(ip: str, username: str, status: str):
    """Registra intentos de inicio de sesión."""
    logger.info(f"Login attempt - IP: {ip} | User: {username} | Status: {status}")
```

### Herramientas de análisis

- **Bandit**: Análisis de seguridad para detectar vulnerabilidades comunes
- **Flake8**: Verificación de estilo según PEP8 y detección de errores potenciales

## Licencia

[MIT](LICENSE)
