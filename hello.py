from flask import Flask, jsonify
from score import  PlayerScore
import datetime
import time


app = Flask(__name__)


@app.route('/scores', methods=['GET'])
def hello():
    result="failed"

    return result


@app.route("/time")
def theTime():
    value = ""
    at = time.strftime(" {year:%Y,month:%m,day:%d,hour:%H,minute:%M,second:%S }")
    value = str(at)
    at = time.localtime(time.time())
    value += "\r\n" + str(at)
    return str(value)


@app.route("/")
def index():
    data = []
    data.append({'id': '1001', 'name': '2', 'score': '3'})
    return jsonify(data)


@app.route("/dbtest")
def dbtest():
    playerData=PlayerScore(1004,"zhang3","500")
    playerData.save()
    return "dbtest"



@app.route("/dbfind")
def dbfind():
    data=PlayerScore.findDB()
    return jsonify(data)



def getYesterday():
    today = datetime.now()
    oneday = datetime.timedelta(days=2)
    # yesterday=today-oneday
    return today


'''    data = []    

	data.append({'id': '1', 'name': '2', 'score': '3'})


	return jsonify({'data': data})
'''

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
