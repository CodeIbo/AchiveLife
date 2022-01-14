from datetime import date
from datetime import datetime
from datetime import timedelta





dailyEndTask = datetime.combine(date.today(), datetime.min.time()) + timedelta(hours=24)


print( datetime.min.time())