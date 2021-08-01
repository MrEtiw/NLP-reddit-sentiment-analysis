import pandas as pd
import datetime
from praw.reddit import Reddit
import time
import os
from fetching_data.querying_reddit import get_info_about_post


def generate_file_name(subreddit_name: str, query: str, sortby_filter: str, time_filter:str) -> str:
    now = datetime.datetime.now()
    year = str(now.year)
    month = str("{:02d}".format(now.month))
    day = str("{:02d}".format(now.day))
    return (
        year
        + "_"
        + month
        + "_"
        + day
        + "_"
        + subreddit_name
        + "_"
        + query
        + "_"
        + sortby_filter
        + "_"
        + time_filter
        + ".csv"
    )


def generate_df_from_urls(reddit_client:Reddit,
                          urls:list,
                          return_invalid_urls = True,
                          file_name_to_save = None):
    all_infos = []
    invalid_urls = []
    print(len(urls))
    # Getting info for each url
    i =0
    for url in urls:
        print(i)
        print(url)
        time.sleep(0.1)

        # Catching invalid urls, like picture posts
        info = get_info_about_post(reddit_client, url)
        if info:
            all_infos.append(info)
        else:
            invalid_urls.append(url)
        i = i+1

    df = pd.DataFrame(all_infos)
    df["creation_date"] = pd.to_datetime(df["creation_utc"], unit="s")
    df = df.drop(["creation_utc"], axis=1)

    if file_name_to_save:
        df.to_csv(os.path.join("./data", file_name_to_save))

    if return_invalid_urls:
        return df, invalid_urls

    return df







