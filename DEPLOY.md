# 🚀 Hướng dẫn Deploy chi tiết

Tài liệu này cung cấp hướng dẫn chi tiết để deploy Telegram Bot lên các platform phổ biến.

## 📋 Mục lục

- [Chuẩn bị trước khi deploy](#chuẩn-bị-trước-khi-deploy)
- [Railway](#railway)
- [Fly.io](#flyio)
- [Render](#render)
- [Google Cloud Run](#google-cloud-run)
- [AWS](#aws)
- [DigitalOcean](#digitalocean)
- [Heroku](#heroku)

## Chuẩn bị trước khi deploy

### 1. Tạo Telegram Bot

1. Mở Telegram và tìm [@BotFather](https://t.me/BotFather)
2. Gửi command `/newbot`
3. Làm theo hướng dẫn để đặt tên và username cho bot
4. Lưu lại **Bot Token** mà BotFather cung cấp

### 2. (Optional) Lấy AI Gateway API Key

Nếu bạn muốn bật các game AI (word chain, Vietnamese king):

1. Đăng ký tại [AI Gateway](https://ai-gateway.vercel.sh)
2. Tạo API key mới
3. Lưu lại API key

### 3. Fork/Clone Repository

```bash
git clone <repository-url>
cd telegram-game-bot
```

## Railway

Railway là platform đơn giản nhất để deploy, có free tier và tự động setup mọi thứ.

### Bước 1: Tạo Account

1. Truy cập [railway.app](https://railway.app)
2. Đăng ký bằng GitHub account

### Bước 2: Tạo Project

1. Click **"New Project"**
2. Chọn **"Deploy from GitHub repo"**
3. Chọn repository của bạn
4. Railway sẽ tự động detect Dockerfile

### Bước 3: Cấu hình Environment Variables

Trong project settings, thêm các biến:

```env
TELEGRAM_TOKEN=your_bot_token_here
WEBHOOK_ENABLED=true
WEBHOOK_URL=https://your-app.railway.app
WEBHOOK_PORT=8443
DATA_PATH=/app/data/users.json
AI_GATEWAY_API_KEY=your_key_here  # Optional
```

**Lưu ý**: `WEBHOOK_URL` sẽ được Railway tự động generate sau khi deploy lần đầu. Ban đầu có thể set `WEBHOOK_ENABLED=false`, sau đó update lại sau khi có URL.

### Bước 4: Add Volume

1. Vào tab **"Settings"** → **"Volumes"**
2. Click **"New Volume"**
3. Mount path: `/app/data`
4. Size: 1GB

### Bước 5: Deploy

1. Click **"Deploy"**
2. Đợi build và deploy hoàn tất
3. Kiểm tra logs để đảm bảo bot chạy thành công
4. Update `WEBHOOK_URL` nếu cần và redeploy

### Giá cả

- Free tier: $5 credit/month
- Đủ để chạy bot 24/7 với traffic vừa phải

## Fly.io

Fly.io cung cấp khả năng deploy global với free tier hào phóng.

### Bước 1: Cài đặt Fly CLI

```bash
# macOS
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh

# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

### Bước 2: Login

```bash
fly auth login
```

### Bước 3: Khởi tạo app

```bash
cd telegram-game-bot
fly launch --no-deploy
```

Khi được hỏi:
- App name: Chọn tên bạn muốn (hoặc để trống cho random)
- Region: Chọn gần bạn nhất (ví dụ: `sin` cho Singapore)
- Database: **No**
- Deploy now: **No**

### Bước 4: Cấu hình secrets

```bash
# Set Telegram token
fly secrets set TELEGRAM_TOKEN=your_token_here

# Set AI key (optional)
fly secrets set AI_GATEWAY_API_KEY=your_key_here

# Set webhook URL (replace với app name của bạn)
fly secrets set WEBHOOK_URL=https://your-app-name.fly.dev
```

### Bước 5: Tạo Volume

```bash
fly volumes create telegram_bot_data --region sin --size 1
```

### Bước 6: Deploy

```bash
fly deploy
```

### Bước 7: Kiểm tra

```bash
# Xem logs
fly logs

# Xem status
fly status

# SSH vào container
fly ssh console
```

### Giá cả

- Free tier: 3 shared-cpu VMs với 256MB RAM
- Volume: 3GB free
- Đủ để chạy bot nhỏ 24/7

## Render

Render có UI thân thiện và dễ sử dụng.

### Bước 1: Tạo Account

1. Truy cập [render.com](https://render.com)
2. Đăng ký bằng GitHub

### Bước 2: Tạo Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect GitHub repository
3. Chọn repository của bạn
4. Cấu hình:
   - **Name**: Tên service của bạn
   - **Environment**: **Docker**
   - **Region**: Singapore hoặc gần bạn
   - **Instance Type**: Free

### Bước 3: Environment Variables

Thêm các biến trong phần **Environment**:

```env
TELEGRAM_TOKEN=your_token_here
WEBHOOK_ENABLED=true
WEBHOOK_URL=https://your-app.onrender.com
WEBHOOK_PORT=8443
DATA_PATH=/app/data/users.json
AI_GATEWAY_API_KEY=your_key_here
```

### Bước 4: Add Disk

1. Scroll xuống **"Disk"**
2. Click **"Add Disk"**
3. Name: `telegram-bot-data`
4. Mount Path: `/app/data`
5. Size: 1GB

### Bước 5: Deploy

1. Click **"Create Web Service"**
2. Đợi build và deploy (5-10 phút)
3. Kiểm tra logs

### Lưu ý về Render Free Tier

- Web service sẽ **sleep** sau 15 phút không có request
- Bot sẽ mất vài giây để wake up khi có message mới
- Nếu cần 24/7, upgrade lên paid plan ($7/month)

### Giá cả

- Free tier: Web service với 750 giờ/tháng
- Disk: Free cho 1GB đầu tiên
- Paid: $7/month cho always-on service

## Google Cloud Run

Cloud Run là serverless platform của Google, chỉ tính tiền khi có request.

### Bước 1: Setup Google Cloud

```bash
# Cài đặt gcloud CLI
# macOS
brew install google-cloud-sdk

# Linux/Windows: https://cloud.google.com/sdk/docs/install

# Login
gcloud auth login

# Tạo project
gcloud projects create telegram-bot-xyz --name="Telegram Bot"
gcloud config set project telegram-bot-xyz

# Enable APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Bước 2: Build và Push Image

```bash
# Build image
gcloud builds submit --tag gcr.io/telegram-bot-xyz/telegram-bot

# Hoặc build local và push
docker build -t gcr.io/telegram-bot-xyz/telegram-bot .
docker push gcr.io/telegram-bot-xyz/telegram-bot
```

### Bước 3: Deploy

```bash
gcloud run deploy telegram-bot \
  --image gcr.io/telegram-bot-xyz/telegram-bot \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --set-env-vars TELEGRAM_TOKEN=your_token,WEBHOOK_ENABLED=true,WEBHOOK_PORT=8443 \
  --set-env-vars WEBHOOK_URL=https://telegram-bot-xyz.run.app \
  --memory 512Mi \
  --port 8443
```

### Bước 4: Setup Volume (Optional)

Cloud Run không support persistent disk. Có thể dùng:
- Google Cloud Storage
- Firestore
- Cloud SQL

### Giá cả

- Free tier: 2 million requests/month
- $0.00002400 per request sau đó
- Rất rẻ cho bot nhỏ/vừa

## DigitalOcean

Deploy trên VPS/Droplet với Docker.

### Bước 1: Tạo Droplet

1. Truy cập [digitalocean.com](https://www.digitalocean.com)
2. Create → Droplets
3. Chọn:
   - **Image**: Docker on Ubuntu 22.04
   - **Plan**: Basic ($6/month)
   - **Region**: Singapore
   - **SSH Key**: Thêm SSH key của bạn

### Bước 2: Connect SSH

```bash
ssh root@your_droplet_ip
```

### Bước 3: Clone và Setup

```bash
# Clone repo
git clone <repository-url>
cd telegram-game-bot

# Tạo .env file
nano .env
```

Thêm vào `.env`:

```env
TELEGRAM_TOKEN=your_token_here
DATA_PATH=/app/data/users.json
WEBHOOK_ENABLED=false
AI_GATEWAY_API_KEY=your_key_here
```

### Bước 4: Run với Docker Compose

```bash
# Install docker-compose (nếu chưa có)
apt install docker-compose -y

# Start bot
docker-compose up -d

# Xem logs
docker-compose logs -f
```

### Bước 5: Setup Auto-start

```bash
# Enable restart on reboot
docker update --restart unless-stopped telegram-game-bot
```

### Giá cả

- Basic Droplet: $6/month
- Có full control và tài nguyên dedicated

## AWS

Deploy lên AWS ECS với Fargate.

### Bước 1: Setup AWS CLI

```bash
# Install AWS CLI
pip install awscli

# Configure
aws configure
```

### Bước 2: Create ECR Repository

```bash
# Create repository
aws ecr create-repository --repository-name telegram-bot

# Get login
aws ecr get-login-password --region ap-southeast-1 | \
  docker login --username AWS --password-stdin \
  YOUR_ACCOUNT_ID.dkr.ecr.ap-southeast-1.amazonaws.com
```

### Bước 3: Build và Push

```bash
# Build
docker build -t telegram-bot .

# Tag
docker tag telegram-bot:latest \
  YOUR_ACCOUNT_ID.dkr.ecr.ap-southeast-1.amazonaws.com/telegram-bot:latest

# Push
docker push YOUR_ACCOUNT_ID.dkr.ecr.ap-southeast-1.amazonaws.com/telegram-bot:latest
```

### Bước 4: Create ECS Cluster

```bash
# Create cluster
aws ecs create-cluster --cluster-name telegram-bot-cluster
```

### Bước 5: Create Task Definition

Tạo file `task-definition.json`:

```json
{
  "family": "telegram-bot",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "telegram-bot",
      "image": "YOUR_ACCOUNT_ID.dkr.ecr.ap-southeast-1.amazonaws.com/telegram-bot:latest",
      "essential": true,
      "environment": [
        {"name": "TELEGRAM_TOKEN", "value": "your_token"},
        {"name": "WEBHOOK_ENABLED", "value": "false"},
        {"name": "DATA_PATH", "value": "/app/data/users.json"}
      ]
    }
  ]
}
```

Register:

```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

### Bước 6: Run Service

```bash
aws ecs create-service \
  --cluster telegram-bot-cluster \
  --service-name telegram-bot-service \
  --task-definition telegram-bot \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

### Giá cả

- Fargate: ~$15/month cho 0.25 vCPU, 0.5GB RAM
- ECR: Free cho 500MB storage đầu tiên

## Heroku

**Lưu ý**: Heroku đã ngừng free tier từ 11/2022. Cần paid plan ($7/month minimum).

### Bước 1: Setup

```bash
# Install Heroku CLI
brew install heroku/brew/heroku  # macOS
# Windows/Linux: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login
```

### Bước 2: Create App

```bash
# Create app
heroku create telegram-bot-xyz

# Add container stack
heroku stack:set container -a telegram-bot-xyz
```

### Bước 3: Set Config

```bash
heroku config:set TELEGRAM_TOKEN=your_token -a telegram-bot-xyz
heroku config:set WEBHOOK_ENABLED=true -a telegram-bot-xyz
heroku config:set WEBHOOK_URL=https://telegram-bot-xyz.herokuapp.com -a telegram-bot-xyz
heroku config:set WEBHOOK_PORT=8443 -a telegram-bot-xyz
```

### Bước 4: Deploy

```bash
# Add Heroku remote
git remote add heroku https://git.heroku.com/telegram-bot-xyz.git

# Deploy
git push heroku main
```

### Giá cả

- Eco Dynos: $7/month (1000 dyno hours)
- Basic: $7/month per dyno (always on)

## 🎯 So sánh Platform

| Platform | Giá Free | Giá Paid | Dễ Setup | Uptime | Khuyến nghị |
|----------|----------|----------|----------|--------|-------------|
| Railway | $5 credit/mo | $10+/mo | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Tốt nhất cho beginner |
| Fly.io | 3 VMs free | $5+/mo | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Tốt cho production |
| Render | 750h/mo (sleep) | $7/mo | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | OK cho bot nhỏ |
| DigitalOcean | - | $6/mo | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Tốt nếu cần control |
| Google Cloud Run | 2M req/mo | Pay-per-use | ⭐⭐ | ⭐⭐⭐⭐ | Rẻ cho low traffic |
| AWS ECS | - | $15+/mo | ⭐⭐ | ⭐⭐⭐⭐⭐ | Enterprise only |
| Heroku | - | $7/mo | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | OK nhưng đắt |

## 🆘 Support

Nếu gặp vấn đề khi deploy, check:

1. Logs của platform
2. Health check endpoint: `curl https://your-app/health`
3. Telegram webhook info: `https://api.telegram.org/bot<TOKEN>/getWebhookInfo`
4. GitHub Issues của repo

## 📚 Resources

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [python-telegram-bot docs](https://docs.python-telegram-bot.org/)
- [Docker docs](https://docs.docker.com/)
