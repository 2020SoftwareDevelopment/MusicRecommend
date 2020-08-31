import pymysql

print('111')

class RS_DB_Utils:

	class UserException(Exception):
		pass

	def __init__(self):
		self.coon = None
		self.cur = None
		self.host = host
		self.port = int(port)
		self.username = user
		self.passwd = pwd
		self.database = db
		self.charset = charset

	def createUserInfo(self):
		sql = """
			CREATE TABLE USER_INFO(
				user_id INT auto_increment,
				user_name VARCHAR (20) not null PRIMARY_KEY,
				password VAECHAR (16) not null,
				favorite_label VARCHAR (200) 
				)
				"""

		self.cur.execute(sql)

	def createSongInfo(self):
		sql = """
			CREATE TABLE SONG_INFO(
				song_id INT auto_increment,
				song_name VARCHAR (100) not null,
				singer VARCHAR (20) not null,
				song_sheet_id_belonged VARCHAR (200) not null,
				label VARCHAR (200) not null,
				primary key (song_name , singer)
				)
				"""

		self.cur.execute(sql)

	def createSongSheetInfo(self):
		sql = """
			CREATE TABLE SONG_SHEET_INFO(
				song_sheet_id INT auto_increment ,
				song_sheet_name VARCHAR (200) not null,
				label VARCHAR (200) not null,
				primary key (song_sheet_id) 
				)
				"""

		self.cur.execute(sql)

	def createUserSongSheet(self):
		sql = """
			CREATE TABLE USER_SONG_SHEET(
				record_id INT auto_increment ,
				user_id INT not null ,
				song_id INT not null ,
				last_click_time DATETIME not null,
				primary key (record_id)
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
			return {"sucess" : False , "error" : str(e) }
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
		except Excception as e:
			return False
		return True


	def dbclose(self):
		if self.conn and self.cur:
			self.cur.close()
			self.conn.close()
		return True

	'''--------------------------------------functions-------------------------------------------------'''

	def addUser(self, user_name, passwd):
		sql = 'insert into USER_INFO (user_name, password) values (%s, %s)'
		try:
			self.cur.excute(sql, [user_name, passwd])
		except Exception as e:
			return {"success": False, "error": str(e)}
		self.conn.commit()
		return {"success": True, "error": ""}


	def addUserLabel(self, user_name, label):
		sql = 'insert into USER_INFO (favourite_label) values (%s)'
		try:
			self.cur.excute(sql, label)
		except Exception as e:
			return {"success": False, "error": str(e)}
		self.conn.commit()
		return {"success": True, "error": ""}



	
