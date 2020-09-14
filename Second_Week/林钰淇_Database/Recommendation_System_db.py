import pymysql
import numpy as np
import os
import configparser
import pandas as pd
print('111')

'''
# 读数据库连接配置文件
config = configparser.ConfigParser()
path = os.path.abspath(os.path.dirname(__file__))
config.read(path+'/db.ini')
host = config.get("db", "host")
port = config.get("db", "port")
user = config.get("db", "user")
pwd = config.get("db", "pwd")
db = config.get("db", "dbname")
charset = config.get("db", "charset")

print(host,port,user,pwd,db,charset)
'''

# 读数据库连接配置文件
config = configparser.ConfigParser()
config.read('RS_db.ini')
host = config.get("RS_db", "host")
port = config.get("RS_db", "port")
user = config.get("RS_db", "user")
pwd = config.get("RS_db", "pwd")
db = config.get("RS_db", "dbname")
charset = config.get("RS_db", "charset")

print(host,port,user,pwd,db,charset)

class RS_DB_Utils:

	class UserException(Exception):
		pass

	def __init__(self):
		self.conn = None
		self.cur = None
		self.host = host
		self.port = int(port)
		self.username = user
		self.passwd = pwd
		self.database = db
		self.charset = charset



	def list2str(self, a, c='、'):
		s = ""
		for it in a:
			s += str(it)
			if it != a[len(a)-1]:
				s += c
		return s


	def str2list(self, s, c='、'):
		return str(s).split(c)



	def createUserInfo(self):
		self.cur.execute("DROP TABLE IF EXISTS USER_INFO")
		#self.cur.execute("DROP TABLE IF EXISTS user_info")
		sql = """
		CREATE TABLE USER_INFO(
			
			user_name VARCHAR (20) not null ,
			password VARCHAR (16) not null,
			favorite_label VARCHAR (200),
			
			primary key(user_name)
		)
		"""

		self.cur.execute(sql)

	def createSongInfo(self):
		self.cur.execute("DROP TABLE IF EXISTS SONG_INFO")
		sql = """
			CREATE TABLE SONG_INFO(
				song_id VARCHAR (20) not null,
				song_name VARCHAR (500) not null,
				singer VARCHAR (20) not null,
				song_sheet_id_belonged VARCHAR (200) not null,
				label VARCHAR (200) not null,
				primary key (song_id)
				)
				"""

		self.cur.execute(sql)

	def createSongSheetInfo(self):
		self.cur.execute("DROP TABLE IF EXISTS SONG_SHEET_INFO")
		sql = """
			CREATE TABLE SONG_SHEET_INFO(
				song_sheet_id VARCHAR (20) not null ,
				song_sheet_name VARCHAR (200) not null,
				label VARCHAR (200) not null,
				primary key (song_sheet_id) 
				)
				"""

		self.cur.execute(sql)
