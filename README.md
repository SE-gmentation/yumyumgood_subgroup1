
# Link
https://github.com/SE-gmentation/yumyumgood_subgroup1
<br/>
## 📢 SubGroup 1

- 주제 소개
  - 회원가입 및 주문하기 주제를 맡은 SUBGROUP1 고은서/오예원 입니다.
  - 총 7가지의 USE-CASE 중 UC-2, UC-3, UC-5의 기능을 구현했습니다.
  - UC-2 : 개수 조절
  - UC-4 : 메뉴 선택
  - UC-5 : 결제

- 기능 명세
  - 학식당 별 메뉴 파싱 및 DB 저장
  - 접속 시간에 구매가능한 학식당 별 메뉴 조회 및 선택
  - 선택한 메뉴 개수조절 및 결제를 통한 QR생성 및 DB 재고 업데이트

<br/>

## 🔨 Tech stacks & Language

- Python3
- Mongo DB (Mongo Atlas)


<br/>

## 🔎 Getting Started
1. Clone this repository

   ```bash
   $ git clone https://github.com/SE-gmentation/yumyumgood.git
   ```

2. Install 

   ```bash
   $ pip install qrcode
   $ pip install dnspython
   $ pip install python-dotenv
   ```

3. Start developing
  - DB Update
    1. 중앙대 홈페이지에서 해당 주차별 학식 파일 다운로드(csv)
    2. parse_date.py 에 파일 경로 입력
    3. DB update 진행

    ```bash
    $ python parse_data.py
    ```

  - 주문 및 결제
    ```bash
    $ python display.py
    ```

<br/>

## 📸 Features & Demo Screenshot

- **데이터 불러오기 및 데이터 파싱 후 DB구축**
  - 다운로드 받은 파일(CSV 형태)
  ![image](https://user-images.githubusercontent.com/63635886/120102026-10679600-c184-11eb-83e5-464187cf175b.png)
  - MongoDB 반영
  ![image](https://user-images.githubusercontent.com/63635886/120101943-ab13a500-c183-11eb-9957-19628cab2ece.png)

- **( UC-4 )  DB구축 및 현재 접속한 시간대에 구매 가능한 학식당 별 메뉴 조회**
  1. 먼저, 포탈 내 학식당 페이지에 접속하여 data로 이용할 식단 데이터를 csv형태로 불러와 파싱한 뒤, MongoDB Atlas에 저장한다.(parse_data.py)
  2. display.py를 실행하게 되면 오늘의 날짜와 시간대를 반영한 선택 가능 학식 리스트를 보인다.

  - 시작 화면
  ![image](https://user-images.githubusercontent.com/63635886/120102072-4c9af680-c184-11eb-9e33-81cc318973de.png)



- **( UC-4 )  메뉴 선택**
  1. 선택 가능한 메뉴와 재고를 함께 나타내 메뉴 선택을 돕는다.
  - 메뉴 선택
  ![image](https://user-images.githubusercontent.com/63635886/120102225-ec588480-c184-11eb-91cd-9dcd5eee6843.png)

- **( UC-2 ) 장바구니에서 담은 메뉴 개수 조절**
  1. 장바구니를 조회하게 되면 개수를 조절할 수 있도록 한다.
  2. 개수 조절의 범위는 1~10개까지이며, 해당 범위를 넘지 않는 선에서 개수를 조절할 수 있도록 한다.
  3. DB 재고 수량을 파악하여 해당 재고 수량을 넘지 않는 선에서 개수를 조절할 수 있도록 한다.

  - 장바구니 화면
  ![image](https://user-images.githubusercontent.com/63635886/120102395-bbc51a80-c185-11eb-9e74-737c585baa82.png)

  - 최대 개수 내 조절 가능
  ![image](https://user-images.githubusercontent.com/63635886/120102418-d8f9e900-c185-11eb-911c-32a532cebebe.png)

  - 재고 수량 내 조절 가능
  ![image](https://user-images.githubusercontent.com/63635886/120102432-f038d680-c185-11eb-8bc5-b735cc1cdd90.png)


- **( UC-5 ) 결제 금액 계산 및 QR코드 생성 및 유효시간 핸들링**
  1. 학생 할인 여부를 반영한 결제 화면을 보인다.
  2. QR 코드를 발급 한다.(파일로서 저장할 수 있으며 QR생성시간+10분까지 유효하다)
  - 결제 화면
  ![image](https://user-images.githubusercontent.com/63635886/120102498-4ad23280-c186-11eb-93b4-169b4b45c04f.png)
  - QR코드 생성 및 이미지 저장
  ![image](https://user-images.githubusercontent.com/65647080/120113274-ac10fa80-c1b4-11eb-817a-84673e9cebad.png)
    <img src="https://user-images.githubusercontent.com/65647080/120113321-e11d4d00-c1b4-11eb-873c-5758927b8423.png" width="200">
  
  - 디비 반영 결과 (재고 | 10 ▶ 6, 10 ▶ 9)
  ![image](https://user-images.githubusercontent.com/65647080/120113184-47ee3680-c1b4-11eb-917b-a42a6f759121.png)



<br/>

## 📍 SSD(Class Diagram) 대조표
- UC4 ( 메뉴 선택 )

>   | 클래스명(함수명) |  SSD 내 컨셉(클래스)이름  |
>   | --- | ---  |
>   |**Controller 클래스 내 UC4_controller()** |컨트롤러|
>   |**Button_Click 클래스 내 available_num()&putMenu()** |버튼객체|
>   |**Tmp_cart 클래스**|장바구니Storage|
>   |**Menu 클래스** |메뉴DB|
>   |**PM_Interface 클래스 내 UC4_interface()** |페이지생성&인터페이스페이지(팝업생성&팝업-예외)|

- UC2 ( 개수 조절 )

>   | 클래스명(함수명) |  SSD 내 컨셉(클래스)이름  |
>   | --- | ---  |
>   |**Controller 클래스 내 UC2_controller()**|컨트롤러|
>   |**Button_Click 클래스 내 control_menu_num()**|버튼객체|
>   |**Tmp_cart 클래스**|장바구니Storage|
>   |**Order 클래스**|주문DB|
>   |**PM_Interface 클래스 내 UC2_interface()** |페이지생성&인터페이스페이지(팝업생성&팝업-예외)|
>   |**Data_filter 클래스** |데이터여과|
>   |**Menu 클래스** |메뉴DB|

- UC5 ( 결제 )

>   | 클래스명(함수명) |  SSD 내 컨셉(클래스)이름  |
>   | --- | ---  |
>   |**Controller 클래스 내 UC5_controller()**  |컨트롤러|
>   |**Button_Click 클래스 내 payment_process()** |버튼객체|
>   |**Order 클래스** |주문DB|
>   |**Calculator 클래스** |결제 금액 계산 처리기&회원DB연결|
>   |**QRcode 클래스** |QR코드처리기|
>   |**PM_Interface 클래스 내 UC5_interface()**|페이지생성&인터페이스페이지(팝업생성&팝업-예외)|
  
<br/>

<br/>

## 💻 참고사항
- 코드 작업 위치 : yumyumgood_subgroup1 respository
- DB 연결 시 URL이 필요합니다. 저희는 따로 env파일에 설정 후 작업하였기에, 혹시 필요하시다면 말씀해주세요 ! ! 
- 해당 주차 별 학식 데이터 파일을 세팅해야합니다.
  (참슬기 : cham.csv, 블루미르: blue.csv)



