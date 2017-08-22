# http://swopenAPI.seoul.go.kr/api/subway/(인증키)/xml/realtimeStationArrival/0/5/서울
# https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts/python

import random
import requests
from xml.etree import ElementTree
import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import time 
import numpy
import pickle
import pandas as pd

# Seoul Open API key
key='XXXX'
url1='http://openAPI.seoul.go.kr:8088/'
url2='/xml/SemaPsgudInfoEng/1/1000/'

url = url1 + key + url2
req = requests.request('GET', url)
tree = ElementTree.fromstring(req.content)

# MS congnitive service key
subscription_key = 'XXXX'

headers = {
    # Request headers.
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

params = urllib.parse.urlencode({
    # Request parameters. All of them are optional.
    'visualFeatures': 'Categories,Description,Color',
    'language': 'en',
})

imageinfo = []
picurl = []

# hold because of MS API limit
hold = numpy.arange(3, 961, 19)

for i in range(3,961):
# Replace the three dots below with the URL of a JPEG image of a celebrity.
    body = "{'url':'"+ tree[i][18].text + "'}"
    if i in hold:
        time.sleep(62)
# try:
    # Execute the REST API call and get the response.
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        imageinfo.append(data)
        picurl.append(tree[i][18].text)
    else:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        imageinfo.append(data)
        picurl.append(tree[i][18].text)

# check data len
len(imageinfo)
len(picurl)

# data backup
with open("imageinfo_full.txt", "wb") as fp:   #Pickling
    pickle.dump(imageinfo, fp)

# data w/ image info
check=[]

for i in range(0,len(imageinfo)):
    data = json.loads(imageinfo[i])
    check.append(data)

text_df=pd.DataFrame(check)

# url data
text_url=pd.DataFrame(picurl)
text_url.columns = ['url']

text = pd.concat([text_df, text_url], axis=1)

# artworks image url
showpic=[]

for i in range(3,961):
    showpic.append(tree[i][17].text)

text_show=pd.DataFrame(showpic)
text_show.columns = ['show']

text = pd.concat([text, text_show], axis=1)

# title and info
nametitle=[]

for i in range(3,961):
    nametitle_str=repr(tree[i][6].text)+"/ "+repr(tree[i][9].text)+"/ "+repr(tree[i][16].text)
    nametitle.append(nametitle_str)

text_title=pd.DataFrame(nametitle)
text_title.columns = ['title']
text = pd.concat([text, text_title], axis=1)

text_wo_na=text.fillna(0)

# write all data w/ csv file
text_wo_na.to_csv('text_pic_title_en.csv', encoding='utf-8')
