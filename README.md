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

3. Create a small **startup script** `start_bot.sh` in the bot folder:

```bash
#!/bin/bash
source /path/to/bot/venv/bin/activate
cd /path/to/bot
python bot.py
```

Make it executable:

```bash
chmod +x start_bot.sh
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

To run the bot **24/7** on a Linux server using the startup script:

1. Create a systemd service file:

```ini
[Unit]
Description=Telegram Reminders Bot
After=network.target

[Service]
User=your_username
WorkingDirectory=/path/to/bot
ExecStart=/path/to/bot/start_bot.sh
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

✅ Now the bot will run inside your venv automatically.

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.  