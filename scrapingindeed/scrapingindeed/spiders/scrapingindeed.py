# importing required libraries
import re  # The `re` library handles pattern-matching and text manipulation.
import json  # The `json` library handles encoding/decoding JSON data in Python.
from typing import Any
import scrapy  # The 'scrapy' library used to scrape website
from requests import Response  # `Response` from `requests` handles HTTP responses from web server requests.
from ..items import ScrapingindeedItem  # importing the 'ScrapingindeedItem' class from items.py file


# Code written to create a class for scraping indeed website
class IndeedScraping(scrapy.Spider):
    name = "indeedscraper"  # Name of the scrapy spider
    next_page_number = 10  # Varaiable used for pagination
    start_urls = [
        'https://ie.indeed.com/jobs?q=java+developer&l=Dublin%2C+County+Dublin&start=0'
    ]  # start_urls store the staring url for scraping

    # code has been written to create a method to parse the website and scrape the data
    def parse(self, response: Response, **kwargs: Any):
        # Initializing the ScrapyindeedItem class
        items = ScrapingindeedItem()

        # Extracts JSON-like data from specific JavaScript in HTML response.
        script_tag = re.findall(
            r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});',
            response.text)
        # Converts the first extracted JSON string into a Python dictionary.
        json_blob = json.loads(script_tag[0])

        # navigating to the results where the job data to be scraped is present
        jobs_list = json_blob["metaData"]['mosaicProviderJobCardsModel']['results']

        # code written to extract the required data form job_list
        for index, job in enumerate(jobs_list):
            if job.get('jobkey') is not None:
                Company = job.get('company')
                CompanyRating = job.get('companyRating')
                CompanyReviewCount = job.get('companyReviewCount')
                jobTitle = job.get('displayTitle')
                JobLocation = job.get('formattedLocation')

                if job.get('extractedSalary') is None:
                    MaxSalary = 0
                else:
                    MaxSalary = job.get('extractedSalary').get('max')

                if job.get('extractedSalary') is None:
                    MinSalary = 0
                else:
                    MinSalary = job.get('extractedSalary').get('min')

                if job.get('salarySnippet'):
                    Currency = "EUR"
                else:
                    Currency = job.get('salarySnippet').get('currency')

                if job.get('extractedSalary') is None:
                    SalaryType = 'Not Disclosed'
                else:
                    SalaryType = job.get('extractedSalary').get('type')

                if job.get('remoteWorkModel') is None:
                    WorkModel = 'Not Disclosed'
                else:
                    WorkModel = job.get('remoteWorkModel').get('text')

                items["Company"] = Company
                items["CompanyRating"] = CompanyRating
                items["CompanyReviewCount"] = CompanyReviewCount
                items["JobTitle"] = jobTitle
                items["JobLocation"] = JobLocation
                items["MaxSalary"] = float(MaxSalary)
                items["MinSalary"] = float(MinSalary)
                items["Currency"] = Currency
                items["SalaryType"] = SalaryType
                items["WorkModel"] = WorkModel

                yield items

        # Below code is written for pagination
        next_page = f"https://ie.indeed.com/jobs?q=java+developer&l=Dublin%2C+County+Dublin&start={str(self.next_page_number)}"

        if IndeedScraping.next_page_number < 210:
            IndeedScraping.next_page_number += 10
            yield response.follow(next_page, callback=self.parse)
