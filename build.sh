#!/usr/bin/env bash
set -o errexit

# Install project dependencies
pip install -r requirements.txt

echo "Removing sourceMappingURL references from django-adminlte4..."

ADMINLTE_DIR=$(python - <<'PY'
from pathlib import Path
import site

for site_dir in site.getsitepackages():
    path = Path(site_dir) / "adminlte4"
    if path.exists():
        print(path)
        break
PY
)

if [ -n "$ADMINLTE_DIR" ] && [ -d "$ADMINLTE_DIR" ]; then
    grep -RIl 'sourceMappingURL=' "$ADMINLTE_DIR" \
        | while read -r file; do
            echo "Patching $file"
            sed -i '/sourceMappingURL=/d' "$file"
        done
else
    echo "django_adminlte4 package not found"
fi

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate