# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


# Code has been written to create a database using sqlite3 package

class ScrapingindeedPipeline:
    # Initializing the connection and creating the database
    def __init__(self):
        self.create_connection()
        self.create_table()

    # Code written to create connection to the database
    def create_connection(self):
        self.connection = sqlite3.connect('INDEED_JOBS.db')  # Database file
        self.cur = self.connection.cursor()

    # Code written to drop table first if existed and creating again to avoid overriding of data in database
    def create_table(self):
        self.cur.execute("""DROP TABLE IF EXISTS INDEED_JOBS""")  # Correct table name
        self.cur.execute("""CREATE TABLE INDEED_JOBS(
            Company TEXT,
            CompanyRating TEXT,
            CompanyReviewCount TEXT,
            JobTitle TEXT,
            JobLocation TEXT,
            MaxSalary REAL,
            MinSalary REAL,
            Currency TEXT,
            SalaryType TEXT,
            WorkModel TEXT
        )""")

    # Code written to store values extracted by scrapy crawler into the database
    def store_db(self, item):
        self.cur.execute("""INSERT INTO INDEED_JOBS
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
            item.get("Company", ""),
            item.get("CompanyRating", ""),
            item.get("CompanyReviewCount", ""),
            item.get("JobTitle", ""),
            item.get("JobLocation", ""),
            item.get("MaxSalary", ""),
            item.get("MinSalary", ""),
            item.get("Currency", ""),
            item.get("SalaryType", ""),
            item.get("WorkModel", "")
        ))
        self.connection.commit()

    # Code written to call the store_db function
    def process_item(self, item, spider):
        self.store_db(item)
        return item

    # Code written to close the connection when all the data has been scraped
    def close_spider(self, spider):
        self.connection.close()
