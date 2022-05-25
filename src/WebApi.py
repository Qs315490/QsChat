import time
from hashlib import md5

from Api import *

userTokenList = {}


def login(userID, userPassword):
	"""
	登录
	:param userID: 用户ID
	:param userPassword: 用户密码
	"""
	if ifUserNotDefine(userID):
		return {"code": 1, "msg": "用户不存在"}
	cursor.execute("SELECT userPassword FROM userInfo WHERE userID=?",
				   (userID))
	if cursor.fetchone()[0] == userPassword:
		userToken = md5(userID+userPassword+time.time).hexdigest()
		# 判断用户是否已被使用
		if ifToken(userToken):
			return {"code": 2, "msg": "用户已被使用, Token相同。开发者提示：用户Token重复是非常小概率事件，请重新登录。如果问题持续存在，请联系开发者。"}
		userTokenList[userToken] = userID
		return {"code": 0, "msg": "登录成功", "token": userToken}
	else:
		return {"code": -1, "msg": "密码错误"}


def register(userName, userPassword, userIcon=None):
	"""
	注册用户, 注册成功返回用户ID
	:param userName: 用户名称
	:param userPassword: 用户密码
	:param userIcon: 用户头像 (可选)
	"""
	userID = addUser(userName, userPassword, userIcon)
	if userID != None:
		return {"code": 0, "msg": "注册成功", "userID": userID}
	else:
		return {"code": -1, "msg": "站点未开放注册"}


def logout(userToken):
	"""
	退出登录
	:param userToken: 用户token
	"""
	if ifToken(userToken):
		userTokenList.pop(userToken)
		return {"code": 0, "msg": "退出成功"}
	else:
		return {"code": -1, "msg": "退出失败, 用户未登录"}


def ifToken(userToken):
	"""
	判断用户token是否有效
	:param userToken: 用户token
	"""
	return userToken in userTokenList


def token2UserID(userToken):
	"""
	将用户token转换为用户ID
	:param userToken: 用户token
	:return: 用户ID
	"""
	# if ifToken(userToken):
	# 	return userTokenList[userToken]
	# else:
	# 	return None
	return userTokenList[userToken]


def timeStr2Unix(timeStr):
	"""
	将时间字符串转换为时间戳
	:param timeStr: 时间字符串
	"""
	return time.mktime(time.strptime(timeStr, "%Y-%m-%d %H:%M:%S"))


failMsg = {"code": -1, "msg": "操作失败, 请重新登录"}


def getUserInfo(userToken, userID):
	"""
	获取用户信息
	:param userToken: 用户token
	:param userID: 用户ID
	"""
	if ifToken(userToken):
		# 判断用户是否存在
		if ifUserNotDefine(userID):
			return {"code": 1, "msg": "用户不存在"}
		return {"code": 0, "msg": "获取用户信息成功", "userInfo": getUserInfo(userID)}
	else:
		return failMsg


def getGroupInfo(userToken, groupID):
	"""
	获取群信息
	:param userToken: 用户token
	:param groupID: 群ID
	"""
	if ifToken(userToken):
		# 判断群是否存在
		if ifGroupNotDefine(groupID):
			return {"code": 1, "msg": "群不存在"}
		return {"code": 0, "msg": "获取群信息成功", "groupInfo": getGroupInfo(groupID)}
	else:
		return failMsg


def getGroupMember(userToken, groupID):
	"""
	获取群成员
	:param userToken: 用户token
	:param groupID: 群ID
	"""
	if ifToken(userToken):
		# 判断群是否存在
		if ifGroupNotDefine(groupID):
			return {"code": 1, "msg": "群不存在"}
		return {"code": 0, "msg": "获取群成员成功", "groupMember": getGroupMember(groupID)}
	else:
		return failMsg


def getGroupMessage(userToken, groupID, time=None):
	"""
	获取群消息
	:param userToken: 用户token
	:param groupID: 群ID
	:param time: 时间 (可选) 获取指定时间后的消息 时间格式为 %Y-%m-%d %H:%M:%S
	"""
	if ifToken(userToken):
		# 判断群是否存在
		if ifGroupNotDefine(groupID):
			return {"code": 1, "msg": "群不存在"}
		return {"code": 0, "msg": "获取群消息成功", "groupMessage": getGroupMessage(groupID, time)}
	else:
		return failMsg


def updateUserInfo(userToken, userName=None, userPassword=None, userIcon=None):
	"""
	更新用户信息
	:param userToken: 用户token
	:param userName: 用户名称 (可选)
	:param userPassword: 用户密码 (可选)
	:param userIcon: 用户头像 (可选)
	"""
	if ifToken(userToken):
		userID = token2UserID(userToken)
		# 判断用户是否存在
		if ifUserNotDefine(userID):
			return {"code": 1, "msg": "用户不存在"}
		# 判断用户是否有权限
		if token2UserID(userToken) != userID:
			return {"code": 2, "msg": "没有权限修改"}
		updateUserInfo(userID, userName, userPassword, userIcon)
		return {"code": 0, "msg": "更新用户信息成功"}
	else:
		return failMsg


