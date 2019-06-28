import csv
import re
from textblob import TextBlob
import time
import numpy


def clean(comment):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", comment).split())


def analyze(file_loc, write_loc, first, postyear):
    if first:
        with open(write_loc, 'a') as file:
            file.write("month,year,sentiment,polarity_score,comment_score\n")
        file.close()

    with open(file_loc) as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                analysis = TextBlob(clean(row['body']))
                month = time.strftime('%m', time.localtime(int(row['created_utc'])))
                year = time.strftime('%Y', time.localtime(int(row['created_utc'])))

                if analysis.sentiment.polarity > 0:
                    val = (month + "," + year + ',positive,' + str(analysis.sentiment.polarity) + "," + row['score'] + "," + "\n")
                elif analysis.sentiment.polarity == 0:
                    val = (month + "," + year + ',neutral,' + str(analysis.sentiment.polarity) + "," + row['score'] + "," + "\n")
                else:
                    val = (month + "," + year + ',negative,' + str(analysis.sentiment.polarity) + "," + row['score'] + "," + "\n")

                with open(write_loc, 'a') as file:
                    file.write(val)
                file.close()
        except UnicodeDecodeError:
            print("Unicode failure.")
    csvfile.close()


def main():
    file_loc_main = "REPLACE WITH FILE PATH HERE"
    write_loc_main = "REPLACE WITH FILE PATH HERE"

    republican_years = ["2010", "2011", "2012", "2013", "2014"]
    democrat_years = ["2011", "2012", "2013", "2014"]
    politics_years = ["2008", "2009", "2010", "2011", "2012", "2013", "2014"]

    directories = {"obama-democrats/": democrat_years, "obama-politics/": politics_years,
                   "obama-republicans/": republican_years}


    for element in directories:
        file_extension = element
        years = directories[element]
        file_loc = file_loc_main + file_extension + "/"
        first = True

        for year in years:
            file_loc = file_loc + year + ".csv"

            write_loc = write_loc_main + file_extension + "output.csv"
            analyze(file_loc, write_loc, first, year)

            file_loc = file_loc_main + file_extension + "/"
            first = False


if __name__ == '__main__':
    main()
