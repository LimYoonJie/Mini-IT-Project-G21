cd C:\Mini-IT-Project-G21
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000

open using http://127.0.0.1:8000

## Stripe test checkout

Copy `.env.example` to `.env` for local development. Use Stripe **test-mode** API
keys from your Stripe Dashboard; never put real card details or live secret keys
in this repository. Checkout redirects customers to Stripe-hosted Checkout. The
order is marked paid only after Django receives a signed Stripe webhook at
`/stripe/webhook`. Configure these events in Stripe:

- `checkout.session.completed`
- `checkout.session.async_payment_succeeded`
- `checkout.session.expired`
- `checkout.session.async_payment_failed`

For a local webhook, install the Stripe CLI and run
`stripe listen --forward-to localhost:8000/stripe/webhook`; put the printed
webhook signing secret in `STRIPE_WEBHOOK_SECRET`. Use Stripe's test card
`4242 4242 4242 4242`, any future expiry date, and any CVC. Test-mode payments
do not move money. Do not enter real card details in test mode.

## Deploying to PythonAnywhere

The free account uses a `your-username.pythonanywhere.com` subdomain. Its
outbound internet access is limited, so verify that the account can reach
Stripe's API before relying on Stripe Checkout there. PythonAnywhere's plan
limits can change; check its current [pricing page](https://www.pythonanywhere.com/pricing/).

1. Push the `feature-development` branch to GitHub and clone it from a
	PythonAnywhere Bash console with
	`git clone -b feature-development https://github.com/LimYoonJie/Mini-IT-Project-G21.git`.
2. Create a virtual environment with Python 3.10 or newer, activate it, and
	install dependencies with `pip install -r requirements.txt`.
3. In the Web tab, create a **Manual Configuration** web app using the same
	Python version. Set its source and working directory to the folder containing
	`manage.py`, then edit its WSGI file to use `ecommerce.settings`.
4. Set these environment variables in the web app configuration. Generate a
	unique, long `DJANGO_SECRET_KEY` (for example, using
	`python -c "import secrets; print(secrets.token_urlsafe(64))"`); never reuse
	the development fallback.

	```text
	DJANGO_DEBUG=False
	DJANGO_SECRET_KEY=<a-long-random-secret>
	DJANGO_ALLOWED_HOSTS=<your-username>.pythonanywhere.com
	DJANGO_CSRF_TRUSTED_ORIGINS=https://<your-username>.pythonanywhere.com
	STRIPE_SECRET_KEY=<Stripe test secret key>
	STRIPE_WEBHOOK_SECRET=<Stripe webhook signing secret>
	```

5. In a Bash console, run `python manage.py migrate` and
	`python manage.py collectstatic --noinput`. Configure the Web tab's static
	files mapping from `/static/` to the project's `staticfiles` directory, then
	reload the web app.
6. In Stripe's test-mode webhook settings, add
	`https://<your-username>.pythonanywhere.com/stripe/webhook` and subscribe to
	the four events listed above. Use test keys and test cards until the full
	webhook flow works.

The PythonAnywhere [Django deployment guide](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)
has the current Web tab and WSGI instructions. Uploaded product images live in
`media/`; configure persistent storage and backups before treating the site as
production.