import shutil
from pathlib import Path

REMOVE_PATHS = [
    {%- if "vscode" not in ide %}
    ".vscode",
    {%- endif %}
    {%- if license == "Proprietary" %}
    "LICENSE",
    {%- endif %}
    {%- if package_type != "cli" %}
    Path("{{ package_name }}") / "cli.py",
    {%- endif %}
]

for path in REMOVE_PATHS:
    path = Path(path)
    if path and path.exists():
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
