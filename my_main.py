import praw
from initialize_reddit_client import set_credentials_env_var, get_reddit_client
from querying_reddit import (
    get_subreddit_by_name,
    get_posts_including_a_query,
    get_url_of_posts,
    get_redditor_of_post,
    get_info_about_redditor,
    get_info_about_post,
    get_top_level_comments_from_url,
)

reddit_client = set_credentials_env_var("reddit_credentials.json")
reddit_client = get_reddit_client()
sub_reddit = get_subreddit_by_name(reddit_client, "wallstreetbets")
posts = get_posts_including_a_query(sub_reddit, "AMC")
urls = get_url_of_posts(posts)

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
