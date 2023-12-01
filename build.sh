#!/usr/bin/env bash
# exit on error
set -o errexit

# poetry install
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# instalar las dependencias y hacer las migraciones para la base de datos sino no funciona