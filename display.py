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
restaurant =""

db = client.meal
globalDB = db.cham

# clear()
def cls():
    os.system('cls' if os.name=='nt' else 'clear' )

class Controller:
    def UC4_controller(self):
        interface = PM_Interface()
        meal_time=interface.UC4_interface()

        button = Button_click()
        button.available_now(meal_time)
    
    def UC2_controller(self,tmp_cart):
        order = Order()
        
        # 주문목록(장바구니에 담긴 메뉴, 수량) 담기
        for meal in tmp_cart:
            order.append_order([meal,1])

        while(1):
            interface=PM_Interface()
            c = interface.UC2_interface(tmp_cart,order.get_order())
            
            button = Button_click()
            button.control_menu_num(c,order)
    
    def UC5_controller(self,orders):
        calculator = Calculator(orders)
        costs,total = calculator.calculate_amount()
        discount = calculator.calculate_discount()
        pay=calculator.calculate_pay(discount)

        interface=PM_Interface()
        interface.UC5_interface(costs,total,discount,pay,orders)

        button = Button_click()
        button.payment_process(orders)

class PM_Interface:
    def UC2_interface(self,tmp_cart,order):
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

        return c

    def UC4_interface(self):
        global date_token
        global restaurant
        global globalDB
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

        return meal_time

    def UC5_interface(self,costs,total,discount,pay,orders):
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

class Button_click:
    def available_now(self,meal_time):
        global date_token
        global restaurant
        global globalDB
        try:
            
            res = input("조회를 원하는 식당이나 옵션을 선택해주세요. : ")

            if(res =="1" or res == "2"):
                if(res =="1"):
                    restaurant="참슬기"
                    picked = list(globalDB.find({"date":date_token[0]}))
                    picked = picked[0]
                elif(res == "2"):
                    restaurant="블루미르홀"
                    globalDB = db.blue
                    picked = list(globalDB.find({"date":date_token[0]}))
                    picked = picked[0]

                menu=Menu()
                menu_list=menu.today_menu(picked,meal_time)

                self.putMenu(menu_list)

            elif(res == "3"):
                print("\n프로그램을 종료합니다 ! 빠이빠이")
                sys.exit()
            #cls()
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다 ! 빠이빠이")
            sys.exit()
        cls()

    # 메뉴 디스플레이하고 선택하는 함수
    def putMenu(self,menu):
        tmp_cart=Tmp_cart()
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

            print("담긴 개수 | ",len(tmp_cart.get_tmp_cart()))

            ret = int(input("원하는 메뉴들을 담아주세요 : "))
            while(ret<=0 or ret>c+3):
                ret = int(input("다시 입력해주세요 : "))

            if(ret == c+2): # 뒤로 가기 (어떤 메뉴도 클릭하지 않았다.)
                print("이전 화면으로 돌아갑니다.")
                cls()
                return 0 

            elif(ret == c+3): # 장바구니 보러가기 기능
                if len(tmp_cart.get_tmp_cart())==0:
                    print("메뉴를 1개 이상 담아주세요.")
                    time.sleep(0.5)
                else:
                    controller = Controller()
                    controller.UC2_controller(tmp_cart.get_tmp_cart())
            else:
                tmp_cart.compute_total_num(menu[ret-1])

    def control_menu_num(self,c,order):
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
            controller = Controller()
            controller.UC5_controller(order.get_order())
            # pay_list(order.get_order()) # 결제 하러 가기 (주문 내역 및 결제버튼 확인하는 화면으로 이동)
            pass
        else:
            num = int(input("원하는 만큼 개수 조절을 해주세요 : "))

            data_filter=Data_filter()
            data_filter.filtering(num,order,ret)
            
            order.control_menu_num(ret-1,num)
            # -> 특정 메뉴 클릭, 개수 입력 / 단 0,10 사이로만 가능함

    def payment_process(self,orders):
        go=int(input("결제를 원하시면 2번을 선택해주세요. :"))
        if(go == 1): # 뒤로 가기 (어떤 메뉴도 클릭하지 않았다.)
            print("이전 화면으로 돌아갑니다.")
            cls()
            return 0 
        else:
            menu = Menu()
            menu.stock_update(orders)

            qr = QRcode()
            qr.create_qrcode(orders)

