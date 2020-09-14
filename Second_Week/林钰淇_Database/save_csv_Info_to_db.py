import numpy as np
import pandas as pd
import Recommendation_System_db
import time
import warnings
import pickle
warnings.filterwarnings("ignore")

'''----------------------song_info--------------------------'''

df = pd.read_csv('song-test.csv',header=0,encoding='gbk')
print(df.head())

df = df[['song_id','song_name','song_artist','playlist_id','song_label']]
print(df.head())
print(len(df))
#print(df['song_label'][0])
for k in range(len(df)):
    df['song_artist'][k] = df['song_artist'][k][1:-1] 
    df['playlist_id'][k] = df['playlist_id'][k][1:-1] 
    df['song_label'][k] = df['song_label'][k][1:-1]
    #print(df['song_label'][k])
print(df.head(10))
#print(df['song_label'][1:5])
#print(df['song_label'].values[1:5][1:-2])
data = df.values
#print(data)


'''----------------------song_sheet_info----------------------'''

df2 = pd.read_csv('playlist-test.csv',header=0,encoding='gbk')
print(df2.head())

df2 = df2[['playlist_id','playlist_name','Playlist_label']]
print(df2.head())
print(len(df2))

#print(df['song_label'][1:5])
#print(df['song_label'].values[1:5][1:-2])
data2 = df2.values
#print(data2)



print('000')
sdb = Recommendation_System_db.RS_DB_Utils()
print('222')
print(sdb.dbconnect())
print('333')
print(sdb.createTable())
print('444')
print(sdb.searchAllUserInfo())
print('555')
print(sdb.searchAllSongInfo())

for i in range(50):
    #print(i)
    if i%10 ==0:
        print(sdb.addSongInfo(data[i][0],data[i][1],data[i][2],data[i][3],data[i][4]))
    else:
        sdb.addSongInfo(data[i][0],data[i][1],data[i][2],data[i][3],data[i][4])
print(sdb.searchAllSongInfo())



for j in range(10):
    #print(j)
    print(sdb.addSongSheetInfo(data2[j][0],data2[j][1],data2[j][2]))
print(sdb.searchAllSongSheetInfo())

print(sdb.addUser('liming','123456','说唱、流行'))
print('111')
t1 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
print(sdb.addUserSongSheet('liming','1295187450',str(t1)))
print(sdb.searchAllSongUserListen('liming'))
print('------------------------------------------------------------------------')
res = sdb.getMatrix('liming')['data']
print(res)
#print(size(res))
print(res.describe())


print('--------------------------------------------------------')
print(sdb.searchUserInfo('liming'))
print(sdb.getDict('liming')['data'])


print(sdb.deleteUserSongSheetRecord('liming','1295187450'))
print(sdb.searchAllUserSongInfo())
      
'''
f=open('test_data.pkl',"wb")
pickle.dump(res,f,True)
f.close()
'''
