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


async def get(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        roll = context.args[0]
        password = context.args[1]

        await update.message.reply_text("Fetching attendance... ⏳")

        data = get_attendance(roll, password)

        subjects = []
        total_held = 0
        total_attended = 0

        for row in data:
            if len(row) >= 5 and row[0].isdigit():

                subject = row[1]
                held = int(row[2])
                attend = int(row[3])
                percent = row[4]

                subjects.append((subject, held, attend, percent))

                total_held += held
                total_attended += attend

        overall = (total_attended / total_held) * 100
        max_bunk = int((total_attended - 0.75 * total_held) / 0.75)

        message = "📊 ATTENDANCE REPORT\n\n"

        for s in subjects:
            message += f"{s[0]} : {s[2]}/{s[1]} ({s[3]}%)\n"

        message += f"\nTOTAL: {total_attended}/{total_held}"
        message += f"\nPercentage: {round(overall,2)} %"
        message += f"\n\nYou can bunk {max_bunk} classes and stay above 75%"

        await update.message.reply_text(message)

    except:
        await update.message.reply_text("Usage:\n/get rollnumber password")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("get", get))

app.run_polling()