from scraper import scrapeSalary
import pandas as pd

salaryDF = scrapeSalary();
print(salaryDF.head(5))
