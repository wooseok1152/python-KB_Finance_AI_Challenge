from Postgre import PostgreConn;
import json;
import sys;
import numpy as np;

alphaToNum = {};

alphas = list("ABCDEFGHIJKLMNO");

for i in range(15):
    alphaToNum[alphas[i]] = i;

def main(configFile, number, outFile):

    with open(configFile) as jsonFile:
        jsonData = json.load(jsonFile);

    user = jsonData["user"];
    password = jsonData["password"];
    host = jsonData["host"];
    port = jsonData["port"];
    DB = jsonData["database"];
    
    conn = PostgreConn(user, password, host, port, DB);
    
    actionData = [];
    
    for i in range(1, number + 1):
        result = conn.select(f"select url from LOGS where userID = {i} and method = 'GET' and url != '/';");
        actionData.append(result);
        
    preprocessed = [];
    
    for action in actionData:
        # action은 한사람 데이터
        a = b = c = d = e = f = g = h = I = 0;
        
        for i in range(len(action)):
            actNum = int(action[i][0][7:]);
            
            if actNum < 100:
                a += 1;
            elif actNum < 200:
                b += 1;
            elif actNum < 300:
                c += 1;
            elif actNum < 400:
                d += 1;
            elif actNum < 500:
                e += 1;
            elif actNum < 600:
                f += 1;
            elif actNum < 700:
                g += 1;
            elif actNum < 800:
                h += 1;
            elif actNum < 900:
                I += 1;
        
        preprocessed.append([a,b,c,d,e,f,g,h,I]);
        
    for i in range(1, number + 1):
        result = conn.select(f"select job, gender, age, hasCar, hasHouse, getMarried, children, incomeLevel, assetsLevel from CUSTOMER where userID = {i};");
        for item in result[0]:
            if item in list("ABCDEFGHIJKLMNO"):
                stop = alphaToNum[item];
                for j in range(15):
                    if j == stop:
                        preprocessed[i-1].append(1);
                    else:
                        preprocessed[i-1].append(0);
            else:
                preprocessed[i-1].append(item);
    
    saveArr = np.asarray(preprocessed);
    
    print(saveArr);
    
    np.save(outFile, saveArr);
    
    conn.close();

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3]);