def updateGroupInfo(userToken, groupID, groupName=None, groupIcon=None, groupOwner=None, groupDesc=None):
	"""
	更新群信息
	:param userToken: 用户token
	:param groupID: 群ID
	:param groupName: 群名称 (可选)
	:param groupIcon: 群头像 (可选)
	:param groupOwner: 群主ID (可选)
	:param groupDesc: 群描述 (可选)
	"""
	if ifToken(userToken):
		userID = token2UserID(userToken)
		if ifUserIsGroupOwner(groupID, userID) or getUserTag(groupID, userID) >= 2:
			updateGroupInfo(groupID, groupName,
							groupIcon, groupOwner, groupDesc)
			return {"code": 0, "msg": "更新群信息成功"}
		return {"code": 1, "msg": "您不是群主或管理员"}
	return failMsg


def addGroupMember(userToken, groupID, addUserID=None):
	"""
	普通用户加入群或管理员添加群成员, 普通用户加入无需传入addUserID
	:param userToken: 用户token
	:param groupID: 群ID
	:param addUserID: 用户ID (可选)
	"""
	if ifToken(userToken):
		# 判断群是否存在
		if ifGroupNotDefine(groupID):
			return {"code": 3, "msg": "群不存在"}
		# 判断用户是否在群里
		userID=token2UserID(userToken)
		if ifUserNotInGroup(groupID, userID):
			if addUserID == None:
				addGroupMember(groupID, userID)
				return {"code": 0, "msg": "加入群 %s 成功" % groupID}
			return {"code": 2, "msg": "您不在群里"}
		# 判断用户是否是群主或管理员
		if ifUserIsGroupOwner(groupID,userID) or getUserTag(groupID,userID) >= 2:
			addGroupMember(groupID, userID)
			return {"code": 0, "msg": "添加成员成功"}
		return {"code": 1, "msg": "您不是群主或管理员"}
	return failMsg


def deleteGroup(userToken, groupID):
	"""
	删除群
	:param userToken: 用户token
	:param groupID: 群ID
	"""
	if ifToken(userToken):
		# 判断群是否存在
		if ifGroupNotDefine(groupID):
			return {"code": 2, "msg": "群不存在"}
		# 判断用户是否是群主或管理员
		userID = token2UserID(userToken)
		if ifUserIsGroupOwner(groupID, userID) or getUserTag(groupID, userID) >= 2:
			deleteGroup(groupID)
			return {"code": 0, "msg": "删除群成功"}
		return {"code": 1, "msg": "您不是群主或管理员"}
	return failMsg


def deleteGroupMember(userToken, groupID, leaveUserID=None):
	"""
	普通用户退出群或管理员踢出群成员, 普通用户退出群时无需传入leaveUserID
	:param userToken: 用户token
	:param groupID: 群ID
	:param leaveUserID: 被踢出的用户ID (可选)
	"""
	if ifToken(userToken):
		if ifGroupNotDefine(groupID):
			return {"code": 3, "msg": "群不存在"}

		if ifUserNotInGroup(groupID, leaveUserID):
			return {"code": 2, "msg": "用户 %s 不在群里" % leaveUserID}

		userID = token2UserID(userToken)
		# 普通用户退出群
		if leaveUserID == None:
			removeGroupMember(groupID, userID)
			return {"code": 0, "msg": "退出群成功"}

		# 管理员删除流程
		if ifUserIsGroupOwner(groupID) or getUserTag(groupID, userID) >= 2:
			removeGroupMember(groupID, leaveUserID)
			return {"code": 0, "msg": "删除成员成功"}
		return {"code": 1, "msg": "您不是群主或管理员"}

	return failMsg


def sendGroupMessage(userToken, groupID, message, messageTime=None):
	"""
	发送群消息
	:param userToken: 用户token
	:param groupID: 群ID
	:param message: 消息内容
	:param messageTime: 消息发送时间 (可选)
	"""
	if ifToken(userToken):
		userID = token2UserID(userToken)
		if ifUserNotInGroup(groupID, userID):
			return {"code": 2, "msg": "您不在群里"}

		if ifGroupNotDefine(groupID):
			return {"code": 3, "msg": "群不存在"}

		if getUserTag(groupID, userID) == 0 or getUserTag(groupID, userID) == 2:
			addGroupMessage(groupID, userID, message, messageTime)
			return {"code": 0, "msg": "发送消息成功"}

		return {"code": 1, "msg": "您已被禁言"}

	return failMsg


def deleteGroupMessage(userToken, groupID, messageID):
	"""
	删除群消息
	:param userToken: 用户token
	:param groupID: 群ID
	:param messageID: 消息ID
	"""
	if ifToken(userToken):
		if ifGroupNotDefine(groupID):
			return {"code": 3, "msg": "群不存在"}

		userID = token2UserID(userToken)
		userTag = getUserTag(userID)  # 获取用户权限
		# 管理员和群主删除流程
		if userTag >= 2 or ifUserIsGroupOwner(groupID, userID):
			back = cursor.execute(
				"SELECT userID,messageTime FROM groupMessage WHERE groupID=? AND messageID=?", (groupID, messageID))
			if back == None:
				return {"code": -1, "msg": "消息不存在"}
			removeGroupMessage(groupID, messageID)
			return {"code": 0, "msg": "删除消息成功"}

		# 正常成员删除流程
		back = cursor.execute(
			"SELECT userID,messageTime FROM groupMessage WHERE groupID=? AND messageID=?", (groupID, messageID))
		if back == None:
			return {"code": -1, "msg": "消息不存在"}
		if timeStr2Unix(back[1]) < time.time()-2*60:
			return {"code": 1, "msg": "消息继发出已超过2分钟"}
		if back[0] == userID:
			removeGroupMessage(groupID, messageID)
			return {"code": 0, "msg": "删除消息成功"}

		return {"code": 2, "msg": "您没有此权限"}

	return failMsg
