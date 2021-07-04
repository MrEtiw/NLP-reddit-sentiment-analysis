class Reddit:
    def __init__(self, reddit_client, sub_reddits, key_words):
        self.reddit_client = reddit_client
        self.sub_reddits = sub_reddits
        self.key_words = key_words
