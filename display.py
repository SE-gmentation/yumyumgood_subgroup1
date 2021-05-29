import qrcode 
#import parse_data as pd
from datetime import *
import time
import os,sys
import time

from pymongo import MongoClient
from dotenv import load_dotenv

date_token=[]
load_dotenv(verbose=True)
client = MongoClient(os.getenv('MONGO_URL'))

db = client.meal
globalDB = db.cham

def create_qrcode(orders):
    # 현재 시간 가져오기
    current = datetime.now()
    # 10분 후 시간 가져오기
    ten_minutes_later = current + timedelta(minutes=10)
    ten_minutes_later = ten_minutes_later.strftime('%H시 %M분')
    
    print("\n            [. . . . . . loading . . . . . .]\n")
    time.sleep(1)
    QR=qrcode.make(orders) # 주문 내역에 대한 정보 qr코드에 저장

    print("======================================================================")
    print("                      QR이 정상적으로 생성되었습니다.")
    print("{}까지 {}학식당에 가서 큐알코드를 보여주세요 (유효시간:10분)".format(ten_minutes_later,"은서>_<")) # 아직 학식당 안불러옴 나중에 디비에서 빼장
    print("======================================================================\n")
    
    # stock_update() # 디비 재고 업데이트 하는 부분! 

    num=int(input("QR이미지를 저장하시겠습니까? (1) yes (2) no : "))

    if num==1:
        QR.save(("qr_image.png"))

    print("\n주문이 성공적으로 접수되었습니다!!")
    print("첫 화면으로 돌아갑니다.")
    time.sleep(2)

    cls()
    main()
    
# qrcode 생성과 동시에 db접근하여 재고 수량 업데이트
def stock_update(orders):
    for order in orders:
        temp = order[0]
        temp[2] -= order[1]
        globalDB.update_one({"date":date_token[0]}, {"$set":{temp[3]:temp}},  upsert=True)

def pay_list(orders):
    total=0
    costs=[]
    for order in orders:
        cost=int(order[0][1][0]+order[0][1][2:-1])
        costs.append(cost)
        total+=cost*order[1]

    discount=total//10 # 일단 회원할인 전체 금액의 10프로 할인이라고 가정
    pay=total-discount

    print("=========================[주문 내역]=========================")
    # 회원인지 비회원인지는 이미 등록되어 온 상태라고 가정한다.
    # 총금액, 회원할인금액, 결제 금액까지 보여주고 / 결제하러가기 클릭 
    total_num =0
    for i, order in enumerate(orders):
        if(order[1]==0): continue
        print("{}".format(order[0][0]))
        print("                                     수량:{}개 | 가격:{}원 |".format(order[1],costs[i]*order[1]))
        total_num=total_num+order[1]
        print("-------------------------------------------------------------")
    print(" 총수량 | {}".format(total_num))
    print("=============================================================")
    print("\n\n")


    print("=========================[결제 내역]=========================")
    print("총금액    |                                     {}원".format(total))
    print("회원 할인 ㅣ                                    {}원".format(discount))
    print("결제 금액 |                                     {}원".format(pay))
    print("=============================================================")
    
    print("\n")
    print("({}). 뒤로 가기".format(1))
    print("\n")
    print("({}). 결제 하러 가기 (QR코드) \n".format(2))

    go=int(input("결제를 원하시면 2번을 선택해주세요. :"))
    if(go == 1): # 뒤로 가기 (어떤 메뉴도 클릭하지 않았다.)
        print("이전 화면으로 돌아갑니다.")
        cls()
        return 0 
    else:
        stock_update(orders)
        create_qrcode(orders)
        pass

def cart(tmp_cart):
    
    order=[]
    
    # 주문목록(장바구니에 담긴 메뉴, 수량) 담기
    for meal in tmp_cart:
        order.append([meal,1])

    # print("장바구니 목록 보여주기",tmp_cart)
    while(1):
        cls()
        print("=========[장바구니]=========")
        c = 0
        for idx, meal in enumerate(tmp_cart):
            c = idx
            print("({}). {} [담은 개수 : {}]".format(idx+1, meal[1],order[idx][1])) # 가격 표시
            print(meal[0]) # 메뉴 표시
            print("\n")

        print("({}). 뒤로 가기".format(c+2))
        print("\n")

        print("({}). 주문 내역 보러 가기 ".format(c+3))
        print("\n")

        ret = int(input("개수를 조절하고픈 메뉴를 선택해주세요 : "))
        while(ret<=0 or ret>c+3):
            ret = int(input("다시 입력해주세요 : "))
        

        if(ret == c+2): # 뒤로 가기 (어떤 메뉴도 클릭하지 않았다.)
            print("이전 화면으로 돌아갑니다.")
            cls()
            return 0 

        elif(ret == c+3):
            time.sleep(0.5)
            cls()
            pay_list(order) # 결제 하러 가기 (주문 내역 및 결제버튼 확인하는 화면으로 이동)
            pass
        else:
            num = int(input("원하는 만큼 개수 조절을 해주세요 : "))
            while((num<0 or num>10) or num > meal[2] ):
                if(num<0 or num>10): # 개수 조절 범위 : 0~10
                    num = int(input("개수 조절 허용 범위는 0~10입니다.다시 입력해주세요 : "))
                elif(num > meal[2]): # 재고 수량보다 넘겼을 경우
                    num = int(input("재고({})보다 많은 수량을 주문할 수 없습니다. 다시 입력해주세요: ".format(meal[2])))
            order[ret-1][1]=num
            # -> 특정 메뉴 클릭, 개수 입력 / 단 0,10 사이로만 가능함


