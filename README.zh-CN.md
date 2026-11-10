=======================================================================
Google AI Pro (5 TB) 零成本两年全自动控制台
=======================================================================

[English](README.md) | [Bahasa Indonesia](README.id.md) | [Tiếng Việt](README.vi.md) | **中文 (简体)**

**多语言支持：** 中文 (简体) | English | Bahasa Indonesia (Indonesia) | Tiếng Việt (越南语)

> ⚠️ **免责声明：** 本项目以开源形式提供，仅供社区分析与学习使用。批量自动化注册可能违反 Google 服务条款。

> 📖 详细使用指南（越南语）：**[HUONGDAN.md](HUONGDAN.md)**

---

## 一、系统要求

1. Windows 10 / 11，或支持 Python 的 Linux/macOS
2. 已安装 Google Chrome 浏览器（默认路径即可）
3. Python 3.10 以上（安装时请勾选 "Add to PATH"）
4. 网络：需要本地美国代理，或在控制台中配置代理模板

---

## 二、快速开始

### 方式一：Windows 批处理文件

1. 首次运行：双击 **1_setup_install_deps_and_start.bat**
2. 日常使用：双击 **2_start_console.bat**
3. 浏览器会自动打开：http://127.0.0.1:8765

### 方式二：手动运行 Python

```bash
pip install -r requirements.txt
python app.py
# 打开 http://127.0.0.1:8765
```

### 语言切换

点击右上角的语言下拉菜单进行切换：

- 中文 (简体) — 简体中文
- English
- Bahasa Indonesia
- Tiếng Việt — 越南语

语言偏好保存在浏览器的 `localStorage` 中。

---

## 三、配置与账号设置

### 1. 信用卡配置（必填）

- 进入 **"全球免税区域、两年零成本 Pro 方案与银行卡配置"** 区域
- 填写 Visa / Mastercard 外币卡：
  - 卡号（16 位）
  - 有效期（月/年，例如 `08/29`）
  - 安全码（CVC，3 位）
  - 持卡人姓名（使用拉丁字母）
  - 免税邮编：`97201`（美国俄勒冈州）—— 默认值，无需修改
- 点击 **"💾 保存配置"**
- 注意：内置严格的 $0 费用保护，只有当结账页显示 **US$0.00** 时才会点击"订阅"

### 2. 配置美国代理（必须，否则无法获得 $0.00 定价）

在 **"🛡️ 全局代理模板"** 输入框中填入美国代理。支持以下三种格式：

```
# A. host:port:user:pass
dc.decodo.com:10001:<username>:<password>

# B. http://user:pass@host:port   （推荐，最标准）
http://<username>:<password>@dc.decodo.com:10001

# C. user:pass@host:port
<username>:<password>@dc.decodo.com:10001
```

动态占位符：`{country}` / `{COUNTRY}`（取自"目标区域"）与 `{session}` / `{SESSION}`（按账号自动生成）。

点击 **"🔍 测试代理连通性"** 确认出口 IP 为 🇺🇸 美国。

> 🔴 **没有美国代理 → 出口 IP 位于其他国家 → Google 显示当地货币价格，永远拿不到 $0.00。** 这是最常见的失败原因。

### 3. 批量导入 Google 账号

- 在 **"📥 批量账号导入区"** 粘贴账号（每行一个），支持以下格式：
  - `email----password----recovery_email`
  - `email----password----recovery_email----2FA_key`
  - `email----password----2FA_key`
- 点击 **"➕ 一键导入账号列表"**

### 4. 全自动执行

- 在单个账号上点击 **"▶ 开始运行"**，或点击顶部的 **"▶ 一键运行全部待处理账号"**
- 自动化流程：
  - **第 1 步：** 自动登录 Google + 恢复邮箱 / 2FA 验证
  - **第 2 步：** 内联绑定免税卡 + 第 1 层 12 个月免费（US$0.00）
  - **第 3 步：** 叠加第 2 层 6 个月免费（US$0.00 → 18 个月）
  - **第 4 步：** 叠加第 3 层 6 个月免费（US$0.00 → 满 24 个月）
  - **第 5 步：** 在 Play 商店自动关闭自动续订，锁定 2 年到期日 + 截图存证

---

## 四、功能特性

- ✅ 全自动化：登录 → 验证 → 多层叠加 → 锁定退订
- ✅ 零成本保护：结账前校验 $0.00
- ✅ 多语言界面：中文 / English / Indonesia / 越南语
- ✅ 实时日志与进度监控
- ✅ 批量账号处理
- ✅ 代理支持（HTTP / HTTPS / SOCKS5），内置代理认证桥接
- ✅ 账号状态持久化
- ✅ 每一步的证明截图（screenshots/）

---

## 五、免费周期的真实结构（已实测验证）

订阅实际上是一个由两个项目组成的 **套装（bundle）**，各自有独立的结束日期：

| 项目 | 试用 | 结束日期 |
|---|---|---|
| YouTube Premium Individual Add On | 1 个月 | 例如 2026-12-09 |
| Google AI Pro (5 TB) | 12 个月（递延） | 第 1 层 → 2027-11-09 · +第 2 层 → 2028-05-10 · +第 3 层 → 2028-11-09 |

