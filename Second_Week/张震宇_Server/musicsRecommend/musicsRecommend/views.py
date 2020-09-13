from django.shortcuts import render
import traceback
import json
from django.http import JsonResponse,HttpResponse
import DataBase
from datetime import datetime
from recommender import Recommender
recommend=Recommender()

db=DataBase.RS_DB_Utils()
print(db.dbconnect())
#db.createTable()
def sign_in(request):
    return render(request,'newlogan.html')
#登录时传进来用户名与密码
def login(request):
    try:
        db.dbconnect()
        params=json.loads(request.body)
        username=params["username"]
        password=params["password"]
        ret=db.getPassword(username)
        if ret["success"]==True:
            if ret["data"]==password:
                request.session["is_logan"]=True
                request.session["username"]=username
                print("login函数中")
                print(request.session["username"])
                print(request.session["is_logan"])
                return JsonResponse({"success":True,"error":""})
            else:
                return JsonResponse({"success":False,"error":"密码错误"})
        else:
            return JsonResponse({"success":False,"error":"账号或密码错误"})
    except Exception as e:
        return JsonResponse({"success":False,"error":str(e)})

#注册时把用户名传过来，服务器判断此用户名是否存在
def usernameExist(request):
    try:
        params=json.loads(request.body)
        print("params:",params)
        ret=db.judgeUserExist(params['username'])
        print('ret:',ret)
        if ret['success']==False:
            return JsonResponse({"success":False,"error":ret["error"]})
        else:
            return JsonResponse({"success":True,"error":ret["error"]})
    except Exception as e:
        return JsonResponse({"success":False,"error":str(e)})

#注册之后增加用户信息
def addUserInformation(request):
    try:
        params=json.loads(request.body)
        ret=db.addUser(params["username"],params["password"],params["label"])
        if ret["success"]==True:
            return JsonResponse({"success":True,"error":"","data":""})
        else:
            return JsonResponse({"success":False,"error":ret["error"],"data":""})
    except Exception as e:
        return JsonResponse({"success":False,"error":e,"data":""})


def register(request):
    db.dbconnect()
    return render(request,'newregister.html')

def Recommendsong(request):
    try:
        if request.session["is_logan"]==True:
            ret=db.searchAllSongUserListen(request.session["username"])
            print(ret)
            if ret["success"]==True and ret["data"]:#个人歌单不为空
                recomSongId=recommend.cfRecommend(request.session["username"],8)
                print("recomSongId",recomSongId)
                data=[]
                for i in recomSongId:
                    Song=db.searchSongInfo(str(i))
                    #print(Song)
                    data.append({"songid":i,"songname":Song["data"][0][1],"singer":Song["data"][0][2],"label":Song["data"][0][4]})
            else:
                print("ready to enter recommend.initRecommend")
                print("username",request.session["username"])
                print("userInfor",db.searchUserInfo(request.session["username"]))
                recomSongId=recommend.initRecommend(request.session["username"],8)
                print("quit the recommend.initRecommend")
                data=[]
                print("recomSongId",recomSongId)
                for i in recomSongId:
                    Song=db.searchSongInfo(i)
                    print(Song)
                    data.append({"songid":i,"songname":Song["data"][0][1],"singer":Song["data"][0][2],"label":Song["data"][0][4]})
            print(data)
            context={"data":data}
            return render(request,'newPersonalRecommend.html',context=context)
        else:
            return render(request,'newlogan.html')
    except Exception as e:
        return JsonResponse({"success":False,"error":str(traceback.print_exc())})

        

def test(request):
    try:
        if request.session["is_logan"]==True:
            data=[{"num":1,"name":"消化内科","sort":"内科","people":"张三","tel":"12345432"},
            {"num":2,"name":"牙科","sort":"外科","people":"李四","tel":"98765432"}]
            context={"data":data}
            return render(request,'mainKS.html',context=context)
        else:
            return render(request,'newlogan.html')
    except Exception as e:
        return JsonResponse({"success":False,"error":str(e)})

