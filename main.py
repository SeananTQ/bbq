from flask import Flask, jsonify, request, Response, make_response
from MyMongoHelper import PlayerScore
import datetime
import time
import random
import json

app = Flask(__name__)


@app.route('/scores', methods = ['GET'])
def hello():
	result = "failed"

	return result


@app.route("/time")
def theTime():
	at = time.strftime(" {year:%Y,month:%m,day:%d,hour:%H,minute:%M,second:%S}")
	return str(at)


'''
接收客户端POST的参数，并加以验证，返回结果
'''


@app.route("/bbq/<int:model_type>/<int:getId>/<int:getCount>", methods = ['GET', 'POST'])
def bbqRoute(model_type,getId,getCount):
	resultMsg = ""
	if request.method == 'POST':
		playerId = int(request.form.get('pid'))
		playerName = request.form.get('pname')
		newScore = int(request.form.get('score'))
		password = request.form.get('passwd')
		# 首先验证数据合法性
		if password:
			print('password is :%s' % password)
			resultMsg=saveNewScore(playerId, playerName, newScore)
		else:
			# 如果密码错误就返回警告信息
			resultMsg = 'password error'
			print('password error')
	else:
		resultMsg= getCurRank(getId,getCount)

	return resultMsg


def getCurRank(playerId,getCount):
	# 首先验证数据合法性
	if type(playerId) !=int or  type(getCount) != int :
		print("参数类型错误")
		return "error"

	# 如果是GET的话，就返回排行榜前10名
	count = getCount
	tempC = PlayerScore.getTopGroup('score', -1, count)
	# 通过迭代将前10名的数据
	topArray = []
	for i in tempC:
		topArray.append(i)
	# 然后返回该账号当前排名
	curRank = PlayerScore.rankIndex('_id', playerId,)

	reDice = {}
	reDice['count'] = count
	reDice['rank'] = curRank
	reDice['top'] = topArray

	resultMsg = json.dumps(reDice)
	return   resultMsg


def saveNewScore(playerId, playerName, newScore):
	# 查询该角色是否存在
	tempStr = str(PlayerScore.exist('_id', playerId))
	if tempStr == "None":
		print('所查询角色%s不存在' % playerId)
		# 如果不存在则新增
		playerData = PlayerScore(playerId, playerName, newScore)
		playerData.save()
		print('新增数据')
		resultMsg = "新增角色成功"
	else:
		tempStr = tempStr.replace("'", '"')
		print('存在!%s' % tempStr)
		# 如果存在就反序列化JSON
		tempJson = json.loads(tempStr)
		tempScore = int(tempJson['score'])
		print('新分数是%d 原始分数是%d' % (newScore, tempScore))
		# 然后比较分数，分数大则更新数据
		if newScore > tempScore:
			playerData = PlayerScore(playerId, playerName, newScore)
			playerData.save()
			resultMsg = "更新分数记录成功%s" % playerName
			print("更新分数记录成功%s" % playerName)
		else:
			resultMsg = "没有取得更好的分数%s" % playerName
			print("没有取得更好的分数%s" % playerName)
	return resultMsg


@app.route("/test/<pid>/<pname>/<score>", methods = ['GET', 'POST'])
def test(pid, pname, score):
	# result = PlayerScore.exist('pname', pname)
	# print("BB %s" % result)
	playerData = PlayerScore(pid, pname, int(score))
	playerData.save()
	return "保存数据"


@app.route("/test2")
def test2():
	data = PlayerScore.find('_id', 1003)
	dic = str(data).replace("'", '"')
	print('data is :%s' % dic)
	# out: <class 'str'> {"age": 23, "job": "student"}
	dic_obj = json.loads(dic)
	print(dic_obj['pname'])
	# out: <class 'dict'> {'age': 23, 'job': 'student'}
	return "okey%s" % dic


def Response_headers(content):
	resp = Response(content)
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp


@app.route("/")
def index():
	data = []
	data.append({'id': 1001, 'name': 2, 'score': 3})
	data.append({'id': 1001, 'name': 2, 'score': 3})
	# return jsonify(data)
	return str(data)


def getYesterday():
	today = datetime.now()
	oneday = datetime.timedelta(days = 2)
	# yesterday=today-oneday
	return today


if __name__ == "__main__":
	app.run(debug = True, host = '0.0.0.0')
