from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from db import init_db, create_reservation, list_reservations, reservation_exists
from config import SERVICES, SOCIALS, SALON_NAME, SALON_NAME_AM
import os, threading, asyncio

load_dotenv()
app=Flask(__name__)
app.secret_key=os.getenv("FLASK_SECRET","change-this")
init_db()

def notify_telegram(text):
    token=os.getenv("TELEGRAM_BOT_TOKEN"); chat_id=os.getenv("ADMIN_CHAT_ID")
    if not token or not chat_id: return
    try:
        from telegram import Bot
        async def send():
            async with Bot(token=token) as bot:
                await bot.send_message(chat_id=chat_id,text=text)
        threading.Thread(target=lambda: asyncio.run(send()),daemon=True).start()
    except Exception as e: print("Telegram notification:",e)

@app.get("/")
def home():
    return render_template("index.html",services=SERVICES,socials=SOCIALS,
      salon_name=SALON_NAME,salon_name_am=SALON_NAME_AM)

@app.post("/reserve")
def reserve():
    f=request.form
    name=f.get("name","").strip(); phone=f.get("phone","").strip()
    service=f.get("service","").strip(); date=f.get("date","").strip()
    time=f.get("time","").strip(); note=f.get("note","").strip()
    if not all([name,phone,service,date,time]):
        flash("Please complete all required fields.","error")
        return redirect(url_for("home")+"#booking")
    if reservation_exists(date,time):
        flash("That time is already reserved. Please choose another time.","error")
        return redirect(url_for("home")+"#booking")
    rid=create_reservation(name,phone,service,date,time,note)
    notify_telegram(f"✨ NEW MAYA BEAUTY RESERVATION ✨\n\nBooking #{rid}\nClient: {name}\nPhone: {phone}\nService: {service}\nDate: {date}\nTime: {time}\nNote: {note or '—'}")
    flash(f"Reservation #{rid} received. Maya Beauty will contact you to confirm.","success")
    return redirect(url_for("home")+"#booking")

@app.get("/admin")
def admin():
    return render_template("admin.html",reservations=list_reservations())

if __name__=="__main__": app.run(debug=True)
