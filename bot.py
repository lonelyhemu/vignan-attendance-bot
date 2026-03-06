from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from attendance_selenium import get_attendance
import json
import os




BOT_TOKEN = "8688562927:AAFrE3hB5RX1i56QM9ZDzWUf3ck8dfbSTD0"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Vignan Attendance Bot\n\n"
        "Use:\n"
        "/get rollnumber password"
        "/login rollnumber password - to save login details\n"
        "/attendance - to get attendance using saved login"
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

        result = "📊 SUBJECT WISE ATTENDANCE\n\n"

        total_held = 0
        total_attended = 0

        for subject, held, attend, percent in data:
            if held=="Held":
                continue
            held = int(held)
            attend = int(attend)

            total_held += held
            total_attended += attend

            result += f"{subject}: {attend}/{held} ({percent}%)\n"

        overall = round((total_attended / total_held) * 100, 2)

        # bunk calculation
        safe_bunks = int((total_attended / 0.75) - total_held)

        result += "\n📈 TOTAL\n"
        result += f"{total_attended} / {total_held}\n"
        result += f"Percentage: {overall}%\n\n"

        if safe_bunks > 0:
            result += f"✅ You can bunk {safe_bunks} classes and stay above 75%"
        else:
            result += "⚠️ You must attend upcoming classes to stay above 75%"

        

        await update.message.reply_text(result)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def login(update, context):

    message = update.message.text.split()

    if len(message) != 3:
        await update.message.reply_text(
            "Usage:\n/login rollnumber password"
        )
        return

    roll = message[1]
    password = message[2]

    user_id = str(update.message.from_user.id)

    if os.path.exists("users.json"):
        with open("users.json","r") as f:
            users = json.load(f)
    else:
        users = {}

    users[user_id] = {
        "roll": roll,
        "password": password
    }

    with open("users.json","w") as f:
        json.dump(users,f)

    await update.message.reply_text("✅ Login saved successfully!")

async def attendance(update, context):

    user_id = str(update.message.from_user.id)

    if not os.path.exists("users.json"):
        await update.message.reply_text("❌ Please login first using /login")
        return

    with open("users.json","r") as f:
        users = json.load(f)

    if user_id not in users:
        await update.message.reply_text("❌ Please login first using /login")
        return

    roll = users[user_id]["roll"]
    password = users[user_id]["password"]

    await update.message.reply_text("Fetching attendance... ⏳")

    from attendance_selenium import get_attendance
    data = get_attendance(roll, password)

    result = "📊 SUBJECT WISE ATTENDANCE\n\n"

    total_held = 0
    total_attended = 0

    for subject, held, attend, percent in data:

        if held == "Held":
            continue

        held = int(held)
        attend = int(attend)

        total_held += held
        total_attended += attend

        result += f"{subject}: {attend}/{held} ({percent}%)\n"

    overall = round((total_attended / total_held) * 100,2)
    safe_bunks = int((total_attended / 0.75) - total_held)

    result += "\n📈 TOTAL\n"
    result += f"{total_attended} / {total_held}\n"
    result += f"Percentage: {overall}%\n\n"

    if safe_bunks > 0:
        result += f"✅ You can bunk {safe_bunks} classes and stay above 75%"
    else:
        result += "⚠️ You must attend upcoming classes to stay above 75%"

    await update.message.reply_text(result)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("get", get))
app.add_handler(CommandHandler("login", login))
app.add_handler(CommandHandler("attendance", attendance))

app.run_polling()