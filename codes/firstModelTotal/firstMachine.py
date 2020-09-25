from Postgre import PostgreConn;
import json;
import sys;
import numpy as np;

convToInterest = {0:"여행/숙박", 1:"백화점/패션", 2:"인테리어", 3:"식사", 4:"영화", 5:"연극/공연", 6:"스포츠/레저", 7:"술/유흥", 8:"전자기기", 9:"편의점",
                    10:"카페/간식", 11:"교통", 12:"차량", 13:"뷰티/미용", 14:"학습/교육"};

def bringData(count):
    with open("config.json") as jsonFile:
        jsonData = json.load(jsonFile);

    user = jsonData["user"];
    password = jsonData["password"];
    host = jsonData["host"];
    port = jsonData["port"];
    DB = jsonData["database"];
    
    conn = PostgreConn(user, password, host, port, DB);
    
    consumptions = [];
    for i in range(1, count + 1):
        result = conn.select(f"select a,b,c,d,e,f,g,h,i,j,k,l,m,n,o from CONSUMPTION where userID = {i} order by consumeDate desc limit 90;");
        vector = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
        
        for j in range(90):
            for k in range(15):
                vector[k] += result[j][k] * (2 - 0.02 * j);
        
        consumptions.append(vector);
        
    conn.close();
    
    return consumptions;
    
def parseInterest(consumptions, count):
        
    interests = [];
    interestsWord = [];
    for i in range(count):
        first = consumptions[i].index(max(consumptions[i]));
        consumptions[i][consumptions[i].index(max(consumptions[i]))] -= 100000000;
        
        second = consumptions[i].index(max(consumptions[i]));
        consumptions[i][consumptions[i].index(max(consumptions[i]))] -= 100000000;
        
        third = consumptions[i].index(max(consumptions[i]));
        
        interests.append([first, second, third]);
        interestsWord.append([convToInterest[first], convToInterest[second], convToInterest[third]]);
    
    # print(interestsWord);
    # 이를 말로 표현한 것
    
    return interests;
    

def main(num, outFile):
    data = bringData(num);
    
    interestsMatrix = parseInterest(data, num);
    
    np.save(outFile, np.asarray(interestsMatrix));

if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2]);