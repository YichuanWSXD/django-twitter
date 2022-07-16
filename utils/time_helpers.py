from datetime import datetime
import pytz

def utc_now():
    return datetime.now().replace(tzinfo=pytz.utc)


def convert_datetime_helper(dt):
    return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.utc)