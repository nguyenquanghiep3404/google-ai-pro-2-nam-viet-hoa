# Hướng Dẫn Sử Dụng — Google AI Pro (5 TB) Console Tự Động

> Giao diện: http://127.0.0.1:8765 · Đổi ngôn ngữ ở dropdown góc trên bên phải (Tiếng Việt / English / Bahasa Indonesia / 中文)
>
> [English](README.md) | [Bahasa Indonesia](README.id.md) | **Tiếng Việt** | [中文 (简体)](README.zh-CN.md)

---

## 1. Khởi động & Dừng chương trình

```bash
# Chạy lần đầu (cài deps + mở trình duyệt)
1_setup_install_deps_and_start.bat

# Chạy thường ngày
2_start_console.bat
```

Hoặc thủ công:

```bash
pip install -r requirements.txt
python app.py
```

Dừng: nhấn `Ctrl + C` trong cửa sổ console. Đổi cổng: `python app.py --port 9000` *(chưa hỗ trợ, sửa `uvicorn.run` dòng cuối `app.py`)*.

> **Lưu ý:** Server phải chạy trong cửa sổ console (không đóng) trong suốt quá trình tự động hóa.

---

## 2. Thiết lập bắt buộc (theo thứ tự)

### 2.1 Thẻ tín dụng quốc tế — BẮT BUỘC

Ở khung **"Cấu Hình Toàn Cầu Vùng Thuế 0..."**, điền:

| Trường | Giá trị |
|---|---|
| Số thẻ | Visa/Mastercard 16 số (thẻ nội địa VN sẽ không dùng được) |
| Ngày hết hạn | MM / YY — ví dụ `09` / `28` |
| Mã bảo mật | CVC 3 số |
| Tên chủ thẻ | Chữ cái Latin, ví dụ `NGUYEN QUANG HIEP` |
| Địa chỉ | `700 SW 5th Ave` (mặc định) |
| Mã bưu chính | `97201` · Tiểu bang `OR` (Oregon — vùng thuế 0, **giữ nguyên**) |

Nhấn **"💾 Lưu Cấu Hình"**.

⚠️ **Thiếu thẻ → pipeline dừng ngay ở Bước 2** với thông báo *"Please fill in complete payment card info"*.

### 2.2 Proxy Mỹ — BẮT BUỘC để được giá $0.00

Ở ô **"🛡️ Mẫu Proxy Toàn Cầu"** nhập proxy Mỹ. **Cả 3 định dạng sau đều được hỗ trợ:**

```
# A. host:port:user:pass
dc.decodo.com:10001:<username>:<password>

# B. http://user:pass@host:port  (khuyến nghị - chuẩn nhất)
http://<username>:<password>@dc.decodo.com:10001

# C. user:pass@host:port
<username>:<password>@dc.decodo.com:10001
```

> ⚠️ Copy-paste thẳng từ dashboard nhà cung cấp — **chữ `I` (i hoa) và `l` (i thường) trông giống nhau**, gõ nhầm sẽ ra `407 Unauthorized`.

**Placeholder động** (khi dùng proxy rotating, mỗi tài khoản 1 node riêng):

| Placeholder | Ý nghĩa |
|---|---|
| `{country}` / `{COUNTRY}` | Quốc gia, lấy từ "Khu Vực Mục Tiêu" (để `US`) |
| `{session}` / `{SESSION}` | Chuỗi session ngẫu nhiên, tự sinh theo tài khoản |

Ví dụ:
```
http://user:pass@gate.provider.com:1234?country={country}&session={SESSION}
```

Nếu dùng **FloppyData**, chỉ cần điền **API key 32 ký tự** (không có `:` hoặc `@`) — chương trình tự gọi API và dựng sẵn proxy dạng:
`geo.g-w.info:10080` với `type-residential-country-US-session-...`

Nhấn **"🔍 Kiểm Tra Kết Nối Proxy"** để xác nhận IP ra là **🇺🇸 US**.
Kết quả mong đợi: `✅ Connection Successful！Egress IP: <ip> (United States · <city>)`

> 🔴 **Không có proxy Mỹ → IP ra là VN (Hanoi) → Google hiển thị giá VND, KHÔNG BAO GIỜ được $0.00.** Đây là nguyên nhân thất bại phổ biến nhất. Sau khi chạy, kiểm tra dòng log `🌐 Independent environment egress IP check passed` — nếu quốc gia ≠ `US` thì dừng và sửa proxy.

### 2.3 Nhập tài khoản

Ô **"📥 Khu Vực Nhập Hàng Loạt Tài Khoản"**, mỗi dòng một tài khoản. Dấu phân cách linh hoạt (`----`, `/`, `|`, khoảng trắng):

