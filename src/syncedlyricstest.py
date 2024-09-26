import syncedlyrics # type: ignore

def synlyr(track: str, artist: str) -> tuple[list, str]:
    """Fetches synced lyrics using syncedlyrics, then reformats it

    Parameters
    ----------
    track : str
        Name of song/track
    artist : str
        Name of artist

    Returns
    -------
    sdata: list
        Synced lyrics in list format
    data: str
        Unsynced lyrics, created from synced lyrics after reformatting
    """

    # Initialise search entry
    entry = track + ' ' + artist
    # Order lyrics source hierarchy
    sources = ['netease', 'musixmatch', 'lrclib']
    # Standard synced lyrics start index for [xx:xx.xx] time format
    index=11
    source = ''
    for i in sources:
        source = i
        # Find lyrics
        lyrics: str = syncedlyrics.search(f'{entry}', providers=[f'{i}'])
        try:
            lrc = lyrics.split('\n')
        except AttributeError:
            continue
        # Netease has special format
        if i == 'netease':
            ending = False
            endpoint = 0
            # First few lines give song/artist details
            # Those lines have an extra ' ' extra timestamp
            # They are found and removed
            for j, line in enumerate(lrc):
                # If the last row of details is found, break
                if ending:
                    break
                found = False
                counter = 0
                for k in line:
                    # if the right square bracket is found
                    if found:
                        # If next is ' ', then it's still details line
                        if k == ' ':
                            break
                        # If not, lyrics have started, and loop will break next loop
                        else:
                            ending = True
                            endpoint=j
                            break
                    # Find where right bracket is, both for loop
                    # And finding timestamp format
                    if k == ']':
                        index = counter + 1
                        found = True
                    counter += 1
            # Cut out details
            lrc = lrc[endpoint:]
            # Remove weird characters
            for a, b in enumerate(lrc):
                lrc[a] = b.replace('\xa0',' ')
                # i = i.replace('\xa0', ' ')

        break

    sdata = list()
    data = str()

    for i in lrc:
        # ignore empty elements
        if i =='':
            continue
        # separate time (in ms) and text with previously determined index
        try:
            time  = int(i[7:9])*10 + int(i[4:6])*1000 + int(i[1:3])*1000*60
            text = i[index:]
            sdata.append((text, time))
            data = data + text + '\n'

        # account for different format, in this case unsynced lyrics with [verse] [chorus] etc
        except ValueError:
            sdata = None # type: ignore
            for i in lrc:
                if i == '':
                    continue
                if i[0] == '[':
                    continue
                else:
                    data = data + i + '\n'

    return sdata, data
