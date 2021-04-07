from datetime import timedelta, datetime

def seq_date(start: datetime.date, end: datetime.date):
    length = (end - start).days
    return [start + timedelta(days = i) for i in range(length)]

def filter_weekends(dates: list):
    clean_dates = [] 
    for date in dates:
        day = date.weekday()
        if day >= 0 and day < 5:
            clean_dates.append(date)

    return clean_dates

def seq_date_clean(start: datetime.date, end: datetime.date):
    return filter_weekends(seq_dates(start, end))

def as_date(str_date: str):
    return datetime.strptime(str_date, "%Y-%m-%d").date()
