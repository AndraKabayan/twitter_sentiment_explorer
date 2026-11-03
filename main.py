import os

from models import CSV_FILE, TEXT_WIDTH, VALID_SENTIMENTS, TweetCollection
from data_loader import load_tweets
from text_utils import shorten, clean_text
import analysis

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROWS = 10
SENTIMENT_ALIASES = {
    "positif": "Positive",
    "negatif": "Negative",
    "netral": "Neutral",
    "tidak relevan": "Irrelevant",
}


#  fungsi bantu input (setiap ketikan diperiksa) 
def ask_int(prompt, low, high):
    while True:
        typed = input(prompt).strip()
        if typed == "":
            print("  Input tidak boleh kosong.")
        elif not (typed.isdigit() or (typed[0] == "-" and typed[1:].isdigit())):
            print(f"  '{typed}' bukan bilangan bulat.")
        elif int(typed) < low or int(typed) > high:
            print(f"  Masukkan angka dari {low} sampai {high}.")
        else:
            return int(typed)


def ask_text(prompt):
    while True:
        typed = input(prompt).strip()
        if typed != "":
            return typed
        print("  Input tidak boleh kosong.")


def ask_entity(prompt, entities):
    while True:
        typed = ask_text(prompt)
        if typed == "?":
            print("  Daftar entitas: " + ", ".join(entities))
            continue
        found = analysis.find_entity(entities, typed)
        if found is not None:
            return found
        print(f"  '{typed}' bukan entitas yang dikenal (atau terlalu umum). Ketik ? untuk melihat daftar.")


def ask_sentiment():
    while True:
        typed = input("Sentimen (Positif/Negatif/Netral/Tidak relevan, Enter = semua): ").strip()
        if typed == "":
            return None
        cleaned = clean_text(typed)
        if cleaned in SENTIMENT_ALIASES:
            return SENTIMENT_ALIASES[cleaned]
        for valid in VALID_SENTIMENTS:
            if cleaned == valid.lower():
                return valid
        print(f"  '{typed}' bukan sentimen yang valid.")


#  fungsi bantu output (kolom rata) 
def print_tweets(tweets, limit=DEFAULT_ROWS):
    if len(tweets) == 0:
        print("  Tidak ada tweet yang ditemukan.")
        return
    print(f"\n{'ID':<7}{'Entitas':<24}{'Sentimen':<11}{'Panjang':>4}  {'Teks'}")
    print("-" * (7 + 24 + 11 + 4 + 2 + TEXT_WIDTH))
    for tweet in tweets[:limit]:
        entity = shorten(tweet.entity, 22)
        text = shorten(tweet.text, TEXT_WIDTH)
        print(f"{tweet.tweet_id:<7}{entity:<24}{tweet.sentiment:<11}{tweet.length:>4}  {text}")
    if len(tweets) > limit:
        print(f"... menampilkan {limit} dari {len(tweets)} tweet")
    else:
        print(f"{len(tweets)} tweet ditampilkan")


def print_summary_header():
    print(f"\n{'Entitas':<34}{'Total':>6}{'Pos':>5}{'Neg':>5}{'Net':>5}{'Irr':>5}"
          f"{'Pos%':>8}{'Neg%':>8}{'RataPjg':>9}")
    print("-" * 85)


def print_summary_row(s):
    print(f"{shorten(s['entity'], 32):<34}{s['total']:>6}{s['positive']:>5}{s['negative']:>5}"
          f"{s['neutral']:>5}{s['irrelevant']:>5}{s['positive_pct']:>8.1f}"
          f"{s['negative_pct']:>8.1f}{s['avg_length']:>9.1f}")


#  aksi untuk setiap menu 
def do_search(collection):
    keyword = ask_text("Kata kunci yang dicari: ")
    results = analysis.search_tweets(collection.tweets, keyword)
    print(f"\nDitemukan {len(results)} tweet yang mengandung '{keyword.strip()}'.")
    print_tweets(results)


def do_list(collection):
    entity = ask_entity("Entitas (ketik ? untuk daftar): ", collection.entities())
    sentiment = ask_sentiment()
    results = analysis.filter_tweets(collection.tweets, entity=entity, sentiment=sentiment)
    label = sentiment if sentiment else "semua sentimen"
    print(f"\n{entity} / {label}: {len(results)} tweet")
    print_tweets(results)


def do_top(collection):
    n = ask_int(f"Berapa tweet yang ingin ditampilkan (1-{len(collection)})? ", 1, len(collection))
    results = analysis.top_longest(collection.tweets, n)
    print(f"\n{n} tweet terpanjang:")
    print_tweets(results, limit=n)
    # hitung kategori panjang tweet yang ditampilkan (if/elif/else ada di analysis.py)
    counts = {"short": 0, "medium": 0, "long": 0}
    for tweet in results:
        counts[analysis.categorize_length(tweet.length)] += 1
    print(f"Kategori panjang (short=pendek, medium=sedang, long=panjang): {counts}")


def do_summary(collection):
    summaries = analysis.summarize_all(collection.tweets, collection.entities())
    print("\nRingkasan sentimen per entitas (diurutkan dari persentase positif tertinggi):")
    print_summary_header()
    for summary in summaries:
        print_summary_row(summary)


def do_compare(collection):
    entities = collection.entities()
    first = ask_entity("Entitas pertama (ketik ? untuk daftar): ", entities)
    second = ask_entity("Entitas kedua (ketik ? untuk daftar): ", entities)
    if first == second:
        print("  Pilih dua entitas yang berbeda.")
        return
    print_summary_header()
    for name in (first, second):
        print_summary_row(analysis.summarize_entity(collection.tweets, name))
    a = analysis.summarize_entity(collection.tweets, first)
    b = analysis.summarize_entity(collection.tweets, second)
    if a["positive_pct"] > b["positive_pct"]:
        print(f"\n{first} lebih positif daripada {second}.")
    elif a["positive_pct"] < b["positive_pct"]:
        print(f"\n{second} lebih positif daripada {first}.")
    else:
        print("\nKedua entitas punya persentase tweet positif yang sama.")


MENU = """
===== Penjelajah Sentimen Twitter =====
1. Cari tweet berdasarkan kata kunci
2. Daftar tweet per entitas / sentimen
3. Top N tweet terpanjang
4. Ringkasan sentimen per entitas
5. Bandingkan dua entitas
6. Keluar"""


def main():
    path = os.path.join(HERE, CSV_FILE)
    try:
        tweets, skipped = load_tweets(path)
    except FileNotFoundError as error:
        print(error)
        return
    collection = TweetCollection(tweets)
    print(f"Berhasil memuat {len(collection)} record, {skipped} baris tidak terbaca dilewati.")
    if len(collection) == 0:
        print("Tidak ada data untuk dijelajahi. Program berhenti.")
        return

    running = True                        # bool: penanda menu masih berjalan
    while running:                        # while: menu terus berulang sampai Keluar
        print(MENU)
        try:
            choice = ask_int("Pilih menu 1-6: ", 1, 6)
            if choice == 1:
                do_search(collection)
            elif choice == 2:
                do_list(collection)
            elif choice == 3:
                do_top(collection)
            elif choice == 4:
                do_summary(collection)
            elif choice == 5:
                do_compare(collection)
            else:
                running = False
        except EOFError:
            print("\nInput ditutup. Sampai jumpa!")
            running = False
    print("Sampai jumpa!")


if __name__ == "__main__":
    main()
