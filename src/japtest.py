import pykakasi
from syncedlyricstest import synlyr

def unsynced(lyrics):
    kks = pykakasi.kakasi()
    lyrics = lyrics.split('\n')
    end = str()
    for i in lyrics:
        if i == '':
            continue
        result = kks.convert(i)
        for i in result:
            end = end + i['hepburn']
        end = end + '\n'
    return end

def synced(lyrics):
    translated = list()
    kks = pykakasi.kakasi()
    for i in lyrics:
        # if i[0] == '':
        #     translated.append((i))
        #     continue
        result = kks.convert(i[0])
        line = str()
        for j in result:
            line = line + j['hepburn']
        translated.append((line, i[1]))
    return translated