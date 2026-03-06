from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from attendance_selenium import get_attendance

BOT_TOKEN = "8688562927:AAFrE3hB5RX1i56QM9ZDzWUf3ck8dfbSTD0"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Vignan Attendance Bot\n\n"
        "Use:\n"
        "/get rollnumber password"
    )


async def get(update, context):
    text = update.message.text.strip()
    parts = text.split()

    if len(parts) != 3:
        await update.message.reply_text(
            "Usage:\n/get rollnumber password"
        )
        return

    roll = parts[1]
    password = parts[2]

    await update.message.reply_text("Fetching attendance... ⏳")

    try:
        from attendance_selenium import get_attendance
        data = get_attendance(roll, password)

        result = " 📊 ATTENDANCE REPORT\n\n"

        for subject, held, attend, percent in data:
            result += f"{subject}: {attend}/{held} ({percent}%)\n" 

        

        await update.message.reply_text(result)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("get", get))

app.run_polling()