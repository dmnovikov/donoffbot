from datetime import datetime 
from time import sleep

dt1= datetime.now()
sleep(5)
dt2=datetime.now()


dtimesec = dt2-dt1

dsec=int(dtimesec.total_seconds())

print(dsec)