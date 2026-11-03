
CSV_FILE = "twitter_validation.csv"   
EXPECTED_COLUMNS = 4                  
VALID_SENTIMENTS = ["Positive", "Negative", "Neutral", "Irrelevant"]  
SHORT_LIMIT = 60                      
MEDIUM_LIMIT = 140                    
TEXT_WIDTH = 55                       


class Tweet:
    def __init__(self, tweet_id, entity, sentiment, text):
        self.tweet_id = tweet_id      
        self.entity = entity          
        self.sentiment = sentiment    
        self.text = text              

    @property
    def length(self):
        return len(self.text)

    @property
    def word_count(self):
        return len(self.text.split())

    def __str__(self):
        return f"[{self.tweet_id}] {self.entity} ({self.sentiment}): {self.text[:TEXT_WIDTH]}"


class TweetCollection:

    def __init__(self, tweets=None):
        self.tweets = list(tweets) if tweets else []

    def add(self, tweet):
        self.tweets.append(tweet)

    def __len__(self):
        return len(self.tweets)

    def entities(self):
        names = []
        for tweet in self.tweets:
            if tweet.entity not in names:
                names.append(tweet.entity)
        for i in range(1, len(names)):
            current = names[i]
            j = i - 1
            while j >= 0 and names[j].lower() > current.lower():
                names[j + 1] = names[j]
                j -= 1
            names[j + 1] = current 
        return names

    def __str__(self):
        return f"TweetCollection with {len(self.tweets)} tweets"
