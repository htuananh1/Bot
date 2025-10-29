# ⚡ Quick Start Guide - Discord Game Bot

Hướng dẫn nhanh để chạy bot trong 5 phút!

## 🚀 Cách 1: Chạy với Docker (Khuyến nghị)

### Yêu cầu
- Docker và Docker Compose đã cài đặt
- Discord Bot Token

### Tạo Discord Bot

1. Truy cập [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"** → Đặt tên bot
3. Vào tab **"Bot"** → Click **"Add Bot"**
4. Copy **Bot Token** (giữ kỹ, chỉ hiện 1 lần!)
5. Bật **Privileged Gateway Intents**:
   - ✅ **Message Content Intent**
   - ✅ **Server Members Intent**
6. Vào tab **"OAuth2"** → **"URL Generator"**
   - Scopes: Chọn `bot` và `applications.commands`
   - Bot Permissions: Chọn `Send Messages`, `Read Messages`, `Embed Links`
   - Copy URL và mở để invite bot vào server

### Các bước chạy bot

1. **Clone repository**
```bash
git clone <repository-url>
cd discord-game-bot
```

2. **Tạo file .env**
```bash
cp .env.example .env
nano .env  # Hoặc dùng editor bạn thích
```

Thêm token:
```env
DISCORD_TOKEN=your_bot_token_here
```

3. **Chạy bot**
```bash
docker-compose up -d
```

4. **Kiểm tra**
```bash
# Xem logs
docker-compose logs -f discord-bot

# Kiểm tra health
curl http://localhost:8080/health
```

5. **Thử nghiệm trên Discord**
- Mở Discord server đã invite bot
- Gửi `!start` hoặc `!help`
- Bot sẽ trả lời!

✅ **Xong!** Bot đã sẵn sàng!

---

## 🐍 Cách 2: Chạy với Python

### Yêu cầu
- Python 3.11+
- pip

### Các bước

1. **Clone và setup**
```bash
git clone <repository-url>
cd discord-game-bot

# Tạo virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Cài đặt dependencies
pip install -r requirements.txt
```

2. **Tạo Discord Bot** (như hướng dẫn ở trên)

3. **Cấu hình**
```bash
cp .env.example .env
nano .env
```

Thêm token:
```env
DISCORD_TOKEN=your_bot_token_here
```

4. **Chạy**
```bash
python main.py
```

hoặc

```bash
chmod +x start.sh
./start.sh
```

5. **Thử nghiệm bot trên Discord**

---

## ☁️ Deploy lên Cloud trong 5 phút

### Railway (Dễ nhất)

1. Fork repository này trên GitHub
2. Truy cập [railway.app](https://railway.app) và đăng nhập
3. Click **"New Project"** → **"Deploy from GitHub"**
4. Chọn repository đã fork
5. Trong **Variables**, thêm:
   - Key: `DISCORD_TOKEN`
   - Value: Token bot của bạn
6. Click **"Deploy"**

✅ Bot sẽ online trong < 2 phút!

### Fly.io (Free tier tốt)

```bash
# Cài đặt Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Deploy (từ thư mục project)
fly launch --no-deploy

# Set secrets
fly secrets set DISCORD_TOKEN=your_token_here

# Deploy
fly deploy
```

✅ Bot online trong < 3 phút!

---

## 🎮 Sử dụng Bot

### Lệnh cơ bản

```
!start       - Bắt đầu chơi
!help        - Xem danh sách lệnh
!balance     - Xem số dư (alias: !bal, !money)
```

### Game kiếm tiền

```
!work        - Làm việc kiếm tiền (cooldown 20 phút)
!daily       - Nhận quà hằng ngày
!dice        - Chơi xúc xắc may rủi
!slots       - Quay hũ slot machine
```

### Game phiêu lưu

```
!fish        - Chiến dịch câu cá
!mine        - Khai thác hầm mỏ
```

### Game trí tuệ (cần AI key)

```
!wordchain   - Nối từ với AI
!vietking    - Thử thách Vua Tiếng Việt
```

---

## 🔧 Tùy chỉnh

### Đổi Command Prefix

Mặc định bot dùng `!`. Để đổi sang `?` hay `/`:

```env
# .env
COMMAND_PREFIX=?
```

Sau đó restart bot.

### Thêm Discord Webhook

Để bot gửi notifications qua webhook:

1. Tạo webhook trong Discord channel:
   - Click vào channel settings (⚙️)
   - Integrations → Webhooks → New Webhook
   - Copy Webhook URL

2. Thêm vào `.env`:
```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

---

## 🆘 Troubleshooting

### Bot không khởi động

**Kiểm tra:**
```bash
# Xem logs
docker-compose logs -f discord-bot

# Hoặc với Python
python main.py
```

**Lỗi thường gặp:**
- `Missing DISCORD_TOKEN` → Chưa set token
- `Invalid token` → Token sai hoặc hết hạn
- `Privileged intent` → Chưa bật intents trong Developer Portal

### Bot không trả lời

1. **Kiểm tra bot online chưa**
   - Bot có tên màu xanh trong server không?

2. **Kiểm tra quyền bot**
   - Bot có quyền `Read Messages` và `Send Messages` không?
   - Right-click server → Server Settings → Roles → Xem quyền bot

3. **Kiểm tra prefix**
   - Mặc định là `!`
   - Thử `!help` hoặc `!start`

4. **Xem logs**
   ```bash
   docker-compose logs -f discord-bot
   ```

### Port bị chiếm

Nếu port 8080 đã được dùng:

```env
# .env
WEBHOOK_PORT=8081
```

Restart bot.

---

## 📊 Commands Overview

| Command | Mô tả | Cooldown |
|---------|-------|----------|
| `!start` | Welcome message | - |
| `!help` | Danh sách lệnh | - |
| `!balance` | Xem số dư | - |
| `!work` | Làm việc kiếm tiền | 20 phút |
| `!daily` | Nhận quà | 20 giờ |
| `!dice` | Xúc xắc | - |
| `!slots` | Quay hũ | - |
| `!fish` | Câu cá | - |
| `!mine` | Khai mỏ | - |
| `!wordchain` | Nối từ AI | - |
| `!vietking` | Vua TV | - |

---

## 🎉 Hoàn thành!

Bot của bạn giờ đã sẵn sàng! Hãy thử các game và tận hưởng nhé! 🚀

**Tips:**
- Dùng `!daily` mỗi ngày để tăng streak bonus
- Dùng `!work` mỗi 20 phút để kiếm tiền
- `!fish` và `!mine` có thể cho jackpot lớn!

Cần trợ giúp? Xem [README.md](README.md) để biết thêm chi tiết!
