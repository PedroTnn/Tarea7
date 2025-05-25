# Arquitectura Modular del Microservicio de Autenticación

## Descripción General

Este documento describe la arquitectura modular implementada en el microservicio de autenticación. La arquitectura se ha diseñado siguiendo los principios de modularidad, separación de responsabilidades y seguridad.

## Estructura del Proyecto

```
app/
├── __init__.py
├── main.py        # Rutas y endpoints de la API
├── auth.py        # Lógica de autenticación y seguridad
├── models.py      # Modelos de datos y validación
└── utils.py       # Funciones de utilidad y soporte
```

## Componentes Principales

### 1. Capa de API (app/main.py)

Responsabilidades:
- Definición de endpoints REST
- Gestión de solicitudes HTTP
- Validación inicial de entrada
- Enrutamiento a servicios de lógica
- Manejo de respuestas y códigos de estado HTTP

Tecnologías:
- FastAPI para la definición de API
- Pydantic para validación de datos de entrada
- Middleware CORS para seguridad de navegador

### 2. Capa de Lógica de Negocio (app/auth.py)

Responsabilidades:
- Implementación de la lógica de autenticación
- Gestión de usuarios y contraseñas
- Mecanismo de bloqueo de cuentas
- Verificación de credenciales

Tecnologías:
- Passlib con bcrypt para hash seguro de contraseñas
- Gestión de intentos fallidos y bloqueo temporal

### 3. Capa de Modelos (app/models.py)

Responsabilidades:
- Definición de la estructura de datos
- Validación de datos
- Serialización/deserialización

Tecnologías:
- Pydantic para definición y validación de modelos
- Validadores personalizados para reglas de negocio específicas

### 4. Capa de Utilidades (app/utils.py)

Responsabilidades:
- Funciones auxiliares reutilizables
- Logging y monitoreo
- Formateo de respuestas
- Medición de rendimiento

Tecnologías:
- Biblioteca estándar de Python
- Decoradores para medición de rendimiento
- Logging para registro de eventos

## Flujo de Datos

1. El cliente envía una solicitud HTTP a un endpoint definido en `main.py`
2. FastAPI valida automáticamente los datos de entrada según los modelos de `models.py`
3. El controlador en `main.py` registra la solicitud y llama al servicio apropiado en `auth.py`
4. El servicio en `auth.py` implementa la lógica de negocio y utiliza funciones de `utils.py`
5. El resultado se devuelve al controlador, que formatea la respuesta HTTP
6. Se registra el resultado de la operación y se envía la respuesta al cliente

## Cumplimiento de Requisitos

### Requisitos Funcionales

| ID | Descripción | Implementación |
|----|-------------|----------------|
| REQ-FUNC-001 | Permitir inicio de sesión con usuario y contraseña | Endpoint `/login` en `main.py` + `AuthService.login()` en `auth.py` |
| REQ-FUNC-002 | Verificar credenciales | `verify_password()` en `auth.py` |
| REQ-FUNC-003 | Emitir respuesta clara tras autenticación | Formato de respuesta estándar con `format_response()` en `utils.py` |

### Requisitos No Funcionales

| ID | Descripción | Implementación |
|----|-------------|----------------|
| REQ-SEC-001 | Bloqueo después de 5 intentos fallidos por 15 minutos | `register_login_attempt()` en `auth.py` con constantes `MAX_ATTEMPTS` y `BLOCK_DURATION` |
| REQ-SEC-002 | Contraseñas cifradas con bcrypt | `pwd_context` configurado con bcrypt en `auth.py` |
| REQ-SEC-003 | Registrar intentos de inicio de sesión | `log_login_attempt()` en `utils.py` |
| REQ-SEC-004 | Responder en máximo 2 segundos | Decorador `measure_execution_time()` en `utils.py` para monitoreo |

## Elección de Tecnologías Seguras

### FastAPI

- Framework moderno y de alto rendimiento
- Validación automática de tipos y datos con Pydantic
- Documentación automática con OpenAPI
- Soporte para asincronía que mejora el rendimiento

### Bcrypt (via Passlib)

- Algoritmo de hashing de contraseñas resistente a ataques de fuerza bruta
- Implementa automáticamente salt único para cada contraseña
- Configurable para ajustar el factor de costo según necesidades de seguridad
- Recomendado por OWASP para almacenamiento seguro de contraseñas

### JWT (preparado para implementación)

- Estándar para la creación de tokens de autenticación
- Permite implementar autenticación sin estado (stateless)
- Soporta firma digital para verificar la integridad
- Extensible para incluir información adicional del usuario

## Ventajas de la Arquitectura Modular

1. **Mantenibilidad**: Cada módulo tiene una responsabilidad clara y bien definida
2. **Testabilidad**: Los componentes pueden probarse de forma aislada
3. **Escalabilidad**: Facilita la expansión y mejora de funcionalidades
4. **Seguridad**: Centraliza la lógica de seguridad en componentes especializados
5. **Reutilización**: Las funcionalidades comunes están disponibles para todo el sistema

## Conclusiones

La arquitectura modular implementada proporciona una base sólida para el microservicio de autenticación, cumpliendo con todos los requisitos funcionales y no funcionales. La separación clara de responsabilidades facilita el mantenimiento y la evolución del sistema, mientras que la elección de tecnologías modernas y seguras garantiza un alto nivel de protección para los usuarios.
