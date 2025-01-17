import pyfiglet

from Speedo import CMD_HELP
from Speedo.utils import admin_cmd, edit_or_reply, sudo_cmd
from Speedo.cmdhelp import CmdHelp

@bot.on(admin_cmd(pattern="figlet ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="figlet ?(.*)", allow_sudo=True))
async def figlet(event):
    if event.fwd_from:
        return
    CMD_FIG = {
        "slant": "slant",
        "3D": "3-d",
        "5line": "5lineoblique",
        "alpha": "alphabet",
        "banner": "banner3-D",
        "doh": "doh",
        "iso": "isometric1",
        "letter": "letters",
        "allig": "alligator",
        "dotm": "dotmatrix",
        "bubble": "bubble",
        "bulb": "bulbhead",
        "digi": "digital",
    }
    input_str = event.pattern_match.group(1)
    if ":" in input_str:
        text, cmd = input_str.split(":", maxsplit=1)
    elif input_str is not None:
        cmd = None
        text = input_str
    else:
        await edit_or_reply(event, "Please add some text to figlet")
        return
    if cmd is not None:
        cmd = cmd.strip()
        try:
            font = CMD_FIG[cmd]
        except KeyError:
            await edit_or_reply(event, "Invalid selected font.")
            return
        result = pyfiglet.figlet_format(text, font=font)
    else:
        result = pyfiglet.figlet_format(text)
    await edit_or_reply(event, "‌‌‎`{}`".format(result))


CmdHelp("figlet").add_command(
  'figlet', 'text or text : type', 'The types are slant, 3D, 5line, alpha, banner, doh, iso, letter, allig, dotm, bubble, bulb, digi'
).add()