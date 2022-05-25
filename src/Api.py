import sqlite3
import time

connection = sqlite3.connect('QsChat.sqlite3')
cursor = connection.cursor()
cursor.executescript("""CREATE TABLE IF NOT EXISTS userInfo(
	userID INTEGER NOT NULL PRIMARY KEY,
	userName TEXT NOT NULL,
	userPassword TEXT NOT NULL,
	userIcon TEXT
	);
	CREATE TABLE IF NOT EXISTS groupInfo(
		groupID INTEGER NOT NULL PRIMARY KEY,
		groupName TEXT NOT NULL,
		groupOwner INTEGER NOT NULL,
		groupIcon TEXT,
		groupDesc TEXT
	);
	CREATE TABLE IF NOT EXISTS groupMember(
		groupID INTEGER NOT NULL,
		userID INTEGER NOT NULL,
		userNewName TEXT,
		userTag INTEGER DEFAULT 0,
		PRIMARY KEY(groupID, userID)
		);
	CREATE TABLE IF NOT EXISTS groupMessage(
		messageID INTEGER NOT Null PRIMARY KEY,
		groupID INTEGER NOT NULL,
		userID INTEGER NOT NULL,
		message TEXT NOT NULL,
		messageTime TEXT NOT NULL
	);
	""")


def addUser(userName, userPassword, userIcon=None):
	"""
	添加用户
	:param userName: 用户名
	:param userPassword: 用户密码
	:param userIcon: 用户头像 (可选)
	:return: 用户ID
	"""
	if False:
		return None
	cursor.execute("INSERT INTO userInfo(userName, userPassword, userIcon) VALUES(?,?)",
				   (userName, userPassword))
	rowid = cursor.lastrowid
	if userIcon != None:
		cursor.execute(
			"UPDATE userInfo SET userIcon=? WHERE userID=?", (userIcon, rowid))
	connection.commit()
	return rowid


def addGroup(groupName, groupOwner, groupIcon=None, groupDesc=None):
	"""
	添加群
	:param groupName: 群名
	:param groupOwner: 群主
	:param groupIcon: 群头像 (可选)
	:param groupDesc: 群描述 (可选)
	:return: 群ID
	"""
	cursor.execute(
		"INSERT INTO groupInfo(groupName, groupOwner) VALUES(?,?)", (groupName, groupOwner))
	rowid = cursor.lastrowid
	if groupIcon != None:
		cursor.execute(
			"UPDATE groupInfo SET groupIcon=? WHERE groupID=?", (groupIcon, rowid))
	if groupDesc != None:
		cursor.execute(
			"UPDATE groupInfo SET groupDesc=? WHERE groupID=?", (groupDesc, rowid))
	connection.commit()
	return rowid


def addGroupMember(groupID, userID):
	"""
	添加群成员
	:param groupID: 群ID
	:param userID: 用户ID
	"""
	cursor.execute(
		"INSERT INTO groupMember(groupID, userID) VALUES(?,?)", (groupID, userID))
	connection.commit()


def addGroupMessage(groupID, userID, message, messageTime=None):
	"""
	添加群消息
	:param groupID: 群ID
	:param userID: 用户ID
	:param message: 消息内容
	:param messageTime: 消息时间 (可选)
	:return: 是否成功
	"""
	if ifUserNotInGroup(groupID, userID):
		return False
	cursor.execute("INSERT INTO groupMessage(groupID, userID, message, messageTime) VALUES(?,?,?,?)",
				   (groupID, userID, message, time.strftime("%Y-%m-%d %H:%M:%S")))
	if messageTime != None:
		cursor.execute("UPDATE groupMessage SET messageTime=? WHERE messageID=?",
					   (messageTime, cursor.lastrowid))
	connection.commit()
	return True


def updateUserInfo(userID, userName=None, userPassword=None, userIcon=None):
	"""
	更新用户信息
	:param userID: 用户ID
	:param userName: 用户名 (可选)
	:param userPassword: 用户密码 (可选)
	:param userIcon: 用户头像 (可选)
	"""
	if userName != None:
		cursor.execute(
			"UPDATE userInfo SET userName=? WHERE userID=?", (userName, userID))
	if userPassword != None:
		cursor.execute(
			"UPDATE userInfo SET userPassword=? WHERE userID=?", (userPassword, userID))
	if userIcon != None:
		cursor.execute(
			"UPDATE userInfo SET userIcon=? WHERE userID=?", (userIcon, userID))
	connection.commit()


