#!/usr/bin/env python3
import datetime, os, sqlite3

from finlab.crawler import (
    update_table, 
    crawl_price, 
    crawl_monthly_report, 
    crawl_finance_statement_by_date,
    date_range, month_range, season_range
)
import finlab.crawler as cr


"""
Connect to db
"""
if not os.path.exists("./data"):
    os.makedirs("./data")
conn = sqlite3.connect(os.path.join('data', "data.db"))


"""
Set ranges of date
"""
rangeBegin = datetime.date(2015,1,1)
rangeEnd = datetime.date.today()
dateRange = date_range(datetime.date(2015,1,1), datetime.date.today())
monthRange = month_range(datetime.date(2015,1,1), datetime.date.today())
seasonRange = season_range(datetime.date(2015,1,1), datetime.date.today())
print("Initialize date range: from {} to {}".format(rangeBegin.strftime('%Y/%m/%d'), rangeEnd.strftime('%Y/%m/%d')))
print("=========================================================")

"""
Start to download
"""
#update_table(conn, 'price', crawl_price, dateRange)
#print("\"date\" is downloaded.")
#
#update_table(conn, 'monthly_revenue', crawl_monthly_report, monthRange)
#print("\"monthly_revenue\" is downloaded.")

FinStmtTableName = 'finance_statement'
if table_exist(conn, FinStmtTableName):
    tableBegin = table_earliest_date(conn, FinStmtTableName)
    tableEnd = table_latest_date(conn, FinStmtTableName)
    if rangeBegin < tableBegin:
        '''
        Download twice
        '''
        seasonRange = season_range(datetime.date(rangeBegin, tableBegin)
        print("\n(2 step downloading...")
        print("{} table exists, filling up the data for missing date from {} to {}.".format( \
                FinStmtTableName, rangeBegin, tableBegin))
        update_table(conn, FinStmtTableName, crawl_finance_statement_by_date, seasonRange)
    # if table exists, only download from the end of table.
    rangeBegin = tableEnd
    rangeEnd = datetime.date.today()
    seasonRange = season_range(rangeBegin, rangeEnd)

print("Downloading {} from {} to {}".format(FinStmtTableName, \
    rangeBegin.strftime('%Y/%m/%d'), rangeEnd.strftime('%Y/%m/%d')))
update_table(conn, FinStmtTableName, crawl_finance_statement_by_date, seasonRange)
print("\"finance_statement\" is downloaded.")

print("Congratulations!! All of the financial data updated.")
