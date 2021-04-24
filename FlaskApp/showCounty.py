import requests
import sys
from uszipcode import SearchEngine
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from csv import writer
from csv import reader
#This below Code shows us the county for the zipcode we will search
#####################################################################################################################################

search = SearchEngine(simple_zipcode=True) # set simple_zipcode=False to use rich info database
zipcode = search.by_zipcode("76201")
searchedZipCode = zipcode.county
strippedCounty = searchedZipCode.split(' ', 1)[0] #Strips the word 'County' off of the county we got from uszipcode
print(strippedCounty)