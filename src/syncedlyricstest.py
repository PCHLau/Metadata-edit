import syncedlyrics
import re

def synlyr(track, artist):

    entry = track + ' ' + artist

    sources = ['netease', 'musixmatch', 'lrclib']
    index=11
    for i in sources:
        # pick the source that starts the earliest
        lrc = syncedlyrics.search(f'{entry}', providers=[f'{i}'])
        try:
            lrc = lrc.split('\n')
        except AttributeError:
            continue

        if i == 'netease':
            ending = False
            endpoint = 0
            for i in range(len(lrc)):
                if ending == True:
                    break
                found = False
                counter = 0
                for j in lrc[i]:
                    if found == True:
                        if j == ' ':
                            break
                        else:
                            ending = True
                            endpoint=i
                            break
                    if j == ']':
                        index = counter + 1
                        found = True
                    counter += 1
            
            lrc = lrc[endpoint:]

            for a, b in enumerate(lrc):
                lrc[a] = b.replace('\xa0',' ')
                # i = i.replace('\xa0', ' ')

        break

    sdata = list()
    data = str()

    for i in lrc:
        if i =='':
            continue
        try:
            time  = int(i[7:9])*10 + int(i[4:6])*1000 + int(i[1:3])*1000*60
            text = i[index:]
            sdata.append((text, time))
            data = data + text + '\n'

        # account for different format, in this case unsynced lyrics with [verse] [chorus] etc
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