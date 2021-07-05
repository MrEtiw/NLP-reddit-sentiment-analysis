import praw

def get_subreddit_by_name(reddit_client, subreddit_name):
    return reddit_client.subreddits.search_by_name(subreddit_name, include_nsfw=True, exact=True)[0]

def get_posts_including_a_query(subreddit, query, time_filter = "all"):
    return subreddit.search(query = query,
                            time_filter = time_filter,
                            limit = 100000)

def get_url_of_posts(list_of_posts):
    list_of_url = []
    for post in list_of_posts:
        list_of_url.append(post.url)
    return list_of_url

def get_info_about_post(reddit_client, post_url):
    check = reddit_client.submission(url=post_url)
    info = {}
    info["title"] = check.title
    info["submission_name"] = check.name
    info["num_comments"] = check.num_comments
    info["num_upvotes"] = check.score
    info["upvote_ratio"] = check.upvote_ratio
    info["post_text"] = check.selftext
    return info

def get_redditor_of_post(reddit_client, post_url):
    return reddit_client.submission(url=post_url).author

def get_info_about_redditor(redditor):
    info = {}
    info["author_name"] = redditor.name
    info["author_comment_karma"] = redditor.comment_karma
    info["author_has_verified_email"] = redditor.has_verified_email
    info["author_is_employee"] = redditor.is_employee
    info["author_is_mod"] = redditor.is_mod
    return info

def get_top_level_comments_from_url(reddit_client, post_url):
    submission = reddit_client.submission(url = post_url)
    top_level_comments = []
    comments = submission.comments
    for comment in comments:
        if isinstance(comment, praw.models.Comment):
            top_level_comments.append(comment.body)
        else:
            pass

    return top_level_comments

