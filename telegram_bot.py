import os
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from db import init_db, create_reservation, list_reservations, reservation_exists
from config import SERVICES, SALON_NAME

load_dotenv(); init_db()
NAME,PHONE,SERVICE,DATE,TIME,NOTE=range(6)

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
      f"✨ Welcome to {SALON_NAME}! ✨\n\nሰላም! ወደ ማያ የውበት ሳሎን እንኳን በደህና መጡ 💎\n\n"
      "/services — See services\n/book — Make a reservation\n/reservations — Admin list")

async def services(update,context):
    await update.message.reply_text("💎 MAYA BEAUTY SERVICES\n\n"+"\n".join(f"• {s['name']} — {s['price']}" for s in SERVICES))

async def book(update,context):
    context.user_data.clear(); await update.message.reply_text("What is your full name?"); return NAME
async def get_name(update,context):
    context.user_data["name"]=update.message.text.strip(); await update.message.reply_text("Your phone number?"); return PHONE
async def get_phone(update,context):
    context.user_data["phone"]=update.message.text.strip()
    await update.message.reply_text("Choose service by number:\n"+"\n".join(f"{i+1}. {s['name']}" for i,s in enumerate(SERVICES))); return SERVICE
async def get_service(update,context):
    try: context.user_data["service"]=SERVICES[int(update.message.text)-1]["name"]
    except: await update.message.reply_text("Send the service number, e.g. 1."); return SERVICE
    await update.message.reply_text("Preferred date? YYYY-MM-DD"); return DATE
async def get_date(update,context):
    try: datetime.strptime(update.message.text.strip(),"%Y-%m-%d")
    except: await update.message.reply_text("Please use YYYY-MM-DD."); return DATE
    context.user_data["date"]=update.message.text.strip(); await update.message.reply_text("Preferred time? Example 10:30"); return TIME
async def get_time(update,context):
    context.user_data["time"]=update.message.text.strip(); await update.message.reply_text("Special request? Send - if none."); return NOTE
async def get_note(update,context):
    note=update.message.text.strip(); note="" if note=="-" else note; d=context.user_data
    if reservation_exists(d["date"],d["time"]):
        await update.message.reply_text("That time is already reserved. Please /book again.")
        return ConversationHandler.END
    rid=create_reservation(d["name"],d["phone"],d["service"],d["date"],d["time"],note)
    await update.message.reply_text(f"✅ Booking request #{rid} received!\n\n{d['service']}\n{d['date']} at {d['time']}\n\nMaya Beauty will contact you to confirm.")
    admin_id=os.getenv("ADMIN_CHAT_ID")
    if admin_id:
        await context.bot.send_message(chat_id=admin_id,text=f"✨ NEW BOOKING #{rid}\nClient: {d['name']}\nPhone: {d['phone']}\nService: {d['service']}\nDate: {d['date']}\nTime: {d['time']}\nNote: {note or '—'}")
    return ConversationHandler.END

async def reservations(update,context):
    if str(update.effective_chat.id)!=str(os.getenv("ADMIN_CHAT_ID")):
        await update.message.reply_text("This command is for the salon admin."); return
    rows=list_reservations(50)
    text="📋 UPCOMING RESERVATIONS\n\n" + "\n".join(
      f"#{r['id']} • {r['date']} {r['time']} • {r['service']} • {r['name']} • {r['phone']} • {r['status']}" for r in rows)
    await update.message.reply_text(text[:4000] if rows else "No reservations yet.")

def main():
    token=os.getenv("TELEGRAM_BOT_TOKEN")
    if not token: raise RuntimeError("Set TELEGRAM_BOT_TOKEN in .env")
    a=ApplicationBuilder().token(token).build()
    conv=ConversationHandler(entry_points=[CommandHandler("book",book)],
      states={NAME:[MessageHandler(filters.TEXT&~filters.COMMAND,get_name)],
      PHONE:[MessageHandler(filters.TEXT&~filters.COMMAND,get_phone)],
      SERVICE:[MessageHandler(filters.TEXT&~filters.COMMAND,get_service)],
      DATE:[MessageHandler(filters.TEXT&~filters.COMMAND,get_date)],
      TIME:[MessageHandler(filters.TEXT&~filters.COMMAND,get_time)],
      NOTE:[MessageHandler(filters.TEXT&~filters.COMMAND,get_note)]},fallbacks=[])
    a.add_handler(CommandHandler("start",start)); a.add_handler(CommandHandler("services",services))
    a.add_handler(CommandHandler("reservations",reservations)); a.add_handler(conv)
    print("Maya Telegram bot running..."); a.run_polling()

if __name__=="__main__": main()
