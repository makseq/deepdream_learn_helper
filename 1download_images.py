#!/usr/bin/python
from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import cookielib
import json


def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)), 'html.parser')


def get_soup_file(url,header):
    return BeautifulSoup(open(url), 'html.parser')

work_dir = 'data'
print 'Enter working dir (where you stored input.html): ',
work_dir = raw_input()

query = 'download'
image_type="ActiOn"
query= query.split()
query='+'.join(query)
#url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
url = work_dir + '/input.html'
print url

#add the directory for your image here
DIR=work_dir
header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
soup = get_soup_file(url, header)


ActualImages = []  # contains the link for Large original images, type of  image
for a in soup.find_all("div", {"class": "rg_meta"}):
    link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
    ActualImages.append((link, Type))

print "there are total", len(ActualImages), "images"

if not os.path.exists(DIR):
    os.mkdir(DIR)
DIR = os.path.join(DIR, query.split()[0])

if not os.path.exists(DIR):
    os.mkdir(DIR)

### print images
for i, (img, Type) in enumerate(ActualImages):
    try:
        req = urllib2.Request(img, headers={'User-Agent': header})
        raw_img = urllib2.urlopen(req).read()

        cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
        print cntr
        path = os.path.join(DIR, image_type + "_"+ str(cntr)+".jpg") if len(Type)==0 else os.path.join(DIR, image_type + "_" + str(cntr) + "." + Type)
        if os.path.exists(path):
            continue
        f = open(path, 'wb')
        f.write(raw_img)
        f.close()
    except Exception as e:
        print "could not load : "+img
        print e
