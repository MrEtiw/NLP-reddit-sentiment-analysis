import praw
from praw.reddit import Reddit
from praw.models.reddit.subreddit import Subreddit
from praw.models.listing.generator import ListingGenerator
from praw.models.reddit.redditor import Redditor



def get_subreddit_by_name(reddit_client: Reddit,
                          subreddit_name: str) -> Subreddit:
    return reddit_client.subreddits.search_by_name(
        subreddit_name, include_nsfw=True, exact=True
    )[0]


def get_posts_including_a_query(subreddit: Subreddit,
                                query: str,
                                sort_by:str,
                                limit:int,
                                time_filter) -> ListingGenerator:
    return subreddit.search(query=query, time_filter=time_filter, sort=sort_by, limit=limit)



#TODO: combine get_url_of_posts and get_info_about_post in a single function call. That way, will only ping reddit once, instead of twice like currently
def get_url_of_posts(list_of_posts: list) -> list:
    list_of_url = []
    for post in list_of_posts:
        list_of_url.append(post.url)
    return list_of_url


def get_info_about_post(reddit_client: Reddit,
                        post_url: str) -> dict:
    try:
        check = reddit_client.submission(url=post_url)
        info = {}
        info["id"] = check.id
        info["url"] = post_url
        info["creation_utc"] = check.created_utc
        info["title"] = check.title
        info["num_comments"] = check.num_comments
        info["num_upvotes"] = check.score
        info["upvote_ratio"] = check.upvote_ratio
        info["post_text"] = check.selftext
        return info
    except Exception:
        return None


def get_redditor_of_post(reddit_client: Reddit,
                         post_url: str) -> Redditor:
    return reddit_client.submission(url=post_url).author


def get_info_about_redditor(redditor: Redditor) -> dict:
    info = {}
    info["author_name"] = redditor.name
    info["author_comment_karma"] = redditor.comment_karma
    info["author_has_verified_email"] = redditor.has_verified_email
    info["author_is_employee"] = redditor.is_employee
    info["author_is_mod"] = redditor.is_mod
    return info


def get_top_level_comments_from_url(reddit_client: Redditor,
                                    post_url: str) -> list:
    submission = reddit_client.submission(url=post_url)
    top_level_comments = []
    comments = submission.comments
    for comment in comments:
        if isinstance(comment, praw.models.Comment):
            top_level_comments.append(comment.body)
        else:
            pass

    return top_level_comments
