from urllib import parse
from lxml import etree
from urllib3 import disable_warnings
import requests
import csv
import re
import urllib.request
import urllib.error
import urllib.parse
import cloudmusic
import pandas as pd
'''
headers = {  # 请求头部
        'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
'''
def get_song(data2,data4):

    for j in range(len(data2)):
        musiclist=cloudmusic.getPlaylist(data2[j])
        for music in musiclist:

            writer.writerow([music.id, music.name, music.url, music.artist,music.artistId, music.album,music.albumId,data4[j],data2[j]])
    csv_file.close()



#读csv表格
data = pd.read_csv(r'.\\playlist.csv', header=0,encoding='utf-8')
data1=data.loc[:, ['playlist_id']]
data2=data1.values
data3=data.loc[:, [ 'Playlist_label']]
data4=data3.values

csv_file = open("song.csv", "a", encoding='utf-8', newline='')
writer = csv.writer(csv_file)
writer.writerow(['song_id', 'song_name', 'song_url', 'song_artist', 'artistid', 'album','albumid','song_label','playlist_id'])
#print(data2[0][0])
get_song(data2,data4)