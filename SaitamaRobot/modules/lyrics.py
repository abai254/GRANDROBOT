import re

import lyricsgenius

from SaitamaRobot.modules.disable import DisableAbleCommandHandler

from SaitamaRobot import dispatcher

async def lyrics(event):  # sourcery no-metrics
    "To fetch song lyrics"
    
    match = event.pattern_match.group(1)
    songno = re.findall(r"-n\d+", match)
    listview = re.findall(r"-l", match)
    try:
        songno = songno[0]
        songno = songno.replace("-n", "")
        match = match.replace("-n" + songno, "")
        songno = int(songno)
    except IndexError:
        songno = 1
    if songno < 1 or songno > 10:
        return m.reply(f"`song number must be in between 1 to 10 use -l flag to query results`",
        )
    match = match.replace("-l", "")
    listview = bool(listview)
    query = match.strip()
    genius = lyricsgenius.Genius(GENIUS)
    if "-" in query:
        args = query.split("-", 1)
        artist = args[0].strip(" ")
        song = args[1].strip(" ")
        m = message.reply(f"`Searching lyrics for {artist} - {song}...`"
        )
        try:
            songs = genius.search_song(song, artist)
        except TypeError:
            songs = None
        if songs is None:
            return m.edit(f"Song **{artist} - {song}** not found!")
        result = f"**Search query**: \n`{artist} - {song}`\n\n```{songs.lyrics}```"
    else:
        m = message.reply(f"`Searching lyrics for {query}...`")
        response = genius.search_songs(query)
        msg = f"**The songs found for the given query:** `{query}`\n\n"
        if len(response["hits"]) == 0:
            return m.edit(f"**I can't find lyrics for the given query: **`{query}`"
            )
        for i, an in enumerate(response["hits"], start=1):
            msg += f"{i}. `{an['result']['title']}`\n"
        if listview:
            result = msg
        else:
            result = f"**The song found for the given query:** `{query}`\n\n"
            if songno > len(response["hits"]):
                return m.edit(
                    f"**Invalid song  selection for the query select proper number**\n{msg}",
                )
            songtitle = response["hits"][songno - 1]["result"]["title"]
            result += f"`{genius.search_song(songtitle).lyrics}`"
            __help__ = """
             /lyrics- 
            `-l`: to get list of search lists.
            `-g`: To get paticular song lyrics.
  
            `lyrics -g <song name>`
            """
            
            
__mod_name__ = "Lyrics"

LYRICS_HANDLER = DisableAbleCommandHandler(
   "lyrics", lyrics)

dispatcher.add_handler(LYRICS_HANDLER)
