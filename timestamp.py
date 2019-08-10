import sys
from datetime import datetime

if len(sys.argv) > 1:
    date_time = sys.argv[1]
    dt_obj = datetime.strptime(str(date_time) + ' 00:00:01', '%m.%d.%Y %H:%M:%S')
    millisec = dt_obj.timestamp() * 1000
    print(millisec)
else:
    print(" No arguments ")



