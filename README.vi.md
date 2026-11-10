=======================================================================
Google AI Pro (5 TB) — Bảng Điều Khiển Tự Động 2 Năm Miễn Phí
=======================================================================

[English](README.md) | [Bahasa Indonesia](README.id.md) | **Tiếng Việt** | [中文 (简体)](README.zh-CN.md)

**Hỗ trợ đa ngôn ngữ:** 中文 (Trung Quốc) | English | Bahasa Indonesia (Indonesia) | Tiếng Việt (Việt Nam)

> ⚠️ **Disclaimer:** Dự án được cung cấp dưới dạng mã nguồn mở để cộng đồng phân tích và học tập. Việc tự động hóa đăng ký hàng loạt có thể vi phạm Điều khoản Dịch vụ của Google.

---

## I. Yêu cầu hệ thống

1. Windows 10 / 11, hoặc Linux/macOS có hỗ trợ Python
2. Đã cài trình duyệt Google Chrome (đường dẫn mặc định là được)
3. Python 3.10+ (nhớ chọn "Add to PATH" khi cài đặt)
4. Mạng: cần proxy Mỹ, hoặc cấu hình proxy trong console

---

## II. Khởi động nhanh

### Cách 1: File Batch trên Windows

1. Lần đầu: nhấp đúp **1_setup_install_deps_and_start.bat**
2. Hàng ngày: nhấp đúp **2_start_console.bat**
3. Trình duyệt tự mở: http://127.0.0.1:8765

### Cách 2: Chạy trực tiếp bằng Python

```bash
pip install -r requirements.txt
python app.py
# Mở http://127.0.0.1:8765
```

### Chọn ngôn ngữ

Nhấp vào dropdown ngôn ngữ (góc trên bên phải) để chuyển:

- 中文 (简体) — Trung Quốc (Giản thể)
- English
- Bahasa Indonesia
- **Tiếng Việt**

Lựa chọn được lưu trong `localStorage` của trình duyệt.

> 📖 Hướng dẫn sử dụng chi tiết (tiếng Việt): **[HUONGDAN.md](HUONGDAN.md)**

---

## III. Cấu hình & thiết lập tài khoản

### 1. Cấu hình thẻ tín dụng (BẮT BUỘC)

- Vào mục **"Cấu Hình Toàn Cầu Vùng Thuế 0, Gói Pro 2 Năm Miễn Phí & Thẻ Tín Dụng"**
- Nhập thẻ Visa / Mastercard nước ngoài:
  - Số thẻ (16 chữ số)
  - Ngày hết hạn (tháng/năm, ví dụ `08/29`)
  - Mã bảo mật (CVC 3 chữ số)
  - Tên chủ thẻ bằng chữ cái Latin
  - Mã bưu chính vùng thuế 0: `97201` (Oregon, Hoa Kỳ) — mặc định, không cần đổi
- Nhấn **"💾 Lưu Cấu Hình"**
- Lưu ý: có sẵn cơ chế bảo vệ chi phí $0 nghiêm ngặt — chỉ bấm "đăng ký" khi trang checkout hiển thị **US$0.00**

### 2. Cấu hình proxy Mỹ (BẮT BUỘC để có giá $0.00)

Ở ô **"🛡️ Mẫu Proxy Toàn Cầu"** nhập proxy Mỹ. Cả 3 định dạng đều được hỗ trợ:

```
# A. host:port:user:pass
dc.decodo.com:10001:<username>:<password>

# B. http://user:pass@host:port   (khuyến nghị - chuẩn nhất)
http://<username>:<password>@dc.decodo.com:10001

# C. user:pass@host:port
<username>:<password>@dc.decodo.com:10001
```

Placeholder động: `{country}` / `{COUNTRY}` (lấy từ "Khu Vực Mục Tiêu") và `{session}` / `{SESSION}` (tự sinh theo tài khoản).

Nhấn **"🔍 Kiểm Tra Kết Nối Proxy"** để xác nhận IP ra là 🇺🇸 Hoa Kỳ.

> 🔴 **Không có proxy Mỹ → IP ra là nước khác → Google hiển thị giá nội địa, KHÔNG BAO GIỜ được $0.00.** Đây là nguyên nhân thất bại phổ biến nhất.

### 3. Nhập hàng loạt tài khoản Google

