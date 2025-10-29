# 🎮 Discord Game Bot

Bot Discord với nhiều mini game giải trí như làm việc, xúc xắc, quay hũ và nhận quà hằng ngày. Bot lưu dữ liệu người chơi để đảm bảo trải nghiệm mượt mà không bị mất tiến trình.

## ✨ Tính năng chính

- **Làm việc** (`!work`): kiếm thêm tiền với thời gian hồi 20 phút
- **Xúc xắc may rủi** (`!dice`): nhận thưởng lớn hoặc mất tiền tùy may mắn
- **Quay hũ** (`!slots`): ba ô biểu tượng với mức thưởng đa dạng
- **Quà hằng ngày** (`!daily`): chuỗi đăng nhập giúp tăng thưởng
- **Chiến dịch câu cá** (`!fish`): nhiều lượt quăng lưới với khả năng gặp sinh vật huyền thoại
- **Khai thác mỏ** (`!mine`): khai phá nhiều mỏ, có cơ hội nhặt kho báu cổ đại
- **Nối từ** (`!wordchain`): MC AI tạo chuỗi nối từ tiếng Việt sinh động
- **Vua Tiếng Việt** (`!vietking`): thử thách tiếng Việt nâng cao do AI biên soạn
- **Xem số dư** (`!balance`) và lệnh `!help` giải thích chi tiết

## 🏗️ Kiến trúc

Bot được cấu trúc modular với **main.py** làm orchestrator trung tâm:

```
main.py (Orchestrator)
├── bot/config.py (Configuration)
├── bot/discord_bot.py (Discord client)
├── bot/webhook_server.py (Flask webhook server)
├── bot/storage.py (Data persistence)
├── bot/games.py (Game engine)
└── bot/games/ (Individual game modules)
    ├── work.py
    ├── dice.py
    ├── slots.py
    ├── daily.py
    ├── fishing.py
    └── mining.py
```

## 📋 Yêu cầu

