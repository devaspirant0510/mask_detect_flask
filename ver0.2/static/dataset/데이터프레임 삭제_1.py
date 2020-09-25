import pandas as pd
import time
import sys

df=pd.read_csv("dataset.csv")
print("현재  userdataset.csv 파일 내용\n",df)
time.sleep(1)
print("정말 삭제하시겠습니까?")
print("삭제시 복구가 불가능합니다.")
print("삭제하고싶으면 y 아니면 n")
while True:
    yn=input()
    if yn=='y' or yn=='Y':
        df=pd.DataFrame(columns=['date','user','id','mask','nomask'])
        df.to_csv('dataset.csv')
        print("삭제하였습니다.")
        print("프로그램은 자동으로 종료됩니다.")
        time.sleep(1)
        sys.exit()
    elif yn=='n' or yn=='N':
        print("데이터는 그대로 보존됩니다.")
        print("프로그램은 자동으로 종료됩니다.")
        print("현재  dataset.csv 파일 내용\n",df)
        time.sleep(2)
        sys.exit()
    else:
        print("입력이 잘못됬습니다. y또는 n을 입력해주세요.")
        continue

