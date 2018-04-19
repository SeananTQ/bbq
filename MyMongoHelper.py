#-*-coding:utf-8-*-
import pymongo
import random

def GetColl():
    client = pymongo.MongoClient('127.0.0.1', 27017)
    db = client.bbq_db
    rankList = db.rank_list_challenge
    return rankList


class PlayerScore:
    def __init__(self, playerId, playerName, score):
        self.playerId=playerId
        self.playerName = playerName
        self.score = score

    def save(self):
        # ps = { _id:self.playerId,"pname": self.playerName, "score": self.score}
        # data="{_id:%s,pname:%s,score:%d}" % (self.playerId,self.playerName,self.score)
        data={'_id': self.playerId,'pname':self.playerName,'score':self.score}
        print('data is :%s' %data)
        coll = GetColl()
        id = coll.save(data)
        print('成功save了%s' % id)


    @staticmethod
    def find(name,value):
        print("find %s  %d" % (name,value))
        coll=GetColl()
        result=coll.find_one({name:value})
        return result



    @staticmethod
    def exist(name, value):
        print("判断是否存在 %s " % value)
        coll=GetColl()
        result=coll.find_one({name:value})
        return result

    #查询角色的排名
    @staticmethod
    def rankIndex(name, value):
        print("查询 %s的排名  %d" % (name,value))
        coll=GetColl()
        result=coll.find({name:{'$gte':value}})
        return result

    #取得排行榜前几名玩家的数据
    #name:按什么排序
    #tpye:1正序2倒序
    #count:取前几名
    @staticmethod
    def getTopGroup(name, type,count):
        print("查询 %s的前%d 名"  % (name, count))
        coll = GetColl()
        result = coll.find().sort({name:type}.limit(count))
        return result
