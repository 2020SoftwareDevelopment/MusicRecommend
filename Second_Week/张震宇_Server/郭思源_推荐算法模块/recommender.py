import pickle
import heapq
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from Database import getDictionary, getMatrix

class Recommender():
    def __init__(self):
        pass

    def initRecommend(self, user_name, num=5):
        """
        初始化推荐——解决冷启动问题
        :param user_name: 用户名
        :param num: 推荐歌曲数
        :return recommendList: List对象，包含num个推荐歌曲id
        """
        dictionary = getDictionary(user_name)
        labelNum = len(dictionary)
        labelList = list(dictionary.keys())
        recommendList = []
        count = 0
        while count <= num:
            label = labelList[count % labelNum]
            songList = dictionary[label]
            songNum = len(songList)
            rand = np.random.randint(0, songNum)
            if songList[rand] not in recommendList:
                recommendList.append(songList[rand])
                count += 1
        return recommendList

    def cfRecommend(self, user_name, num=5):
        """
        基于协同过滤的个性化推荐
        Algorithm: itemKNN
        :param user_name: 用户名
        :param num: 推荐歌曲数
        :return recommendList: List对象，包含num个推荐歌曲id
        """
        # file = open("test_data.pkl", 'rb')
        # matrix = pickle.load(file)
        # matrix['1311198393']['liming'] = 1
        matrix = getMatrix(user_name)
        songIDList = np.array(matrix.columns, dtype=np.int)
        observation = np.array(matrix.values[:-1])
        userObservation = np.array(matrix.values[-1])
        sheetNum, songNum = observation.shape
        observation = np.transpose(observation)
        itemList = np.reshape(np.argwhere(userObservation == 1), [-1])
        distance = np.zeros(songNum)
        for item in itemList:
            for song in range(songNum):
                if song in itemList:
                    continue
                distance[song] += np.sum(np.abs(observation[item] - observation[song]))
        nsmallestList = heapq.nsmallest(itemList.shape[0]+num, enumerate(distance), key=lambda x:x[1])
        indices, vals = zip(*nsmallestList)
        recommendList = [songIDList[x] for x in indices[itemList.shape[0]:]]
        return recommendList


if __name__ == "__main__":
    r = Recommender()
    # print(r.initRecommend('hey'))
    print(r.cfRecommend("hey"))