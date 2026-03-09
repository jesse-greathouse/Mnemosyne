import os
import subprocess
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = APP_ROOT / "src"
MANAGE_PY = SRC_DIR / "backend" / "manage.py"
VENV_PYTHON = APP_ROOT / "opt" / "venv" / "bin" / "python"

if not MANAGE_PY.exists():
    raise FileNotFoundError(f"manage.py not found at: {MANAGE_PY}")

if not VENV_PYTHON.exists():
    raise FileNotFoundError(f"Virtual environment python not found at: {VENV_PYTHON}")

env = os.environ.copy()
env.setdefault("PYTHONPATH", str(SRC_DIR))
env.setdefault("DJANGO_SETTINGS_MODULE", "backend.config.settings")

subprocess.run([str(VENV_PYTHON), str(MANAGE_PY), "migrate"], check=True, env=env)
