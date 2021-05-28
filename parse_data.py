import csv
import json

"""
{
    "날짜" :{
        중식 : [메뉴, 가격, 재고]
    }
    ...
}
"""

def printP(data):
    print(json.dumps(data,ensure_ascii = False,sort_keys=True, indent=4))

def cham_res():
    f = open('cham.csv', 'r', encoding='cp949')

    rdr = csv.reader(f)
    count = 0

    data = {}
    t_date = []

    mealStr = ["중식", "중식-특식", "석식-특식", "석식"]

    mealIdx = 0
    for row, line in enumerate(rdr):
        if(row < 4):
            if(row == 0):
                data["restaurant"] = line[0][1:]
            if(row == 3): 
                for date in line[1:-2]:
                    date = date[-6:-1]
                    data[date] = {}

                    t_date.append(date)           
        else:
            if(row != 12 and row %4 ==0):
                for idx,meal in enumerate(line[2:-2]):
                    if(len(meal)!= 0 and "코로나" not in meal):
                        data[t_date[idx]][mealStr[mealIdx]] = [meal]
            elif(row == 12):
                for idx,meal in enumerate(line[1:-2]):
                    if(len(meal)!= 0 and "코로나" not in meal):
                        data[t_date[idx]][mealStr[mealIdx]] = [meal]
            elif(row % 4 == 3):
                for idx, price in enumerate(line[:-2]):
                    price = price.strip()
                    if(len(price) > 3):
                        data[t_date[idx]][mealStr[mealIdx]].append(price.strip())
                        data[t_date[idx]][mealStr[mealIdx]].append(10)
                mealIdx += 1
    f.close()   
    return data

def blue_res():
    f = open('blue.csv', 'r', encoding='cp949')

    rdr = csv.reader(f)
    count = 0
    data = {}
    t_date = []

    mealStr = ["중식", "중식-1","중식-2","중식-3","중식-4","중식-5", "석식", \
                "간식", "간식-1", "간식-2", "간식-3", "간식-4", "간식-5"]    
    mealIdx = 0
    for row, line in enumerate(rdr):
        if(row < 4):
            if(row == 0):
                data["restaurant"] = line[0][1:]
            if(row == 3): 
                for date in line[1:]:
                    date = date[-6:-1]
                    data[date] = {}

                    t_date.append(date)
        else:
            if(row != 4 and row != 28 and row != 32 and row % 4==0 ):
                for idx,meal in enumerate(line[1:]):
                    if(len(meal)!= 0):
                        data[t_date[idx]][mealStr[mealIdx]] = [meal]
            elif(row == 4 or row == 28 or row == 32):
                for idx,meal in enumerate(line[2:]):
                    if(len(meal)!= 0):
                        data[t_date[idx]][mealStr[mealIdx]] = [meal]
            elif(row % 4 == 3):
                for idx, price in enumerate(line[:]):
                    if(len(price) != 0):
                        data[t_date[idx]][mealStr[mealIdx]].append(price.strip())
                        data[t_date[idx]][mealStr[mealIdx]].append(10)
                mealIdx += 1
    f.close()
    #printP(data)
    return data