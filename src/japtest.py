import pykakasi

def unsynced(lrc: str) -> str:
    """Takes in string format unsynced lyrics and translates japanese to romaji

    Parameters
    ----------
    lyrics : str
        Imported unsynced lyrics from elsewhere 

    Returns
    -------
    str
        Unsynced lyrics in romaji
    """
    kks = pykakasi.kakasi()
    lyrics = lrc.split('\n')
    end = str()
    for i in lyrics:
        # empty string otherwise creates error with translation module
        if i == '':
            continue
        result = kks.convert(i)
        # module returns dict., we want hepburn
        for j in result:
            end = end + j['hepburn']
        end = end + '\n'
    return end

def synced(slyrics: list) -> list:
    """Takes in list format synced lyrics and translated japanese to romaji

    Parameters
    ----------
    slyrics : list
        Imported synced lyrics from elsewhere

    Returns
    -------
    list
        Synced lyrics in romaji
    """
    translated = list()
    kks = pykakasi.kakasi()
    for i in slyrics:
        result = kks.convert(i[0])
        line = str()
        for j in result:
            line = line + j['hepburn']
        translated.append((line, i[1]))
    return translated
