cd C:\Mini-IT-Project-G21
python -m venv .venv
Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000

open using http://127.0.0.1:8000