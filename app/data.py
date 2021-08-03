from datetime import datetime
import pandas as pd
import pytz
import sys
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# function to convert timezone from UTC to EST
def convertTimezone(x):
    fmt = '%Y-%m-%d %H:%M:%S'
    utc = pytz.timezone('UTC')
    est = pytz.timezone('US/Eastern')
    x = pytz.utc.localize(datetime.strptime(x.split('.')[0], fmt)).astimezone(est).strftime(fmt)
    return x

def getDate(x):
    return x.split(" ")[0]

# function to process the input file and write an output file in the requried format
def processFile(fileName):
    # read csvfile using pandas library
    print("Reading input file from samplecsv folder: " + fileName)
    df = pd.read_csv("samplecsv/{}".format(fileName),warn_bad_lines=True,error_bad_lines=False)

    print("processing input file")
    # replaces blank data in the ppcs column with 0.00
    df['PPC'].fillna(0.00, inplace=True)

    # replace all other empty columns with NULL
    df = df.fillna("NULL")

    # convert the click_date from UTC to Eastern Time Zone
    df['CLICK_DATE'] = df.CLICK_DATE.apply(convertTimezone)

    # create a new column with date only, also converted to Eastern Time Zone.
    df['DATE'] = df['CLICK_DATE']
    df['DATE'] = df.DATE.apply(getDate)

    # transforms the browser vendor, name, and version columns into one column into the format "BROWSER_VERSION
    # BROWSER_NAME - VERSION"
    df.insert(5, 'BROWSER_VENDOR BROWSER_NAME - VERSION', df["BROWSER_VENDOR"])
    df["BROWSER_VENDOR BROWSER_NAME - VERSION"] = df['BROWSER_VENDOR'] + " " + df['BROWSER_NAME'] + "-" + df[
        'BROWSER_VERSION'].astype(str)
    df.drop(['BROWSER_VENDOR', 'BROWSER_NAME', 'BROWSER_VERSION'], inplace=True, axis=1)

    outputFileName = fileName.replace('sample-data', 'result').replace('csv', 'psv')

    # export the output in pipe delimited format   
    df.to_csv('results/{}'.format(outputFileName), index=False, sep="|")

    print("Created output file in results folder: " + outputFileName)

# Defining main function
def main():
    fileName = sys.argv[1]
    if (os.path.isfile("samplecsv/{}".format(fileName))== False):
        print("File not Found")
        exit()
    else:
        processFile(fileName)

if __name__=="__main__":
    main()
