@echo off
echo === Ejecutando pruebas con reporte de cobertura ===
python -m pytest --cov=app tests/ --cov-report=term --cov-report=html

echo.
echo === Reporte de cobertura generado en htmlcov/ ===
