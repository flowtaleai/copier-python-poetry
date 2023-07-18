import shutil
from pathlib import Path

REMOVE_PATHS = [
    {%- if "vscode" not in cookiecutter.ide %}
    ".vscode",
    {%- endif %}
    {%- if cookiecutter.license == "Proprietary" %}
    "LICENSE",
    {%- endif %}
]

for path in REMOVE_PATHS:
    path = Path(path.strip())
    if path and path.exists():
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