- Vào mục **"📥 Khu Vực Nhập Hàng Loạt Tài Khoản"**, dán tài khoản (mỗi dòng một tài khoản), hỗ trợ các định dạng:
  - `email----password----recovery_email`
  - `email----password----recovery_email----2FA_key`
  - `email----password----2FA_key`
- Nhấn **"➕ Nhập Danh Sách Tài Khoản Một Chạm"**

### 4. Chạy tự động

- Nhấn **"▶ Chạy Pipeline"** trên từng tài khoản, hoặc **"▶ Chạy Tự Động Toàn Bộ Tài Khoản"** ở trên cùng
- Quy trình 5 bước:
  - **Bước 1:** Tự động đăng nhập Google + xác minh qua email khôi phục / 2FA
  - **Bước 2:** Gắn thẻ thuế 0 nội tuyến + tầng 1 miễn phí 12 tháng (US$0.00)
  - **Bước 3:** Cộng dồn tầng 2 miễn phí 6 tháng (US$0.00 → 18 tháng)
  - **Bước 4:** Cộng dồn tầng 3 miễn phí 6 tháng (US$0.00 → đạt 24 tháng)
  - **Bước 5:** Tự động hủy gia hạn trên Play Store, khóa hạn 2 năm + ảnh minh chứng

---

## IV. Cấu trúc thời hạn thực tế (đã kiểm chứng)

Gói đăng ký là một **bundle** gồm 2 khoản mục, mỗi khoản mục có hạn riêng:

| Khoản mục | Dùng thử | Hạn |
|---|---|---|
| YouTube Premium Individual Add On | 1 tháng | đến 2026-12-09 |
| Google AI Pro (5 TB) | 12 tháng (deferred) | Tầng 1 → 2027-11-09 · +Tầng 2 → 2028-05-10 · +Tầng 3 → 2028-11-09 |

**Cơ chế:** mỗi lần mua thêm một offer, Google **đẩy ngày hết hạn của gói AI Pro thêm 6 tháng** (dùng balance của gói hiện tại). Trong popup checkout, trường `开始日期` của Google AI Pro chính là **ngày trial kết thúc** — dùng nó để kiểm tra tầng đã "ăn" hay chưa.

> ⚠️ **Google trả lời "success" ngay cả khi offer không làm thay đổi gì.** Vì vậy Bước 4 trong bản này tự đọc ngày hết hạn thật từ dialog "Quản lý" (Play) và tự thử token tiếp theo nếu ngày không dịch.

**Đọc ngày hết hạn thật:** trang `play.google.com/store/account/subscriptions` **không** hiển thị ngày hết hạn — chỉ có "ngày tính tiền tiếp theo". Phải bấm **管理 / Manage**, rồi đọc trong phần *套装 (bundle)*:

```
Google AI Pro (5 TB)               - 将于 2028年11月9日结束
YouTube Premium Individual Add On  - 将于 2026年12月9日结束
```

---

## V. Tính năng

- ✅ Tự động hoàn toàn: đăng nhập → xác minh → cộng dồn nhiều tầng → khóa hủy gia hạn
- ✅ Bảo vệ chi phí $0: kiểm tra $0.00 trước khi thanh toán
- ✅ Giao diện đa ngôn ngữ: Trung Quốc / English / Indonesia / **Tiếng Việt**
- ✅ Nhật ký & theo dõi tiến trình thời gian thực
- ✅ Xử lý hàng loạt tài khoản
- ✅ Hỗ trợ proxy (HTTP / HTTPS / SOCKS5), có cầu nối xác thực proxy
- ✅ Lưu trạng thái tài khoản giữa các phiên
- ✅ Ảnh minh chứng cho từng bước (screenshots/)

---

## VI. Cấu trúc thư mục

```
├── app.py                 # Backend FastAPI
├── automation_engine.py   # Logic tự động hóa Playwright
├── config.json            # Cấu hình & dữ liệu tài khoản (KHÔNG commit - chứa số thẻ)
├── requirements.txt       # Thư viện Python
├── templates/
│   └── index.html         # Giao diện web đa ngôn ngữ
├── i18n_zh_cn.json        # Bản dịch Trung Quốc
├── i18n_en_us.json        # Bản dịch English
├── i18n_id_id.json        # Bản dịch Indonesia
├── i18n_vi_vn.json        # Bản dịch Tiếng Việt
├── README.vi.md           # README tiếng Việt
├── README.id.md           # README Bahasa Indonesia
├── README.zh-CN.md        # README Trung Quốc (Giản thể)
├── HUONGDAN.md            # Hướng dẫn sử dụng chi tiết (tiếng Việt)
├── profiles/              # Profile Chrome riêng cho mỗi tài khoản (tự sinh)
└── screenshots/           # Ảnh minh chứng (tự sinh)
```

