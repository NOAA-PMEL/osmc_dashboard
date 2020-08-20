import feedparser as fp
import requests
import zipfile
import shutil
import os.path
from os import path


def get_cones(url):

    feed = fp.parse(url)

    for e in feed['entries']:
        if "Cone" in e['title']:
            kmz = requests.get(e['link'], allow_redirects=True)
            open('cones_download.kmz', 'w+b').write(kmz.content)
            with zipfile.ZipFile('cones_download.kmz', 'r') as zip_ref:
                zip_ref.extractall('cones')


def clean(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


clean('cones')
if not path.exists('cones'):
    os.makedirs('cones')


get_cones('https://www.nhc.noaa.gov/gis-at.xml')
get_cones('https://www.nhc.noaa.gov/gis-ep.xml')
