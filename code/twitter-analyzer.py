import csv
import re
from textblob import TextBlob
import numpy as np


def clean(comment):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", comment).split())


def analyze(file_loc, write_loc):
    results = list()
    x = 0
    with open(write_loc, 'a') as file:
        file.write("date,sentiment,polarity_score\n")
    file.close()

    with open(file_loc, encoding='latin-1') as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                x += 1
                tweet = row['tweet']

                if "obama" in tweet.lower():
                    analysis = TextBlob(tweet)
                else:
                    continue
                date = row['date'].split(" ")[1] + " " + row['date'].split(" ")[2] + " " + row['date'].split(" ")[5]
                if analysis.sentiment.polarity > 0:
                    results.append(date + ',positive,' + str(analysis.sentiment.polarity) + "\n")
                elif analysis.sentiment.polarity == 0:
                    results.append(date + ',neutral,' + str(analysis.sentiment.polarity) + "\n")
                else:
                    results.append(date + ',negative,' + str(analysis.sentiment.polarity) + "\n")
                if x % 100 == 0:
                    print(str(x) + " lines analyzed.")
                    with open(write_loc, 'a') as file:
                        for element in results:
                            file.write(element)
                    file.close()
                    results = list()
        except UnicodeDecodeError:
            print(str(x) + " is location of failure.")
    csvfile.close()


def daily_analysis(file_loc, write_loc):
    dates_and_sentiment = {}
    with open(file_loc, encoding='latin-1') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if str(row['date']) not in dates_and_sentiment:
                dates_and_sentiment[str(row['date'])] = list()
            dates_and_sentiment[str(row['date'])].append(row['polarity_score'])
    csvfile.close()

    #print(str(dates_and_sentiment))

    with open(write_loc, 'a') as file:
        file.write("date,average polarity score\n")
        for key in dates_and_sentiment:
            averages = np.array(dates_and_sentiment[key]).astype(np.float)
            avg = np.average(averages)
            #print((key + "," + str(avg) + "\n"))
            file.write(key + "," + str(avg) + "\n")
    file.close()

    #print(str(dates_and_sentiment))


def monthly_analysis(read_loc):
    apr_1 = list()
    apr_2 = list()
    apr_3 = list()
    apr_4 = list()
    may_1 = list()
    may_2 = list()
    may_3 = list()
    may_4 = list()
    jun_1 = list()
    jun_2 = list()
    jun_3 = list()
    jun_4 = list()

    with open(read_loc) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = row['date']
            month = date.split(" ")[0]
            day = int(date.split(" ")[1])
            polarity_score = float(row['polarity_score'])

            if month == "Apr":
                if day < 8:
                    apr_1.append(polarity_score)
                if day < 15:
                    apr_2.append(polarity_score)
                if day < 22:
                    apr_3.append(polarity_score)
                else:
                    apr_4.append(polarity_score)
            if month == "May":
                if day < 8:
                    may_1.append(polarity_score)
                if day < 15:
                    may_2.append(polarity_score)
                if day < 22:
                    may_3.append(polarity_score)
                else:
                    may_4.append(polarity_score)
            else: # June
                if day < 8:
                    jun_1.append(polarity_score)
                if day < 15:
                    jun_2.append(polarity_score)
                if day < 22:
                    jun_3.append(polarity_score)
                else:
                    jun_4.append(polarity_score)

    dates = ["apr_1", "apr_2", "apr_3", "apr_4", "may_1", "may_2", "may_3", "may_4", "jun_1", "jun_2", "jun_3", "jun_4"]
    dates_arr = [apr_1, apr_2, apr_3, apr_4, may_1, may_2, may_3, may_4, jun_1, jun_2, jun_3, jun_4, ]
    week_and_sentiment = dict()

    for x in range(len(dates)):
        if len(dates_arr[x]) == 0:
            week_and_sentiment[dates[x]] = "no-data"
        else:
            week_and_sentiment[dates[x]] = sum(dates_arr[x]) / len(dates_arr[x])

    for element in week_and_sentiment:
        print(str(element) + " : " + str(week_and_sentiment[element]))


def main():
    file_loc = "REPLACE WITH FILE PATH"
    write_loc = "REPLACE WITH FILE PATH"
    analyze(file_loc, write_loc)

    # write_loc = "REPLACE WITH FILE PATH"
    # daily_analysis(file_loc, write_loc)
    # monthly_analysis(write_loc)

if __name__ == '__main__':
    main()

