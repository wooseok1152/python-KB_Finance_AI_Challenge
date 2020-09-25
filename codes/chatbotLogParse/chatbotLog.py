from Postgre import PostgreConn;
import json;
import sys;
import numpy as np;

def convToScore(count):
    if count == 0:
        return 0;
    elif count == 1:
        return 1;
    elif count <= 3:
        return 2;
    elif count <= 6:
        return 3;
    elif count <= 9:
        return 4;
    else:
        return 5;

def bringData(count):
    with open("config.json") as jsonFile:
        jsonData = json.load(jsonFile);

    user = jsonData["user"];
    password = jsonData["password"];
    host = jsonData["host"];
    port = jsonData["port"];
    DB = jsonData["database"];
    
    conn = PostgreConn(user, password, host, port, DB);
	
    interestDict = {};
    
    for i in range(1, count + 1):
        interestDict[i] = [];
        result = conn.select(f"select userID, url from logs where userID = {i} and url like '%chatbot%';");
        for item in result:
            interestDict[item[0]].append(item[1]);
    
    conn.close();
    
    return interestDict;
    
def parseData(interestDict, count, npFile):
    chatbotUsers = [];
    interests = {};
    for i in range(1, count + 1):
        if len(interestDict[i]) > 0:
            chatbotUsers.append(i);
        interests[i] = [];
        if len(interestDict[i]) > 1:
            for j in range(len(interestDict[i])):
                try:
                    interests[i].append(int(interestDict[i][j][9:]));
                except:
                    pass;
        
    interestMatrix = np.load(npFile);
    
    users = {};
    for i in range(1, count + 1):
        users[i] = {};
        for item in interestMatrix[i-1]:
            users[i][item] = interests[i].count(item);
            
    machineData = {};
    for i in range(15):
        machineData[i] = [];
        
    for i in chatbotUsers:
        # print(i, " : ", users[i]);
        for j in range(15):
            try:
                # 단순 유저별 조회수
                # machineData[j].append([i, users[i][j]]);
                # 유저별 조회수를 점수로 환산
                machineData[j].append([i, convToScore(users[i][j])]);
            except:
                pass;
                
    for i in range(15):
        np.save(f"trainDataForMachine_{i}.npy", np.asarray(machineData[i]));
    
def main(num, inputFile):
    results = bringData(num);
    
    parseData(results, num, inputFile);
    
if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2]);