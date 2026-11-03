import csv
import os

from models import Tweet, EXPECTED_COLUMNS, VALID_SENTIMENTS
from text_utils import mask_handles, one_line, clean_text


def parse_row(row):
    if len(row) != EXPECTED_COLUMNS:
        return None
    id_text, entity, sentiment, text = row

    id_text = id_text.strip()
    if not id_text.isdigit():
        return None

    entity = entity.strip()
    text = one_line(text)
    if entity == "" or text == "":
        return None

    matched = None
    for valid in VALID_SENTIMENTS:
        if clean_text(sentiment) == valid.lower():
            matched = valid
    if matched is None:
        return None

    return Tweet(int(id_text), entity, matched, mask_handles(text))


def load_tweets(path):
    tweets = []
    skipped = 0
    if not os.path.exists(path):
        raise FileNotFoundError(f"File data tidak ditemukan: {path}")
    with open(path, newline="", encoding="utf-8-sig", errors="replace") as file:
        reader = csv.reader(file)
        for row in reader:                # for: memproses setiap baris
            if not row:                   # baris kosong total: abaikan
                continue
            tweet = parse_row(row)
            if tweet is None:
                skipped += 1              # hitung baris yang rusak
            else:
                tweets.append(tweet)
    return tweets, skipped