```
email----password----recovery_email
email----password----recovery_email----2FA_key
email----password----2FA_key
```

Nhấn **"➕ Nhập Danh Sách Tài Khoản Một Chạm"**.

> `recovery_email` = email dự phòng dùng để nhận mã xác minh. `2FA_key` = khóa TOTP dạng base32 (dùng để tự sinh OTP). Thiếu cả hai → tài khoản dùng xác minh bằng email, Google sẽ gửi mã vào recovery email.

---

## 3. Chạy Pipeline

| Nút | Tác dụng |
|---|---|
| **▶ Chạy Pipeline** (trong từng dòng) | Chạy 1 tài khoản, chọn điểm bắt đầu bằng dropdown cạnh nút |
| **▶ Chạy Tự Động Toàn Bộ Tài Khoản** (trên cùng) | Chạy hàng loạt tất cả tài khoản chưa `completed` |
| **🌐 Trình duyệt** | Mở Chrome thủ công cho tài khoản để xử lý reCAPTCHA bằng tay |
| **⏹ Dừng** / **⏹ Dừng Tác Vụ** | Dừng tài khoản đó / dừng cả hàng đợi |

**Chọn điểm bắt đầu** (dropdown "Batch Execution Start Step"):

| Bước | Dùng khi |
|---|---|
| 1 | Tài khoản mới — chạy trọn 5 bước |
| 2 | Đã đăng nhập xong, chỉ cần cộng dồn 3 tầng $0 |
| 3 | Đã có 12 tháng — chạy tầng 2 + 3 |
| 4 | Đã có 18 tháng — cộng dồn đủ 24 tháng + hủy gia hạn |
| 5 | Chỉ hủy tự động gia hạn trên Google Play |

### Quy trình 5 bước

```
Bước 1 · Đăng Nhập & Xác Minh      → tự điền email/mật khẩu, xử lý email khôi phục hoặc OTP 2FA
Bước 2 · Tầng 1 Miễn Phí 12 Tháng  → Pro 5TB 12 tháng + dùng thử YT (tự gắn thẻ nếu chưa có)
Bước 3 · Tầng 2 Cộng Dồn 6 Tháng   → S25 Pro 6 tháng → mở rộng lên 18 tháng
Bước 4 · Tầng 3 Cộng Dồn 6 Tháng   → Pixel 6 tháng → đủ 24 tháng (2028-10)
Bước 5 · Tự Động Hủy Gia Hạn       → hủy gia hạn trên Play Store + chụp ảnh minh chứng US$0.00
```

Chương trình chỉ bấm "đăng ký" khi trang checkout hiển thị **US$0.00** — có bảo vệ chi phí $0.

#### Cấu trúc thời hạn (đã kiểm chứng thực tế)

Gói là một **bundle** 2 khoản mục, mỗi khoản mục có hạn riêng:

| Khoản mục | Trial | Hạn |
|---|---|---|
| YouTube Premium Individual Add On | 1 tháng | đến 2026-12-09 |
| Google AI Pro (5 TB) | 12 tháng (deferred) | Tier 1 → 2027-11-09 · +Tier 2 → 2028-05-10 · +Tier 3 → 2028-11-09 |

Cơ chế: mỗi lần mua thêm 1 offer, Google **đẩy ngày hết hạn của gói AI Pro thêm 6 tháng** (dùng balance của gói hiện tại). Trong popup checkout, trường `开始日期` của Google AI Pro chính là **ngày trial kết thúc** — dùng nó để kiểm tra tầng đã ăn hay chưa.

> ⚠️ **Google trả lời "success" ngay cả khi offer không làm thay đổi gì.** Bước 4 đã được sửa để đọc ngày hết hạn thật từ dialog "Quản lý" (Play) và tự thử token tiếp theo nếu ngày không dịch.

#### Đọc ngày hết hạn thật

Trang `play.google.com/store/account/subscriptions` **không** hiển thị ngày hết hạn — chỉ có "ngày tính tiền tiếp theo". Phải bấm **管理 / Manage** rồi đọc trong phần *套装 (bundle)*:

```
Google AI Pro (5 TB)               - 将于 2028年11月9日结束
YouTube Premium Individual Add On  - 将于 2026年12月9日结束
```

### Theo dõi tiến trình

- Cột **"Tiến Trình Pipeline"** hiện 5 chấm (1→5), chấm xanh = đã xong, chấm vàng = đang chạy
- Khung **"Nhật Ký Thực Thi"** phía dưới là log thời gian thực
- Cột **"Ảnh Chứng Minh"** → nút 🖼 Xem để xem ảnh chụp sau mỗi bước

---

