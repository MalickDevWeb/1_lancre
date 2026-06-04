#!/bin/sh
set -e

echo "▶ Exécution des migrations Django..."
python manage.py migrate --noinput

echo "▶ Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "▶ Démarrage du serveur Gunicorn..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120
