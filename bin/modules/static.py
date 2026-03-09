import subprocess
import os
from pathlib import Path
from dotenv import load_dotenv

APP_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = APP_ROOT / "src"
MANAGE_PY = SRC_DIR / "backend" / "manage.py"
ENV_FILE = SRC_DIR / ".env"
VENV_PYTHON = APP_ROOT / "opt" / "venv" / "bin" / "python"

if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE)


def collect_static():
    cmd = [
        str(VENV_PYTHON),
        str(MANAGE_PY),
        "collectstatic",
        "--noinput",
    ]

    env = os.environ.copy()
    env.setdefault("PYTHONPATH", str(SRC_DIR))
    env.setdefault("DJANGO_SETTINGS_MODULE", "backend.config.settings")

    subprocess.run(cmd, check=True, env=env)


if __name__ == "__main__":
    collect_static()
