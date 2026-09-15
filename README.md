# Maya Beauty Salon & Hair

Luxury Ethiopian beauty-salon website + synchronized Telegram reservation bot.

## Features
- Luxury responsive women's beauty-salon design
- English + Amharic service labels
- Hair, human hair, braids, manicure, pedicure, nail art, makeup, lashes, brows, facial and spa
- Online reservation form
- Shared SQLite database
- Telegram reservation flow and admin notifications
- Admin reservation dashboard
- Animated CSS/SVG salon graphics
- Social-media buttons ready for the real accounts

## Run
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Telegram
Create a bot with BotFather, copy `.env.example` to `.env`, then set:
TELEGRAM_BOT_TOKEN=...
ADMIN_CHAT_ID=...
SALON_PHONE=...

Run:
```bash
python telegram_bot.py
```

Website and Telegram use the same `maya_salon.db`, so bookings are synchronized.

Edit social URLs in `config.py`.
