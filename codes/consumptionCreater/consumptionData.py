from Postgre import PostgreConn;
import json;
import sys;
from random import randint;

def storeToDB(inputData):
    with open("config.json") as jsonFile:
        jsonData = json.load(jsonFile);

    user = jsonData["user"];
    password = jsonData["password"];
    host = jsonData["host"];
    port = jsonData["port"];
    DB = jsonData["database"];
    
    conn = PostgreConn(user, password, host, port, DB);
    
    conn.insert(sql="insert into CONSUMPTION(userID, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, consumeDate) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", bulk=True, records=inputData);
    
    print("Data is inserted to DB successfully.");
    conn.close();
    
def createData(num):
    ids = range(1, num + 1);
    consumption = [[randint(1 ,10),randint(1 ,10),randint(1 ,10),randint(1 ,10),randint(1 ,10),randint(1 ,10),randint(1 ,10),randint(1 ,10),randint(1 ,10),randint(1 ,10),randint(1 ,10),randint(1 ,10),randint(1 ,10),randint(1 ,10),randint(1 ,10)] for _ in range(90 * num)];
    # 16개 카테고리
    for i in range(90 * num):
        subSum = sum(consumption[i]);
        dayTotal = randint(10000, 300000);
        for j in range(15):
            consumption[i][j] = consumption[i][j] / subSum * dayTotal;
    # 카테고리별 소비내역을 %로 나눈다.
    
    dates = ["2020-06-01","2020-06-02","2020-06-03","2020-06-04","2020-06-05","2020-06-06","2020-06-07","2020-06-08","2020-06-09","2020-06-10",
            "2020-06-11","2020-06-12","2020-06-13","2020-06-14","2020-06-15","2020-06-16","2020-06-17","2020-06-18","2020-06-19","2020-06-20",
            "2020-06-21","2020-06-22","2020-06-23","2020-06-24","2020-06-25","2020-06-26","2020-06-27","2020-06-28","2020-06-29","2020-06-30",
            "2020-07-01","2020-07-02","2020-07-03","2020-07-04","2020-07-05","2020-07-06","2020-07-07","2020-07-08","2020-07-09","2020-07-10",
            "2020-07-11","2020-07-12","2020-07-13","2020-07-14","2020-07-15","2020-07-16","2020-07-17","2020-07-18","2020-07-19","2020-07-20",
            "2020-07-21","2020-07-22","2020-07-23","2020-07-24","2020-07-25","2020-07-26","2020-07-27","2020-07-28","2020-07-29","2020-07-30",
            "2020-08-01","2020-08-02","2020-08-03","2020-08-04","2020-08-05","2020-08-06","2020-08-07","2020-08-08","2020-08-09","2020-08-10",
            "2020-08-11","2020-08-12","2020-08-13","2020-08-14","2020-08-15","2020-08-16","2020-08-17","2020-08-18","2020-08-19","2020-08-20",
            "2020-08-21","2020-08-22","2020-08-23","2020-08-24","2020-08-25","2020-08-26","2020-08-27","2020-08-28","2020-08-29","2020-08-30"];
    # 90일치 데이터
    
    inputData = [];
    for i in range(num):
        for j in range(90):
            inputData.append((ids[i],consumption[90 * i + j][0],consumption[90 * i + j][1],consumption[90 * i + j][2],consumption[90 * i + j][3],consumption[90 * i + j][4],
                            consumption[90 * i + j][5],consumption[90 * i + j][6],consumption[90 * i + j][7],consumption[90 * i + j][8],consumption[90 * i + j][9],
                            consumption[90 * i + j][10],consumption[90 * i + j][11],consumption[90 * i + j][12],consumption[90 * i + j][13],consumption[90 * i + j][14], dates[j]));
    
    print("inputData is created successfully.");
    return inputData;

def main(count):
    inputData = createData(count);
    
    storeToDB(inputData);


if __name__ == '__main__':
    main(int(sys.argv[1]));