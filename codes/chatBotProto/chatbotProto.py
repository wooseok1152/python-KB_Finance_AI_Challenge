from Postgre import PostgreConn;
import json;
import sys;

convToInterest = {0:"여행/숙박", 1:"백화점/패션", 2:"인테리어", 3:"식사", 4:"영화", 5:"연극/공연", 6:"스포츠/레저", 7:"술/유흥", 8:"전자기기", 9:"편의점",
                    10:"카페/간식", 11:"교통", 12:"차량", 13:"뷰티/미용", 14:"학습/교육"};
					
def bringData(userID):
    with open("config.json") as jsonFile:
        jsonData = json.load(jsonFile);

    user = jsonData["user"];
    password = jsonData["password"];
    host = jsonData["host"];
    port = jsonData["port"];
    DB = jsonData["database"];
    
    conn = PostgreConn(user, password, host, port, DB);
    
    result = conn.select(f"select a,b,c,d,e,f,g,h,i,j,k,l,m,n,o from CONSUMPTION where userID = {userID} order by consumeDate desc limit 90;");
    vector = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
        
    for j in range(90):
        for k in range(15):
            vector[k] += result[j][k] * (2 - 0.02 * j);
            
    vecSum = sum(vector);
    for i in range(15):
        vector[i] /= vecSum;
    
    conn.close();
    # vector는 카테고리에 대한 비중을 나타낸다.
    
    return vector;
    
def parseInterest(data):
    first = data.index(max(data));
    data[data.index(max(data))] -= 1;
    
    second = data.index(max(data));
    data[data.index(max(data))] -= 1;
    
    third = data.index(max(data));
    
    return [first, second, third];
    
def main(userID):
    data = bringData(userID);
    
    interest = parseInterest(data);
    # 여기까지 interest는 index value
    
    for i in range(3):
        interest[i] = convToInterest[interest[i]];
    
    print(interest);

if __name__ == '__main__':
    main(int(sys.argv[1]));