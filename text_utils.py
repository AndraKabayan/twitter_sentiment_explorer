import re
import unicodedata


def remove_accents(text):
    # NFKD memisahkan huruf dari tanda aksennya
    decomposed = unicodedata.normalize("NFKD", text)
    result = ""
    for ch in decomposed:
        if not unicodedata.combining(ch):     # buang karakter aksen
            result += ch
    return result


def clean_text(text):
    if text is None:
        return ""
    text = remove_accents(str(text)).lower()
    text = text.replace("-", " ").replace("_", " ")
    words = text.strip().split()          # split() tanpa argumen juga membuang spasi ganda
    return " ".join(words)


def mask_handles(text):
    return re.sub(r"@\w+", "@user", text)


def one_line(text):
    return " ".join(text.replace("\r", " ").replace("\n", " ").split())


def shorten(text, width):
    text = one_line(text)
    if width < 4:
        return text[:max(width, 0)]
    if len(text) > width:
        return text[:width - 3] + "..."
    return text
