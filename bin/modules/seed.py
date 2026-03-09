import subprocess
import os
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = APP_ROOT / "src"
MANAGE_PY = SRC_DIR / "backend" / "manage.py"
VENV_PYTHON = APP_ROOT / "opt" / "venv" / "bin" / "python"


def seed():
    print("Running seed routines...\n")

    seeds = [
        (
            "Initialize groups",
            [str(VENV_PYTHON), str(MANAGE_PY), "init_groups"],
        ),
    ]

    for label, command in seeds:
        print(f"→ {label}")

        try:
            env = os.environ.copy()
            env.setdefault("PYTHONPATH", str(SRC_DIR))
            env.setdefault("DJANGO_SETTINGS_MODULE", "backend.config.settings")

            subprocess.run(command, check=True, env=env)

        except subprocess.CalledProcessError as e:
            print(f"✗ Failed: {label}\n  Error: {e}")
            break

        else:
            print(f"✓ Done: {label}\n")

    print("Seeding complete.")


if __name__ == "__main__":
    seed()
