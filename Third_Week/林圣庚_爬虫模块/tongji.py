
import csv

import cloudmusic
import pandas as pd


#读csv表格
data = pd.read_csv(r'.\\song_20200910_utf8.csv', header=0,encoding='utf-8')
data1=data.loc[:, ['song_label']]
data2=data1.values

biaoqian=[]
for i in range(len(data2)):
    biaoqian.append(data2[i][0])
print(biaoqian[0])
liuxing=0
shuochang=0
qingyinyue=0
yaogun=0
huayu=0
omei=0
langman=0
for i in range(len(biaoqian)):
    if '流行' in biaoqian[i]:
        liuxing=liuxing+1
    if '说唱' in biaoqian[i]:
        shuochang=shuochang+1
    if '轻音乐' in biaoqian[i]:
        qingyinyue=qingyinyue+1
    if '摇滚' in biaoqian[i]:
        yaogun=yaogun+1
    if '华语' in biaoqian[i]:
        huayu=huayu+1
    if '欧美' in biaoqian[i]:
        omei=omei+1
    if '浪漫' in biaoqian[i]:
        langman=langman+1

print(liuxing)
print(shuochang)
print(qingyinyue)
print(yaogun)
print(huayu)
print(omei)
print(langman)

import matplotlib.pyplot as plt
import numpy as np

# 这两行代码解决 plt 中文显示的问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

waters = ('流行', '说唱', '轻音乐', '摇滚', '华语','欧美','浪漫')
buy_number = [liuxing, shuochang, qingyinyue, yaogun, huayu,omei,langman]

bars=plt.bar(waters, buy_number)
for bar in bars:
    bar.set_color('#' + str(np.random.randint(100000, 999999)))
plt.title('网易云最受欢迎的歌曲风格统计')

plt.show()


'''


csv_file = open("song.csv", "a", encoding='utf-8', newline='')
writer = csv.writer(csv_file)
writer.writerow(['song_id', 'song_name', 'song_url', 'song_artist', 'artistid', 'album','albumid','song_label','playlist_id'])
#print(data2[0][0])
get_song(data2,data4)


'''