#!/usr/bin/env bash
set -o errexit

# Install project dependencies
pip install -r requirements.txt

echo "Patching django-adminlte4..."
python <<'PY'
from pathlib import Path
import site

print(f"Searching for *.map references in site-packages: {site.getsitepackages()}")

for site_dir in site.getsitepackages():
    map_file_dir = (
        Path(site_dir)
        / "adminlte4"
        / "static"
        / "admin-lte"
        / "plugins"
        / "bootstrap-slider"
        / "css"
    )

    if map_file_dir.exists():
        (map_file_dir / "bootstrap-slider.css.map").touch(exist_ok=True)
        print(f"Created: {map_file_dir / 'bootstrap-slider.css.map'}")

        (map_file_dir / "bootstrap-slider.min.css.map").touch(exist_ok=True)
        print(f"Created: {map_file_dir / 'bootstrap-slider.min.css.map'}")

        break
else:
    print("bootstrap-slider directory not found")
PY

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate