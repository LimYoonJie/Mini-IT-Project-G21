cd C:\Mini-IT-Project-G21
python -m venv .venv
Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000

open using http://127.0.0.1:8000

## Contact email delivery

The contact form sends messages to `mmusecondhandmarketplace@gmail.com`. Configure
Gmail SMTP in a local `.env` file for real delivery:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-sending-account@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=your-sending-account@gmail.com
MARKETPLACE_SUPPORT_EMAIL=mmusecondhandmarketplace@gmail.com
```

Use a Gmail app password rather than your normal account password. Without these
variables, Django uses its console email backend for local development.