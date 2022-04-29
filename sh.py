from pynput import keyboard,mouse
import sqlalchemy
import pandas as pd
import datetime
import pymssql
CODE = ""
line = "0000000000"
def on_press(key):
    global CODE
    global line
    try:
        CODE += key.char
        if CODE[0]=="0":
            line=CODE
        # print(key.char)
        if len(CODE) == 10 and CODE[0]!="0":
            serial_to_shsqlserver(CODE,line)
        if key.char not in ["0","1","2","3","4","5","6","7","8","9",]:
            CODE = ""
        return line
    except AttributeError:
        # print(key)
        CODE=""
    except Exception:
        pass

def on_release(key):
    global CODE

def serial_to_shsqlserver(SerialNo,procudure):
    current_datetime=datetime.datetime.now()
    current_date=str(current_datetime.date()).replace("-",'')
    SerialNo_column = ["SerialNumber", "DateTime", "Procedure", "Date_id"]
    serialNo_to_sqlserver=pd.DataFrame(columns=SerialNo_column)
    value=[SerialNo,current_datetime,procudure,current_date]
    serialNo_to_sqlserver.loc[1]=value
    df0_list=[]
    try:
        conn=pymssql.connect(server="DW-SQL\DW",user="s00015",password="Start123!",database="ThroughPutTime")
        sql_ASS="select SerialNumber from Data_aquisition_scrstartserialnumber"
        df0=pd.read_sql(sql_ASS,conn)
        df0_list=df0["SerialNumber"].tolist()[-80:]
    except Exception:
        pass
    if SerialNo in df0_list:
        try:
            engine = sqlalchemy.create_engine(r'mssql+pymssql://s00015:Start123!@DW-SQL\DW/ThroughPutTime?charset=utf8', )
            serialNo_to_sqlserver.to_sql(name='Data_aquisition_scrserialnumber', con=engine, if_exists='append',index=False)
        except Exception:
            pass
    else:
        try:
            engine = sqlalchemy.create_engine(
            r'mssql+pymssql://s00015:Start123!@DW-SQL\DW/ThroughPutTime?charset=utf8', )
            serialNo_to_sqlserver.to_sql(name='Data_aquisition_shserialnumber', con=engine, if_exists='append',
                                         index=False)
        except Exception:
            pass


if __name__ == '__main__':
    while True:
        try:
            with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
                listener.join()
        except Exception:
            pass