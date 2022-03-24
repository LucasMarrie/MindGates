import os, json
from settings import SCOREDATA_FILE

def getScores():
    try:
        if os.path.exists(SCOREDATA_FILE):
            with open(SCOREDATA_FILE, "r") as file:
                return json.load(file)
    except Exception as ex:
        print("Error while get scores: " + ex)

    return []

def addScore(score, time):
    data = getScores()
    scoreDict = {"score": score, "time": time}
    data.append(scoreDict)
    try: 
        with open(SCOREDATA_FILE, "w") as file:
            json.dump(data, file)
    except Exception as ex:
        print("Error while adding score: " + ex)

def getSortedScores():
    scores = getScores()
    scores.sort(key = lambda x: x["time"])
    scores.sort(key = lambda x: x["score"], reverse=True)
    return scores

def clearScores():
    try: 
        with open(SCOREDATA_FILE, "w") as file:
            json.dump([], file)
    except Exception as ex:
        print("Error while deleting scores: " + ex)