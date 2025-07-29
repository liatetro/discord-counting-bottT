import discord
from discord.ext import commands
import random
import json
import os

# --- הגדרות הבוט ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # חשוב בשביל חלוקת רולים

bot = commands.Bot(command_prefix="!", intents=intents)

# --- הגדרות ספציפיות לחדר ---
COUNTING_CHANNEL_ID = 1399454279948828712
current_count = 0
last_user_id = None

# --- קובץ שמירת זהב ---
GOLD_DATA_FILE = "gold_data.json"
ROLE_PRIZES = ["שקט", "תותח/ית", "מרשמלו", "בר מזל", "גיימר/ית"]

# --- ניהול הזהב ---
def load_gold_data():
    if os.path.exists(GOLD_DATA_FILE):
        with open(GOLD_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_gold_data(data):
    with open(GOLD_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_gold(user_id, amount):
    data = load_gold_data()
    data[str(user_id)] = data.get(str(user_id), 0) + amount
    save_gold_data(data)

# --- כשהבוט מתחבר ---
@bot.event
async def on_ready():
    print(f"הבוט מחובר בתור {bot.user}")

# --- טיפול בהודעות בספירה ---
@bot.event
async def on_message(message):
    global current_count, last_user_id

    if message.author.bot:
        return

    if message.channel.id != COUNTING_CHANNEL_ID:
        return

    try:
        number = int(message.content)
    except ValueError:
        await message.delete()
        return

    if number != current_count + 1 or message.author.id == last_user_id:
        await message.delete()
        return

    current_count += 1
    last_user_id = message.author.id

    # סיכוי של 5% לפרס
    if random.random() <= 0.05:
        prize_type = random.choice(["gold", "role"])

        if prize_type == "gold":
            amount = random.randint(10000, 50000)
            add_gold(message.author.id, amount)
            await message.reply(f"🏅 זכית ב־{amount} מטילי זהב!")
        else:
            role_name = random.choice(ROLE_PRIZES)
            role = discord.utils.get(message.guild.roles, name=role_name)
            if role:
                await message.author.add_roles(role)
                await message.reply(f"🎉 קיבלת את הרול **{role_name}**!")

    await bot.process_commands(message)

# --- התחלת הבוט ---
with open("token.txt") as f:
    token = f.read().strip()

bot.run(token)

