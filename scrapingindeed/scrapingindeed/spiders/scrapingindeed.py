import re
import json
from typing import Any
import scrapy
from requests import Response

from ..items import ScrapingindeedItem
import numpy as np


class IndeedScraping(scrapy.Spider):
    name = "indeedscraper"
    next_page_number = 10
    start_urls = [
        'https://ie.indeed.com/jobs?q=python&l=Dublin&start=0'
    ]

    def parse(self, response: Response, **kwargs: Any):

        items = ScrapingindeedItem()
        script_tag = re.findall(
            r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});',
            response.text)
        json_blob = json.loads(script_tag[0])
        jobs_list = json_blob["metaData"]['mosaicProviderJobCardsModel']['results']

        print(type(jobs_list))
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

                if job.get('salarySnippet') is None:
                    Currency = 0
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

                if job.get("hiringMultipleCandidatesModel") is None:
                    HiringCandidates = 'Not Disclosed'
                else:
                    HiringCandidates = job.get("hiringMultipleCandidatesModel").get("hiresNeededExact")

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
                items["HiringCandidates"] = HiringCandidates
                yield items

        next_page = f"https://ie.indeed.com/jobs?q=python&l=Dublin&start={str(self.next_page_number)}"

        if IndeedScraping.next_page_number < 310:
            IndeedScraping.next_page_number += 10
            yield response.follow(next_page, callback=self.parse)
