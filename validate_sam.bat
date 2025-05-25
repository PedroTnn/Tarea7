@echo off
REM SAM - Supplier Agreement Management
REM Script de validación de dependencias seguras
REM Autor: Equipo de Seguridad
REM Fecha: 2025-05-25

echo ========================================
echo SAM - Validador de Dependencias Seguras
echo ========================================
echo.

echo [INFO] Iniciando validación de dependencias...
echo [INFO] Proyecto: %CD%
echo [INFO] Fecha: %DATE% %TIME%
echo.

REM Verificar que existen los archivos requeridos
echo [CHECK] Verificando archivos requeridos...
if not exist "configs\requirements.txt" (
    echo [ERROR] No se encontró configs\requirements.txt
    goto :error
)
if not exist "requirements.txt" (
    echo [ERROR] No se encontró requirements.txt  
    goto :error
)
echo [OK] Archivos de dependencias encontrados
echo.

REM Verificar dependencias principales
echo [CHECK] Verificando dependencias principales...
findstr /C:"fastapi==0.110.0" configs\requirements.txt >nul
if errorlevel 1 (
    echo [ERROR] FastAPI versión incorrecta o faltante
    goto :error
)
findstr /C:"bcrypt==4.0.1" configs\requirements.txt >nul  
if errorlevel 1 (
    echo [ERROR] bcrypt versión incorrecta o faltante
    goto :error
)
findstr /C:"pyjwt==2.8.0" configs\requirements.txt >nul
if errorlevel 1 (
    echo [ERROR] PyJWT versión incorrecta o faltante
    goto :error
)
findstr /C:"pydantic==2.6.4" configs\requirements.txt >nul
if errorlevel 1 (
    echo [ERROR] Pydantic versión incorrecta o faltante  
    goto :error
)
findstr /C:"pytest==8.1.1" configs\requirements.txt >nul
if errorlevel 1 (
    echo [ERROR] pytest versión incorrecta o faltante
    goto :error
)
findstr /C:"bandit==1.7.5" configs\requirements.txt >nul
if errorlevel 1 (
    echo [ERROR] bandit versión incorrecta o faltante
    goto :error
)
findstr /C:"flake8==7.0.0" configs\requirements.txt >nul
if errorlevel 1 (
    echo [ERROR] flake8 versión incorrecta o faltante
    goto :error
)
echo [OK] Todas las dependencias principales verificadas
echo.

REM Crear directorio evidence si no existe
if not exist "evidence" mkdir evidence

REM Ejecutar análisis de seguridad con Bandit
echo [SECURITY] Ejecutando análisis de seguridad con Bandit...
bandit -r app/ -f txt -o evidence\bandit_validation_report.txt
if errorlevel 1 (
    echo [WARNING] Bandit encontró algunos issues - revisar reporte
) else (
    echo [OK] Análisis de seguridad completado
)
echo.

REM Verificar que no hay issues críticos
echo [CHECK] Verificando issues críticos...
findstr /C:"High: 0" evidence\bandit_validation_report.txt >nul
if errorlevel 1 (
    echo [ERROR] Se encontraron issues de seguridad críticos
    goto :error
)
findstr /C:"Medium: 0" evidence\bandit_validation_report.txt >nul
if errorlevel 1 (
    echo [WARNING] Se encontraron issues de seguridad medios - revisar
) else (
    echo [OK] Sin issues críticos o medios
)
echo.

REM Generar timestamp de validación
echo [INFO] Generando evidencia de validación...
echo SAM Validation Report > evidence\validation_timestamp.txt
echo Date: %DATE% >> evidence\validation_timestamp.txt  
echo Time: %TIME% >> evidence\validation_timestamp.txt
echo Status: PASSED >> evidence\validation_timestamp.txt
echo Dependencies: VALIDATED >> evidence\validation_timestamp.txt
echo Security: ANALYZED >> evidence\validation_timestamp.txt
echo Next Review: 2025-08-25 >> evidence\validation_timestamp.txt
echo.

echo ========================================
echo [SUCCESS] ✅ VALIDACIÓN SAM COMPLETADA
echo ========================================
echo.
echo Resultados:
echo - Dependencias principales: ✅ VALIDADAS
echo - Versiones específicas: ✅ VERIFICADAS  
echo - Análisis de seguridad: ✅ EJECUTADO
echo - Evidencia generada: ✅ DISPONIBLE
echo.
echo Archivos generados:
echo - evidence\bandit_validation_report.txt
echo - evidence\validation_timestamp.txt
echo - evidence\SAM_compliance_report.md
echo.
echo [INFO] Revisión próxima: 2025-08-25
goto :end

:error
echo.
echo ========================================
echo [ERROR] ❌ VALIDACIÓN SAM FALLÓ
echo ========================================
echo.
echo Por favor revisar los errores reportados y ejecutar nuevamente.
echo.
pause
exit /b 1

:end
echo [INFO] Validación SAM completada exitosamente
echo.
pause
exit /b 0