# 이 함수는 clear 명령어 같은 것 !
def cls():
    os.system('cls' if os.name=='nt' else 'clear' )

def today_menu(picked,meal_time): #오늘(지금) 구매 가능한 메뉴 리스트 정보 담는 함수 따로 분기
    menu = []
    for time in picked:    
        if(meal_time in time or "간식" in time):
            meal = picked[time] # meal[0] = 메뉴 이름, meal[1] = 가격, meal[2] = 재고, meal[3] = 카테고리
            meal.append(time)
            menu.append(meal)
    return menu

# 메뉴 디스플레이하고 선택하는 함수
def lookup(menu):
    tmp_cart=[] # 장바구니 화면에서 이어서 보여져야할 구매목록들
    while(1):
        cls()
        print("=========[메뉴 선택]========")
        c = 0
        for idx, meal in enumerate(menu):
            c = idx
            print("({}). {} / 재고 : {}".format(idx+1, meal[1], meal[2])) # 가격 표시
            print(meal[0]) # 메뉴 표시
            print("\n")

        print("({}). 뒤로 가기".format(c+2))
        print("\n")

        print("({}). 장바구니 보러가기 ".format(c+3))
        print("\n")

        print("담긴 개수 | ",len(tmp_cart))

        ret = int(input("원하는 메뉴들을 담아주세요 : "))
        while(ret<=0 or ret>c+3):
            ret = int(input("다시 입력해주세요 : "))

        if(ret == c+2): # 뒤로 가기 (어떤 메뉴도 클릭하지 않았다.)
            print("이전 화면으로 돌아갑니다.")
            cls()
            return 0 

        elif(ret == c+3): # 장바구니 보러가기 기능
            if len(tmp_cart)==0:
                print("메뉴를 1개 이상 담아주세요.")
                time.sleep(0.5)
            else:
                cart(tmp_cart)
        else:
            # 개수조절 또는 담은 메뉴 삭제는 장바구니 화면에서만 할 수 있음
            # 따라서 if문으로 분기 
            try:
                if menu[ret-1] in tmp_cart:
                    print("이미 담은 메뉴입니다.")
                    time.sleep(0.5)
                else:
                    tmp_cart.append(menu[ret-1])
                    print("장바구니에 정상적으로 담겼습니다.")
                    # print("장바구니 목록:",tmp_cart)
                    time.sleep(0.5)
            except IndexError:
                tmp_cart.append(menu[ret-1])
                print("장바구니에 정상적으로 담겼습니다.")
                time.sleep(0.5)
                # print("장바구니 목록:",tmp_cart)



# main
def main():
    global date_token
    global globalDB
    while(1):
        try:
            now = datetime.now()
            # dt_string = now.strftime("%m/%d %H:%M")
            dt_string = "05/28 12:30"
            date_token = dt_string.split(" ")
            meal_time = ""

            hour = int(date_token[1].split(":")[0])

            if( 11<= hour and hour <= 13):
                meal_time = "중식"
            else:
                meal_time = "석식"

            print("! 환영합니다 !")
            print("접속 시각 : {}, {}".format(date_token[0], date_token[1]))

            print("지금은 {} 조회가 가능해요.\n".format(meal_time))
            print("1. 참슬기 식당(310관 B4층)")
            print("2. 블루미르홀 308관")
            print("3. 종료하기\n")
            res = input("조회를 원하는 식당이나 옵션을 선택해주세요. : ")

            if(res =="1" or res == "2"):
                if(res =="1"):
                    picked = list(globalDB.find({"date":date_token[0]}))
                    picked = picked[0]
                elif(res == "2"):
                    globalDB = db.blue
                    picked = list(globalDB.find({"date":date_token[0]}))
                    picked = picked[0]

                menu=today_menu(picked,meal_time)
                lookup(menu)
            elif(res == "3"):
                print("\n프로그램을 종료합니다 ! 빠이빠이")
                sys.exit()
            #cls()
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다 ! 빠이빠이")
            sys.exit()

if __name__ == "__main__":
    main()