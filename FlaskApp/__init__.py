from flask import Flask, redirect, url_for, render_template, request, send_file
from uszipcode import SearchEngine
import pandas as pd # Used for data manipulation
#import matplotlib.pyplot as plt #used to plot our data
import numpy as np # used for math operations
from datetime import datetime, timedelta
from pydataset import data
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import csv
import codecs
import requests
import sys
from csv import writer
from csv import reader
import schedule
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
csv.field_size_limit(sys.maxsize)
app = Flask(__name__)
us_state_abbrev = {
'Alabama': 'AL',
'Alaska': 'AK',
'American Samoa': 'AS',
'Arizona': 'AZ',
'Arkansas': 'AR',
'California': 'CA',
'Colorado': 'CO',
'Connecticut': 'CT',
'Delaware': 'DE',
'District of Columbia': 'DC',
'Florida': 'FL',
'Georgia': 'GA',
'Guam': 'GU',
'Hawaii': 'HI',
'Idaho': 'ID',
'Illinois': 'IL',
'Indiana': 'IN',
'Iowa': 'IA',
'Kansas': 'KS',
'Kentucky': 'KY',
'Louisiana': 'LA',
'Maine': 'ME',
'Maryland': 'MD',
'Massachusetts': 'MA',
'Michigan': 'MI',
'Minnesota': 'MN',
'Mississippi': 'MS',
'Missouri': 'MO',
'Montana': 'MT',
'Nebraska': 'NE',
'Nevada': 'NV',
'New Hampshire': 'NH',
'New Jersey': 'NJ',
'New Mexico': 'NM',
'New York': 'NY',
'North Carolina': 'NC',
'North Dakota': 'ND',
'Northern Mariana Islands':'MP',
'Ohio': 'OH',
'Oklahoma': 'OK',
'Oregon': 'OR',
'Pennsylvania': 'PA',
'Puerto Rico': 'PR',
'Rhode Island': 'RI',
'South Carolina': 'SC',
'South Dakota': 'SD',
'Tennessee': 'TN',
'Texas': 'TX',
'Utah': 'UT',
'Vermont': 'VT',
'Virgin Islands': 'VI',
'Virginia': 'VA',
'Washington': 'WA',
'West Virginia': 'WV',
'Wisconsin': 'WI',
'Wyoming': 'WY'
}


def scrapeData():

    URL = "https://github.com/nytimes/covid-19-data/blob/master/live/us-counties.csv"
    results = requests.get(URL) #get the URL we want

    #print("SYSTEM CHECK: ")
    #print(results.status_code)



    src = results.content #sets the content of the URL to a var called src (source)
    soup = BeautifulSoup(src, 'lxml')

    now = datetime.now()
    earlier = now - timedelta(days=1)
    todayDate = now.strftime("%m-%d-%Y")
    yesterdayDate = earlier.strftime("%m-%d-%Y")

    #
    #filename1 = todayDate + ".csv"
    filename1 = "/var/www/FlaskApp/FlaskApp/cases.csv"
    #filename1 = "01-18-2021.csv"
    filename2 = yesterdayDate + ".csv"


    f= open(filename1, 'a')

    #headers = 'Date, County, State, Cases \n'
     #f.write(headers)


    i = 0
    x = 0
    # Open the input_file in read mode and output_file in write mode
    with open(filename1, 'r',buffering=-1, encoding = 'utf8', errors = None, newline = None, closefd = True) as read_obj, \
            open('/var/www/FlaskApp/FlaskApp/output_1.csv', 'w', buffering=-1, encoding = 'utf8', errors = None,  newline='', closefd = True) as write_obj:
        # Create a csv.reader object from the input file object
        csv_reader = reader(read_obj)
        # Create a csv.writer object from the output file object
        csv_writer = writer(write_obj)
        # Read each row of the input csv file as list
        for row in csv_reader:
            if todayDate not in row:
                 csv_writer.writerow(row)

    x = 0
    i = 0
    read_obj.close
    write_obj.close



    with open('/var/www/FlaskApp/FlaskApp/output_1.csv', 'r',buffering=-1, encoding = 'utf8', errors = None, newline = None, closefd = True) as read_obj1, \
            open(filename1, 'w', buffering=-1, encoding = 'utf8', errors = None,  newline='', closefd = True) as write_obj1:
            csv_reader1 = reader(read_obj1)
            csv_writer1 = writer(write_obj1)
            for row in enumerate(csv_reader1):
            # Add the updated row / list to the output file
                csv_writer1.writerow(row)


    for tr_tag in soup.find_all('tr', class_="js-file-line"):
        td_tag = tr_tag.find_all('td')

        if(len(td_tag) != 1):
            county = ((td_tag[2]).text)
            state = ((td_tag[3]).text)
            totalCases = ((td_tag[5]).text)
            f.write((todayDate + ',' + county + ',' + state + ',' +  '1,' + totalCases + ',1' + "\n").encode())
    print("Scraped")

#sched = BackgroundScheduler(daemon=True)
#sched.add_job(scrapeData,'interval',minutes=1)
#sched.start()


def findPopulation(state, county):
    f = codecs.open("/var/www/FlaskApp/FlaskApp/Population Estimates 2010-19-Table 1 2.csv", 'r', 'utf8')
    for rows in f:
        if state in rows and county in rows:
            holder = rows.split("\"", 2)[1]
            holder = holder.replace(',', '', 3)
            return(holder)

def Next5Days():
    day = datetime.today().weekday()

    daysToPrint = 5
    day = day + 1
    next_5_days = []

    days_of_week=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    while daysToPrint > 0:
        if day == 7:
            day = 0
        next_5_days.append(days_of_week[day])
        day = day + 1
        daysToPrint = daysToPrint - 1

    return(next_5_days)


