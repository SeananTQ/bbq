import pymongo

def GetColl():
    client = pymongo.MongoClient('127.0.0.1', 27017)
    db = client.bbq_db
    rankList = db.rand_list_challenge
    return rankList


class PlayerScore:
    def __init__(self, playerId, playerName, score):
        self.playerId = playerId
        self.playerName = playerName
        self.score = score

    def save(self):
        ps = {"_id": self.playerId, "pname": self.playerName, "score": self.score}
        coll = GetColl()
        id = coll.insert(ps)
        print(id)


    def findDB(self):
        data = GetColl().find()
        return data
