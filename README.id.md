=======================================================================
Google AI Pro (5 TB) Konsol Otomatis 2 Tahun Tanpa Biaya
=======================================================================

[English](README.md) | **Bahasa Indonesia** | [Tiếng Việt](README.vi.md) | [中文 (简体)](README.zh-CN.md)

**Dukungan Multi-bahasa:** 中文 (Chinese) | English | Bahasa Indonesia (Indonesia) | Tiếng Việt (Vietnamese)

> ⚠️ **Pernyataan:** Proyek ini disediakan sebagai open-source untuk keperluan analisis dan pembelajaran komunitas. Otomatisasi pendaftaran massal mungkin melanggar Ketentuan Layanan Google.

> 📖 Panduan penggunaan lengkap (Bahasa Vietnam): **[HUONGDAN.md](HUONGDAN.md)**

---

## I. Persyaratan Sistem

1. Windows 10 / 11, atau Linux/macOS dengan dukungan Python
2. Google Chrome sudah terpasang (path default sudah cukup)
3. Python 3.10+ (centang "Add to PATH" saat instalasi)
4. Jaringan: proxy Amerika Serikat aktif, atau konfigurasikan template proxy di konsol

---

## II. Mulai Cepat

### Opsi 1: File Batch Windows

1. Jalankan pertama: klik dua kali **1_setup_install_deps_and_start.bat**
2. Pemakaian harian: klik dua kali **2_start_console.bat**
3. Browser terbuka otomatis: http://127.0.0.1:8765

### Opsi 2: Menjalankan Python Manual

```bash
pip install -r requirements.txt
python app.py
# Buka http://127.0.0.1:8765
```

### Memilih Bahasa

Klik dropdown bahasa (kanan atas) untuk berganti:

- 中文 (简体) — Chinese Simplified
- English
- **Bahasa Indonesia**
- Tiếng Việt — Vietnamese

Preferensi bahasa disimpan di `localStorage` browser.

---

## III. Konfigurasi & Persiapan Akun

### 1. Konfigurasi Kartu Kredit (Wajib)

- Buka bagian **"Konfigurasi Global Zona Bebas Pajak, Paket Pro 2 Tahun Tanpa Biaya & Kartu Kredit"**
- Masukkan kartu Visa / Mastercard mata uang asing:
  - Nomor kartu (16 digit)
  - Tanggal kedaluwarsa (bulan/tahun, mis. `08/29`)
  - Kode keamanan (CVC 3 digit)
  - Nama pemilik kartu dalam huruf Latin
  - Kode pos bebas pajak: `97201` (Oregon, AS) — bawaan, tidak perlu diubah
- Klik **"💾 Simpan Konfigurasi"**
- Catatan: ada proteksi biaya $0 yang ketat; tombol subscribe hanya diklik bila halaman checkout menampilkan **US$0.00**

### 2. Proxy Amerika Serikat (WAJIB agar harga $0.00)

Isi kotak **"🛡️ Template Proxy Global"** dengan proxy AS. Ketiga format ini didukung:

```
# A. host:port:user:pass
dc.decodo.com:10001:<username>:<password>

# B. http://user:pass@host:port   (paling standar, disarankan)
http://<username>:<password>@dc.decodo.com:10001

# C. user:pass@host:port
<username>:<password>@dc.decodo.com:10001
```

Placeholder dinamis: `{country}` / `{COUNTRY}` (diambil dari "Wilayah Target") dan `{session}` / `{SESSION}` (dibuat otomatis per akun).

Klik **"🔍 Uji Konektivitas Proxy"** untuk memastikan IP keluar adalah 🇺🇸 AS.

> 🔴 **Tanpa proxy AS → IP keluar berada di negara lain → Google menampilkan harga lokal, TIDAK PERNAH $0.00.** Ini adalah penyebab kegagalan paling umum.

### 3. Impor Massal Akun Google

- Di bagian **"📥 Zona Impor Akun Massal"**, tempel akun (satu per baris), format yang didukung:
  - `email----password----recovery_email`
  - `email----password----recovery_email----2FA_key`
  - `email----password----2FA_key`
