from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
import os
import logging

# 🔥 Logging (Terminal)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# 🔑 ENV VARIABLES (Heroku Config Vars)
API_ID = int(os.environ.get("API_ID", "123456"))
API_HASH = os.environ.get("API_HASH", "YOUR_API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN")

# 📢 Logger Channel (Telegram)
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0"))

# 👇 Channels list (public + private)
CHANNELS = [
    "channel1",
    "channel2",
    "channel3",
    "your_private_channel"
]

app = Client(
    "mustjoinbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ✅ Check if user joined all channels
async def is_joined_all(client, user_id):
    for ch in CHANNELS:
        try:
            member = await client.get_chat_member(ch, user_id)
            if member.status in ["left", "kicked"]:
                return False
        except UserNotParticipant:
            return False
    return True

# 🚀 START COMMAND
@app.on_message(filters.command("start"))
async def start(client, message):
    user = message.from_user

    # 🔥 Terminal Log
    logging.info(f"START -> {user.id} | {user.first_name} | @{user.username}")

    # 📢 Telegram Log
    if LOG_CHANNEL:
        try:
            await client.send_message(
                LOG_CHANNEL,
                f"🚀 New User Started Bot\n\n"
                f"👤 Name: {user.first_name}\n"
                f"🆔 ID: {user.id}\n"
                f"🔗 Username: @{user.username}"
            )
        except:
            pass

    # ❌ Not Joined
    if not await is_joined_all(client, user.id):

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔥 Join mms Channel 1", url="https://t.me/+DbhAK7r-j65kZTI5")],
            [InlineKeyboardButton("⚡ mallu Channel 2", url="https://t.me/+p7W5R59EqCtiYTNl")],
            [InlineKeyboardButton("💎 Join desi Channel 3", url="https://t.me/+ozB_lh6oVjs0YTAx")],
            [InlineKeyboardButton("🔒 Join desi Private Channel", url="https://t.me/+DPyCRXqNcSRkZmZl")],
            [InlineKeyboardButton("✅ Joined / Requested", callback_data="check_join")]
        ])

        await message.reply(
            "⏳ Bhai pehle sab channels join karo 👇\n\n"
            "👉 Private desi channel me request bhejna padega\n"
            "👉 Admin approve karega tabhi video access milega",
            reply_markup=buttons
        )

    # ✅ Joined
    else:
        await message.reply("✅ Welcome bhai! Tum join kar chuke ho 🚀")

# 🔄 CHECK JOIN BUTTON
@app.on_callback_query(filters.regex("check_join"))
async def check_join(client, callback_query):
    user = callback_query.from_user

    # 🔥 Terminal log
    logging.info(f"CHECK JOIN -> {user.id}")

    if await is_joined_all(client, user.id):
        await callback_query.message.edit(
            "✅ Approval done! Ab tum access use kar sakte ho 🚀"
        )
    else:
        await callback_query.answer(
            "⏳ Abhi pending hai ya join nahi kiya!",
            show_alert=True
        )

app.run()
