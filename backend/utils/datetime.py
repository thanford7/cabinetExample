import time
from datetime import datetime


def get_unix_datetime(date_time: datetime):
    return int(time.mktime(date_time.timetuple()))