- Python 3.11 trở lên
- Discord Bot Token ([tạo bot tại Discord Developer Portal](https://discord.com/developers/applications))
- (Tuỳ chọn) Discord Webhook URL cho notifications
- (Tuỳ chọn) AI Gateway API Key cho game AI

## 🚀 Cài đặt và Chạy Local

### 1. Clone repository

```bash
git clone <repository-url>
cd discord-game-bot
```

### 2. Tạo virtual environment và cài đặt dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # Trên Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Tạo Discord Bot

1. Truy cập [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" và đặt tên bot
3. Vào tab "Bot" → Click "Add Bot"
4. Copy **Bot Token**
5. Bật **Privileged Gateway Intents**:
   - ✅ Message Content Intent
   - ✅ Server Members Intent
6. Vào tab "OAuth2" → "URL Generator"
   - Chọn scopes: `bot`, `applications.commands`
   - Chọn permissions: `Send Messages`, `Read Messages`, `Embed Links`
   - Copy URL và mở để invite bot vào server

### 4. Cấu hình biến môi trường

```bash
cp .env.example .env
nano .env  # Hoặc dùng editor bạn thích
```

Cập nhật file `.env`:

```env
DISCORD_TOKEN=your_discord_bot_token_here
DISCORD_WEBHOOK_URL=  # Optional
DATA_PATH=bot/data/users.json
WEBHOOK_PORT=8080
COMMAND_PREFIX=!
AI_GATEWAY_API_KEY=  # Optional, for AI games
```

### 5. Chạy bot

```bash
python main.py
```

Hoặc dùng script tiện lợi:

```bash
chmod +x start.sh
./start.sh
```

## 🐳 Chạy với Docker

### Sử dụng Docker Compose (Khuyến nghị)

```bash
# Build và chạy
docker-compose up -d

# Xem logs
docker-compose logs -f discord-bot

# Dừng bot
docker-compose down
```

### Sử dụng Docker trực tiếp

```bash
# Build image
docker build -t discord-game-bot .

# Chạy container
docker run -d \
  --name discord-bot \
  -e DISCORD_TOKEN=your_token_here \
  -v $(pwd)/data:/app/data \
  -p 8080:8080 \
  discord-game-bot
```

## ☁️ Deploy lên Cloud

### 🚂 Railway

1. Push code lên GitHub
2. Tạo project mới trên [Railway](https://railway.app)
3. Connect với GitHub repository
4. Set environment variables:
   - `DISCORD_TOKEN`
   - `AI_GATEWAY_API_KEY` (optional)
5. Add volume mount tại `/app/data`
6. Deploy!

### ✈️ Fly.io

```bash
# Cài đặt Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Launch app
fly launch --no-deploy

# Set secrets
fly secrets set DISCORD_TOKEN=your_token_here
fly secrets set AI_GATEWAY_API_KEY=your_key_here

# Create volume
fly volumes create discord_bot_data --size 1

# Deploy
fly deploy
```

### 🎨 Render

1. Push code lên GitHub
2. Tạo Web Service trên [Render](https://render.com)
3. Select **Docker** environment
4. Add environment variables
5. Add disk storage at `/app/data`
6. Deploy

### 🖥️ VPS

```bash
# Với Docker
git clone <repository-url>
cd discord-game-bot
cp .env.example .env
nano .env  # Thêm DISCORD_TOKEN
docker-compose up -d

# Setup auto-restart
docker update --restart unless-stopped discord-game-bot
```

## 🎮 Sử dụng Bot

### Lệnh cơ bản

- `!start` - Bắt đầu chơi
- `!help` - Xem danh sách lệnh
- `!balance` (hoặc `!bal`, `!money`) - Xem số dư

### Game kiếm tiền

- `!work` - Làm việc (cooldown 20 phút)
- `!daily` - Nhận quà hằng ngày
- `!dice` - Chơi xúc xắc
- `!slots` - Quay hũ

### Game phiêu lưu

- `!fish` - Câu cá
- `!mine` - Khai thác mỏ

### Game trí tuệ (cần AI key)

- `!wordchain` - Nối từ với AI
- `!vietking` - Thử thách Vua Tiếng Việt

## ⚙️ Cấu hình nâng cao

### Biến môi trường

| Biến | Mô tả | Mặc định | Bắt buộc |
|------|-------|----------|----------|
| `DISCORD_TOKEN` | Token bot từ Developer Portal | - | ✅ |
| `DISCORD_WEBHOOK_URL` | URL webhook để gửi notifications | - | ❌ |
| `DATA_PATH` | Đường dẫn file lưu dữ liệu | `bot/data/users.json` | ❌ |
| `WEBHOOK_PORT` | Port cho webhook server | `8080` | ❌ |
| `WEBHOOK_PATH` | Path endpoint webhook | `/discord-webhook` | ❌ |
| `COMMAND_PREFIX` | Prefix cho commands | `!` | ❌ |
| `AI_GATEWAY_API_KEY` | API key cho AI games | - | ❌ |

### Thay đổi Command Prefix

Muốn dùng prefix khác (ví dụ `?` hay `/`):

```env
COMMAND_PREFIX=?
```

## 📊 Monitoring

Bot có health check endpoint tại `http://localhost:8080/health`:

```bash
curl http://localhost:8080/health
# Response: {"status": "ok", "service": "discord-bot"}
```

## 🔧 Development

### Thêm game mới

1. Tạo file mới trong `bot/games/`:

```python
# bot/games/new_game.py
class NewGame:
    def __init__(self, store):
        self.store = store
    
    async def play(self, user_id: int) -> tuple[str, int]:
        # Game logic here
        return "Message", coins_delta
```

2. Import trong `bot/games/__init__.py`
3. Khởi tạo trong `GameEngine` (`bot/games.py`)
4. Thêm command trong `bot/discord_bot.py`

### Cấu trúc module

```
bot/
├── __init__.py
├── config.py              # Configuration management
├── discord_bot.py         # Discord bot client
├── webhook_server.py      # Flask webhook server
├── storage.py             # Data persistence
├── games.py               # Game engine orchestrator
└── games/                 # Individual game modules
    ├── __init__.py
    ├── work.py
    ├── dice.py
    ├── slots.py
    ├── daily.py
    ├── fishing.py
    └── mining.py
```

## 🐛 Troubleshooting

### Bot không start

```bash
# Kiểm tra logs
docker-compose logs -f

# Hoặc
python main.py
```

**Lỗi thường gặp:**
- `Missing DISCORD_TOKEN` → Chưa set token trong .env
- `Invalid token` → Token sai hoặc hết hạn
- `Privileged intent required` → Chưa bật intents trong Developer Portal

### Bot không trả lời

1. Kiểm tra bot có online trên Discord không
2. Verify bot có quyền `Send Messages` trong channel
3. Kiểm tra command prefix (`!` mặc định)
4. Xem logs có error không

### Data bị mất

- Đảm bảo volume được mount đúng:
  ```yaml
  volumes:
    - ./data:/app/data
  ```
- Backup file `data/users.json` định kỳ

## 🔒 Bảo mật

- ✅ Không commit file `.env` vào Git
- ✅ Token lưu trong secrets/environment variables
- ✅ Giới hạn quyền bot trong Discord (chỉ cần thiết)
- ✅ Backup data định kỳ

## 📝 Cấu trúc File

```
discord-game-bot/
├── main.py                   # Entry point (orchestrator)
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker image
├── docker-compose.yml        # Docker Compose config
├── .env.example              # Environment template
├── .gitignore               # Git ignore rules
├── start.sh                 # Quick start script
├── fly.toml                 # Fly.io config
├── railway.json             # Railway config
├── render.yaml              # Render config
├── README.md                # This file
└── bot/                     # Bot source code
    ├── __init__.py
    ├── config.py            # Config management
    ├── discord_bot.py       # Discord bot
    ├── webhook_server.py    # Webhook server
    ├── storage.py           # Data persistence
    ├── games.py             # Game engine
    └── games/               # Game modules
        ├── __init__.py
        ├── work.py
        ├── dice.py
        ├── slots.py
        ├── daily.py
        ├── fishing.py
        └── mining.py
```

## 🤝 Đóng góp

Contributions, issues và feature requests đều được chào đón!

## 📄 License

MIT License

## 🙏 Credits

Bot được xây dựng với:
- [discord.py](https://github.com/Rapptz/discord.py) - Discord API wrapper
- [Flask](https://flask.palletsprojects.com/) - Webhook server
- [OpenAI API](https://openai.com/) - AI games (optional)

---

**Enjoy the games! 🎮🎉**
