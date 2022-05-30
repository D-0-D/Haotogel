import contextlib
import logging
import os
import asyncio
from telethon import TelegramClient, events, Button, errors
from telethon.sessions import StringSession
from decouple import config

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(message)s",
)
log = logging.getLogger(__name__)

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


async def steal(chat_id, message_id, get_groups):
    try:
        message = (await client.get_messages(chat_id, ids=[message_id]))[0]
    except errors.FloodWaitError as e:
        await asyncio.sleep(e.seconds + 10)
        log.info("Floodwait, sleeping for %s seconds", (e.seconds + 10))
    media = await message.download_media()
    msg = message.text
    buttons = message.buttons or []
    logged = await client.upload_file(media) if media else None
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
        try:
            await client.send_message(
                int(i), msg, file=logged, buttons=buttons, noforwards=True
            )
        except errors.FloodWaitError as e:
            await asyncio.sleep(e.seconds + 10)
            log.info("Floodwait, sleeping for %s seconds.", (e.seconds + 10))
    if media and os.path.exists(media):
        os.remove(media)


@client.on(events.ChatAction())
async def chataction(event):
    with contextlib.suppress(Exception):
        if event.user_joined or event.user_added:
            user = await event.get_user()
            full_name = ""
            if user.first_name:
                full_name += f"{user.first_name}"
            if user.last_name:
                full_name += f" {user.last_name}"
            msg = await event.reply(
                f"Hi [{full_name}](tg://user?id={user.id}), welcome to the chat!"
            )
            await asyncio.sleep(60)
            await msg.delete()


log.info("Started userbot.")
client.run_until_disconnected()
