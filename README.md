# 🎮 Telegram Game Bot

Bot Telegram cày tiền với nhiều mini game giải trí như làm việc, xúc xắc, quay hũ và nhận quà hằng ngày. Bot lưu dữ liệu người chơi để đảm bảo trải nghiệm mượt mà không bị mất tiến trình.

## ✨ Tính năng chính

- **Làm việc** (`/work`): kiếm thêm tiền với thời gian hồi 20 phút.
- **Xúc xắc may rủi** (`/dice`): nhận thưởng lớn hoặc mất tiền tùy may mắn.
- **Quay hũ** (`/slots`): ba ô biểu tượng với mức thưởng đa dạng.
- **Quà hằng ngày** (`/daily`): chuỗi đăng nhập giúp tăng thưởng.
- **Chiến dịch câu cá** (`/fish`): nhiều lượt quăng lưới với khả năng gặp sinh vật huyền thoại.
- **Khai thác mỏ quy mô lớn** (`/mine`): khai phá nhiều mỏ, có cơ hội nhặt kho báu cổ đại.
- **Nối từ** (`/wordchain`): MC AI tạo chuỗi nối từ tiếng Việt sinh động.
- **Vua Tiếng Việt** (`/vietking`): thử thách tiếng Việt nâng cao do AI biên soạn.
- **Xem số dư** (`/balance`) và lệnh `/help` giải thích chi tiết.

## 📋 Yêu cầu

