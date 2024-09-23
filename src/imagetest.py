import requests
import numpy as np
from PIL import Image

def cropper(url: str) -> None:
    """Crops image into desired size, usually square of adequate size

    Saves image as 'thumbnail.png'

    Parameters
    ----------

    url : str
        url at which target image is located

    """
    # initialise the image
    im = Image.open(requests.get(url, stream=True).raw)
    pix = im.load()

    # create standard square or standard 1280x720
    if im.size == (1280, 720):
        # initialise test square within expected border regions for later testing
        #  randomly select pixels from square
        hor_1 = np.random.randint(90,190, 10)
        hor_2 = np.random.randint(1090, 1190, 10)
        hor = np.concatenate((hor_1, hor_2))
        ver = np.random.randint(260,460,20)
        r = np.array([])
        g = np.array([])
        b = np.array([])
        # loads the colors of the pixels in border region into numpy arrays
        for i in range(len(hor)):
            for j in range(len(ver)):
                c = np.array(pix[i,j])
                r = np.append(r, c[0])
                g = np.append(g, c[1])
                b = np.append(b, c[2])
        # determine if border regions are of the same colour
        #  if so save square image, if not save rectangular image
        if np.max(r) - np.min(r) < 10 and np.max(g) - np.min(g) < 10 and np.max(b) - np.min(b) < 10:
            box = (280, 0, 1000, 720)
            region = im.crop(box)
            region.save("thumbnail.png")
        else:
            im.save("thumbnail.png")
    # for images of non-standard size, assumption is that these are all old album covers
    # need to be cropped into square of various sizes
    # might need to add functionality later for determining if image needs to be squared at all
    else:
        try:
            # crop into square of size height
            left = int((im.size[0]-im.size[1])/2)
            right = int(im.size[0] - ((im.size[0]-im.size[1])/2))
            box = (left, 0, right, im.size[1])
            region = im.crop(box)
            # initialise data for smaller square creation
            hor_mid = int((right-left)/2)
            ver_mid = int(im.size[1]/2)
            pix = region.load()
            rgbx = []
            rgby = []
            broke = False
            diff = 0
            # keeps searching from top and left center of the image for when the border region stops
            for i in range(im.size[1]):
                if broke:
                    break
                x = pix[i, ver_mid]
                y = pix[hor_mid, i]
                rgbx.append(x)
                rgby.append(y)
                if len(rgbx) > 2:
                    for j in range(3):
                        if abs(rgbx[-1][j] - rgbx[-2][j]) > 10 or abs(rgby[-1][j] - rgby[-2][j]) > 10:
                            broke = True
                            break
                diff = i
            # crop to remove border region
            box2 = (diff, diff, im.size[1]-diff, im.size[1]-diff)
            reg = region.crop(box2)
            reg.save("thumbnail.png")
        # in the case the image is already square
        except ZeroDivisionError:
            im.save("thumbnail.png")#

    return