- Klik **"➕ Impor Daftar Akun Sekali Klik"**

### 4. Eksekusi Otomatis Penuh

- Klik **"▶ Jalankan Pipeline"** pada tiap akun, atau **"▶ Jalankan Otomatis Semua Akun Tertunda"** di bagian atas
- Otomatisasi akan menyelesaikan:
  - **Langkah 1:** Login Google otomatis + verifikasi email pemulihan / 2FA
  - **Langkah 2:** Pengikatan kartu bebas pajak inline + lapisan 1 gratis 12 bulan (US$0.00)
  - **Langkah 3:** Tumpukan lapisan 2 gratis 6 bulan (US$0.00 → 18 bulan)
  - **Langkah 4:** Tumpukan lapisan 3 gratis 6 bulan (US$0.00 → batas 24 bulan)
  - **Langkah 5:** Otomatis membatalkan perpanjangan di Play Store, mengunci masa berlaku 2 tahun + bukti tangkapan layar

---

## IV. Fitur

- ✅ Otomatisasi penuh: login → verifikasi → tumpukan multi-lapisan → kunci berhenti berlangganan
- ✅ Proteksi tanpa biaya: memvalidasi $0.00 sebelum checkout
- ✅ Antarmuka multi-bahasa: Chinese / English / Indonesian / Vietnamese
- ✅ Log real-time & pemantauan kemajuan
- ✅ Pemrosesan akun massal
- ✅ Dukungan proxy (HTTP / HTTPS / SOCKS5), dengan jembatan autentikasi proxy
- ✅ Status akun tersimpan permanen
- ✅ Bukti tangkapan layar untuk setiap langkah (screenshots/)

---

## V. Struktur Masa Gratis (Terverifikasi)

Langganan sebenarnya adalah **paket (bundle)** berisi dua item, masing-masing dengan tanggal berakhir sendiri:

| Item | Uji coba | Tanggal berakhir |
|---|---|---|
| YouTube Premium Individual Add On | 1 bulan | mis. 2026-12-09 |
| Google AI Pro (5 TB) | 12 bulan (ditunda) | Lapisan 1 → 2027-11-09 · +Lapisan 2 → 2028-05-10 · +Lapisan 3 → 2028-11-09 |

**Mekanismenya:** setiap offer tambahan menggeser tanggal berakhir Google AI Pro **maju 6 bulan**, dengan memakai saldo paket yang sedang aktif. Di popup checkout, kolom `开始日期` milik Google AI Pro sebenarnya adalah **tanggal berakhir uji coba** — itulah cara melihat apakah suatu lapisan benar-benar berhasil.

> ⚠️ **Google membalas "success" bahkan ketika offer tidak mengubah apa pun.** Karena itu, Langkah 4 pada versi ini membaca tanggal berakhir sebenarnya dari dialog [Kelola] Play dan otomatis mencoba offer token berikutnya bila tanggal tidak bergeser.

**Cara membaca masa berlaku sebenarnya:** `play.google.com/store/account/subscriptions` hanya menampilkan *tanggal penagihan berikutnya*, bukan tanggal berakhir. Buka **管理 / Kelola**, lalu baca bagian *套装 (bundle)*:

```
Google AI Pro (5 TB)               - 将于 2028年11月9日结束
YouTube Premium Individual Add On  - 将于 2026年12月9日结束
```

---

## VI. Struktur Direktori

```
├── app.py                 # Backend FastAPI
├── automation_engine.py   # Logika otomatisasi Playwright
├── config.json            # Konfigurasi & data akun (jangan di-commit, berisi nomor kartu)
├── requirements.txt      # Dependensi Python
├── templates/
│   └── index.html       # Antarmuka web multi-bahasa
├── i18n_zh_cn.json      # Terjemahan Chinese
├── i18n_en_us.json      # Terjemahan English
├── i18n_id_id.json      # Terjemahan Indonesian
├── i18n_vi_vn.json      # Terjemahan Vietnamese
├── README.vi.md         # README Bahasa Vietnam
├── HUONGDAN.md          # Panduan penggunaan lengkap (Bahasa Vietnam)
└── screenshots/         # Tangkapan layar bukti akun
```

