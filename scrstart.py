from pynput import keyboard,mouse
import sqlalchemy
import pandas as pd
import datetime
import pymssql
CODE = ""
line = ""
def on_press(key):
    global CODE
    global line
    try:
        CODE += key.char
        if CODE[0]=="0":
            line=CODE
        # print(key.char)
        if len(CODE) == 10 and CODE[0]!="0":
            print(CODE)
            serial_to_sqlserver(CODE,line)
            # CODE=""
        if key.char not in ["0","1","2","3","4","5","6","7","8","9",]:
            CODE = ""
    except AttributeError:
        # print(key)
        CODE=""

def on_release(key):
    global CODE

def serial_to_sqlserver(SerialNo,procudure):
    print("start")
    current_datetime=datetime.datetime.now()
    current_date=str(current_datetime.date()).replace("-",'')
    SerialNo_column = ["SerialNumber", "DateTime", "Procedure", "Date_id"]
    serialNo_to_sqlserver=pd.DataFrame(columns=SerialNo_column)
    value=[SerialNo,current_datetime,procudure,current_date]
    serialNo_to_sqlserver.loc[1]=value
    print("data_ready")
    try:
        engine = sqlalchemy.create_engine(r'mssql+pymssql://s00015:Start123!@DW-SQL\DW/ThroughPutTime?charset=utf8', )
        print("connection success")
        serialNo_to_sqlserver.to_sql(name='Data_aquisition_scrstartserialnumber', con=engine, if_exists='append',index=False)
        print("saved success")
    except Exception:
        print("failure")
        pass

if __name__ == '__main__':
    while True:
        try:
            with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
                listener.join()
        except Exception:
            pass
