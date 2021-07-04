def get_comments(reddit_client, url):
    bodyComment = []
    check = reddit.submission(url=url)
    subComments = check.comments

    for comment in subComments:
        bodyComment.append(comment.body)
    return
