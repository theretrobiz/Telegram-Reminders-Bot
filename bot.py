import json
from datetime import datetime
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# --- Configuration ---
TOKEN = "YOUR_BOT_TOKEN"
DATA_FILE = "events.json"

# --- Main menu keyboard ---
menu = ReplyKeyboardMarkup(
    [
        ["➕ Add event"],
        ["📊 Days left"],
        ["📅 My events"],
        ["⏰ Notification time", "🔔 Toggle notifications"]
    ],
    resize_keyboard=True
)

# --- Load and save JSON data ---
def load_data():
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# --- Keyboards for date/time selection ---
def month_keyboard():
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    buttons = [InlineKeyboardButton(m, callback_data=f"month_{i+1}") for i, m in enumerate(months)]
    rows = [buttons[i:i+3] for i in range(0, 12, 3)]
    return InlineKeyboardMarkup(rows)

def day_keyboard(month):
    days = 31
    if month in [4,6,9,11]: days = 30
    elif month == 2: days = 29
    buttons = [InlineKeyboardButton(str(i), callback_data=f"day_{i}") for i in range(1, days+1)]
    rows = [buttons[i:i+7] for i in range(0, len(buttons), 7)]
    rows.append([InlineKeyboardButton("⬅ Back", callback_data="back_month")])
    return InlineKeyboardMarkup(rows)

def year_keyboard():
    current_year = datetime.now().year
    buttons = [InlineKeyboardButton(str(current_year+i), callback_data=f"year_{current_year+i}") for i in range(5)]
    return InlineKeyboardMarkup([buttons, [InlineKeyboardButton("⬅ Back", callback_data="back_day")]])

def repeat_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Repeat yearly", callback_data="repeat_yes")],
        [InlineKeyboardButton("➖ No repeat", callback_data="repeat_no")]
    ])

def hour_keyboard():
    buttons = [InlineKeyboardButton(str(i).zfill(2), callback_data=f"hour_{i}") for i in range(24)]
    rows = [buttons[i:i+6] for i in range(0, 24, 6)]
    return InlineKeyboardMarkup(rows)

def minute_keyboard():
    buttons = [InlineKeyboardButton(str(i).zfill(2), callback_data=f"minute_{i}") for i in range(0,60,5)]
    rows = [buttons[i:i+6] for i in range(0,60,6)]
    return InlineKeyboardMarkup(rows)

# --- Calculate days left until event ---
def days_left(event):
    now = datetime.now()
    date = datetime.strptime(event["date"], "%Y-%m-%d")
    if event.get("repeat"):
        next_date = date.replace(year=now.year)
        if next_date < now:
            next_date = next_date.replace(year=now.year+1)
        return (next_date - now).days
    return (date - now).days

# --- /start command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Event Reminder Bot", reply_markup=menu)

# --- Handle text messages ---
async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = str(update.message.chat_id)
    text = update.message.text
    data = load_data()
    if user not in data:
        data[user] = {"events": [], "enabled": True, "hour":10, "minute":0}

    if text == "➕ Add event":
        context.user_data["state"] = "add_name"
        await update.message.reply_text("Send event name")

    elif context.user_data.get("state") == "add_name":
        context.user_data["name"] = text
        context.user_data["state"] = "month"
        await update.message.reply_text("Choose month", reply_markup=month_keyboard())

    elif context.user_data.get("state") == "edit_name":
        i = context.user_data["edit_index"]
        data[user]["events"][i]["name"] = text
        save_data(data)
        e = data[user]["events"][i]
        await update.message.reply_text(f"{e['name']}\nDate: {e['date']}\nDays left: {days_left(e)}")
        context.user_data.clear()

    elif text == "📊 Days left":
        events = data[user]["events"]
        if not events:
            await update.message.reply_text("No events yet")
            return
        msg = "Days left:\n\n" + "\n".join([f"{e['name']} — {days_left(e)} days" for e in events])
        await update.message.reply_text(msg)

    elif text == "📅 My events":
        events = data[user]["events"]
        if not events:
            await update.message.reply_text("No events yet")
            return
        buttons = [[InlineKeyboardButton(e["name"], callback_data=f"event_{i}")] for i,e in enumerate(events)]
        await update.message.reply_text("Your events", reply_markup=InlineKeyboardMarkup(buttons))

    elif text == "🔔 Toggle notifications":
        data[user]["enabled"] = not data[user]["enabled"]
        save_data(data)
        status = "enabled" if data[user]["enabled"] else "disabled"
        await update.message.reply_text(f"Notifications {status}")

    elif text == "⏰ Notification time":
        context.user_data["state"] = "hour"
        await update.message.reply_text("Select hour", reply_markup=hour_keyboard())

