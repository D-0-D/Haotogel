import logging
import os
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from decouple import config

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(message)s",
)
log = logging.getLogger(__name__)

log.info("Connecting bot...")
try:
    bot = TelegramClient(None, config("API_ID", cast=int), config("API_HASH")).start(
        bot_token=config("BOT_TOKEN")
    )
except Exception as e:
    log.error(e)
    exit(1)
log.info("Connected bot.")

log.info("Connecting user...")
try:
    client = TelegramClient(
        StringSession(config("SESSION")), config("API_ID", cast=int), config("API_HASH")
    ).start()
except Exception as e:
    log.error(e)
    exit(1)
log.info("Connected user.")

try:
    chats = eval(config("CHATS"))
except Exception as e:
    log.error(e)
    log.error("Malformed CHATS config.")
    exit(0)

# log_chat = config("LOG_CHAT", cast=int)

target_channels = [int(i) for i in chats]


@client.on(events.NewMessage(chats=target_channels))
async def listener(event):
    get_groups = chats[event.chat_id]
    await steal(event.chat_id, event.message.id, get_groups)


@bot.on(events.NewMessage(pattern="/start"))
async def send_welcome(event):
    await event.reply(
        "Hai bosku, Kamu akan di hubungkan dengan salah satu admin kami.\nMohon tunggu !\n\nPastikan bosku hanya mendaftar di link resmi official HAOTOGEL. link pendaftaran klik tombol di bawah ini👇",
        buttons=[
            Button.url("🔥 LINK DAFTAR RESMI 🔥", url="bit.ly/Haotogel-Official"),
            Button.url("💥 LINK ALTERNATIF 💥", url="bit.ly/ALTERNATIF-HAOTOGEL"),
        ],
    )


async def steal(chat_id, message_id, get_groups):
    message = (await client.get_messages(chat_id, ids=[message_id]))[0]
    media = await message.download_media()
    msg = message.text
    buttons = message.buttons or []
    logged = await bot.upload_file(media) if media else None
    buttons.append(
        [Button.url("🔥 DAFTAR DI SINI 🔥", url="https://bit.ly/Haotogel-Official")],
    )
    buttons.append(
        [Button.url("💥 LINK ALTERNATIF 💥", url="https://bit.ly/ALTERNATIF-HAOTOGEL")],
    )
    buttons.append(
        [Button.url("🎯 PREDIKSI 🎯", url="https://t.me/HaoTogelLivedraw")],
    )
    # logged_ = await client.send_message(log_chat, msg, file=media)
    # msg = (await client.get_messages(log_chat, ids=[logged_.id]))[0]
    for i in get_groups:
        await bot.send_message(
            int(i), msg, file=logged, buttons=buttons, noforwards=True
        )
    if media and os.path.exists(media):
        os.remove(media)


log.info("Started bot.")
client.run_until_disconnected()
