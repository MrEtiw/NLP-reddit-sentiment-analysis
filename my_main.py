import praw
from setup.initialize_reddit_client import set_credentials_env_var, get_reddit_client
from fetching_data.querying_reddit import (
    get_subreddit_by_name,
    get_posts_including_a_query,
    get_url_of_posts,
    get_redditor_of_post,
    get_info_about_redditor,
    get_top_level_comments_from_url,
)

from fetching_data.generating_result_files import (generate_df_from_urls,
                                                   generate_file_name)






# set up connection
reddit_client = set_credentials_env_var("reddit_credentials.json")
reddit_client = get_reddit_client()

# input arguments
subreddit_name = "wallstreetbets"
query = "AMC"
sort_by = "new"
time_filter = "week"
limit = 100

# getting urls related to input arguments
subreddit = get_subreddit_by_name(reddit_client, subreddit_name)
posts = get_posts_including_a_query(subreddit, query, sort_by, limit, time_filter)
urls = get_url_of_posts(posts)

# fetching info about those urls
file_name = generate_file_name(subreddit_name, query, sort_by, time_filter)
all_infos, invalid_urls = generate_df_from_urls(reddit_client,
                                                urls,
                                                return_invalid_urls=True,
                                                file_name_to_save=file_name)











redditor = get_redditor_of_post(reddit_client, urls[0])
info_redditor = get_info_about_redditor(redditor)

submission = reddit_client.submission(url=urls[0])


def iter_top_level(comments):
    for top_level_comment in comments:
        if isinstance(top_level_comment, praw.models.MoreComments):
            yield from iter_top_level(top_level_comment.comments())
        else:
            yield top_level_comment


for comment in iter_top_level(submission.comments):
    print(comment)
    print(comment.body)


a = get_top_level_comments_from_url(reddit_client, urls[0])
