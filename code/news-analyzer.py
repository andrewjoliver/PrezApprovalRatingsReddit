import csv
import re
from textblob import TextBlob
from datetime import datetime
import numpy as np
import math


def clean(comment):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", comment).split())


def analyze(file_loc, write_loc):
    results = list()
    x = 0
    with open(write_loc, 'a') as file:
        file.write("date,sentiment,polarity_score,num_likes,num_comments,num_shares\n")
    file.close()

    with open(file_loc) as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                x += 1
                content = clean(row['name'] + " " + row['message'] + " " + row['description']).lower()
                if "obama" not in content:
                    continue
                analysis = TextBlob(content)
                date = datetime.strptime(row['posted_at'].split("T")[0], '%Y-%m-%d')
                date = datetime.strftime(date, '%b %Y')
                if analysis.sentiment.polarity > 0:
                    results.append(date + ',positive,' + str(analysis.sentiment.polarity) + "," + row['likes_count'] + "," + row['comments_count'] + "," + row['shares_count'] + "\n")
                elif analysis.sentiment.polarity == 0:
                    results.append(date + ',neutral,' + str(analysis.sentiment.polarity) + "," + row['likes_count'] + "," + row['comments_count'] + "," + row['shares_count'] + "\n")
                else:
                    results.append(date + ',negative,' + str(analysis.sentiment.polarity) + "," + row['likes_count'] + "," + row['comments_count'] + "," + row['shares_count'] + "\n")
                if x % 1 == 0:
                    print(str(x) + " lines analyzed.")
                    with open(write_loc, 'a') as file:
                        for result in results:
                            file.write(result)
                        results = list()
                    file.close()
        except UnicodeDecodeError:
            print(str(x) + " is location of failure.")
    csvfile.close()


def monthly_analysis(file_loc, write_loc):
    dates_and_sentiment = {}
    with open(file_loc) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if str(row['date']) not in dates_and_sentiment:
                dates_and_sentiment[str(row['date'])] = list()
            dates_and_sentiment[str(row['date'])].append(row['polarity_score'])
    csvfile.close()

    with open(write_loc, 'a') as file:
        file.write("date,average polarity score\n")
        for key in dates_and_sentiment:
            averages = np.array(dates_and_sentiment[key]).astype(np.float)
            avg = np.average(averages)
            # print((key + "," + str(avg) + "\n"))
            file.write(key + "," + str(avg) + "\n")
    file.close()

    # print(str(dates_and_sentiment))


def weighting(file_loc):
    likes = list()
    shares = list()
    first_row = True
    with open(file_loc) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if first_row:
                first_row = False
                continue
            likes.append(int(row['num_likes']))
            shares.append(int(row['num_shares']))
    csvfile.close()

    likes_avg = round(float(np.median(likes)))
    shares_avg = round(float(np.median(shares)))

    likes_over_shares = round(likes_avg / shares_avg)
    return likes_over_shares, likes_avg, shares_avg

    # print("Likes: " + str(likes_avg) + " | Shares: " + str(shares_avg) + " multiple: " + str(likes_over_shares))


def monthly_weighted_analysis(file_loc, write_loc, likes_avg, shares_avg, shares_weight):
    dates_and_sentiment = {}
    with open(file_loc) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if str(row['date']) not in dates_and_sentiment:
                dates_and_sentiment[str(row['date'])] = list()

            likes_curr = int(row['num_likes'])
            likes_weight = 0
            if likes_curr > likes_avg:
                likes_weight = likes_curr / likes_avg

            shares_curr = int(row['num_shares'])
            shares_weight = 0
            if shares_curr > shares_avg:
                shares_weight = shares_curr / shares_avg * shares_weight

            final_weight = 1 + round(likes_weight + shares_weight)
            for x in range(final_weight):
                dates_and_sentiment[str(row['date'])].append(row['polarity_score'])
    csvfile.close()

    with open(write_loc, 'a') as file:
        file.write("date,average polarity score\n")
        for key in dates_and_sentiment:
            averages = np.array(dates_and_sentiment[key]).astype(np.float)
            avg = np.average(averages)
            # print((key + "," + str(avg) + "\n"))
            file.write(key + "," + str(avg) + "\n")
    file.close()


def main():
    file_loc_base = "REPLACE WITH YOUR DIRECTORY PATH HERE"
    file_loc_end = ["abc", "bbc", "cbs", "cnn", "fox", "fox_and_friends", "la_times", "nbc", "npr"]

    for file_loc_element in file_loc_end:
        file_loc = file_loc_base + "/" + file_loc_element + "/" + file_loc_element + ".csv"
        write_loc = file_loc_base + "/" + file_loc_element + "/output.csv"
        # file_loc = write_loc
        # write_loc = file_loc_base + "/" + file_loc_element + "/monthly-weighted-output.csv"

        analyze(file_loc, write_loc)
        monthly_analysis(file_loc, write_loc)
        print("-------------------------------------")
        print(file_loc_element)
        # shares_weights, likes_avg, shares_avg = weighting(file_loc)
        # monthly_weighted_analysis(file_loc, write_loc, likes_avg, shares_avg, shares_weights)


if __name__ == '__main__':
    main()