def previous5days():
    day = datetime.today().weekday()

    daysToPrint = 5
    day = day - 1
    last_5_days = []

    days_of_week=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    while daysToPrint > 0:
        if day == -1:
            day = 6
        last_5_days.append(days_of_week[day])
        day = day -1
        daysToPrint = daysToPrint - 1

    # next_5_days = "  ".join(map(str, next_5_days))
    return(last_5_days)

def TodaysCases(county, state):
    f= codecs.open("/var/www/FlaskApp/FlaskApp/cases.csv", 'r', 'utf8')
    date = 1
    cases = []
    for names in f:
        if county in names and state in names:
            datastring = names
            case = datastring.split(",",5)[4]
            date = date + 1
            cases.append(case)
    f.close()
    todayscases = cases[-1]
    return(todayscases)

def Last5Days(county, state):
    f= codecs.open("/var/www/FlaskApp/FlaskApp/cases.csv", 'r', 'utf8')
    date = 1
    cases = []
    last5 = []
    for names in f:
        if county in names and state in names:
            datastring = names
            case = datastring.split(",",5)[4]
            date = date + 1
            cases.append(case)
    f.close()
    todayscases = cases[-1]
    last5 = [cases[-2], cases[-3], cases[-4], cases[-5], cases[-6]]
    print(last5)
    #flat_list = [item for sublist in last5 for item in sublist]
    #last5 = " ".join(map(str, last5))
    return(last5)

def PredictionLR(county, state, population):
    filename1 = "/var/www/FlaskApp/FlaskApp/LinearRegression.csv"
    f= codecs.open("/var/www/FlaskApp/FlaskApp/cases.csv", 'r', 'utf8')
    f2= codecs.open(filename1, 'w', 'utf8')
    f2.write("Dates,Cases\n")
    date = 1
    stopper = 1
    cases = []
    for names in f:
        if county in names and state in names:

            datastring = names
            case = datastring.split(",",5)[4]
            f2.write(str(date) + ',' + case + '\n')
            date = date + 1
            cases.append(case)
            stopper = stopper + 1

    f.close()
    f2.close()
    data = pd.read_csv('/var/www/FlaskApp/FlaskApp/LinearRegression.csv')

    next_5_days = []
    counter = 0
    casesplus = []
    while counter < 5:
        X_train, X_test, y_train, y_test = train_test_split(data.Dates, data.Cases)
        LR = LinearRegression()
        LR.fit(X_train.values.reshape(-1,1), y_train.values)
        predictions = LR.predict(X_test.values.reshape(-1,1))
                next_5_days.append(np.rint(LR.predict(np.array([[date + counter]]))))
        counter = counter + 1
    counter = 4
    while counter >= 0:
        if counter == 0:
            holding = round( ((int(next_5_days[counter]) - int(cases[-1]))/ int(population)*100), 2)
            if holding < 0:
                holding = 0
                casesplus.append(holding)
            else:
                casesplus.append(holding)
        else:
            holding = round(((int(next_5_days[counter]) - int(next_5_days[counter - 1])) / int(population)*100), 2)
            if holding < 0:
                holding = 0
                casesplus.append(holding)
            else:
                casesplus.append(holding)
        counter = counter - 1
    flat_list = [item for sublist in next_5_days for item in sublist]
    next_5_days= flat_list
    return next_5_days, casesplus

abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["name"]
        #We need zip, county name, cases next week, cases today
        search = SearchEngine(simple_zipcode=True) # set simple_zipcode=False to use rich info database
        zipcode = search.by_zipcode(user)
        searchedZipCode = zipcode.county
        strippedCounty = searchedZipCode.split(' County', 1)[0] #Strips the word 'County' off of the county we got from uszipcode
        #strippedCounty = strippedCounty.replace(" County", ',',1)
        population = findPopulation(zipcode.state, strippedCounty)
        strippedCounty2 = strippedCounty +','
        res, casePercent = PredictionLR(strippedCounty2, abbrev_us_state[zipcode.state], population)
        todayscases = TodaysCases(strippedCounty2, abbrev_us_state[zipcode.state])
        last5 = Last5Days(strippedCounty2, abbrev_us_state[zipcode.state])
        nextdays = Next5Days()
        last = previous5days()
        return render_template("Zipcode.html", var1 = user, var2 = strippedCounty, var3 = res, var4 = todayscases, var6 = last5, var7 = casePercent, var8 = last5[0] + ".0", var9 = last5[1]+ ".0", var10 = last5[2]+ ".0", var11 = last5[3]+ ".0", var12 = last5[4]+ ".0", var13 = nextdays[0],var14 = nextdays[1],var15 = nextdays[2],var16 = nextdays[3],var17 = nextdays[4], var18 = res[0], var19 = res[1], var20 = res[2], var21 = res[3], var22 = res[4], var23 = last[0], var24 = last[1], var25 = last[2], var26 = last[3], var27 = last[4], var28 = casePercent[0],var29 = casePercent[1],var30 = casePercent[2],var31 = casePercent[3],var32 = casePercent[4])
    else:
        return render_template("index.html")

@app.route("/home", methods=["POST", "GET"])
def goHome():
    return render_template("index.html")

@app.route("/Contact", methods=["POST", "GET"])
def goContactUS():
    return render_template("Contact-Us.html")


@app.route("/FAQ", methods=["POST", "GET"])
def goFAQ():
    return render_template("FAQ.html")

@app.route('/download')
def download_file():
    p = "Justin_Rapczynski_Resume -2.pdf"
    return send_file(p,as_attachment=True)

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)