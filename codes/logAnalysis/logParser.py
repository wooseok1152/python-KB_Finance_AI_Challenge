from Postgre import PostgreConn;
import json;
import sys;

engToNum = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6,
            "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12};

# ip / datetime / method / url / status / referer / userid
# varchar(30) / datetime / varchar(20) / varchar / int / varchar / int

def storeToDB(inputData):
    with open("config.json") as jsonFile:
        jsonData = json.load(jsonFile);

    user = jsonData["user"];
    password = jsonData["password"];
    host = jsonData["host"];
    port = jsonData["port"];
    DB = jsonData["database"];
    
    conn = PostgreConn(user, password, host, port, DB);
    
    conn.insert(sql="insert into LOGS(ip, accessTime, method, url, statusCode, referer, userID) values(%s, %s, %s, %s, %s, %s, %s)", bulk=True, records=inputData);
    
    conn.saveJSON("LOGS", "logs.json");
    conn.close();

def parseToDB(logs):
    bulkDatas = [];
    for log in logs:
        splitedLog = log.split(" ");
        
        time = splitedLog[3];
        if time[2] == "/":
            day = time[1];
            month = engToNum[time[3:6]];
            year = time[7:11];
            T = time[12:];
        else:
            day = time[1:3];
            month = engToNum[time[4:7]];
            year = time[8:12];
            T = time[13:];
        
        datetime = f"{year}-{month}-{day} {T}";
        
        bulkData = (splitedLog[0], datetime, splitedLog[5].strip('"'), splitedLog[6],
                    splitedLog[8], splitedLog[10].strip('"[]'), splitedLog[-1].rstrip("\n"));
        
        bulkDatas.append(bulkData);
        
    print("Log parsing complete");
    return bulkDatas;

def main(inputFile):

    f = open("./%s"%inputFile, 'r');
    logs = f.readlines();
    f.close();
    
    inputDatas = parseToDB(logs);
    
    storeToDB(inputDatas);
        
if __name__ == '__main__':
    main(sys.argv[1]);