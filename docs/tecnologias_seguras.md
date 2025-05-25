# Tecnologías Seguras Utilizadas

Este documento describe las tecnologías seguras utilizadas en el microservicio de autenticación y su justificación.

## FastAPI

FastAPI es un framework moderno de Python para construir APIs con alto rendimiento y validación automática de datos.

### Ventajas de seguridad:

1. **Validación automática de datos**: Utiliza Pydantic para validar y serializar datos, reduciendo errores y vulnerabilidades.
2. **Documentación automática**: Genera documentación interactiva (OpenAPI/Swagger) que facilita la comprensión y uso seguro de la API.
3. **Tipado estático**: Reduce errores en tiempo de ejecución gracias al sistema de tipos de Python.
4. **Soporte nativo para CORS**: Configuración sencilla para prevenir ataques de origen cruzado.
5. **Gestión integrada de excepciones**: Manejo estructurado de errores que evita filtrar información sensible.

## bcrypt

Bcrypt es un algoritmo de hash de contraseñas diseñado específicamente para el almacenamiento seguro de contraseñas.

### Ventajas de seguridad:

1. **Resistencia a ataques de fuerza bruta**: Mediante el uso de salt aleatorio y función de costo ajustable.
2. **Factor de trabajo configurable**: Permite aumentar la complejidad computacional para adaptarse a hardware más potente.
3. **Salt incorporado**: Genera y almacena automáticamente un salt único para cada contraseña.
4. **Lento por diseño**: Deliberadamente lento para dificultar los ataques por fuerza bruta.
5. **Ampliamente auditado**: Ha sido revisado exhaustivamente por expertos en seguridad.

## JWT (JSON Web Tokens)

JWT es un estándar abierto (RFC 7519) que define una forma compacta y autónoma para transmitir información de forma segura entre partes como un objeto JSON.

### Ventajas de seguridad:

1. **Firma digital**: Garantiza que el token no ha sido modificado en tránsito.
2. **Escalabilidad**: No requiere estado en el servidor, lo que facilita la escalabilidad horizontal.
3. **Expiración incorporada**: Incluye campos estándar para tiempo de expiración (exp).
4. **Información encapsulada**: Contiene toda la información necesaria, reduciendo consultas a la base de datos.
5. **Estándar ampliamente adoptado**: Implementado en múltiples lenguajes y frameworks.

## Implementación en el Microservicio

### FastAPI

- Utilizamos FastAPI para definir los endpoints y validar automáticamente las entradas mediante modelos Pydantic.
- Configuramos CORS para permitir solicitudes seguras desde el frontend.
- Implementamos manejadores de excepciones personalizados para errores de autenticación.

### bcrypt

- Utilizamos bcrypt a través de la biblioteca `passlib` para el hash seguro de contraseñas.
- Configuramos un número de rondas adecuado (12) para equilibrar seguridad y rendimiento.
- Implementamos verificación segura de contraseñas contra los hashes almacenados.

### JWT

- Utilizamos la biblioteca `python-jose` para la implementación de JWT.
- Configuramos tiempos de expiración adecuados para los tokens (30 minutos).
- Implementamos endpoints específicos para obtener y renovar tokens.
- Utilizamos dependencias de FastAPI para proteger endpoints que requieren autenticación.

## Seguridad Adicional

Además de estas tecnologías principales, implementamos otras medidas de seguridad:

1. **Bloqueo temporal de cuentas**: Después de múltiples intentos fallidos de inicio de sesión.
2. **Validación estricta de entradas**: Para nombres de usuario y contraseñas.
3. **Logging de eventos de seguridad**: Para auditoría y detección de intrusiones.
4. **Limitación de tasa**: Para prevenir ataques de fuerza bruta.
5. **Sanitización de entradas**: Para prevenir inyecciones y XSS.

## Conclusión

La combinación de FastAPI, bcrypt y JWT proporciona una base sólida para la implementación de un microservicio de autenticación seguro. Estas tecnologías se complementan entre sí para abordar diferentes aspectos de la seguridad, desde la validación de entradas hasta el almacenamiento seguro de contraseñas y la gestión de sesiones sin estado.
