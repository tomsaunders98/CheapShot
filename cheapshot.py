import requests, datafilter, twint, pandas as pd, sys, argparse, os


def checktoxic(tweets):
    # clean data
    cleandata = []
    url = 'http://localhost:5000/model/predict'
    tweetlist = tweets["tweet"].tolist()
    print("Processing Tweets...")
    for word in tweetlist:
        word = datafilter.correct(word)
        cleandata.append(word)
    post = {"text": cleandata}
    # post data
    print("Analysing Tweets ... ")
    res = requests.post(url, json=post)
    toxictweets = []
    if res.ok:
        predictions = res.json()
        for i in range(0, len(predictions["results"])):
            tweet = tweetlist[i]
            date = tweets.loc[tweets["tweet"] == tweet, "date"].values[0]
            link = tweets.loc[tweets["tweet"] == tweet, "link"].values[0]
            result = predictions["results"][i]["predictions"]
            if result["toxic"] > 0.5:
                tweetdata = [tweet, date, link, str(result["toxic"])]
                if tweet not in toxictweets:
                    toxictweets.append(tweetdata)
            if result["severe_toxic"] > 0.5:
                tweetdata = [tweet, date, link, str(result["severe_toxic"])]
                toxictweets.append(tweetdata)
            if result["obscene"] > 0.5:
                tweetdata = [tweet, date, link, str(result["obscene"])]
                toxictweets.append(tweetdata)
            if result["threat"] > 0.5:
                tweetdata = [tweet, date, link, str(result["threat"])]
                toxictweets.append(tweetdata)
            if result["insult"] > 0.5:
                tweetdata = [tweet, date, link, str(result["insult"])]
                toxictweets.append(tweetdata)
            if result["identity_hate"] > 0.5:
                tweetdata = [tweet, date, link, str(result["identity_hate"])]
                toxictweets.append(tweetdata)
    if os.path.isfile("temp.csv"):
        os.remove("temp.csv")
    return toxictweets


def findtweets(usernames):
    for username in usernames:
        print(f"Searching for Tweets for @{username}")
        print("===================================================")
        c = twint.Config()
        c.Username = username
        c.Debug = True
        c.Store_csv = True
        c.Custom_csv = ["tweet", "date"]
        c.Output = "temp.csv"
        c.Hide_output = True
        twint.run.Search(c)
        tweets = pd.read_csv("temp.csv")
        if len(tweets) > 0:
            print(f"Found {len(tweets)} tweets.")
            return checktoxic(tweets)
        else:
            print("No tweets found.")
            sys.exit(1)


def get_parser():
    parser = argparse.ArgumentParser(
        description="The Toxic Tweet Utility"
    )
    parser.add_argument(
        "-u",
        "--username",
        help="A Twitter Username",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="A List of Twitter Usernames",
    )
    return parser

def mainquery():
    parser = get_parser()
    opts = parser.parse_args()
    if not opts.username and not opts.file:
        print("At least one must be set: --username, --file")
        sys.exit(1)
    if opts.username and opts.file:
        print("Cannot set both --file and --username")
        sys.exit(1)
    if opts.username:
        usernames = [opts.username]
    if opts.file:
        with open(opts.file) as f:
            usernames = [line.rstrip() for line in f]
    tweets = findtweets(usernames)
    if len(tweets) == 0:
        print("No bad tweets found.")
    else:
        print("Toxic Tweets found:")
        print("-----------------------------------------------")
        for tweet in tweets:

            print(tweet[0])
            print("---")
            print(f"({tweet[1]}, {tweet[2]}, Confidence: {tweet[3]}%)")
            print("-----------------------------------------------")




if __name__ == '__main__':
    mainquery()

