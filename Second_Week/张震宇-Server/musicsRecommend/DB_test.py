import datetime

import pymysql
import traceback
import logging
import configparser
import os

import DataBase

db=DataBase.RS_DB_Utils()
print(db.dbconnect())
db.createUserInfo()
print(db.searchAllSongUserListen("yyy"))