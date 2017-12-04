import tweepy
import json
import urllib.request
import os
import random
from PIL import Image; import numpy as np
import sys
import io


consumer_key ="CONSUMER_KEY"
consumer_secret ="CONSUMER_SECRET"
access_token ="ACCESS_TOKEN"
access_token_secret ="ACCESS_TOKEN_SECRET"

auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

page = 1

images = []
imageNames = []

statuses = api.user_timeline(screen_name="cuteemergency")
if statuses:
    for status in statuses:
        statusJson = json.loads(json.dumps(status._json))
        if('media' in statusJson['entities']):
            image = statusJson['entities']['media'][0]['media_url']
            imageName = image.split('/')[-1]
            images.append(image)
            imageNames.append(imageName)

selector = random.randrange(0, len(images))


#ascii converter
chars = np.asarray(list(' .,:;irsXA253hMHGS#9B&@'))

#if len(sys.argv) != 4: print( 'Usage: ./asciinator.py image scale factor' ); sys.exit()
#gets argument
#f = picture path
#sc = scale factor
GCF, WCF = 3, 7/4

img_url = images[selector]
print(img_url)

file = io.BytesIO(urllib.request.urlopen(img_url).read())

img = Image.open(file)

#img = Image.open(f)

rows, columns = os.popen('stty size', 'r').read().split()
SC = float(img.size[1] / int(rows))
#S = ( round(img.size[0]*SC*WCF), round(img.size[1]*SC) )
#S = ( round((img.size[0] / int(columns)*WCF)), round((img.size[1] / int(rows))) )
print(img.size[0])
print(img.size[1])
aspectRation = (img.size[0])/(img.size[1] * WCF)
print(aspectRation)
if(img.size[0] >= img.size[1]):
    print("wide")
    S = (int(float(columns)), int(float(rows)))
else:
    print("tall")
    S = (int(float(columns)), int(float(rows)))

img = np.sum( np.asarray( img.resize(S) ), axis=2)
img -= img.min()
img = (1.0 - img/img.max())**GCF*(chars.size-1)

print( "\n".join( ("".join(r) for r in chars[img.astype(int)]) ) )
exit(0)
