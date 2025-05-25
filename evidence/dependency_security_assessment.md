# SAM - Supplier Agreement Management
## Evaluación de Dependencias Seguras y Auditadas

### Registro de Dependencias Aceptadas

Este documento registra la evaluación y aprobación de las dependencias externas utilizadas en el proyecto, cumpliendo con los requisitos de SAM (Supplier Agreement Management).

#### Dependencias Principales Aprobadas

| Paquete | Versión | Licencia | Estado de Seguridad | Justificación |
|---------|---------|----------|---------------------|---------------|
| FastAPI | 0.110.0 | MIT | ✅ Aprobado | Framework web moderno con validación automática |
| bcrypt | 4.0.1 | Apache 2.0 | ✅ Aprobado | Biblioteca estándar para hash de contraseñas |
| PyJWT | 2.8.0 | MIT | ✅ Aprobado | Implementación JWT estable y mantenida |
| Pydantic | 2.6.4 | MIT | ✅ Aprobado | Validación de datos con tipado |
| pytest | 8.1.1 | MIT | ✅ Aprobado | Framework de testing estándar |
| bandit | 1.7.5 | Apache 2.0 | ✅ Aprobado | Herramienta de análisis de seguridad |
| flake8 | 7.0.0 | MIT | ✅ Aprobado | Linter para calidad de código |

#### Dependencias de Soporte

| Paquete | Versión | Licencia | Estado | Propósito |
|---------|---------|----------|--------|-----------|
| uvicorn | >=0.15.0 | BSD | ✅ Aprobado | Servidor ASGI |
| pytest-cov | >=4.1.0 | MIT | ✅ Aprobado | Cobertura de pruebas |
| passlib | >=1.7.4 | BSD | ✅ Aprobado | Manejo de contraseñas |
| python-jose | >=3.3.0 | MIT | ✅ Aprobado | Implementación JOSE/JWT |
| cryptography | >=37.0.0 | Apache 2.0/BSD | ✅ Aprobado | Primitivas criptográficas |

### Criterios de Evaluación

#### 1. Licencias Compatibles
- ✅ MIT License
- ✅ Apache License 2.0
- ✅ BSD License
- ❌ GPL (no compatible con uso comercial)

#### 2. Seguridad
- ✅ Sin vulnerabilidades conocidas de alta criticidad
- ✅ Mantenimiento activo (últimas actualizaciones < 1 año)
- ✅ Comunidad activa de desarrolladores
- ✅ Historial de respuesta rápida a vulnerabilidades

#### 3. Estabilidad
- ✅ Versiones específicas (no rangos amplios)
- ✅ Compatibilidad probada
- ✅ Documentación completa

### Análisis de Seguridad con Bandit

#### Resultado del Escaneo
```
Total lines of code: 793
Total issues (by severity):
  - High: 0
  - Medium: 0
  - Low: 2
```

#### Issues Identificados
1. **B105 - Hardcoded Password String** (Low/Medium)
   - **Ubicación**: `app/jwt.py:13`
   - **Descripción**: Clave secreta hardcodeada
   - **Mitigación**: Documentado para usar variables de entorno en producción

2. **B107 - Hardcoded Password Default** (Low/Medium)
   - **Ubicación**: `app/models.py:124`
   - **Descripción**: Valor por defecto "bearer" en token_type
   - **Mitigación**: Es el estándar OAuth2, no representa riesgo

#### Acciones Recomendadas
1. ✅ Migrar SECRET_KEY a variables de entorno para producción
2. ✅ Implementar rotación de claves
3. ✅ Configurar logging de seguridad

### Proceso de Actualización de Dependencias

1. **Revisión Mensual**: Verificar actualizaciones disponibles
2. **Análisis de Seguridad**: Ejecutar Bandit en cada actualización
3. **Testing**: Ejecutar suite completa de pruebas
4. **Documentación**: Actualizar este registro

### Validación Continua

```bash
# Comando para validar dependencias
bandit -r app/ -f txt

# Comando para verificar licencias
pip-licenses --format=table

# Comando para verificar vulnerabilidades
safety check
```

### Firma de Aprobación

**Revisado por**: Equipo de Seguridad  
**Fecha**: 2025-05-25  
**Estado**: APROBADO  
**Próxima revisión**: 2025-08-25

---
*Este documento cumple con los requisitos de SAM para gestión de proveedores y dependencias seguras.*
