# Checklist de Aseguramiento de Calidad (PQA)

Este documento proporciona un checklist detallado para verificar el cumplimiento de los estándares de calidad en el proyecto de Autenticación Segura.

## Estándares de seguridad (OWASP)

| ID | Control | Descripción | Verificación | Estado |
|----|---------|-------------|--------------|--------|
| SEC-01 | Almacenamiento seguro de contraseñas | Las contraseñas deben almacenarse con hash usando algoritmos seguros (bcrypt) | Bandit + Revisión manual | ✅ |
| SEC-02 | Bloqueo de cuentas | Implementar bloqueo tras múltiples intentos fallidos | Tests unitarios | ✅ |
| SEC-03 | Validación de entrada | Validar todas las entradas del usuario | Bandit + Flake8 | ✅ |
| SEC-04 | Logging seguro | Implementar logging sin datos sensibles | Bandit | ✅ |
| SEC-05 | Protección CSRF | Implementar tokens anti-CSRF | Pendiente | ⚠️ |
| SEC-06 | Cabeceras HTTP seguras | Configurar cabeceras de seguridad | Pendiente | ⚠️ |

## Estándares de código (PEP8)

| ID | Control | Descripción | Verificación | Estado |
|----|---------|-------------|--------------|--------|
| PEP-01 | Longitud de línea | Máximo 79 caracteres | Flake8 | ✅ |
| PEP-02 | Indentación | 4 espacios por nivel | Flake8 | ✅ |
| PEP-03 | Imports | Ordenados y agrupados | Flake8 | ✅ |
| PEP-04 | Espacios en blanco | Uso consistente | Flake8 | ✅ |
| PEP-05 | Comentarios | Docstrings para todas las funciones | Flake8 | ✅ |
| PEP-06 | Convención de nombres | snake_case para funciones y variables | Flake8 | ✅ |

## Pruebas y cobertura

| ID | Control | Descripción | Verificación | Estado |
|----|---------|-------------|--------------|--------|
| TST-01 | Tests unitarios | Pruebas para cada función crítica | pytest | ✅ |
| TST-02 | Cobertura de código | >80% de cobertura | pytest-cov, coverage.py | ✅ |
| TST-03 | Tests de integración | Pruebas de APIs | pytest | ✅ |
| TST-04 | Tests de seguridad | Pruebas específicas de seguridad | Bandit | ✅ |
| TST-05 | Flujos críticos | Pruebas de bloqueo de cuentas | pytest | ✅ |
| TST-06 | Flujos críticos | Pruebas de autenticación | pytest | ✅ |

## V&V - Verification and Validation

### Implementación de pruebas unitarias con pytest

El proyecto implementa pruebas unitarias completas utilizando el framework pytest. Estas pruebas verifican tanto componentes individuales como flujos de proceso completos.

#### Casos de prueba para flujos críticos

```python
# tests/test_auth.py - Ejemplo de pruebas para flujos críticos

from app.auth import login, register_login_attempt, is_user_blocked
import pytest

def test_login_fails_and_blocks():
    """
    Prueba que verifica el mecanismo de bloqueo de cuentas después de
    múltiples intentos fallidos de login.
    """
    username = "testuser"
    
    # Realizar 5 intentos fallidos de login
    for _ in range(5):
        with pytest.raises(Exception) as e:
            login(username, "wrong")
        assert "Credenciales inválidas" in str(e.value.detail)
    
    # El sexto intento debe producir error de bloqueo
    with pytest.raises(Exception) as e:
        login(username, "wrong")
    assert "Usuario bloqueado" in str(e.value.detail)

def test_successful_authentication():
    """
    Prueba el flujo de autenticación exitosa.
    """
    username = "testuser"
    password = "correct_password"
    
    # Registro y login exitoso
    register_user(username, password)
    result = login(username, password)
    assert "exitoso" in result["msg"]
```

### Reportes de cobertura con coverage.py

El proyecto utiliza coverage.py para generar reportes detallados de cobertura de código. Estos reportes permiten identificar áreas del código que no están siendo adecuadamente probadas.

#### Ejecución de pruebas con cobertura

```bash
# Ejecutar pruebas con reporte de cobertura
pytest --cov=app tests/

# Generar reporte HTML de cobertura
pytest --cov=app --cov-report=html tests/
```

#### Resultados de cobertura (23/05/2025)

| Módulo | Líneas | Cobertura |
|--------|--------|-----------|
| app/auth.py | 91 | 92% |
| app/main.py | 51 | 85% |
| app/utils.py | 16 | 100% |
| **TOTAL** | **158** | **90%** |

### Enfoque de pruebas

El proyecto implementa una estrategia de pruebas en múltiples niveles:

1. **Pruebas unitarias**: Verifican componentes individuales como funciones de validación
2. **Pruebas de integración**: Verifican la interacción entre componentes
3. **Pruebas de flujos críticos**: 
   - Bloqueo de cuentas después de múltiples intentos fallidos
   - Proceso completo de registro e inicio de sesión
   - Desbloqueo automático después del tiempo establecido
   - Manejo de errores en la validación de entrada

## Proceso de verificación

Para cada cambio en el código, se debe:

1. Ejecutar análisis estático local:
   ```bash
   # Windows
   .\run_qa.bat
   
   # Linux/Mac
   ./run_qa.sh
   ```

2. Revisar los resultados y corregir cualquier problema antes de commit.

3. El pipeline de CI ejecutará automáticamente todas las verificaciones.

4. Documentar los resultados en la matriz de trazabilidad.

## Auditoría y mejora continua

- Realizar auditoría completa de seguridad cada 3 meses
- Actualizar la matriz de trazabilidad con cada nueva función
- Revisar y actualizar este checklist según evolucionen los estándares
