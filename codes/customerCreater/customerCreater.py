# 웹 크롤링을 이용한 사람 이름 리스트 뽑기
import requests;
from bs4 import BeautifulSoup;
from Postgre import PostgreConn;
import json;
import random;
import sys;

def main(count):
    # 여성 이름 리스트
    f = open("womenNames.txt", encoding='utf-8');
    webpage = f.read();

    soup = BeautifulSoup(webpage, "html.parser");

    name = soup.select(".ant-table-row-level-0 > td > a");

    womenNames = [a.text for a in name];

    # print(len(womenNames)); // 1000개
    # print(womenNames);

    f.close();

    # 남성 이름 리스트
    f = open("menNames.txt", encoding='utf-8');
    webpage = f.read();

    soup = BeautifulSoup(webpage, "html.parser");

    name = soup.select(".ant-table-row-level-0 > td > a");

    menNames = [a.text for a in name];

    # print(len(menNames)); // 1000개
    # print(menNames);

    f.close();

    # 성씨 데이터 크롤링
    webpage = requests.get("https://ko.wikipedia.org/wiki/%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EC%9D%B8%EA%B5%AC%EC%88%9C_%EC%84%B1%EC%94%A8_%EB%AA%A9%EB%A1%9D");
    soup = BeautifulSoup(webpage.content, "html.parser");

    lastname = soup.select(".wikitable > tbody > tr > td > b");

    # lastname[0:7]에는 성씨로써 의미가 없는 데이터가 포함되었기 때문에 lastname[7:]로 지정
    # a.text[0]을 지정한 이유는 성씨 데이터가 "김(한자 김)"으로 되어있기 때문에 앞의 1글자만 추출
    lastName = [a.text[0] for a in lastname[7:]];

    # print(len(lastName));  // 98개
    # print(lastName);

    # Database에 랜덤한 자료를 다량 확보하고 싶은 경우 해결방법

    # 실제 사용 시, 원하는 정보를 Web crawling을 이용하여 각각의 자료 확보
    # 지금은 간단한 이름정보를 입력하는 것으로 크롤링이 된 상태를 가정 (귀찮아서 이름은 그냥 A~Z 중 하나로 해두었다.) <수정 완료>
    firstName = womenNames + menNames;
    peoples = [];
    phones = [];
    alphas = list("abcdefghijklmnopqrstuvwxyz");
    Alphas = list("ABCDEFGHIGKLMN");
    emails = [];
    IDs = [];
    genders = [random.choice([0, 1]) for _ in range(count)];
    ages = [random.choice(range(20, 75)) for _ in range(count)];
    hasCar = [random.choice([0, 1]) for _ in range(count)];
    getMarried = [random.choice([0, 1]) for _ in range(count)];
    children = [random.choice(range(0, 5)) for _ in range(count)];
    incomeLevel = [random.randint(1, 10) for _ in range(count)];
    assetsLevel = [random.randint(0, 10) + incomeLevel[i] for i in range(count)];
    jobs = [];

    # random.choice() 함수를 이용하여 원하는 정보 랜덤하게 생성
    # 난수적 이름 생성기 경우의 수 : 98 * 2000 = 196000가지 이름 생성 가능
    for i in range(count):
        IDs.append(i+1);
        peoples.append(random.choice(lastName)+random.choice(firstName));
        phones.append(f"010-{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}-{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}");
        emails.append(f"{random.choice(alphas)}{random.choice(alphas)}{random.choice(alphas)}{random.choice(alphas)}{random.choice(alphas)}{random.randint(0, 9)}{random.randint(0, 9)}@example.com");
        jobs.append(random.choice(Alphas));
    
    #    print(IDs[i], peoples[i], phones[i], emails[i], departments[i]);
    
    # 남성의 이름과 여성의 이름을 구분하여 생성하는 것 또한 위 코드에서 조금만 조작하면 가능
    # 이름 데이터에 대해서 txt이나 html파일로 읽어온 것은 해당 사이트 웹 크롤링으로 긁어오는 것이 불가능했기 때문에 html자료를 복사하여 파일로 만들어 사용한 것

    # DB table schema : userID, name, gender, age, phone, email, job, hasCar, hasHouse, getMarried, children, incomeLevel, assetsLevel

    # mariaDB or mySQL
    """
    import pymysql;

    conn = pymysql.connect(host="localhost", user="root", password="zjdzjd11", db="test", port=33061);

    cursor = conn.cursor();

    for i in range(10000):
        cursor.execute(f"insert into EMPLOYEE(name, phone, email, department) values('{peoples[i]}', '{phones[i]}', '{emails[i]}', '{departments[i]}');");
    
    conn.commit();

    conn.close();
    """

    inputData = [];

    for i in range(count):
        infoTuple = (IDs[i], peoples[i], genders[i], ages[i], phones[i], emails[i], jobs[i], hasCar[i], getMarried[i], children[i], incomeLevel[i], assetsLevel[i]);
    
        inputData.append(infoTuple);



    with open("config.json") as jsonFile:
        jsonData = json.load(jsonFile);

    user = jsonData["user"];
    password = jsonData["password"];
    host = jsonData["host"];
    port = jsonData["port"];
    DB = jsonData["database"];
    
    conn = PostgreConn(user, password, host, port, DB);
    
    conn.insert(sql="""insert into CUSTOMER(userID, name, gender, age, phone, email, job, hasCar, getMarried, children, incomeLevel, assetsLevel)
                    values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", bulk=True, records=inputData);
    
    conn.close();

if __name__ == '__main__':
    main(int(sys.argv[1]));