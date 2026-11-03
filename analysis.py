from models import SHORT_LIMIT, MEDIUM_LIMIT, VALID_SENTIMENTS
from text_utils import clean_text


def safe_divide(top, bottom):
    if bottom == 0:
        return 0.0
    return top / bottom


def percent(part, total):
    return safe_divide(part, total) * 100


def average_length(tweets):
    total = 0
    for tweet in tweets:
        total += tweet.length             # operator aritmetika: penjumlahan
    return safe_divide(total, len(tweets))


def categorize_length(length):
    if length <= SHORT_LIMIT:
        return "short"
    elif length <= MEDIUM_LIMIT:
        return "medium"
    else:
        return "long"


def search_tweets(tweets, keyword):
    needle = clean_text(keyword)
    results = []                          # list baru untuk menampung hasil
    if needle == "":
        return results
    for tweet in tweets:
        if needle in clean_text(tweet.text):
            results.append(tweet)
    return results


def filter_tweets(tweets, entity=None, sentiment=None):
    results = []
    for tweet in tweets:
        entity_ok = entity is None or clean_text(tweet.entity) == clean_text(entity)
        sentiment_ok = sentiment is None or tweet.sentiment == sentiment
        if entity_ok and sentiment_ok:    # operator logika: and
            results.append(tweet)
    return results


def sort_descending(items, key_func):
    result = list(items)                  # salinan
    for i in range(1, len(result)):
        current = result[i]
        j = i - 1
        # geser item yang nilainya lebih kecil ke kanan
        while j >= 0 and key_func(result[j]) < key_func(current):
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = current
    return result


def top_longest(tweets, n):
    if n <= 0:
        return []
    ranked = sort_descending(tweets, lambda t: t.length)
    return ranked[:n]                     # slicing: n item pertama


def summarize_entity(tweets, entity):
    subset = filter_tweets(tweets, entity=entity)
    counts = {}
    for sentiment in VALID_SENTIMENTS:    # mulai semua hitungan dari 0
        counts[sentiment] = 0
    for tweet in subset:
        counts[tweet.sentiment] += 1
    total = len(subset)
    return {
        "entity": entity,
        "total": total,
        "positive": counts["Positive"],
        "negative": counts["Negative"],
        "neutral": counts["Neutral"],
        "irrelevant": counts["Irrelevant"],
        "positive_pct": percent(counts["Positive"], total),
        "negative_pct": percent(counts["Negative"], total),
        "avg_length": average_length(subset),
    }


def summarize_all(tweets, entities):
    summaries = []
    for entity in entities:
        summaries.append(summarize_entity(tweets, entity))
    return sort_descending(summaries, lambda s: s["positive_pct"])


def find_entity(entities, typed):
    wanted = clean_text(typed)
    if wanted == "":
        return None
    for name in entities:
        if clean_text(name) == wanted:
            return name
    partial = []
    for name in entities:
        if wanted in clean_text(name):
            partial.append(name)
    if len(partial) == 1:                 # hanya satu kemungkinan: aman dipakai
        return partial[0]
    return None                           # tidak ada atau ambigu
