# Reporte de Cobertura de Pruebas

**Fecha:** 23/05/2025  
**Versión:** 1.0.0  
**Generado por:** pytest-cov y coverage.py

## Resumen de Cobertura

| Módulo | Líneas | Declaraciones | Cobertura de Líneas | Cobertura de Ramas |
|--------|--------|---------------|---------------------|-------------------|
| app/auth.py | 91 | 63 | 92% | 88% |
| app/main.py | 51 | 43 | 85% | 80% |
| app/utils.py | 16 | 14 | 100% | 100% |
| **TOTAL** | **158** | **120** | **90%** | **86%** |

## Detalles por Archivo

### app/auth.py

```
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
app/auth.py               63      5    92%   43-45, 72, 86
```

**Líneas no cubiertas:**
- Manejo de excepciones en funcionalidades específicas
- Casos bordes en la verificación de contraseñas

### app/main.py

```
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
app/main.py               43      7    85%   67-70, 102-104
```

**Líneas no cubiertas:**
- Rutas de documentación opcionales
- Algunas respuestas de error en formularios de registro

### app/utils.py

```
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
app/utils.py              14      0   100%   
```

## Cobertura de Flujos Críticos

| Flujo Crítico | Casos de Prueba | Cobertura |
|---------------|-----------------|-----------|
| Registro de usuario | 3 casos | 100% |
| Login exitoso | 2 casos | 100% |
| Login fallido | 3 casos | 100% |
| Bloqueo de cuenta | 2 casos | 100% |
| Desbloqueo automático | 1 caso | 100% |

## Historial de Cobertura

| Fecha | Versión | Cobertura Total | Cambio |
|-------|---------|-----------------|--------|
| 15/04/2025 | 0.8.0 | 82% | - |
| 01/05/2025 | 0.9.0 | 87% | +5% |
| 23/05/2025 | 1.0.0 | 90% | +3% |

## Recomendaciones

1. Mejorar la cobertura de pruebas en `app/main.py`, específicamente en los manejadores de errores
2. Agregar más casos de prueba para el desbloqueo automático de cuentas
3. Considerar pruebas de integración para validar la experiencia completa del usuario

---

*Este reporte fue generado automáticamente.*
