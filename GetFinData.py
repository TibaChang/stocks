#!/usr/bin/env python3
import datetime, os, sqlite3

from finlab.crawler import (
    update_table, 
    crawl_price, 
    crawl_monthly_report, 
    crawl_finance_statement_by_date,
    date_range, month_range, season_range
)


"""
Connect to db
"""
if not os.path.exists("./data"):
    os.makedirs("./data")
conn = sqlite3.connect(os.path.join('data', "data.db"))


"""
Set ranges of date
"""
rangeBegin = datetime.date(2014,1,1)
rangeEnd = datetime.date.today()
dateRange = date_range(datetime.date(2014,1,1), datetime.date.today())
monthRange = month_range(datetime.date(2014,1,1), datetime.date.today())
seasonRange = season_range(datetime.date(2014,1,1), datetime.date.today())
print("Initialize date range: from {} to {}".format(rangeBegin.strftime('%Y/%m/%d'), rangeEnd.strftime('%Y/%m/%d')))
print("=========================================================")

"""
Start to download
"""
update_table(conn, 'price', crawl_price, dateRange)
print("\"date\" is downloaded.")

update_table(conn, 'monthly_revenue', crawl_monthly_report, monthRange)
print("\"monthly_revenue\" is downloaded.")

update_table(conn, 'finance_statement', crawl_finance_statement_by_date, seasonRange)
print("\"finance_statement\" is downloaded.")

print("Congratulations!! All of the financial data updated.")
