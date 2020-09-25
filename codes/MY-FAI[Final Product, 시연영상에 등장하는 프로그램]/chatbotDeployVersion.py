import tensorflow as tf;
import numpy as np;
from Postgre import PostgreConn;
from tensorflow.keras import layers;
from tensorflow.keras.layers import LeakyReLU, Dropout;
import json;
import sys;
sys.stdout.reconfigure(encoding='utf-8');

convToInterest = {0:"코로나 때문에 국내 관광지에 대한 관심이 많아졌어요! 그동안 관광객으로 북적였던 유명 지역보다는 소규모의, 그동안 알려지지 않았던 히든플레이스로 여행 계획을 세운다고 해요! 제가 한적하고 여태 알려지지 않았던 여행지 리스트를 보여드릴게요! 국내 여행을 하더라도 방역 수칙을 지키는 것을 절대 잊지마세요! (코로나 시대 국내 여행지 추천[link])", 
1:"사회적 거리두기 때문에 여러 백화점들이 라이브 커머스를 진행하고 있습니다! 진행자가 백화점 매장에서 라이브 방송을 하며 제품 설명을 하는 형식이에요! 시청자들이 실시간 채팅을 통해 제품을 더 자세히 설명해달라고 요구할 수도 있고, 많은 할인 행사도 진행한다고 해요! 백화점 별 라이브 커머스에 대한 링크를 안내해드릴게요! (백화점 라이브커머스[link], 백화점 라이브커머스[link])", 
2:"고객님, tvN에서 방영중인 '신박한 정리' 프로그램에서 XX님의 집을 깔끔하게 정리해준 잇아이템들을 모아봤어요! XX님의 집을 개조한 아이템들, 궁금하지 않으신가요?! (상품 모음 보러가기[link])", 
3:"요즘 언택트 소비가 활성화되면서, 오프라인 유명 맛집들이 가정간편식 시장에 유입되고 있다고 합니다! 특정 제조사와 협력하여, 온프라인에서만 맛 볼 수 있던 음식들을 집에서도 먹을 수 있다고 하네요! 유명 맛집들의 음식을 주문할 수 있는 링크를 안내해드릴게요! (함박 스테이크 주문[link], 식당 부대찌개 주문[link])", 
4:"혹시 넷플릭스 가입 요금에 부담을 느끼고 계신가요? 그렇다면, 제가 저렴한 가격으로 넷플릭스에 가입하는 방법을 알려드릴게요! 넷플릭스는 최대 4명과 공유할 수 있고, 이렇게 되면 3600원으로 이용할 수 있습니다! 지금 당장 리브똑똑 친구들에게 메신저로 넷플릭스 계정 공유하자고 연락하는건 어떤가요? (메시지를 보낼 친구 목록 리스트[link])", 
5:"고객님, 이번에 명작 뮤지컬 '노트르담 드 파리'가 XX 문화예술회관에서 9월 14일부터 9월 16일까지 3일간 9회 공연됩니다! (할인쿠폰 받으러가기[link])", 
6:"고객님, XX에서 9월 19일 ~ 9월 26일 일주일간 XX축제가 개최된다고 합니다! 화려한 이벤트와 공연, 즐길거리가 준비되어 있다고 하니 시간 내셔서 방문해보시면 즐거우실것 같아요! (XX축제 세부일정, 구성 보러가기[link])", 
7:"고객님, 이번에 `하이트 진로`에서 참이슬(참참참)[10.2도]를 새로이 출시했습니다! 소주 특유의 알코올향을 약하게 하고, 과일맛은 첨가하지 않았다고 하니 오늘은 참참참, 어떠신가요?! (참이슬(참참참) 자세히 알아보기[link])", 
8:"극심한 미세먼지의 때문에, '안티더스트' 가전제품의 인기가 높다고 해요! 특히 젊은층 중심으로 의류 관리기, 의류건조기를 사용해 본 소비자들의 만족도가 매우 높다고 하네요! 가성비 높은 안티더스트 제품들과 사용법에 대해서 소개해드릴게요! ", 
9:"어느덧 8월이 지나가고 9월이 되었어요! 이번달은 각 편의점들이 어떤 상품들에 대한 이벤트를 할까요?!(두근두근) (GS25, SevenEleven, CU, Emart24 9월 이벤트 모아보기[link])",
10:"고객님, '일회용 컵 보증금제'가 다시 부활한다고 합니다! 2021년부터 카페 매장 안에서 플라스틱컵은 물론 종이컵도 사용할 수 없게 됩니다! 2022년부터는 테이크아웃 컵 보증금제가 본격적으로 도입된다고 합니다! 국민은행 어플리케이션을 사용하여 컵 보증금을 받는 방안도 마련하고 있으니, 이 점 참고해주시길 바랍니다! (일회용 컵 보증금제 부활[link])", 
11:"고객님, 가끔 월말에 빠져나가는 교통비를 보시면 깜짝 놀랄 때가 있으시죠? 교통비가 점점 오르는 상황에서, 미처 챙기지 못했던 교통비 절약 방법들까지 알려드릴게요! (교통비 절약 방법[link])", 
12:"고객님, 요즘 환경을 고려하여 전기차에 대한 수요가 늘고 있다고 합니다! 전기차의 이점과 전기차 요금 관련 혜택사항을 소개해드릴게요! 좀 더 많은 분들이 전기차를 구매하셔서, 환경도 보호하고 비용도 절약하는 혜택을 누리셨으면 합니다! (전기차 이점[link], 전기차 요금 혜택사항[link])", 
13:"최근 5년 새 미세먼지 때문에 피부 건강이 걱정되시죠? 이에 따라 세계 안티폴루션 화장품 시장이 엄청 성장했다고 하네요! 미세먼지 차단에 효과적인 국내 화장품과 해당 상품들을 효과적으로 사용하는 방안에 대해서 알려드릴게요! (안티폴루션 화장품 브랜드[link])", 
14:"4차 산업혁명에 따라 교육 트렌드도 많이 변하고 있습니다! 어떤 교육을 받아야 4차 산업혁명의 흐름에 따라갈 수 있는지, 해당 교육을 어떻게 수강할 수 있는지 알려드릴게요! 더 늦기 전에 해당 교육 기회들을 놓치지 않길 바래요! (2020년에 주목할 교육의 5가지 트렌드[link])"
};

