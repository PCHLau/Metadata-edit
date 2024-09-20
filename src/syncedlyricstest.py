import syncedlyrics
import re

def synlyr(track, artist):

    entry = track + ' ' + artist

    sources = ['musixmatch', 'netease', 'lrclib']
    lrc = None

    length = 10000000
    for i in sources:
        # pick the source that starts the earliest
        result = syncedlyrics.search(f'{entry}', providers=[f'{i}'])
        # print(result)
        try:
            result = result.split('\n')
            if lrc == None:
                lrc = result
        except AttributeError:
            continue
        counter = 0
        if i == 'netease':
            ending = False
            endpoint = 0
            for i in range(len(result)):
                if ending == True:
                    break
                found = False
                for j in result[i]:
                    if found == True:
                        if j == ' ':
                            break
                        else:
                            ending = True
                            endpoint=i
                            break
                    if j == ']':
                        found = True
            
            result = result[endpoint:]
            


                    
            # while result[counter][11] == ' ':
            #     print('hi')
            #     counter+=1
            # result = result[counter:]
        time = int(result[counter][7:9])*10 + int(result[counter][4:6])*1000 + int(result[counter][1:3])*1000*60
        if time < length:
            length = time
            lrc = result

    print(lrc)

    # lrc = syncedlyrics.search(f'{entry}', providers=[true_source])

    # lrc = lrc.split('\n')

    sdata = list()
    data = str()
    

    # data = str()

    for i in lrc:
        if i =='':
            continue
        try:
            time  = int(i[7:9])*10 + int(i[4:6])*1000 + int(i[1:3])*1000*60
            text = i[11:]
            sdata.append((text, time))
            data = data + text + '\n'

        # account for different format, in this case unsynced lyrics with [verse] [chorus] etc
        except ValueError:
            print('hi')
            sdata = None
            for i in lrc:
                if i == '':
                    continue
                if i[0] == '[':
                    continue
                else:
                    data = data + i + '\n'

    return sdata, data

# print(synlyr('colors', 'flow'))