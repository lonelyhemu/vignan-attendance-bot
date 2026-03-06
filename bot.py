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
    try:
        message = update.message.text.split()

        if len(message) != 3:
            await update.message.reply_text(
                "Usage:\n/get rollnumber password"
            )
            return

        roll = message[1]
        password = message[2]

        await update.message.reply_text("Fetching attendance... ⏳")

        from attendance_selenium import get_attendance

        data = get_attendance(roll, password)

        if not data:
            await update.message.reply_text("Could not fetch attendance.")
            return

        result = ""

        for row in data:
            result += " ".join(row) + "\n"

        await update.message.reply_text(result)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("get", get))

app.run_polling()