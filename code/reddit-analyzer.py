import csv
import re
from textblob import TextBlob
import time
import numpy

def clean(comment):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", comment).split())


def analyze(file_loc, write_loc, first):

    if first:
        with open(write_loc, 'a') as file:
            file.write("date,sentiment,polarity_score,comment_score\n")
        file.close()

    with open(file_loc) as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                analysis = TextBlob(clean(row['body']))
                date = time.strftime('%m-%Y', time.localtime(int(row['created_utc'])))
                
                if analysis.sentiment.polarity > 0:
                    val = (date + ',positive,' + str(analysis.sentiment.polarity) + "," + row['score'] + "," + "\n")
                elif analysis.sentiment.polarity == 0:
                    val = (date + ',neutral,' + str(analysis.sentiment.polarity) + "," + row['score'] + "," + "\n")
                else:
                    val = (date + ',negative,' + str(analysis.sentiment.polarity) + "," + row['score'] + "," + "\n")
                with open(write_loc, 'a') as file:
                    file.write(val)
                file.close()
        except UnicodeDecodeError:
            print("Unicode failure.")
    csvfile.close()


def monthly_rating(file_loc, write_loc, year, dates):

    res = dict()
    for date in dates:
        res[date] = list()

    for date in dates:
        [list() for y in range(len(dates))]
        with open(file_loc) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                loc = str(row['date'])
                if loc == date:
                    for y in range(int(row['comment_score'])):
                        res[date].append(float(row['polarity_score']))

    # for key in res:
        # print(str(key) + " : " + str(res[key]))
    calc_avg(res, write_loc)


def calc_avg(vals, write_loc):
    for key in vals:
        curr = numpy.asarray(vals[key])
        avg_score = numpy.average(curr)
        # print(str(key) + " : " + str(avg_score))

        with open(write_loc, 'a') as file:
            file.write(str(key) + "," + str(avg_score) + "\n")

def main():
    file_loc_main = "REAPLCE WITH FILE PATH/"
    write_loc_main = "REAPLCE WITH FILE PATH"

    republican_years = ["2010", "2011", "2012", "2013", "2014"]
    democrat_years = ["2011", "2012", "2013", "2014"]
    politics_years = ["2008", "2009", "2010", "2011", "2012", "2013", "2014"]

    months = ["01-", "02-", "03-", "04-", "05-", "06-", "07-", "08-", "09-", "10-", "11-", "12-"]

    directories = {"obama-democrats/": democrat_years, "obama-politics/": politics_years, "obama-republicans/": republican_years}

    for element in directories:
        file_extension = element
        years = directories[element]
        file_loc = file_loc_main + file_extension + "/"
        first = True

        for year in years:
            file_loc = file_loc + year + ".csv"

            write_loc = write_loc_main + file_extension + "output.csv"
            analyze(file_loc, write_loc, first)

            # file_loc = write_loc
            # write_loc = write_loc_main + file_extension + "monthly-results.csv"
            # dates = list()
            # for month in months:
            #     for year in years:
            #         dates.append(month + year)
            # monthly_rating(file_loc, write_loc, year, dates)
            #
            # file_loc = file_loc_main + file_extension + "/"
            # first = False


if __name__ == '__main__':
    main()

