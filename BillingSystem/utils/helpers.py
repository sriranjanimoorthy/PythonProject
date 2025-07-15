import datetime

def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def validate_phone(phone):
    return phone.isdigit() and len(phone) == 10

