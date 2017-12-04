import urllib.request
import os
from PIL import Image
import numpy as np
import sys
import io
import time
from termcolor import colored, cprint
import colorconsole.terminal


chars = np.asarray(list(' .,:;irsXA253hMHGS#9B&@'))

#if len(sys.argv) != 4: print( 'Usage: ./asciinator.py image scale factor' ); sys.exit()
#gets argument
#f = picture path
#sc = scale factor
GCF, WCF = 1, 7/4

#img_url = images[selector]
#print(img_url)

#le = io.BytesIO(urllib.request.urlopen(img_url).

if(len(sys.argv) >= 2):
    image_path = sys.argv[2]

img = Image.open(image_path) #PATH TO GIF TO B PLAYED
#img = Image.open(file)

#img = Image.open(f)


rows, columns = os.popen('stty size', 'r').read().split()


def printAscii(img):
    SC = float(img.size[1] / int(rows))
    #print(img.size[0])
    #print(img.size[1])

    aspectRation = (img.size[0])/(img.size[1] * WCF)
    #print(aspectRation)

    if(img.size[0] >= img.size[1]):
        #print("wid
        S = (int(float(columns)), int(float(rows)))
    else:
        #print("tall")
        S = (int(float(columns)), int(float(rows)))

#    print(S)
    px = np.asarray(img.resize(S))
    ts = px.ravel()
    img = np.sum( np.asarray( img.resize(S) ), axis=2)
    img -= img.min()
    img = (1.0 - img/img.max())**GCF*(chars.size-1)

    number = 0;
    x = 0
    y = 0
    '''
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
print(R+"hello how are you"+W)



    '''
#    colorconsole.terminal.get_terminal().xterm24bit_set_fg_color(255, 255,  0)
    W  = '\033[0m'  # white (normal)
    R  = '\033[31m' # red
    G  = '\033[32m' # green
    O  = '\033[33m' # orange
    B  = '\033[34m' # blue
    P  = '\033[35m' # purple
    #print( "\n".join( ("".join(r) for r in chars[img.astype(int)]) ) )
    if(len(sys.argv) >= 3 and  sys.argv[2] == "-color"):
        con = colorconsole.terminal.get_terminal()
        for k in img.astype(int):
            x = 0
            y += 1
            output = []
            for r in chars[k]:
                x += 1
                number+=1

                #red = ts[number * 3]
                #green = ts[number * 3 + 1]
                #blue = ts[number * 3 + 2]
                red = px[y-1][x-1][0]
                green = px[y-1][x-1][1]
                blue = px[y-1][x-1][2]
                color = (red, green, blue)
                con.xterm24bit_set_fg_color(red, green,  blue)
                con.print_at(x-1, y-1, "".join(r))
    else:
        print( "\n".join( ("".join(r) for r in chars[img.astype(int)]) ) )



def analyseImage(path):
    '''
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode
    before processing all frames.
    '''
    im = Image.open(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results

def loadGif():
    mode = analyseImage(image_path)['mode']

    im = Image.open(image_path)

    i = 0
    p = im.getpalette()
    last_frame = im.convert('RGBA')
    try:
        while True:
#            print "saving %s (%s) frame %d, %s %s" % (path, mode, i, im.size, im.tile)

            '''
            If the GIF uses local colour tables, each frame will have its own palette.
            If not, we need to apply the global palette to the new frame.
            '''
            if not im.getpalette():
                im.putpalette(p)

            new_frame = Image.new('RGBA', im.size)

            '''
            Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
            If so, we need to construct the new frame by pasting it on top of the preceding frames.
            '''
            if mode == 'partial':
                new_frame.paste(last_frame)

            new_frame.paste(im, (0,0), im.convert('RGBA'))
#            new_frame.save('%s-%d.png' % (''.join(os.path.basename(path).split('.')[:-1]), i), 'PNG')

            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
            printAscii(new_frame)
            time.sleep(0.1)
    except EOFError:
        pass

while 1:
    loadGif()

exit(0)
