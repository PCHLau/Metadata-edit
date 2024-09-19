import syncedlyrics
import re

def synlyr(track, artist):

    entry = track + ' ' + artist

    lrc = syncedlyrics.search(f'{entry}')

    lrc = lrc.split('\n')

    sdata = list()
    data = str()
    

    # data = str()

    for i in lrc:
        time  = int(i[7:9])*10 + int(i[4:6])*1000 + int(i[1:3])*1000*60
        text = i[11:]

        # data = data + '"' + text + '"' + ' $00 ' + str(time) + ' 0A '

        sdata.append((text, time))
        data = data + text + '\n'

    return sdata, data