# 📅 Telegram Reminders Bot

A Telegram bot where you can **add events with dates** and receive **daily notifications**.  
You can **edit or delete events**, set **notification times**, and see the **days remaining** for each event.  

Try the bot here: [@remindersuwubot](https://t.me/remindersuwubot) ✅

---

## ✨ Features

- ➕ Add events with **custom name and date**  
- ✏️ Edit **event name** or **date**  
- 🗑 Delete events  
- ⏰ Set **daily notification time** (hour and minute)  
- 🔁 Support for **repeating yearly events**  
- 📊 View **all events** with days left  
- 📝 Daily reminders with days remaining  
- 📲 Fully interactive with **inline buttons**  

---

## 🛠 Requirements

- Python 3.10+  
- `python-telegram-bot` library  

### Using a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install --upgrade pip
pip install python-telegram-bot
```

---

## ⚙️ Bot Setup

1. **Create a bot** on Telegram using [@BotFather](https://t.me/BotFather) and get your **bot token**.  
2. **Edit the bot code**:

```python
TOKEN = "YOUR_BOT_TOKEN"
```

Replace `"YOUR_BOT_TOKEN"` with the token from BotFather.  

3. Run the bot:

```bash
python bot.py
```

---

## 📝 Usage

### Main Menu

- **➕ Add event** – Add a new event with name, date, and optional yearly repeat  
- **📊 Days left** – Show all events with remaining days  
- **📅 My events** – List events individually, with options to edit or delete  
- **⏰ Notification time** – Set daily notification time with interactive hour/minute buttons  
- **🔔 Toggle notifications** – Enable/disable daily notifications  

### Inline Buttons

- **Month / Day / Year** selection when adding/editing events  
- **Repeat yearly** option  
- **Edit / Delete** individual events  
- **Hour / Minute** selection for notification time  

---

## 💾 Data Storage

The bot stores events in a local JSON file:

```text
events.json
```

Example structure:

```json
{
  "123456789": {
    "events": [
      {"name": "Birthday", "date": "2026-03-20", "repeat": true}
    ],
    "enabled": true,
    "hour": 10,
    "minute": 0
  }
}
```

---

## 🔧 Systemd Setup (Optional)

To run the bot **24/7** on a Linux server:

1. Create a systemd service file:

```ini
[Unit]
Description=Telegram Reminders Bot
After=network.target

[Service]
User=your_username
WorkingDirectory=/path/to/bot
ExecStart=/path/to/bot/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

2. Reload systemd and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-reminders
sudo systemctl start telegram-reminders
```

3. Check status:

```bash
sudo systemctl status telegram-reminders
```

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.  

---