---

## VII. Internasionalisasi (i18n)

Semua teks antarmuka dapat diterjemahkan:

- **i18n_zh_cn.json** — Chinese Simplified (96 kunci)
- **i18n_en_us.json** — English (95 kunci)
- **i18n_id_id.json** — Bahasa Indonesia (95 kunci)
- **i18n_vi_vn.json** — Tiếng Việt (97 kunci)

Preferensi bahasa disimpan di localStorage browser. Cara menambah bahasa baru:
1. Buat `i18n_[kode].json` dengan seluruh kunci
2. Daftarkan kodenya di `lang_map` pada `app.py` (fungsi `load_i18n`)
3. Tambahkan `<option value="[kode]">Nama</option>` pada `#langSelect` di `templates/index.html`

---

## VIII. Endpoint API

| Method | Endpoint | Keterangan |
|---|---|---|
| GET | `/` | Antarmuka web |
| GET | `/api/state` | Status saat ini (akun, log, konfigurasi) |
| GET | `/api/i18n?lang=zh-CN\|en\|id\|vi` | Ambil terjemahan |
| POST | `/api/config` | Perbarui konfigurasi |
| POST | `/api/accounts/import` | Impor akun massal |
| POST | `/api/accounts/delete` | Hapus akun |
| POST | `/api/accounts/reset` | Reset status akun |
| POST | `/api/run/single` | Jalankan satu akun |
| POST | `/api/run/batch` | Jalankan semua akun tertunda |
| POST | `/api/stop` | Hentikan |
| POST | `/api/proxy/test` | Uji konektivitas proxy |
| POST | `/api/open_browser` | Kontrol browser manual |

---

## IX. Pemecahan Masalah

| Gejala | Penyebab | Solusi |
|---|---|---|
| `Chrome did not open the debug port` | Jendela Chrome lama masih memegang profil akun | Tutup semua jendela Chrome proyek ini lalu jalankan ulang (build ini juga membersihkannya otomatis) |
| `Target page, context or browser has been closed` | Jendela Chrome ditutup di tengah jalan | Jalankan ulang dengan langkah awal yang sesuai |
| `Please fill in complete payment card info` | Kartu belum diisi | Lengkapi nomor kartu, kedaluwarsa, dan CVC di panel konfigurasi |
| Negara keluar ≠ US | Belum ada proxy AS | Konfigurasikan proxy AS lalu uji lagi |
| Harga bukan $0.00 | IP negara salah atau akun tidak memenuhi syarat | Periksa baris IP pada log |
| `Batch queue is already running` | Antrean lama macet | Klik **⏹ Hentikan Tugas**, atau jalankan ulang server |
| `407 Unauthorized` saat uji proxy | Username atau password salah | Salin-tempel langsung dari dashboard penyedia: `I` (huruf i besar) dan `l` (huruf L kecil) sangat mirip |

**Port sudah dipakai:** ubah `uvicorn.run(app, host="127.0.0.1", port=8765, ...)` di baris terakhir `app.py`.

**Chrome tidak ditemukan:**
- Pastikan Chrome terpasang di path default
- atau set variabel lingkungan `CHROME_PATH`

---

## X. Referensi

- Proyek asli: https://github.com/worldonlyu/Google_AI_Pro_2Year_ZeroCost_Auto
- Fork i18n: https://github.com/gemhelixx17/google-ai-pro
- Fork Bahasa Vietnam + perbaikan pipeline Windows: https://github.com/nguyenquanghiep3404/google-ai-pro-viet-hoa

---

**Lisensi:** Sesuai ketentuan proyek asli.

## ⚠️ Peringatan

Alat ini mengotomatiskan pendaftaran Google AI Pro pada **banyak akun** dan mengikat kartu kredit. Penggunaan massal dapat **melanggar Ketentuan Layanan Google** dan menyebabkan akun diblokir. Gunakan hanya pada akun yang Anda miliki secara sah, dan tanggung sendiri akibatnya.
