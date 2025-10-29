# ⚡ Quick Start Guide

Hướng dẫn nhanh để chạy bot trong 5 phút!

## 🚀 Cách 1: Chạy với Docker (Khuyến nghị)

### Yêu cầu
- Docker và Docker Compose đã cài đặt
- Bot token từ [@BotFather](https://t.me/BotFather)

### Các bước

1. **Clone repository**
```bash
git clone <repository-url>
cd telegram-game-bot
```

2. **Tạo file .env**
```bash
cp .env.example .env
nano .env  # Hoặc dùng editor bạn thích
```

Chỉnh sửa và thêm token của bạn:
```env
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

3. **Chạy bot**
```bash
./start.sh
# Hoặc
docker-compose up -d
```

4. **Kiểm tra**
```bash
# Xem logs
docker-compose logs -f

# Kiểm tra health
curl http://localhost:8080/health
```

5. **Thử nghiệm**
- Mở Telegram
- Tìm bot của bạn
- Gửi `/start`

✅ **Xong!** Bot đã sẵn sàng hoạt động!

---

## 🐍 Cách 2: Chạy với Python

### Yêu cầu
- Python 3.11+
- pip

### Các bước

1. **Clone và setup**
```bash
git clone <repository-url>
cd telegram-game-bot

# Tạo virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Cài đặt dependencies
pip install -r requirements.txt
```

2. **Cấu hình**
```bash
cp .env.example .env
nano .env
```

Thêm token:
```env
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

3. **Chạy**
```bash
python main.py
```

hoặc

```bash
./start.sh
```

4. **Thử nghiệm bot**
- Mở Telegram và tìm bot
- Gửi `/start` để bắt đầu

---

## ☁️ Deploy lên Cloud trong 5 phút

### Railway (Dễ nhất)

1. Fork repository này
2. Truy cập [railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub"
4. Chọn repository đã fork
5. Thêm environment variable:
   - `TELEGRAM_TOKEN`: Token của bạn
   - `WEBHOOK_ENABLED`: `true`
   - `WEBHOOK_URL`: `https://your-app.railway.app` (Railway sẽ cung cấp)

✅ Deploy xong trong < 2 phút!

### Fly.io (Miễn phí tốt)

```bash
# Cài đặt Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Deploy
fly launch --no-deploy
fly secrets set TELEGRAM_TOKEN=your_token
fly secrets set WEBHOOK_URL=https://your-app.fly.dev
fly deploy
```

✅ Deploy xong trong < 3 phút!

Xem thêm chi tiết trong [DEPLOY.md](DEPLOY.md)

---

## 🎮 Sử dụng Bot

### Các lệnh cơ bản

- `/start` - Bắt đầu sử dụng bot
- `/help` - Xem danh sách lệnh
- `/balance` - Xem số dư
- `/work` - Làm việc kiếm tiền
- `/daily` - Nhận quà hằng ngày

### Các game

- `/dice` - Chơi xúc xắc may rủi
- `/slots` - Quay hũ slot machine
- `/fish` - Chiến dịch câu cá
- `/mine` - Khai thác mỏ
- `/wordchain` - Nối từ với AI (cần API key)
- `/vietking` - Thử thách Vua Tiếng Việt (cần API key)

---

## 🆘 Troubleshooting

### Bot không khởi động

**Kiểm tra token:**
```bash
# Xem logs
docker-compose logs -f

# Hoặc với Python
python main.py  # Xem error message
```

**Lỗi thường gặp:**
- `Missing TELEGRAM_TOKEN`: Chưa set token trong .env
- `Invalid token`: Token sai hoặc hết hạn
- `Port already in use`: Port 8080 hoặc 8443 đang bị chiếm

### Bot không trả lời

1. Kiểm tra bot có đang chạy không:
```bash
curl http://localhost:8080/health
# Kết quả: {"status": "ok", "service": "telegram-bot"}
```

2. Kiểm tra logs:
```bash
docker-compose logs -f telegram-bot
```

3. Thử `/start` lại trong Telegram

### Data bị mất

Đảm bảo volume được mount đúng:
```yaml
# docker-compose.yml
volumes:
  - ./data:/app/data  # ✅ Đúng
```

---

## 📚 Tài liệu đầy đủ

- [README.md](README.md) - Hướng dẫn chi tiết
- [DEPLOY.md](DEPLOY.md) - Deploy lên nhiều platform
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

## 💡 Tips

1. **Backup data**: File `data/users.json` chứa toàn bộ dữ liệu người chơi
2. **Monitor bot**: Dùng health endpoint `/health` để kiểm tra
3. **Logs**: Luôn kiểm tra logs khi có lỗi
4. **Update code**: `git pull` và rebuild Docker image

---

## 🎉 Hoàn thành!

Bot của bạn giờ đã sẵn sàng! Hãy thử các game và tận hưởng nhé! 🚀

Cần trợ giúp? Mở issue trên GitHub hoặc xem [DEPLOY.md](DEPLOY.md) để biết thêm chi tiết.