**机制：** 每多购买一个 offer，Google 就会利用当前套餐的余额，把 Google AI Pro 的结束日期 **往后推 6 个月**。在结账弹窗中，Google AI Pro 的 `开始日期` 字段实际就是 **试用结束日期**，可据此判断某一层是否真正生效。

> ⚠️ **即使 offer 毫无变化，Google 也会返回"成功"。** 因此本版本的第 4 步会从 Play 的 [管理] 对话框读取真实结束日期，若日期没有前移则自动尝试下一个 offer token。

**如何读取真实到期日：** `play.google.com/store/account/subscriptions` 只会显示 *下次扣款日期*，并不显示到期日。请点击 **管理 / Manage**，然后查看 *套装* 区域：

```
Google AI Pro (5 TB)               - 将于 2028年11月9日结束
YouTube Premium Individual Add On  - 将于 2026年12月9日结束
```

---

## 六、文件结构

```
├── app.py                 # FastAPI 后端
├── automation_engine.py   # Playwright 自动化逻辑
├── config.json            # 用户配置与账号数据（不要提交，含卡号）
├── requirements.txt      # Python 依赖
├── templates/
│   └── index.html       # 多语言 Web 界面
├── i18n_zh_cn.json      # 中文翻译
├── i18n_en_us.json      # 英文翻译
├── i18n_id_id.json      # 印尼语翻译
├── i18n_vi_vn.json      # 越南语翻译
├── README.vi.md         # 越南语说明文档
├── HUONGDAN.md          # 详细使用指南（越南语）
└── screenshots/         # 账号证明截图
```

---

## 七、国际化（i18n）

界面上的所有文字均可翻译：

- **i18n_zh_cn.json** — 简体中文（96 个键）
- **i18n_en_us.json** — English（95 个键）
- **i18n_id_id.json** — Bahasa Indonesia（95 个键）
- **i18n_vi_vn.json** — Tiếng Việt（97 个键）

添加新语言：

1. 创建 `i18n_[语言代码].json` 并写齐所有键
2. 在 `app.py` 的 `lang_map`（`load_i18n` 函数）中注册语言代码
3. 在 `templates/index.html` 的 `#langSelect` 中添加 `<option>` 选项

---

## 八、API 接口

| 方法 | 接口 | 说明 |
|---|---|---|
| GET | `/` | Web 界面 |
| GET | `/api/state` | 当前状态（账号、日志、配置） |
| GET | `/api/i18n?lang=zh-CN\|en\|id\|vi` | 获取翻译 |
| POST | `/api/config` | 更新配置 |
| POST | `/api/accounts/import` | 批量导入账号 |
| POST | `/api/accounts/delete` | 删除账号 |
| POST | `/api/accounts/reset` | 重置账号状态 |
| POST | `/api/run/single` | 运行单个账号 |
| POST | `/api/run/batch` | 运行全部待处理账号 |
| POST | `/api/stop` | 停止 |
| POST | `/api/proxy/test` | 测试代理连通性 |
| POST | `/api/open_browser` | 手动打开浏览器 |

---

## 九、问题排查

| 现象 | 原因 | 处理方法 |
|---|---|---|
| `Chrome did not open the debug port` | 残留的 Chrome 窗口仍占用该账号的 profile | 关闭本项目打开的所有 Chrome 窗口后重试（本版本也会自动清理） |
| `Target page, context or browser has been closed` | Chrome 窗口在执行中被关闭 | 重新运行，选择正确的起始步骤 |
| `Please fill in complete payment card info` | 未填写银行卡 | 在配置面板补全卡号、有效期、CVC |
| 出口国家 ≠ US | 未配置美国代理 | 配置美国代理后重新测试 |
| 价格不是 $0.00 | IP 所在国家不对，或账号不符合条件 | 查看日志中的 IP 行 |
| `Batch queue is already running` | 上一批任务卡死 | 点击 **⏹ 停止任务**，或重启服务 |
| 测试代理返回 `407 Unauthorized` | 用户名或密码错误 | 直接从代理商后台复制粘贴：`I`（大写 i）与 `l`（小写 L）非常相似 |

**端口被占用：** 修改 `app.py` 末尾的 `uvicorn.run(app, host="127.0.0.1", port=8765, ...)`。

**找不到 Chrome：** 确认 Chrome 安装在默认路径，或设置环境变量 `CHROME_PATH`。

---

## 十、参考链接

- 原始项目：https://github.com/worldonlyu/Google_AI_Pro_2Year_ZeroCost_Auto
- i18n 分支：https://github.com/gemhelixx17/google-ai-pro
- 越南语分支 + Windows 流水线修复：https://github.com/nguyenquanghiep3404/google-ai-pro-viet-hoa

---

**许可协议：** 遵循原始项目的条款。

## ⚠️ 警告

本工具会在 **多个账号** 上自动注册 Google AI Pro 并绑定银行卡。批量使用账号可能 **违反 Google 服务条款** 并导致账号被封。请仅使用你合法拥有的账号，并自行承担一切后果。
