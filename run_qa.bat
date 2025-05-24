@echo off
echo === Ejecutando análisis de seguridad con Bandit ===
bandit -r app/ -c bandit.yml

echo.
echo === Ejecutando análisis de estilo con Flake8 ===
flake8 app/
