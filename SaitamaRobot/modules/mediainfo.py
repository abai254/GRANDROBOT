import os
import time
from datetime import datetime as dt

from . import *

async def mi(e):
    r = await e.get_reply_message()
    if not (r and r.media):
        return await eod(e, "`Reply to any media`")
    xx = mediainfo(r.media)
    murl = r.media.stringify()
    url = make_html_telegraph("Mediainfo", "Ultroid", f"<code>{murl}</code>")
    ee = await eor(e, f"**[{xx}]({url})**\n\n`Loading More...`", link_preview=False)
    taime = time.time()
    if hasattr(r.media, "document"):
        file = r.media.document
        mime_type = file.mime_type
        filename = r.file.name
        if not filename:
            if "audio" in mime_type:
                filename = "audio_" + dt.now().isoformat("_", "seconds") + ".ogg"
            elif "video" in mime_type:
                filename = "video_" + dt.now().isoformat("_", "seconds") + ".mp4"
        dl = await downloader(
            "resources/downloads/" + filename,
            file,
            ee,
            taime,
            f"`**[{xx}]({url})**\n\n`Loading More...",
        )
        naam = dl.name
    else:
        naam = await r.download_media()
    out, er = await bash(f"mediainfo '{naam}' --Output=HTML")
    urll = make_html_telegraph("Mediainfo", "Ultroid", out)
    if er:
        return await ee.edit(f"**[{xx}]({url})**", link_preview=False)
    await ee.edit(
        f"**[{xx}]({url})**\n\n[More Explained Info]({urll})", link_preview=False
    )
    os.remove(naam)
    
    __help__ = """
 ❍ /mi or /mediainfo get mediainfo of replied media
"""

MEDIAINFO_HANDLER = DisableAbleCommandHandler(["mi", "mediainfo"], mi)

dispatcher.add_handler(MEDIAINFO_HANDLER)

__mod_name__ = "MediaInfo"
__command_list__ = ["mi", "mediainfo"]
__handlers__ = [MEDIAINFO_HANDLER]
