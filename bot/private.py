# Daisyxmusic  & Sophia Video Player   (Telegram bot project )

# Copyright (C) 2021  Dihan Official

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import logging
from bot.msg import Messages as tr
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import Sophia
logging.basicConfig(level=logging.INFO)

@Client.on_message(filters.private & filters.incoming & filters.command(['start']))
def _start(client, message):
    client.send_message(message.chat.id,
        text=tr.START_MSG.format(message.from_user.first_name, message.from_user.id),
        parse_mode="markdown",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("➕ Add me to your Group 🙋‍♀️", url=f"https://t.me/{Sophia.BOT_USERNAME}?startgroup=true")
            ],[
            InlineKeyboardButton("📲 Updates", url=f"https://t.me/sophiaupdates"), 
            InlineKeyboardButton("💬 Support", url=f"https://t.me/sophiasupport_official")
            ],[
            InlineKeyboardButton("🛠 Source Code 🛠", url=f"https://github.com/sophiavideoplayer")
          ]]
        ),
        reply_to_message_id=message.message_id
        )

@Client.on_message(filters.command("start") & ~filters.private & ~filters.channel)
async def gstart(_, message: Message):
    await message.reply_text(
        f"""** Sophia Video Player is online ✅ **""",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬 Support Chat", url=f"https://t.me/sophiasupport_official")]]),
    )


@Client.on_message(filters.private & filters.incoming & filters.command(['help']))
def _help(client, message):
    client.send_message(chat_id = message.chat.id,
        text = tr.HELP_MSG[1],
        parse_mode="markdown",
        disable_web_page_preview=True,
        disable_notification=True,
        reply_markup = InlineKeyboardMarkup(map(1)),
        reply_to_message_id = message.message_id
    )

help_callback_filter = filters.create(lambda _, __, query: query.data.startswith('help+'))

@Client.on_callback_query(help_callback_filter)
def help_answer(client, callback_query):
    chat_id = callback_query.from_user.id
    disable_web_page_preview=True
    message_id = callback_query.message.message_id
    msg = int(callback_query.data.split('+')[1])
    client.edit_message_text(chat_id=chat_id,    message_id=message_id,
        text=tr.HELP_MSG[msg],    reply_markup=InlineKeyboardMarkup(map(msg))
    )


def map(pos):
    if(pos==1):
        button = [
            [InlineKeyboardButton(text = '▶️', callback_data = "help+2")]
        ]
    elif(pos==len(tr.HELP_MSG)-1):
        url = f"https://t.me/SophiaSupport_Official"
        button = [
            [InlineKeyboardButton("➕ Add me to your Group 🙋‍♀️", url=f"https://t.me/{Sophia.BOT_USERNAME}?startgroup=true")],
            [InlineKeyboardButton(text = '📲 Updates', url=f"https://t.me/SophiaUpdates"),
             InlineKeyboardButton(text = '💬 Support', url=f"https://t.me/SophiaSupport_Official")],
            [InlineKeyboardButton(text = '🛠 Source Code 🛠', url=f"https://github.com/sophiavideoplayer")],
            [InlineKeyboardButton(text = '◀️', callback_data = f"help+{pos-1}")]
        ]
    else:
        button = [[
                     InlineKeyboardButton(text = '◀️', callback_data = f"help+{pos-1}"),
                     InlineKeyboardButton(text = '▶️', callback_data = f"help+{pos+1}")
                 ]]
    return button

@Client.on_message(filters.command("help") & ~filters.private & ~filters.channel)
async def ghelp(_, message: Message):
    await message.reply_text(
        f"""**🙋‍♀️ Hello there! I can Stream Youtube Live & Videos in the voice chats of telegram groups & channels.**""",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🟡 Click here for help 🟡", url=f"https://t.me/{Sophia.BOT_USERNAME}?start")]]),
    )
