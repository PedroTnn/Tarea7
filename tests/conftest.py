# tests/conftest.py

import sys
import os
from pathlib import Path

# Añadir el directorio raíz del proyecto al path de Python
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))