alphaToNum = {};

alphas = list("ABCDEFGHIJKLMN");

for i in range(14):
    alphaToNum[alphas[i]] = i;
    
def ageToAger(age):
    return age % 10;

def main(userID):
    models = [tf.keras.models.load_model(f"model_{i}.h5") for i in range(15)];
	
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
            
    result = conn.select(f"select job, gender, age, hasCar, getMarried, children, incomeLevel, assetsLevel from CUSTOMER where userID = {userID};");
    userFeature = [];
    for i in range(len(result[0])):
        if i == 0:
            stop = alphaToNum[result[0][i]];
            for j in range(14):
                if j == stop:
                    userFeature.append(1);
                else:
                    userFeature.append(0);
        elif i == 2:
            for l in range(2, 8):
                if ageToAger(result[0][i]) == l:
                    userFeature.append(1);
                else:
                    userFeature.append(0);
        else:
            userFeature.append(result[0][i]);
            
    vecSum = sum(vector);
    for i in range(15):
        vector[i] /= vecSum;
            
    X = np.asarray([vector + userFeature]);
	
    conn.close();
		
    interests = [models[i].predict(X)[0] for i in range(15)];
    
    first = interests.index(max(interests));
    interests[interests.index(max(interests))] -= 1;
    
    second = interests.index(max(interests));
    interests[interests.index(max(interests))] -= 1;
    
    third = interests.index(max(interests));
    
    result = [first, second, third];
    
    for i in range(3):
        result[i] = convToInterest[result[i]];
    
    print(result[0]);
    print(result[1]);
    print(result[2]);
	
if __name__ == '__main__':
    main(int(sys.argv[1]));
	
    