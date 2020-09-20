
import pandas as pd
from collections import Counter
import numpy as np
from itertools import chain
data = pd.read_csv(r'.\\song.csv', header=0,encoding='ISO-8859-1')
data1=data.loc[:, ['song_id']]
data2=data1.values.tolist()
data3=list(chain.from_iterable(data2))
data4=Counter(data3)
chishu=[]
for i in range(len(data)):
    a=data3[i]
    chishu.append(data4[a])
data['re_times']=chishu
data5=data.drop(index=(data.loc[(data['re_times']==1)].index))
data6=data5.drop(index=(data5.loc[(data5['re_times']==2)].index))
data7=data6.drop(index=(data6.loc[(data6['re_times']==3)].index))
data8=data7.drop(index=(data7.loc[(data7['re_times']==4)].index))
data9=data8.drop(index=(data8.loc[(data8['re_times']==5)].index))
data10=data9.drop(index=(data9.loc[(data9['re_times']==6)].index))
data11=data10.drop(index=(data10.loc[(data10['re_times']==7)].index))
data12=data11.drop(index=(data11.loc[(data11['re_times']==8)].index))
data13=data12.drop(index=(data12.loc[(data12['re_times']==9)].index))
data14=data13.drop(index=(data13.loc[(data13['re_times']==10)].index))
data15=data14.drop(index=(data14.loc[(data14['re_times']==11)].index))
print(data15)

#csv_file = open("song_clean_20200913.csv", "a", encoding='utf-8', newline='')
#writer = csv.writer(csv_file)

data15.to_csv("song_clean_20200915.csv",encoding='ISO-8859-1')