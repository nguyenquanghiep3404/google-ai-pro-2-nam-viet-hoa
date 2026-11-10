========================================================================  
Google AI Pro (5 TB) Zero-Cost 2-Year Full Auto Console  
========================================================================  

**Multilingual Support:** 中文 (Chinese) | English | Bahasa Indonesia (Indonesian) | Tiếng Việt (Vietnamese)

Disclaimer: This project is provided as open-source for community analysis and learning purposes.

## I. System Requirements

1. Windows 10 / 11 or Linux/macOS with Python support
2. Google Chrome browser installed (default path OK)
3. Python 3.10+ (add to PATH during installation)
4. Network: US proxy enabled locally, or configure proxy template in console

## II. Quick Start

### Option 1: Windows Batch Files
1. First run: double-click **1_首次运行_安装依赖并启动.bat**
2. Daily use: double-click **2_启动控制台.bat**
3. Browser opens automatically: http://127.0.0.1:8765

### Option 2: Manual Python
```bash
pip install -r requirements.txt
python app.py
# Open http://127.0.0.1:8765
```

### Language Selection
- Click language dropdown (top-right) to switch:
  - 中文 (简体) - Chinese Simplified
  - English
  - Bahasa Indonesia
  - Tiếng Việt - Vietnamese

## III. Configuration & Account Setup

### 1. Credit Card Configuration (Required)
- Navigate to **Global Config & Tax-Free Card Binding** section
- Enter Visa / Mastercard foreign currency card:
  * Card number (16 digits)
  * Expiration (month/year, e.g. 08/29)
  * Security code (3-digit CVC)
  * Cardholder English name
  * Tax-free postal code: 97201 (Oregon, US) — default, no change needed
- Click **Save Configuration**
- Note: Built-in strict $0 cost protection; only clicks subscribe when checkout shows US$0.00

### 2. Bulk Import Google Accounts
- In **Bulk Account Import** section, paste accounts (one per line), supports formats:
  * email----password----recovery_email
  * email----password----recovery_email----2FA_key
  * email----password----2FA_key
- Click **One-Click Import Account List**

### 3. Fully Automated Execution
- Click **Start Pipeline** on individual account or **One-Click Run All Pending** at top
- Automation completes:
  - **Step 1:** Auto login Google + recovery email / 2FA verification
  - **Step 2:** Inline tax-free card binding + tier 1 12-month free (US$0.00)
  - **Step 3:** Stack tier 2 6-month free (US$0.00 → 18 months)
  - **Step 4:** Stack tier 3 6-month free (US$0.00 → 24 months cap)
  - **Step 5:** Auto cancel auto-renew on Play Store, lock 2-year expiry + screenshot proof

## IV. Features

- ✅ Full automation: login → verification → multi-tier stacking → unsubscribe lock
- ✅ Zero-cost protection: validates $0.00 before checkout
- ✅ Multi-language UI: Chinese / English / Indonesian
- ✅ Real-time logs & progress monitoring
- ✅ Batch account processing
- ✅ Proxy support (HTTP/HTTPS/SOCKS5)
- ✅ Account status persistence

## V. File Structure

```
├── app.py                 # FastAPI backend
├── automation_engine.py   # Playwright automation logic
├── config.json           # User config & account data
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html       # Multi-language web UI
├── i18n_zh_cn.json      # Chinese translations
├── i18n_en_us.json      # English translations
├── i18n_id_id.json      # Indonesian translations
├── i18n_vi_vn.json      # Vietnamese translations
└── screenshots/         # Account proof screenshots
```

## VI. Internationalization (i18n)

All UI text is translatable:
- **i18n_zh_cn.json** - Chinese Simplified (96 keys)
- **i18n_en_us.json** - English (95 keys)
- **i18n_id_id.json** - Indonesian (95 keys)
- **i18n_vi_vn.json** - Vietnamese (97 keys)

Language preference stored in browser localStorage. Add new languages by:
1. Creating `i18n_[lang].json` with all keys
2. Registering the code in `lang_map` inside `app.py` (`load_i18n`)
3. Adding option to language selector in `templates/index.html`

## VII. API Endpoints

- `GET /` - Web UI
- `GET /api/state` - Current state (accounts, logs, config)
- `GET /api/i18n?lang=zh-CN|en|id|vi` - Get translations
- `POST /api/config` - Update configuration
- `POST /api/accounts/import` - Bulk import accounts
- `POST /api/accounts/delete` - Delete account
- `POST /api/accounts/reset` - Reset account state
- `POST /api/run/single` - Run single account
- `POST /api/run/batch` - Run all pending accounts
- `POST /api/stop` - Stop execution
- `POST /api/proxy/test` - Test proxy connectivity
- `POST /api/open_browser` - Manual browser control

## VIII. Troubleshooting

**Port already in use:**
```bash
python app.py --port 9000
```

**Chrome not found:**
- Ensure Chrome is installed in default path
- Or set `CHROME_PATH` environment variable

**Proxy issues:**
- Test proxy in UI using **Test Proxy Connectivity** button
- Verify credentials and format

## IX. References

Original project: https://github.com/worldonlyu/Google_AI_Pro_2Year_ZeroCost_Auto

i18n fork: https://github.com/gemhelixx17/google-ai-pro

---

**License:** As per original project terms
