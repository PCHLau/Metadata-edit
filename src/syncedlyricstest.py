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

        try:
            time  = int(i[7:9])*10 + int(i[4:6])*1000 + int(i[1:3])*1000*60
            text = i[11:]
            sdata.append((text, time))
            data = data + text + '\n'
        except ValueError:
            sdata = None
            for i in lrc:
                if i == '':
                    continue
                if i[0] == '[':
                    continue
                else:
                    data = data + i + '\n'

    return sdata, data