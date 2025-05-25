# Diseño de Arquitectura Modular del Microservicio de Autenticación

Este documento describe la arquitectura modular del microservicio de autenticación segura desarrollado con FastAPI.

## Principios de Diseño

- **Separación de Responsabilidades**: Cada módulo tiene una responsabilidad clara y específica.
- **Alta Cohesión**: Los componentes relacionados están agrupados en el mismo módulo.
- **Bajo Acoplamiento**: Los módulos son independientes y se comunican a través de interfaces bien definidas.
- **Seguridad por Diseño**: Consideraciones de seguridad incorporadas desde el inicio.

## Estructura Modular

```
app/
├── __init__.py        # Inicialización del paquete
├── main.py            # Endpoints de la API y configuración de la aplicación
├── auth.py            # Servicio de autenticación y gestión de usuarios
├── models.py          # Modelos de datos y validación
├── utils.py           # Utilidades generales
└── jwt.py             # Gestión de tokens JWT (JSON Web Tokens)
```

## Descripción de los Módulos

### 1. Módulo Principal (`main.py`)
- **Responsabilidad**: Definir los endpoints de la API y configurar la aplicación FastAPI.
- **Componentes**:
  - Enrutadores (routers) para diferentes funcionalidades
  - Configuración de middleware (CORS, etc.)
  - Inicialización de la aplicación
  - Montaje de archivos estáticos

### 2. Módulo de Autenticación (`auth.py`)
- **Responsabilidad**: Gestionar la autenticación y autorización de usuarios.
- **Componentes**:
  - Servicio de autenticación (`AuthService`)
  - Funciones para hash y verificación de contraseñas usando bcrypt
  - Gestión de intentos de inicio de sesión y bloqueo temporal
  - Registro de usuarios

### 3. Módulo de Modelos (`models.py`)
- **Responsabilidad**: Definir los modelos de datos y su validación.
- **Componentes**:
  - Modelo de solicitud de login (`LoginRequest`)
  - Modelo de solicitud de registro (`RegisterRequest`)
  - Modelo de respuesta de autenticación (`AuthResponse`)
  - Modelos para validación de contraseñas

### 4. Módulo de Utilidades (`utils.py`)
- **Responsabilidad**: Proporcionar funciones auxiliares y utilidades generales.
- **Componentes**:
  - Configuración de logging
  - Validación de nombres de usuario y contraseñas
  - Medición de tiempo de ejecución
  - Formateo de respuestas
  - Limitación de tasa de peticiones

### 5. Módulo JWT (`jwt.py`)
- **Responsabilidad**: Gestionar la generación, validación y renovación de tokens JWT.
- **Componentes**:
  - Generación de tokens de acceso
  - Validación de tokens
  - Manejo de expiración y renovación
  - Extracción de información de tokens

## Flujo de Datos

1. El cliente envía una solicitud HTTP a un endpoint.
2. `main.py` recibe la solicitud y la redirige al controlador adecuado.
3. El controlador utiliza los servicios de `auth.py` y `jwt.py` para procesar la solicitud.
4. Los datos de entrada se validan utilizando los modelos definidos en `models.py`.
5. Se generan respuestas utilizando las funciones de formato de `utils.py`.
6. La respuesta se devuelve al cliente.

## Ventajas de esta Arquitectura

1. **Mantenibilidad**: Cada módulo puede ser modificado de forma independiente.
2. **Escalabilidad**: Nuevas funcionalidades pueden añadirse con facilidad.
3. **Testabilidad**: Los componentes pueden probarse de forma aislada.
4. **Seguridad**: La separación de responsabilidades ayuda a prevenir vulnerabilidades.
5. **Reusabilidad**: Los componentes pueden reutilizarse en diferentes partes del sistema.

## Tecnologías Seguras Utilizadas

- **FastAPI**: Framework moderno para APIs con validación automática y documentación.
- **bcrypt**: Algoritmo de hashing seguro para contraseñas.
- **JWT (JSON Web Tokens)**: Estándar para transmitir información de autenticación de forma segura.
- **Pydantic**: Validación de datos y serialización.
- **Passlib**: Biblioteca de hash de contraseñas.

## Consideraciones de Seguridad

- Almacenamiento seguro de contraseñas con bcrypt
- Bloqueo temporal después de múltiples intentos fallidos
- Validación estricta de entradas
- Autenticación basada en tokens JWT con tiempo de expiración
- Registro de eventos de seguridad
- Limitación de tasa para prevenir ataques de fuerza bruta
