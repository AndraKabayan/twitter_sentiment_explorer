# Twitter Sentiment Explorer

Program Python berbasis menu untuk menjelajahi data tweet dan sentimennya.

## 1. Dataset
- **Nama:** Twitter Entity Sentiment Analysis (file yang dipakai: `twitter_validation.csv`)
- **Tautan Kaggle:** https://www.kaggle.com/datasets/jp797498e/twitter-entity-sentiment-analysis
- **Lisensi:** CC0: Public Domain
- **Alasan memilih:**  Data ini adalah tweet nyata sehingga hasilnya terasa bermakna. Ukurannya (1.000 baris) pas dengan syarat 200 sampai 2.000 baris tanpa perlu dipangkas. Kolomnya sederhana dan lengkap, dengan dua kolom kategori (entitas dan sentimen) yang cocok untuk fitur pencarian, filter, ranking, dan ringkasan. Teksnya yang berantakan (huruf kapital campur, tanda hubung, baris baru) juga membuat fungsi pembersih teks benar-benar berguna.
- **Ukuran:** 1.000 baris, satu file CSV, satu baris = satu tweet, tanpa baris header.

### Kolom
| Kolom | Dipakai? | Keterangan |
|---|---|---|
| 1 – ID tweet | Ya | Bilangan bulat, pengenal tweet. |
| 2 – Entitas | Ya | Game atau perusahaan yang dibicarakan (32 macam). |
| 3 – Sentimen | Ya | Positive / Negative / Neutral / Irrelevant. |
| 4 – Teks tweet | Ya | Baris baru dihapus. `@username` diganti `@user` demi privasi. |

Semua kolom terisi di setiap baris, jadi tidak ada sel kosong yang perlu penanganan khusus.
(Jika ada baris dengan nilai hilang, baris itu dilewati dan dihitung.)

## 2. Cara menjalankan
Hanya butuh Python 3 (pustaka standar saja, tanpa pandas atau numpy).

    python main.py                 # menjalankan program
    python -m unittest             # menjalankan unit test (23 tes)

Jalankan dari dalam folder ini. File `twitter_validation.csv` harus berada di dalam folder yang sama dengan `main.py`.

### Memilih menu
Setelah program dijalankan, muncul pesan jumlah record yang dimuat, lalu menu berikut:

    Berhasil memuat 1000 record, 0 baris tidak terbaca dilewati.

    ===== Penjelajah Sentimen Twitter =====
    1. Cari tweet berdasarkan kata kunci
    2. Daftar tweet per entitas / sentimen
    3. Top N tweet terpanjang
    4. Ringkasan sentimen per entitas
    5. Bandingkan dua entitas
    6. Keluar
    Pilih menu 1-6:

Ketik angka menu (1 sampai 6) lalu tekan Enter. Setelah satu fitur selesai, menu muncul lagi sampai kamu memilih **6 (Keluar)**.

| Menu | Fitur | Yang diminta program | Contoh input |
|---|---|---|---|
| 1 | Cari tweet berdasarkan kata kunci | Kata kunci | `bad-news` |
| 2 | Daftar tweet per entitas / sentimen | Nama entitas, lalu sentimen (Enter = semua) | `fifa`, lalu `positif` |
| 3 | Top N tweet terpanjang | Jumlah tweet (1 sampai jumlah record) | `5` |
| 4 | Ringkasan sentimen per entitas | Tidak ada input | (langsung tampil) |
| 5 | Bandingkan dua entitas | Entitas pertama, lalu entitas kedua | `fifa`, lalu `google` |
| 6 | Keluar | Tidak ada input | (program berhenti) |

Tips penggunaan:
- **Entitas:** huruf besar/kecil dan spasi berlebih tidak berpengaruh. Ketik `?` untuk melihat daftar semua entitas. Nama sebagian yang hanya cocok dengan satu entitas juga diterima.
- **Sentimen:** ketik `positif`, `negatif`, `netral`, atau `tidak relevan` (nama Inggris `Positive`, `Negative`, `Neutral`, `Irrelevant` juga diterima). Tekan Enter tanpa mengetik untuk memilih semua sentimen.
- **Input salah** (huruf saat diminta angka, angka di luar rentang, input kosong, entitas tidak dikenal) menghasilkan pesan yang jelas, lalu program meminta input lagi tanpa berhenti.