---

## VII. Đa ngôn ngữ (i18n)

Toàn bộ chữ trên giao diện đều có thể dịch:

- **i18n_zh_cn.json** — Trung Quốc (96 khóa)
- **i18n_en_us.json** — English (95 khóa)
- **i18n_id_id.json** — Indonesia (95 khóa)
- **i18n_vi_vn.json** — **Tiếng Việt (97 khóa)**

Thêm ngôn ngữ mới:

1. Tạo `i18n_[mã].json` với đầy đủ các khóa
2. Đăng ký mã trong `lang_map` trong `app.py` (hàm `load_i18n`)
3. Thêm `<option value="[mã]">Tên</option>` vào `#langSelect` trong `templates/index.html`

---

## VIII. API Endpoints

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/` | Giao diện web |
| GET | `/api/state` | Trạng thái hiện tại (tài khoản, log, cấu hình) |
| GET | `/api/i18n?lang=zh-CN\|en\|id\|vi` | Lấy bản dịch |
| POST | `/api/config` | Cập nhật cấu hình |
| POST | `/api/accounts/import` | Nhập hàng loạt tài khoản |
| POST | `/api/accounts/delete` | Xóa tài khoản |
| POST | `/api/accounts/reset` | Reset trạng thái tài khoản |
| POST | `/api/run/single` | Chạy 1 tài khoản |
| POST | `/api/run/batch` | Chạy toàn bộ tài khoản còn lại |
| POST | `/api/stop` | Dừng |
| POST | `/api/proxy/test` | Kiểm tra kết nối proxy |
| POST | `/api/open_browser` | Mở trình duyệt thủ công |

---

## IX. Xử lý sự cố

| Triệu chứng | Nguyên nhân | Cách xử lý |
|---|---|---|
| `Chrome did not open the debug port` | Chrome cũ còn giữ profile của tài khoản | Đóng mọi cửa sổ Chrome của dự án rồi chạy lại (bản vá đã tự giết, nhưng nếu vẫn lỗi thì xóa `profiles/profile_<email>`) |
| `Target page, context or browser has been closed` | Cửa sổ Chrome bị đóng giữa chừng | Chạy lại, chọn đúng bước đã dở |
| `Please fill in complete payment card info` | Thiếu thẻ | Điền thẻ ở mục cấu hình |
| Egress country ≠ US | Chưa có proxy Mỹ | Cấu hình proxy Mỹ rồi kiểm tra lại |
| Không ra giá $0.00 | IP sai quốc gia hoặc tài khoản không đủ điều kiện | Xem dòng log IP trong log |
| `Batch queue is already running` | Hàng đợi cũ còn treo | Nhấn **⏹ Dừng Tác Vụ** hoặc khởi động lại server |
| `407 Unauthorized` khi test proxy | Sai user/password hoặc sai định dạng | Copy-paste thẳng từ dashboard nhà cung cấp — chữ `I` (i hoa) và `l` (i thường) trông giống nhau |

**Port đã dùng:** sửa `uvicorn.run(app, host="127.0.0.1", port=8765, ...)` ở cuối `app.py`.

**Không tìm thấy Chrome:** đảm bảo Chrome đã cài ở đường dẫn mặc định, hoặc đặt biến môi trường `CHROME_PATH`.

---

## X. Tham khảo

- Dự án gốc: https://github.com/worldonlyu/Google_AI_Pro_2Year_ZeroCost_Auto
- Fork i18n: https://github.com/gemhelixx17/google-ai-pro
- Bản tiếng Việt + sửa lỗi pipeline: https://github.com/nguyenquanghiep3404/google-ai-pro-viet-hoa

---

**Giấy phép:** Theo điều khoản của dự án gốc.

## ⚠️ Cảnh báo

Công cụ này tự động hóa việc đăng ký Google AI Pro trên **nhiều tài khoản** và gắn thẻ tín dụng. Sử dụng hàng loạt tài khoản có thể **vi phạm Điều khoản Dịch vụ của Google** và khiến tài khoản bị khóa. Chỉ dùng với tài khoản bạn sở hữu hợp pháp, và tự chịu trách nhiệm với mọi hậu quả.
