# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from asyncio import sleep
from telethon import events
import telethon.utils
from telethon.errors import rpcbaseerrors

from Speedo.utils import admin_cmd, sudo_cmd, errors_handler
from Speedo import bot as Speedo
from Speedo import BOTLOG, BOTLOG_CHATID


@Speedo.on(admin_cmd(outgoing=True, pattern="del$"))
@Speedo.on(sudo_cmd(allow_sudo=True, pattern="del$"))
@errors_handler
async def delete_it(safai):
    """ For .del command, delete the replied message. """
    msg_src = await safai.get_reply_message()
    if safai.reply_to_msg_id:
        try:
            await msg_src.delete()
            await safai.delete()
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "#DEL \nDeletion of message was successful"
                )
        except rpcbaseerrors.BadRequestError:
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "Well, I can't delete a message"
                )