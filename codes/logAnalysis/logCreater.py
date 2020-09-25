# 47.29.201.179 - - [28/Feb/2019:13:17:10 +0000] "GET /?p=1 HTTP/2.0" 200 5316 "https://domain1.com/?p=1" "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"

import random as rd;
import sys;
import numpy as np;

getActions = [f"GET /action{i} HTTP/2.0\" 200 {rd.randint(100, 5000)}" for i in range(1,900)];
# 고객이 사이트에서 할 수 있는 행동 [500개]
## postActions = [f"POST /product{i} HTTP/2.0\" 302 {rd.randint(100, 5000)}" for i in range(1, 51)];
## 고객이 상품에 대한 post를 실행할 경우 [50개] (전환고객 seed)
# >>>>> 하나의 상품에 대한 것으로 변경 <product1>
referers = [f"link{i}" for i in range(1, 51)];
referers.append("-");
# 어느 링크를 타고 들어왔는가? ("-"는 url 직접 입력)
browser = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36";
# 클라이언트 브라우저 정보는 현재 우리에게 크게 중요하지 않으므로 Chrome으로 통일

class Customer:
        def __init__(self, ip, time, ID, interests):
            self.ip = ip;
            self.access = time;
            self.ID = ID;
            self.interests = interests;
        
        def post(self, logs):
            logs.append(f"{self.ip} - - {self.access} \"POST /product1 HTTP/2.0\" 302 {rd.randint(100, 5000)} \"-\" \"{browser}\" {self.ID}");
    
        def doActions(self, num, logs):
            for _ in range(num):
                logs.append(f"{self.ip} - - {self.access} \"{rd.choice(getActions)} \"{rd.choice(referers)}\" \"{browser}\" {self.ID}");
            
        def chatbotPick(self, interestList, logs):
            logs.append(f"{self.ip} - - {self.access} \"GET /chatbot/{rd.choice(interestList)} HTTP/2.0\" 200 {rd.randint(100, 5000)} \"{rd.choice(referers)}\" \"{browser}\" {self.ID}");
        
def main(users, inputFile, outFile):

    interestList = np.load(inputFile);
    
    ips = [f"{rd.randint(1,255)}.{rd.randint(0,255)}.{rd.randint(0,255)}.{rd.randint(0,255)}" for _ in range(users)];
    # remote host의 ip 주소 [1000개]
    times = [f"[25/Aug/2020:{rd.randint(0,24)}:{rd.randint(0,59)}:{rd.randint(0,59)} +0000]" for _ in range(users)];
    # 사이트 초기 접속시간 1개 ip당 1개의 난수

    logs = [];
    posts = 0;
    
    customers = [Customer(ips[i], times[i], i + 1, interestList[i]) for i in range(users)];

    for customer in customers:
        count = rd.randint(30, 60);
        logs.append(f"{customer.ip} - - {customer.access} \"GET / HTTP/2.0\" 200 3592 \"{rd.choice(referers)}\" \"{browser}\" {customer.ID}");
        customer.doActions(count, logs);
        if rd.random()*count > 50:
            customer.post(logs);
            posts += 1;
            
        if rd.random() > 0.07:
            customer.chatbotPick([""], logs);
            
            while rd.random() > 0.2:
                customer.chatbotPick(customer.interests, logs);

    f = open("./%s"%outFile, "w");

    for log in logs:
        f.write(log + "\n");
    
    f.close();

    print(f"{len(logs)} logs successfully created. [seeds are {posts}.]");
    
if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2], sys.argv[3]);