## 4. Xử lý reCAPTCHA / xác minh thủ công

Khi gặp reCAPTCHA, trạng thái tài khoản chuyển sang **"🖐️ Đang Chờ CAPTCHA"** và cửa sổ Chrome tự bật lên:

1. Nhấn **🌐 Trình duyệt** nếu cửa sổ chưa hiện
2. Giải CAPTCHA trong cửa sổ Chrome đó
3. Quay lại web console, bấm **▶ Chạy Pipeline** với **Bước 2** để tiếp tục từ điểm dừng

> ⚠️ **Quan trọng:** sau khi giải CAPTCHA xong, **đóng cửa sổ Chrome** đó. Nếu để mở, lần chạy sau sẽ không mở được cổng debug (Chrome chỉ cho phép 1 instance trên 1 profile) → lỗi *"Chrome debug port did not start"*. Bản vá hiện tại đã tự giết Chrome cũ, nhưng đóng cửa sổ vẫn là cách chắc chắn nhất.

---

## 5. Bảng lỗi thường gặp

| Triệu chứng | Nguyên nhân | Cách xử lý |
|---|---|---|
| `Chrome did not open the debug port` | Chrome cũ còn giữ profile | Đóng mọi cửa sổ Chrome của dự án, rồi chạy lại (bản vá tự giết, nhưng nếu vẫn lỗi → xóa thư mục `profiles/profile_<email>`) |
| `Target page, context or browser has been closed` | Cửa sổ Chrome bị đóng giữa chừng | Chạy lại, chọn đúng bước đã dở |
| `Please fill in complete payment card info` | Thiếu thẻ | Điền thẻ ở 2.1 |
| Egress country ≠ US | Chưa có proxy Mỹ | Cấu hình proxy ở 2.2 |
| Không ra giá $0.00 | IP sai quốc gia hoặc tài khoản không đủ điều kiện | Xem log IP, kiểm tra proxy |
| `Batch queue is already running` | Hàng đợi cũ còn treo | Nhấn **⏹ Dừng Tác Vụ**, hoặc khởi động lại server |
| Log không hiện dòng mới | Server in lỗi encoding (đã sửa) | Khởi động lại server |

---

## 6. Cấu trúc thư mục & dữ liệu

```
├── app.py                 # FastAPI backend
├── automation_engine.py   # Logic tự động hóa Playwright
├── config.json            # Cấu hình + dữ liệu tài khoản (tự sinh)
├── profiles/              # Profile Chrome riêng cho mỗi tài khoản (tự sinh)
├── screenshots/           # Ảnh chứng minh sau mỗi bước (tự sinh)
├── templates/index.html   # Giao diện web đa ngôn ngữ
├── i18n_zh_cn.json        # 中文
├── i18n_en_us.json        # English
├── i18n_id_id.json        # Bahasa Indonesia
└── i18n_vi_vn.json        # Tiếng Việt
```

Mỗi tài khoản có profile Chrome riêng tại `profiles/profile_<email>`. Xóa thư mục đó = bắt đầu lại từ đầu với tài khoản đó (kể cả session đăng nhập).

### API endpoints

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/api/state` | Trạng thái hiện tại (tài khoản, log, cấu hình) |
| GET | `/api/i18n?lang=vi\|en\|id\|zh-CN` | Bản dịch |
| POST | `/api/config` | Cập nhật cấu hình + thẻ |
| POST | `/api/accounts/import` | Nhập danh sách tài khoản |
| POST | `/api/accounts/delete` | Xóa tài khoản |
| POST | `/api/accounts/reset` | Reset về `pending` |
| POST | `/api/run/single` | Chạy 1 tài khoản |
| POST | `/api/run/batch` | Chạy hàng loạt |
| POST | `/api/stop` | Dừng |
| POST | `/api/proxy/test` | Test proxy |
| POST | `/api/open_browser` | Mở Chrome thủ công |

---

## 7. Thêm ngôn ngữ mới

1. Tạo `i18n_[mã].json` với đầy đủ các khóa (xem `i18n_vi_vn.json` làm mẫu)
2. Đăng ký trong `app.py` → `load_i18n()` → `lang_map`
3. Thêm `<option value="[mã]">Tên</option>` trong `templates/index.html` → `#langSelect`

---

## ⚠️ Cảnh báo

Công cụ này tự động hóa việc đăng ký Google AI Pro trên **nhiều tài khoản** và gắn thẻ tín dụng. Việc sử dụng hàng loạt tài khoản có thể **vi phạm Điều khoản Dịch vụ của Google** và khiến tài khoản bị khóa. Chỉ dùng với tài khoản bạn sở hữu hợp pháp, và tự chịu trách nhiệm với mọi hậu quả.