class Menu:
    def __init__(self):
        self.menu=[]

    def today_menu(self,picked,meal_time): #오늘(지금) 구매 가능한 메뉴 리스트 정보 담는 함수 따로 분기
        for time in picked:    
            if(meal_time in time or "간식" in time):
                meal = picked[time] # meal[0] = 메뉴 이름, meal[1] = 가격, meal[2] = 재고, meal[3] = 카테고리
                meal.append(time)
                self.menu.append(meal)
        return self.menu

    # qrcode 생성과 동시에 db접근하여 재고 수량 업데이트
    def stock_update(self,orders):
        for order in orders:
            temp = order[0]
            temp[2] -= order[1]
            globalDB.update_one({"date":date_token[0]}, {"$set":{temp[3]:temp}},  upsert=True)

class Tmp_cart:
    def __init__(self):
        self.tmp_cart=[]

    def compute_total_num(self,menu):
        try:
            if menu in self.tmp_cart:
                print("이미 담은 메뉴입니다.")
                time.sleep(0.5)
            else:
                self.append_tmp_cart(menu)
        except IndexError:
            self.append_tmp_cart(menu)

    def append_tmp_cart(self,menu):
        self.tmp_cart.append(menu)
        print("장바구니에 정상적으로 담겼습니다.")
        time.sleep(0.5)
        # print("장바구니 목록:",tmp_cart)

    def get_tmp_cart(self):
        return self.tmp_cart

class Order: # 얘는 uc4의 메뉴리스트 아니고, uc2의 주문(메뉴리스트+담은수량)
    def __init__(self):
        self.order=[]
    
    def append_order(self,order_list):
        self.order.append(order_list)

    def control_menu_num(self,order_idx,control_num): # 개수 조절
        self.order[order_idx][1]=control_num
    
    def get_order(self):
        return self.order

class Data_filter:
    def filtering(self,num,order,ret):
        max_stock = order.get_order()[ret-1][0][2]
        while((num<0 or num>10) or num > max_stock ):
            if(num<0 or num>10): # 개수 조절 범위 : 0~10
                num = int(input("개수 조절 허용 범위는 0~10입니다.다시 입력해주세요 : "))
            elif(num > max_stock): # 재고 수량보다 넘겼을 경우
                num = int(input("재고({})보다 많은 수량을 주문할 수 없습니다. 다시 입력해주세요: ".format(max_stock)))
        return num

class Calculator:
    def __init__(self,orders):
        self.total=0
        self.costs=[]
        self.orders=orders
    
    def calculate_amount(self):
        for order in self.orders:
            cost=int(order[0][1][0]+order[0][1][2:-1])
            self.costs.append(cost)
            self.total+=cost*order[1]
        return self.costs,self.total

    def calculate_discount(self):
        return self.total//10

    def calculate_pay(self,discount):
        return self.total-discount

class QRcode:
    def create_qrcode(self,orders):
        global restaurant
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
        print("{}까지 {} 학식당에 가서 큐알코드를 보여주세요 (유효시간:10분)".format(ten_minutes_later,restaurant)) # 아직 학식당 안불러옴 나중에 디비에서 빼장
        print("======================================================================\n")
        
        num=int(input("QR이미지를 저장하시겠습니까? (1) yes (2) no : "))

        if num==1:
            QR.save(("qr_image.png"))

        print("\n주문이 성공적으로 접수되었습니다!!")
        print("첫 화면으로 돌아갑니다.")
        time.sleep(3)

        cls()
        controller = Controller()
        controller.UC4_controller()

        
if __name__ == "__main__":
    controller = Controller()
    controller.UC4_controller()