#DATETIME格式为‘YYYY-MM-DD HH:MM:SS’，可用如下python代码获得当前时间并转换格式
# 导入time模块
#import time
# 优化格式化化版本
#print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
	def createUserSongSheet(self):
		self.cur.execute("DROP TABLE IF EXISTS USER_SONG_SHEET")
		sql = """
			CREATE TABLE USER_SONG_SHEET(
				
				user_name VARCHAR (20) not null ,
				song_id VARCHAR (20) not null ,
				last_click_time DATETIME not null,
				
				primary key(user_name, song_id)
				
				
				)
				"""

		self.cur.execute(sql)

	def createTable(self):
		try:
			self.createUserInfo()
			self.createSongInfo()
			self.createSongSheetInfo()
			self.createUserSongSheet()
		except Exception as e:
			return {"success" : False , "error" : str(e) }
		return {"success" : True , "error" : ""}


	def dbconnect(self):
		try:
			self.conn = pymysql.connect(host = self.host ,
										port = self.port ,
										user = self.username ,
										password = self.passwd ,
										database = self.database ,
										charset = self.charset)
			if self.conn:
				self.cur = self.conn.cursor()
		except Exception as e:
			return False

		print(self.conn)
		return True


	def dbclose(self):
		if self.conn and self.cur:
			self.cur.close()
			self.conn.close()
		return True

	'''--------------------------------------User_Info functions-------------------------------------------------'''

	def addUser(self, user_name, passwd, label):
		sql = 'insert into USER_INFO (user_name, password, favorite_label) values (%s, %s, %s)'
		try:
			self.cur.execute(sql, [user_name, passwd, label])
		except Exception as e:
			return {"success": False, "error": str(e)}
		self.conn.commit()
		return {"success": True, "error": ""}

	
	
	

	def searchUserInfo(self, user_name):
		sql = 'select * from USER_INFO where user_name = %s'
		try:
			self.cur.execute(sql, user_name)
		except Exception as e:
			return dict(success=False, error=e, data="")
		res = self.cur.fetchall()
		return dict(success=True, error="", data=res)


	def getPassword(self, user_name):
		sql = 'SELECT password FROM USER_INFO WHERE user_name = %s'
		try:
			self.cur.execute(sql, user_name)
			
		except Exception as e:
			return {"success" : False, "error" : str(e), "data" : ""}
		res = self.cur.fetchall()
		return {"success" : True, "error" : "", "data" : res[0][0]}



	def judgeUserExist(self, user_name):
		sql = 'select * from USER_INFO where user_name = %s'
		try:
			self.cur.execute(sql, user_name)
		except Exception as e:
			return dict(success=False, error=e, data="")
		res = self.cur.fetchall()
		#print(res)
		if res:
			return dict(success=False, error="this user already exist", data=res)
		else:
			return dict(success=True, error="", data="")

	'''----------------------------------------------------------SongInfo functions--------------------------------------------'''
	#def deleteUser(self, user_name):
	#	sql = 'delete from USER_INFO where user_name = %s'
	def searchSongInfo(self, song_id):
		sql = 'SELECT * FROM SONG_INFO WHERE song_id = %s'
		try:
			self.cur.execute(sql, song_id)
			
		except Exception as e:
			return {"success" : False, "error" : str(e), "data" : ""}
		res = self.cur.fetchall()
		return {"success" : True, "error" : "", "data" : res}



	def searchSongSheetIdBelonged(self, song_id):
		sql = 'SELECT song_sheet_id_belonged FROM SONG_INFO WHERE song_id = %s'
		try:
			self.cur.execute(sql, song_id)
			
		except Exception as e:
			return {"success" : False, "error" : str(e), "data" : ""}
		res = self.cur.fetchall()
		return {"success" : True, "error" : "", "data" : res}



	def updateSongInfo(self, song_id, song_sheet_id_belonged, label):
		sql = 'update SONG_INFO set song_sheet_id_belonged = %s , label = %s where song_id = %s'#用逗号连接而不是and,否则error:Truncated incorrect DOUBLE value!!!!
		try:
			self.cur.execute(sql, (song_sheet_id_belonged, label, song_id))
		except Exception as e:
			return {"success": False, "error": str(e)}
		self.conn.commit()
		return {"success": True, "error": ""}



	def addSongInfo(self, song_id, song_name, singer, song_sheet_id_belonged, label):
		
		res = self.searchSongInfo(song_id)
		#print(res)
		if res['success'] == True and res['data']:
			sheet_id_str = res['data'][0][3]
			lab_str = res['data'][0][4]
			sheet_id = self.str2list(sheet_id_str)
			lab = self.str2list(lab_str)
			cur_sheet_id = self.str2list(song_sheet_id_belonged)
			cur_lab = self.str2list(label)
			for it in cur_sheet_id:
				#if it not in sheet_id:
				sheet_id.append(it)
			for it in cur_lab:
				#if it not in lab:
				lab.append(it)
			sheet_id_str = self.list2str(np.unique(sheet_id))
			lab_str = self.list2str(np.unique(lab))
			#print('sheet_id_str:',sheet_id_str)
			res = self.updateSongInfo(song_id, sheet_id_str, lab_str)
			return res
		else:
			sql = 'insert into SONG_INFO  values (%s, %s, %s, %s, %s)'
			try:
				self.cur.execute(sql, (song_id, song_name, singer, song_sheet_id_belonged, label))
			except Exception as e:
				return {"success": False, "error": str(e)}
			self.conn.commit()
		return {"success": True, "error": ""}




	def userSearchSong(self, song_name):
		song_str = '%' + str(song_name) + '%'
		sql = "SELECT song_id,song_name,singer,label from SONG_INFO WHERE song_name LIKE %s" 
		try:
			self.cur.execute(sql, song_str)
		except Exception as e:
			return {"success" : False, "error" : str(e), "data" : ""}
		res = self.cur.fetchall()
		
		return {"success" : True, "error" : "", "data" : res}



	'''------------------------------------------------------------------Song_Sheet_Info functions-------------------------------------------------'''
	def addSongSheetInfo(self, song_sheet_id, song_sheet_name, label):
		sql = 'insert into SONG_SHEET_INFO values (%s, %s, %s)'
		try:
			self.cur.execute(sql, (song_sheet_id, song_sheet_name, label))
		except Exception as e:
			return {"success": False, "error": str(e)}
		self.conn.commit()
		return {"success": True, "error": ""}




	'''------------------------------------------------------------------User_Song_Sheet_Info functions-------------------------------------------------'''
	def searchLastClickTime(self, user_name, song_id):
		sql = 'select last_click_time from USER_SONG_SHEET where user_name = %s and song_id = %s'
		try:
			self.cur.execute(sql, (user_name, song_id))
				
		except Exception as e:
			return {"success" : False, "error" : str(e), "data" : ""}
		res = self.cur.fetchall()
		return {"success" : True, "error" : "", "data" : res}



	def updateUserSongSheet(self, user_name, song_id, last_click_time):
		sql = 'update USER_SONG_SHEET set last_click_time = %s where user_name = %s and song_id = %s'
		try:
			self.cur.execute(sql, (last_click_time, user_name, song_id))
		except Exception as e:
			return {"success": False, "error": str(e)}
		self.conn.commit()
		return {"success": True, "error": ""}



	def addUserSongSheet(self, user_name, song_id, last_click_time):
		res = self.searchLastClickTime(user_name, song_id)
		if res['success'] == True and res['data']:
			#print('here1')
			res_update = self.updateUserSongSheet(user_name, song_id, last_click_time)
			return res_update
		else:
			sql = 'insert into USER_SONG_SHEET (user_name, song_id, last_click_time) values ( %s, %s, %s)'#此处要指明(user_name, song_id, last_click_time)，因为还有一列自增的id
			try:
				#print('here2')
				self.cur.execute(sql, ( user_name, song_id, last_click_time))
			except Exception as e:
				return {"success": False, "error": str(e)}
		self.conn.commit()
		return {"success": True, "error": ""}



	def deleteUserSongSheetRecord(self, user_name, song_id):
		sql = 'delete from USER_SONG_SHEET where user_name = %s and song_id = %s'
		try:
			self.cur.execute(sql, (user_name, song_id))
		except Exception as e:
			return {"success": False, "error": str(e)}
		self.conn.commit()
		return {"success": True, "error": ""}




	def searchAllSongUserListen(self, user_name):
		sql = 'select song_id from USER_SONG_SHEET where user_name = %s'
		try:
			self.cur.execute(sql, user_name)
				
		except Exception as e:
			return {"success" : False, "error" : str(e), "data" : ""}
		res = self.cur.fetchall()
		return {"success" : True, "error" : "", "data" : res}


	'''------------------------------------------------------------------Algorithm functions-------------------------------------------------'''
	def getMatrix(self, user_name):
		#行索引
		sql = 'select song_id from SONG_INFO'
		try:
			self.cur.execute(sql)
		except Exception as e:
			return dict(success=False, error=e, data="")
		all_song_id = self.cur.fetchall()

		#列索引
		sql = 'select song_sheet_id from SONG_SHEET_INFO'
		try:
			self.cur.execute(sql)
		except Exception as e:
			return dict(success=False, error=e, data="")
		all_song_sheet_id = self.cur.fetchall()
		

		#前n行矩阵赋值
		matrix = np.zeros((len(all_song_sheet_id)+1, len(all_song_id)))
		for i in range(len(all_song_id)):
			sheet_id_str = self.searchSongSheetIdBelonged(all_song_id[i][0])['data'][0][0]
			sheet_id = self.str2list(sheet_id_str)
			for j in range(len(all_song_sheet_id)):
				if all_song_sheet_id[j][0] in sheet_id:
					matrix[j][i] = 1
					#print('**************************************************************')

		#最后一行矩阵赋值
		song_id_listen = self.searchAllSongUserListen(user_name)['data'][0]
		for i in range(len(all_song_id)):
			if all_song_id[i][0] in song_id_listen:
				matrix[-1][i] = 1

		#转为df
		ind = []
		col = []
		for item in all_song_sheet_id:
			ind.append(item[0])
		ind.append(user_name)
		for item in all_song_id:
			col.append(item[0])
		df = pd.DataFrame(matrix, index = ind, columns = col)
		return {"success" : True, "error" : "", "data" : df}



	
	def getDict(self, user_name):
		sql = 'select favorite_label from USER_INFO where user_name = %s'
		try:
			self.cur.execute(sql, user_name)
		except Exception as e:
			return dict(success=False, error=e, data="")

		#print('self.cur.fetchall()',self.cur.fetchall())
		key_str = self.cur.fetchall()[0][0]
		
		key = self.str2list(key_str)
		#print('key_str',key_str)
		#print('key',key)
		#return dict(success=True, error="", data=res)
		dic = {}

		for k in key:
			label_str = '%' + str(k) + '%'
			sql = "SELECT song_id from SONG_INFO WHERE label LIKE %s order by rand() limit 10" 
			try:
				self.cur.execute(sql, label_str)
			except Exception as e:
				return {"success" : False, "error" : str(e), "data" : ""}
			#print('k',k)
			
			res = self.cur.fetchall()
			val = []
			for i in range(len(res)):
				val.append(res[i][0])
			#print('val',val)
			#print('res[0]',list(res)[0])
			#print('res[0][0]',list(res)[0][0])
			dic[k] = val
		#print(dic)
		return {"success" : True, "error" : "", "data" : dic}
	
	'''------------------------------------------------------------------TEST functions-------------------------------------------------'''
	def searchAllUserInfo(self):
		sql = 'select * from USER_INFO'
		try:
			self.cur.execute(sql)
		except Exception as e:
			return dict(success=False, error=e, data="")
		res = self.cur.fetchall()
		#if not res:
		#	return {"success": False, "error": "no data record in this table"}
		return dict(success=True, error="", data=res)


	def searchAllSongInfo(self):
		sql = 'select * from SONG_INFO'
		try:
			self.cur.execute(sql)
		except Exception as e:
			return dict(success=False, error=e, data="")
		res = self.cur.fetchall()
		#if not res:
		#	return {"success": False, "error": "no data record in this table"}
		return dict(success=True, error="", data=res)


	def searchAllSongSheetInfo(self):
		sql = 'select * from SONG_SHEET_INFO'
		try:
			self.cur.execute(sql)
		except Exception as e:
			return dict(success=False, error=e, data="")
		res = self.cur.fetchall()
		#if not res:
		#	return {"success": False, "error": "no data record in this table"}
		return dict(success=True, error="", data=res)


	def searchAllUserSongInfo(self):
		sql = 'select * from USER_SONG_SHEET'
		try:
			self.cur.execute(sql)
		except Exception as e:
			return dict(success=False, error=e, data="")
		res = self.cur.fetchall()
		#if not res:
		#	return {"success": False, "error": "no data record in this table"}
		return dict(success=True, error="", data=res)





	'''----------------------------------------------------------------多余-------------------------------------------------'''
	def searchUserLabel(self, user_name):
		sql = 'select favorite_label from USER_INFO where user_name = %s'
		try:
			self.cur.execute(sql, user_name)
		except Exception as e:
			return dict(success=False, error=e, data="")
		res = self.cur.fetchall()
		return dict(success=True, error="", data=res)



	def addUserLabel(self, user_name, label):
		#sql = 'insert into USER_INFO (favourite_label) values (%s)'
		sql = 'update USER_INFO set favorite_label = %s where user_name = %s'
		res = self.searchUserLabel(user_name)
		print('res:',res)
		try:
			if res['success'] == True:
				ori_label = res['data'][0][0]
				if(ori_label != None):
					label += ','
					label += str(ori_label)
			else:
				raise self.UserException("this user doesn't exist")
		except self.UserException as ue:
			return {"success": False, "error": str(ue)}

		try:
			print('label:',label)
			self.cur.execute(sql, (label, user_name))
		except Exception as e:
			return {"success": False, "error": str(e)}
		self.conn.commit()
		return {"success": True, "error": ""}
