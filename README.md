# Maya Beauty Salon & Hair — Render Ready

Luxury Ethiopian beauty-salon website + synchronized Telegram reservation bot.

## IMPORTANT PROJECT STRUCTURE

Keep this structure exactly. Do NOT put `index.html` in the repository root.

```
maya-beauty-salon/
├── app.py
├── config.py
├── db.py
├── telegram_bot.py
├── requirements.txt
├── render.yaml
├── .env.example
├── README.md
├── templates/
│   ├── index.html
│   └── admin.html
└── static/
    ├── style.css
    └── images/
        ├── ethiopian-pattern.svg
        └── luxury-salon.svg
```

## Local run

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Render web service

Build Command:

```text
pip install -r requirements.txt
```

Start Command:

```text
gunicorn app:app --bind 0.0.0.0:$PORT
```

## Render environment variables

Add these to the Web Service and Telegram Worker:

```text
DATABASE_URL=your Render PostgreSQL internal connection string
TELEGRAM_BOT_TOKEN=your Telegram bot token
ADMIN_CHAT_ID=your Telegram admin chat ID
FLASK_SECRET=a-long-random-secret
```

`DATABASE_URL` is used for PostgreSQL on Render. If it is not set locally,
the app falls back to `maya_salon.db` for local development.

## Telegram worker

Use a separate Render Background Worker:

```text
Build Command:
pip install -r requirements.txt

Start Command:
python telegram_bot.py
```

The website and Telegram bot use the same PostgreSQL database when
`DATABASE_URL` is configured, so reservations are synchronized.

## GitHub warning

If GitHub currently shows `index.html`, `admin.html`, and `style.css` in the
repository root, do not leave them there. Put the HTML files in `templates/`
and the CSS/images in `static/` as shown above.