- Python 3.11 trở lên
- Token bot Telegram (lấy từ [@BotFather](https://t.me/BotFather))
- (Tuỳ chọn) Khóa AI Gateway để kích hoạt các trò ngôn ngữ

## 🚀 Cài đặt và Chạy Local

### 1. Clone repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Tạo virtual environment và cài đặt dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # Trên Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Cấu hình biến môi trường

Tạo file `.env` từ template:

```bash
cp .env.example .env
```

Chỉnh sửa file `.env` và thêm thông tin của bạn:

```bash
TELEGRAM_TOKEN=your_telegram_bot_token_here
DATA_PATH=bot/data/users.json
WEBHOOK_ENABLED=false
AI_GATEWAY_API_KEY=your_ai_gateway_api_key_here  # Optional
```

### 4. Chạy bot

```bash
python main.py
```

## 🐳 Chạy với Docker

### Sử dụng Docker Compose (Khuyến nghị)

```bash
# Build và chạy
docker-compose up -d

# Xem logs
docker-compose logs -f

# Dừng bot
docker-compose down
```

### Sử dụng Docker trực tiếp

```bash
# Build image
docker build -t telegram-game-bot .

# Chạy container
docker run -d \
  --name telegram-bot \
  -e TELEGRAM_TOKEN=your_token_here \
  -v $(pwd)/data:/app/data \
  telegram-game-bot

# Xem logs
docker logs -f telegram-bot
```

## ☁️ Deploy lên Cloud

Bot hỗ trợ cả **polling mode** (cho VPS) và **webhook mode** (cho cloud platforms). Khi deploy lên cloud platform, nên dùng webhook mode để tiết kiệm tài nguyên.

### 🚂 Railway

1. Fork repository này
2. Tạo project mới trên [Railway](https://railway.app)
3. Connect với GitHub repository
4. Thêm biến môi trường:
   - `TELEGRAM_TOKEN`: Token bot của bạn
   - `WEBHOOK_ENABLED`: `true`
   - `WEBHOOK_URL`: URL Railway cung cấp (dạng `https://your-app.railway.app`)
   - `AI_GATEWAY_API_KEY`: (Optional) API key cho game AI

Railway sẽ tự động detect `Dockerfile` và deploy.

### ✈️ Fly.io

1. Cài đặt [Fly CLI](https://fly.io/docs/hands-on/install-flyctl/)
2. Login: `fly auth login`
3. Tạo app:

```bash
fly launch --no-deploy
```

4. Cấu hình secrets:

```bash
fly secrets set TELEGRAM_TOKEN=your_token_here
fly secrets set AI_GATEWAY_API_KEY=your_key_here
fly secrets set WEBHOOK_URL=https://your-app.fly.dev
```

5. Deploy:

```bash
fly deploy
```

6. Tạo volume cho data persistence:

```bash
fly volumes create telegram_bot_data --size 1
```

### 🎨 Render

1. Fork repository
2. Tạo **Web Service** mới trên [Render](https://render.com)
3. Connect với GitHub repository
4. Chọn **Docker** làm Environment
5. Thêm các environment variables:
   - `TELEGRAM_TOKEN`
   - `WEBHOOK_ENABLED=true`
   - `WEBHOOK_URL=https://your-app.onrender.com`
   - `AI_GATEWAY_API_KEY` (optional)
6. Thêm Disk storage:
   - Mount Path: `/app/data`
   - Size: 1GB

### 🖥️ VPS (Ubuntu/Debian)

#### Cách 1: Sử dụng Docker (Khuyến nghị)

```bash
# Cài đặt Docker và Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Clone repo
git clone <repository-url>
cd <repository-name>

# Tạo file .env
nano .env  # Điền TELEGRAM_TOKEN và các biến khác

# Chạy với Docker Compose
docker-compose up -d

# Setup auto-restart on reboot
docker update --restart unless-stopped telegram-game-bot
```

#### Cách 2: Chạy trực tiếp với systemd

```bash
# Cài đặt Python và dependencies
sudo apt update
sudo apt install python3.11 python3-pip python3-venv -y

# Clone và setup
git clone <repository-url>
cd <repository-name>
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Tạo file .env
nano .env

# Tạo systemd service
sudo nano /etc/systemd/system/telegram-bot.service
```

Nội dung file service:

```ini
[Unit]
Description=Telegram Game Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/bot
Environment="PATH=/path/to/bot/.venv/bin"
ExecStart=/path/to/bot/.venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Kích hoạt service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
sudo systemctl status telegram-bot
```

## 🔧 Cấu hình nâng cao

### Biến môi trường

| Biến | Mô tả | Mặc định | Bắt buộc |
|------|-------|----------|----------|
| `TELEGRAM_TOKEN` | Token bot từ BotFather | - | ✅ |
| `DATA_PATH` | Đường dẫn file lưu dữ liệu | `bot/data/users.json` | ❌ |
| `WEBHOOK_ENABLED` | Bật webhook mode | `false` | ❌ |
| `WEBHOOK_URL` | URL public của bot | - | ⚠️ (nếu webhook enabled) |
| `WEBHOOK_PORT` | Port cho webhook | `8443` | ❌ |
| `WEBHOOK_PATH` | Path endpoint webhook | `/webhook` | ❌ |
| `AI_GATEWAY_API_KEY` | API key cho AI games | - | ❌ |

### Polling vs Webhook

**Polling mode** (mặc định):
- Phù hợp cho: VPS, máy local
- Bot chủ động gọi Telegram API để lấy updates
- Không cần domain/SSL
- Dễ setup

**Webhook mode** (khuyến nghị cho production):
- Phù hợp cho: Railway, Fly.io, Render, cloud platforms
- Telegram push updates đến bot qua HTTPS
- Cần domain và SSL certificate
- Tiết kiệm tài nguyên hơn

Để bật webhook:
```bash
WEBHOOK_ENABLED=true
WEBHOOK_URL=https://your-domain.com
```

## 📊 Monitoring

Bot có health check endpoint tại `http://localhost:8080/health` để kiểm tra trạng thái:

```bash
curl http://localhost:8080/health
# Response: {"status": "ok", "service": "telegram-bot"}
```

Các platform như Railway, Fly.io, Render sẽ tự động sử dụng endpoint này để monitor.

## 🔒 Bảo mật

- ✅ Không commit file `.env` hoặc token vào Git
- ✅ Sử dụng secrets/environment variables cho thông tin nhạy cảm
- ✅ Giới hạn quyền truy cập file data
- ✅ Backup file data định kỳ
- ✅ Sử dụng HTTPS cho webhook

## 🐛 Troubleshooting

### Bot không khởi động được

```bash
# Kiểm tra logs
docker-compose logs -f telegram-bot

# Hoặc với systemd
sudo journalctl -u telegram-bot -f
```

### Lỗi "Missing TELEGRAM_TOKEN"

Đảm bảo bạn đã set biến môi trường hoặc tạo file `.env` với token hợp lệ.

### Webhook không hoạt động

1. Kiểm tra `WEBHOOK_URL` có đúng domain không
2. Đảm bảo domain có SSL certificate hợp lệ
3. Kiểm tra port `WEBHOOK_PORT` có mở không
4. Xem logs để biết chi tiết lỗi

### Data bị mất sau restart

Đảm bảo bạn đã mount volume hoặc directory đúng cách:
- Docker: `-v $(pwd)/data:/app/data`
- Fly.io: Tạo persistent volume
- Railway/Render: Sử dụng disk storage

## 📝 Cấu trúc thư mục

```
.
├── bot/
│   ├── __init__.py
│   ├── bot.py          # Main bot logic
│   ├── config.py       # Configuration
│   ├── games.py        # Game mechanics
│   ├── health.py       # Health check endpoint
│   └── storage.py      # Data persistence
├── main.py             # Entry point
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker image definition
├── docker-compose.yml  # Docker Compose config
├── fly.toml           # Fly.io config
├── railway.json       # Railway config
├── render.yaml        # Render config
├── .env.example       # Environment template
└── README.md          # This file
```

## 🤝 Đóng góp

Contributions, issues và feature requests đều được chào đón!

## 📄 License

MIT License - xem file LICENSE để biết thêm chi tiết.

## 🙏 Credits

Bot được xây dựng với:
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [OpenAI API](https://openai.com/) (cho AI games)