def updateGroupInfo(groupID, groupName=None, groupIcon=None, groupOwner=None, groupDesc=None):
	"""
	更新群信息
	:param groupID: 群ID
	:param groupName: 群名 (可选)
	:param groupIcon: 群头像 (可选)
	:param groupOwner: 群主 (可选)
	:param groupDesc: 群描述 (可选)
	"""
	if groupName != None:
		cursor.execute(
			"UPDATE groupInfo SET groupName=? WHERE groupID=?", (groupName, groupID))
	if groupIcon != None:
		cursor.execute(
			"UPDATE groupInfo SET groupIcon=? WHERE groupID=?", (groupIcon, groupID))
	if groupOwner != None:
		cursor.execute(
			"UPDATE groupInfo SET groupOwner=? WHERE groupID=?", (groupOwner, groupID))
	if groupDesc != None:
		cursor.execute(
			"UPDATE groupInfo SET groupDesc=? WHERE groupID=?", (groupDesc, groupID))
	connection.commit()


def getUserInfo(userID):
	"""
	获取用户信息
	:param userID: 用户ID
	:return: 用户信息
	"""
	cursor.execute("SELECT * FROM userInfo WHERE userID=?", (userID,))
	return cursor.fetchone()


def getGroupInfo(groupID):
	"""
	获取群信息
	:param groupID: 群ID
	:return: 群信息
	"""
	cursor.execute("SELECT * FROM groupInfo WHERE groupID=?", (groupID,))
	return cursor.fetchone()


def getGroupMember(groupID):
	"""
	获取群成员
	:param groupID: 群ID
	:return: 群成员列表
	"""
	cursor.execute("SELECT * FROM groupMember WHERE groupID=?", (groupID,))
	return cursor.fetchall()


def getGroupMessage(groupID, time=None):
	"""
	获取群消息
	:param groupID: 群ID
	:param time: 时间 (可选)
	:return: 群消息列表
	"""
	if time == None:
		cursor.execute(
			"SELECT * FROM groupMessage WHERE groupID=?", (groupID,))
	else:
		cursor.execute(
			"SELECT * FROM groupMessage WHERE groupID=? AND messageTime>?", (groupID, time))
	return cursor.fetchall()


def getUserGroup(userID):
	"""
	获取用户所在的群列表
	:param userID: 用户ID
	:return: 群列表
	"""
	cursor.execute("SELECT groupID FROM groupMember WHERE userID=?", (userID,))
	return cursor.fetchall()


def getUserTag(groupID, userID):
	"""
	获取用户权限
	:param groupID: 群ID
	:param userID: 用户ID
	:return: 用户权限
	0: 正常
	1: 禁言
	2: 管理员
	3: 管理员被禁言
	"""
	cursor.execute(
		"SELECT userTag FROM groupMember WHERE groupID=? AND userID=?", (groupID, userID))
	return cursor.fetchone()[0]


def removeGroupMember(groupID, userID):
	"""
	删除群成员
	:param groupID: 群ID
	:param userID: 用户ID
	:return: 是否成功
	"""
	cursor.execute(
		"DELETE FROM groupMember WHERE groupID=? AND userID=?", (groupID, userID))
	connection.commit()
	return True


def removeGroupMessage(groupID, messageID):
	"""
	根据消息ID删除群消息
	:param groupID: 群ID
	:param messageID: 消息ID
	:return: 是否成功
	"""
	cursor.execute(
		"DELETE FROM groupMessage WHERE groupID=? AND messageID=?", (groupID, messageID))
	connection.commit()
	return True


def ifUserNotInGroup(groupID, userID):
	"""
	判断用户是否在群组中
	:param groupID: 群ID
	:param userID: 用户ID
	:return: 是否在群组中
	存在返回False
	不存在返回True
	"""
	cursor.execute(
		"SELECT * FROM groupMember WHERE groupID=? AND userID=?", (groupID, userID))

	return cursor.fetchone() == None


def ifUserNotDefine(userID):
	"""
	判断用户是否存在
	:param userID: 用户ID
	:return: 是否存在
	存在返回False
	不存在返回True
	"""
	cursor.execute("SELECT * FROM userInfo WHERE userID=?", (userID,))
	return cursor.fetchone() == None


def ifGroupNotDefine(groupID):
	"""
	判断群是否存在
	:param groupID: 群ID
	:return: 是否存在
	存在返回False
	不存在返回True
	"""
	cursor.execute("SELECT * FROM groupInfo WHERE groupID=?", (groupID))
	return cursor.fetchone() == None


def ifUserIsGroupOwner(groupID, userID):
	"""
	判断用户是否是群主
	:param groupID: 群ID
	:param userID: 用户ID
	:return: 是否是群主
	是返回True
	不是返回False
	"""
	cursor.execute(
		"SELECT groupOwner FROM groupInfo WHERE groupID=?", (groupID))
	return cursor.fetchone()[0] == userID
