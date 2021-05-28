import parse_data as pd
from datetime import *
import time
import os,sys
import time

# 이 함수는 clear 명령어 같은 것 !
def cls():
    os.system('cls' if os.name=='nt' else 'clear' )

def today_menu(picked,date_token,meal_time): #오늘(지금) 구매 가능한 메뉴 리스트 정보 담는 함수 따로 분기
    menu = []
    # 오늘 날짜의 메뉴에서 / 중, 석식 가려내기
    for time in picked[date_token[0]]:    
        if(meal_time in time or "간식" in time):
            meal = picked[date_token[0]][time] # meal[0] = 메뉴 이름, meal[1] = 가격, meal[2] = 재고
            menu.append(meal)
    return menu

# 메뉴 디스플레이하고 선택하는 함수
def lookup(menu):
    cls()
    tmp_cart=[] # 장바구니 화면에서 이어서 보여져야할 구매목록들
    while(1):
        c = 0
        for idx, meal in enumerate(menu):
            c = idx
            print("({}). {}".format(idx+1, meal[1])) # 가격 표시
            print(meal[0]) # 메뉴 표시
            print("\n")

        print("({}). 뒤로 가기".format(c+2))
        print("\n")

        print("({}). 장바구니 보러가기 ".format(c+3))
        print("\n")

        ret = int(input("원하시는 메뉴들을 담아주세요 : "))
        print(ret,type(ret))

        if(ret == c+2): # 뒤로 가기 (어떤 메뉴도 클릭하지 않았다.)
            print("이전 화면으로 돌아갑니다.")
            cls()
            return 0 

        elif(ret == c+3): # 장바구니 보러가기 기능
            # cart(tmp_cart)
            pass
        else:
            print("장바구니에 정상적으로 담겼습니다")
            time.sleep(0.5)
    # ##############은서은스ㅓ은서은서은서은서은서은서 은서가 볼곳######3########
    # else: # 선택된 메뉴를 가지고 여기서 으쌰으쌰
    #     print("선택 메뉴: ", menu[ret]) # menu[c]가 선택 메뉴라서 여기서 더 이어서 하면 댐. 리턴을 시켜서 하는게 더 나아 보이긴함
    #     return menu[c]
        
    

# main
def main():
    while(1):
        try:
            now = datetime.now()
            # dt_string = now.strftime("%m/%d %H:%M")
            dt_string = "05/28 12:30"
            date_token = dt_string.split(" ")
            meal_time = ""

            # 데이터 파싱
            cham = pd.cham_res()
            blue = pd.blue_res()

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
            picked = {}
            if(res =="1" or res == "2"):
                if(res =="1"):
                    picked = cham
                elif(res == "2"):
                    picked = blue
                menu=today_menu(picked,date_token,meal_time)
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