## 3. Fitur
1. **Cari kata kunci** – tidak peduli huruf kapital, tanda hubung, aksen, atau spasi berlebih.
2. **Daftar per entitas / sentimen** – memfilter tweet; menampilkan 10 pertama.
3. **Top N tweet terpanjang** – diurutkan dengan insertion sort buatan sendiri (tanpa `sorted()`), N pertama diambil dengan slicing, plus hitungan kategori short/medium/long.
4. **Ringkasan sentimen per entitas** – jumlah, % positif, % negatif, dan rata-rata panjang; diurutkan dari % positif tertinggi.
5. **Bandingkan dua entitas** – dua baris berdampingan dan kalimat yang menyebut entitas mana yang lebih positif.

Saat program mulai, ia mencetak jumlah record yang dimuat dan jumlah baris yang dilewati.
Setiap input diperiksa; input salah menghasilkan pesan dan prompt baru, bukan crash.

## 4. Cara kerja kode (alur singkat)
1. `main.py` memanggil `load_tweets()` di `data_loader.py`.
2. `load_tweets()` membaca CSV baris demi baris dengan modul `csv`. Tiap baris dicek oleh `parse_row()`: jumlah kolom harus 4, ID harus angka, entitas dan teks tidak boleh kosong, sentimen harus salah satu dari empat nilai sah. Baris yang gagal dilewati dan dihitung.
3. Baris yang lolos diubah menjadi objek `Tweet` (`models.py`). `@username` disamarkan oleh `mask_handles()` di `text_utils.py`.
4. Semua `Tweet` dimasukkan ke `TweetCollection`, lalu menu `while` di `main()` berulang sampai pengguna memilih 6 (Exit).
5. Setiap pilihan menu memanggil fungsi di `analysis.py` (cari, filter, urutkan, ringkas). Hasilnya berupa list baru, lalu `main.py` mencetaknya dalam tabel rata dengan f-string.
6. `test_project.py` menguji fungsi-fungsi tersebut dengan data kecil: input normal, kasus tepi (list kosong, nol), dan input salah.

## 5. Keterbatasan
- Label sentimen berasal dari dataset dan belum tentu sesuai penilaian manusia.
- Teks tweet dipotong 55 karakter di tabel.
- Kolom angka asli hanya ID, sehingga analisis memakai nilai turunan (panjang tweet, persentase) dan relatif sederhana.
- Nama entitas dipakai apa adanya dari dataset (misalnya `WorldOfCraft`).
- Tampilan terminal, kode komentar, dan README memakai bahasa Indonesia. Nilai sentimen di data tetap Inggris (Positive, Negative, Neutral, Irrelevant); program menerima ketikan Inggris maupun Indonesia (positif, negatif, netral, tidak relevan).

## 6. Tautan video
https://youtu.be/ZFn0IKo5vPU

## 7. Letak setiap konsep
| Konsep | File | Fungsi / bagian |
|---|---|---|
| Variabel dan tipe data (str, int, float, bool, list; konstanta huruf kapital) | `models.py` | Konstanta `CSV_FILE`, `VALID_SENTIMENTS`, `SHORT_LIMIT`; `Tweet.__init__` |
| Input dan output (input(), loop validasi, f-string, kolom rata) | `main.py` | `ask_int`, `print_tweets`, `print_summary_row` |
| Operator (aritmetika, relasional, and/or/not) | `analysis.py` | `percent`, `average_length`, `filter_tweets` |
| Kondisional (if/elif/else) | `analysis.py` | `categorize_length`; juga `ask_int` di `main.py` |
| Perulangan (for dan while) | `main.py` / `analysis.py` | `while running` di `main()`; `for` di `search_tweets` |
| Fungsi (parameter dan return) | `analysis.py` | `safe_divide`, `summarize_entity`, `top_longest` |
| List (simpan, buat list baru, slicing) | `analysis.py` | `filter_tweets` membuat list; `top_longest` memakai `ranked[:n]` |
| Manipulasi string | `text_utils.py` | `clean_text`, `mask_handles`, `shorten` |
| Class (bonus) | `models.py` | `Tweet` (`__init__`, `__str__`), `TweetCollection` |
| Unit test | `test_project.py` | 23 tes: input normal, tepi, dan salah |