# --- Handle inline button presses ---
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = str(query.message.chat_id)
    data = load_data()
    if user not in data:
        data[user] = {"events": [], "enabled": True, "hour":10, "minute":0}

    if query.data.startswith("month_"):
        context.user_data["month"] = int(query.data.split("_")[1])
        await query.edit_message_text("Choose day", reply_markup=day_keyboard(context.user_data["month"]))
    elif query.data.startswith("day_"):
        context.user_data["day"] = int(query.data.split("_")[1])
        await query.edit_message_text("Choose year", reply_markup=year_keyboard())
    elif query.data.startswith("year_"):
        context.user_data["year"] = int(query.data.split("_")[1])
        await query.edit_message_text("Repeat this event?", reply_markup=repeat_keyboard())
    elif query.data in ["repeat_yes","repeat_no"]:
        name = context.user_data.get("name", "Event")
        y = context.user_data["year"]
        m = context.user_data["month"]
        d = context.user_data["day"]
        repeat = query.data=="repeat_yes"
        date_str = datetime(y,m,d).strftime("%Y-%m-%d")
        data[user]["events"].append({"name":name,"date":date_str,"repeat":repeat})
        save_data(data)
        context.user_data.clear()
        await query.edit_message_text(f"Event added\n{name}\n{date_str}")

    elif query.data.startswith("event_"):
        i = int(query.data.split("_")[1])
        e = data[user]["events"][i]
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✏️ Edit name", callback_data=f"editname_{i}")],
            [InlineKeyboardButton("📅 Edit date", callback_data=f"editdate_{i}")],
            [InlineKeyboardButton("🗑 Delete", callback_data=f"delete_{i}")]
        ])
        await query.edit_message_text(f"{e['name']}\nDate: {e['date']}\nDays left: {days_left(e)}", reply_markup=keyboard)

    elif query.data.startswith("delete_"):
        i = int(query.data.split("_")[1])
        data[user]["events"].pop(i)
        save_data(data)
        await query.edit_message_text("Event deleted")

    elif query.data.startswith("editname_"):
        i = int(query.data.split("_")[1])
        context.user_data["edit_index"] = i
        context.user_data["state"] = "edit_name"
        await query.edit_message_text("Send new name")

    elif query.data.startswith("editdate_"):
        i = int(query.data.split("_")[1])
        context.user_data["edit_index"] = i
        context.user_data["state"] = "month"
        context.user_data["name"] = data[user]["events"][i]["name"]
        await query.edit_message_text("Choose month", reply_markup=month_keyboard())

    elif query.data=="back_month":
        await query.edit_message_text("Choose month", reply_markup=month_keyboard())
    elif query.data=="back_day":
        await query.edit_message_text("Choose day", reply_markup=day_keyboard(context.user_data["month"]))

    elif query.data.startswith("hour_"):
        context.user_data["hour"] = int(query.data.split("_")[1])
        context.user_data["state"] = "minute"
        await query.edit_message_text("Select minute", reply_markup=minute_keyboard())
    elif query.data.startswith("minute_"):
        minute = int(query.data.split("_")[1])
        data[user]["hour"] = context.user_data["hour"]
        data[user]["minute"] = minute
        save_data(data)
        context.user_data.clear()
        await query.edit_message_text(f"Notification time updated: {data[user]['hour']:02d}:{data[user]['minute']:02d}")

# --- Daily notifications ---
async def daily(context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    now = datetime.now()
    for user, info in data.items():
        if not info.get("enabled", True):
            continue
        if now.hour == info.get("hour",10) and now.minute == info.get("minute",0):
            msg = "Daily reminder:\n\n" + "\n".join([f"{e['name']} — {days_left(e)} days" for e in info["events"]])
            await context.bot.send_message(user, msg)

# --- Main function ---
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, messages))
    app.add_handler(CallbackQueryHandler(buttons))
    app.job_queue.run_repeating(daily, interval=60)
    app.run_polling()

if __name__=="__main__":
    main()