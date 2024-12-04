# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class ScrapingindeedPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.connection = sqlite3.connect('INDEED_JOBS.db')  # Database file
        self.cur = self.connection.cursor()

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
            WorkModel TEXT,
            HiringCandidates TEXT
        )""")

    def store_db(self, item):
        self.cur.execute("""INSERT INTO INDEED_JOBS
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
            item.get("Company", ""),
            item.get("CompanyRating", ""),
            item.get("CompanyReviewCount", ""),
            item.get("JobTitle", ""),
            item.get("JobLocation", ""),
            item.get("MaxSalary", ""),
            item.get("MinSalary", ""),
            item.get("Currency", ""),
            item.get("SalaryType", ""),
            item.get("WorkModel", ""),
            item.get("HiringCandidates", "")
        ))
        self.connection.commit()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def close_spider(self, spider):
        self.connection.close()