def personCenter(request):
    try:
        if request.session["is_logan"]==True:
            ret=db.searchAllSongUserListen(request.session["username"])
            print("ret:",ret)
            data=[]
            if ret["success"]==True and ret["data"]:
                #print("不为空")
                for id in ret["data"]:
                    songInfo=db.searchSongInfo(id[0])
                    data.append({"id":id[0],"songname":songInfo["data"][0][1],"singer":songInfo["data"][0][2],"song_sheet_name":songInfo["data"][0][3],"label":songInfo["data"][0][4]})
            print("data:",data)
            context={"data":data}
            return render(request,'newPersonCenter.html',context=context)
        else:
            return render(request,'newlogan.html')
    except Exception as e:
        return JsonResponse({"success":False,"error":str(e)})

def hotSong(request):
    try:
        if request.session["is_logan"]==True:
            username=request.session["username"]
            #这个下次课可以讨论一下songId=recommend.
            data=[{"songname":"歌曲名","singer":"zhangsan","song_sheet_name":"歌曲对应歌单名","label":"欢快","last_click_time":"20200101"},{"songname":"歌曲名","singer":"zhangsan","song_sheet_name":"歌曲对应歌单名","label":"欢快","last_click_time":"20200101"},
            {"songname":"歌曲名","singer":"zhangsan","song_sheet_name":"歌曲对应歌单名","label":"欢快","last_click_time":"20200101"}]
            context={"data":data}
            return render(request,'newHotSong.html',context=context)
        else:
            return render(request,'newlogan.html')
    except Exception as e:
        return JsonResponse({"success":False,"error":str(e)})

#给出搜索页面
def searchSong(request):
    try:
        if request.session["is_logan"]==True:
            return render(request,'searchSong.html')
        else:
            return render(request,'newlogan.html')
    except Exception as e:
        return JsonResponse({"success":False,"error":str(e)})

def search(request):
    try:
        if request.session["is_logan"]==True:
            params=json.loads(request.body)
            print("收到的歌曲名:"+params["song"])
            ret=db.userSearchSong(params["song"])
            print("ret['data']",ret["data"])
            data=[]
            if ret["success"]==True and ret["data"][0][0]!="":
                for i in ret["data"]:
                    data.append({"songid":i[0],"songname":i[1],"singer":i[2],"label":i[3]})
            
            print("data",data)
            return JsonResponse({"success":True,"error":"","data":data})
        else:
            return render(request,'newlogan.html')
    except Exception as e:
        return JsonResponse({"success":False,"error":str(e),"data":""})

def addSongToCenter(request):
    try:
        if request.session["is_logan"]==True:
            username=request.session["username"]
            params=json.loads(request.body)
            print("add Song to personal center")
            print("params[data]:",params["data"])
            for i in params["data"]:
                ret=db.addUserSongSheet(username,i["id"],datetime.now())
                print(ret)
                print(username)
            return JsonResponse({"success":True})
        else:
            return render(request,'newlogan.html')
    except Exception as e:
        return JsonResponse({"success":False,"error":str(e)})

def deleteSongFromCenter(request):
    try:
        if request.session["is_logan"]==True:
            params=json.loads(request.body)
            #下面调用数据库把一些听歌记录从用户的个人中心删除
            print(params["data"])
            username=request.session["username"]
            for i in params["data"]:
                db.deleteUserSongSheetRecord(username,i["songid"])
            return JsonResponse({"success":True})
        else:
            return render(request,'newlogan.html')
    except Exception as e:
        return JsonResponse({"success":False,"error":str(e)})

def exit(request):
    try:
        if request.session["is_logan"]==True:
            request.session["is_logan"]=False
            del request.session["username"]
            return render(request,'newlogan.html')
        else:
            return render(request,'newlogan.html')
    except Exception as e:
        return JsonResponse({"success":False,"error":str(e)})