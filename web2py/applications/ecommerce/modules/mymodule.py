# -*- coding: utf-8 -*-

from datetime import datetime, timedelta


def year_month_list(from_date=None, to_date=None, format='%Y-%m-%d'):
    if from_date is None:
        from_date = datetime.today()
        month = from_date.month
        year = from_date.year
        start = year*100+month
    else:
        from_date = datetime.strptime(from_date, format)
        start = int(from_date.strftime('%Y%m'))
        month = start % 100
        year = start / 100

    if to_date is None:
        to_date = datetime.today()
        end = to_date.year*100+to_date.month
    else:
        to_date = datetime.strptime(to_date, format)
        end = int(to_date.strftime('%Y%m'))

    if start > end:
        return ValueError.message("from_date cannot be bigger them to_date")

    l = []
    while start <= end:
        l.append(datetime(year,month,01).date().strftime(format))
        month += 1
        if month == 13:
            year += 1
            month = 1
        start = year * 100 + month

    return l
