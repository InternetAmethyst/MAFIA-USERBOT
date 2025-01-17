import re

import bs4
import requests
from Speedo.utils import admin_cmd, sudo_cmd, edit_or_reply
from Speedo.cmdhelp import CmdHelp


@bot.on(admin_cmd(pattern="giz ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="giz ?(.*)", allow_sudo=True))
async def gizoogle(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await edit_or_reply(event, "Processing...")
    if not input_str:
        return await edit_or_reply(event, "I can't gizoogle nothing.")
    else:
        try:
            result = text(input_str)
        except:
            result = "Failed to gizoogle the text."
        finally:
            return await edit_or_reply(event, result)


def text(input_text: str) -> str:
    """Taken from https://github.com/chafla/gizoogle-py/blob/master/gizoogle.py"""
    params = {"translatetext": input_text}
    target_url = "http://www.gizoogle.net/textilizer.php"
    resp = requests.post(target_url, data=params)
    # the html returned is in poor form normally.
    soup_input = re.sub(
        "/name=translatetext[^>]*>/", 'name="translatetext" >', resp.text
    )
    soup = bs4.BeautifulSoup(soup_input, "lxml")
    giz = soup.find_all(text=True)
    giz_text = giz[37].strip("\r\n")  # Hacky, but consistent.
    return giz_text

CmdHelp("gizoogle").add_command(
  "giz", "<your sentence>", "Gives you the provided sentence in gangsters language. #Dope_AF")