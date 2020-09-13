import Recommendation_System
import time
if __name__ == "__main__":
    print('000')
    sdb = Recommendation_System.RS_DB_Utils()
    sdb.createTable()
    print('222')
    print(sdb.dbconnect())
    print('333')
    print(sdb.createTable())
    print('444')
    print(sdb.searchAllUserInfo())

    #USER_INFO test
    print(sdb.addUser('zhangsan','123456'))
    print(sdb.searchUserInfo('zhangsan'))
    print('555')
    print(sdb.addUserLabel('zhangsan','pop,JP'))
    
    print('666')
    print(sdb.addUser("李明",'888888'))
    print('777')
    print(sdb.searchAllUserInfo())
    print(sdb.addUser('zhangsan','123456'))
    print(sdb.getPassword("李明"))
    #print(sdb.searchUserInfo('zhangsaning'))


    #SONG_INFO test
    print('888')
    print(sdb.searchAllSongInfo())
    print(sdb.addSongInfo(101,'song1','singer1','11','pop'))
    print('999')
    print(sdb.addSongInfo(101,'song1','singer2','22','JP'))
    print('aaa')
    print(sdb.addSongInfo(120,'song2','singer2','33','JP'))
    print('bbb')
    print(sdb.searchAllSongInfo())



    #SONG_SHEET_INFO TEST 
    print('-------------------------------------------------')
    print('111')
    print(sdb.addSongSheetInfo(10,'sheet10','pop,USA'))
    print(sdb.searchAllSongSheetInfo())




    #SONG_SHEET_INFO TEST 
    print('-------------------------------------------------')
    print('111')
    t1 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
   
    print(sdb.addUserSongSheet('liming',20,str(t1)))
    print('222')
    t2 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print(sdb.addUserSongSheet('liming',20,str(t2)))
    print(sdb.searchAllUserSongInfo())
    
    
    sdb.dbclose()
