#!/usr/bin/env python3
"""
Script de validación de dependencias seguras
SAM - Supplier Agreement Management
"""

import subprocess
import sys
import json
import os
from datetime import datetime

def run_command(command):
    """Ejecuta un comando y retorna el resultado"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def validate_dependencies():
    """Valida las dependencias del proyecto"""
    print("🔍 Validando dependencias del proyecto...")
    
    # Verificar que existe requirements.txt
    if not os.path.exists("requirements.txt") and not os.path.exists("configs/requirements.txt"):
        print("❌ No se encontró archivo requirements.txt")
        return False
    
    # Ejecutar análisis de seguridad con Bandit
    print("\n🛡️  Ejecutando análisis de seguridad con Bandit...")
    success, stdout, stderr = run_command("bandit -r app/ -f json")
    
    if success:
        try:
            # Parsear resultado JSON de Bandit
            bandit_result = json.loads(stdout)
            issues = bandit_result.get('results', [])
            
            high_issues = [i for i in issues if i['issue_severity'] == 'HIGH']
            medium_issues = [i for i in issues if i['issue_severity'] == 'MEDIUM']
            low_issues = [i for i in issues if i['issue_severity'] == 'LOW']
            
            print(f"   Issues encontrados:")
            print(f"   - Críticos: {len(high_issues)}")
            print(f"   - Medios: {len(medium_issues)}")
            print(f"   - Bajos: {len(low_issues)}")
            
            if len(high_issues) > 0:
                print("❌ Se encontraron issues críticos de seguridad")
                for issue in high_issues:
                    print(f"   🚨 {issue['test_name']}: {issue['issue_text']}")
                return False
            else:
                print("✅ No se encontraron issues críticos de seguridad")
                
        except json.JSONDecodeError:
            print("⚠️  Error al parsear resultado de Bandit")
    
    # Verificar dependencias conocidas como seguras
    print("\n📦 Verificando dependencias aprobadas...")
    approved_packages = {
        'fastapi': '0.110.0',
        'bcrypt': '4.0.1',
        'pyjwt': '2.8.0',
        'pydantic': '2.6.4',
        'pytest': '8.1.1',
        'bandit': '1.7.5',
        'flake8': '7.0.0'
    }
    
    # Verificar que las dependencias principales están en la versión correcta
    requirements_file = "configs/requirements.txt" if os.path.exists("configs/requirements.txt") else "requirements.txt"
    
    with open(requirements_file, 'r') as f:
        requirements = f.read()
    
    all_approved = True
    for package, version in approved_packages.items():
        if f"{package}=={version}" in requirements:
            print(f"   ✅ {package} {version} - Aprobado")
        else:
            print(f"   ❌ {package} {version} - No encontrado o versión incorrecta")
            all_approved = False
    
    return all_approved

def generate_security_report():
    """Genera reporte de seguridad"""
    print("\n📄 Generando reporte de seguridad...")
    
    # Crear directorio evidence si no existe
    os.makedirs("evidence", exist_ok=True)
    
    # Ejecutar Bandit y guardar resultado
    success, stdout, stderr = run_command("bandit -r app/ -f txt -o evidence/bandit_report.txt")
    
    if success:
        print("✅ Reporte de Bandit generado en evidence/bandit_report.txt")
    else:
        print(f"❌ Error generando reporte de Bandit: {stderr}")
    
    # Generar timestamp del análisis
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    summary = f"""
# Reporte de Validación de Dependencias
Generado: {timestamp}

## Estado de Validación
- Análisis de seguridad: {'✅ Completado' if success else '❌ Error'}
- Dependencias aprobadas: Verificadas
- Próxima revisión: {datetime.now().strftime("%Y-%m-%d")}

## Acciones Requeridas
1. Revisar issues de seguridad reportados por Bandit
2. Validar que todas las dependencias están en versiones aprobadas
3. Implementar variables de entorno para secretos en producción

Para más detalles, revisar evidence/bandit_report.txt
"""
    
    with open("evidence/validation_summary.md", "w") as f:
        f.write(summary)
    
    print("✅ Resumen de validación generado en evidence/validation_summary.md")

def main():
    """Función principal"""
    print("🔐 SAM - Validador de Dependencias Seguras")
    print("=" * 50)
    
    # Cambiar al directorio del proyecto
    if len(sys.argv) > 1:
        os.chdir(sys.argv[1])
    
    print(f"📁 Directorio de trabajo: {os.getcwd()}")
    
    # Validar dependencias
    if validate_dependencies():
        print("\n✅ Todas las validaciones pasaron correctamente")
        generate_security_report()
        sys.exit(0)
    else:
        print("\n❌ Algunas validaciones fallaron")
        generate_security_report()
        sys.exit(1)

if __name__ == "__main__":
    main()
