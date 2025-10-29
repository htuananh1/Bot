# ✅ Deployment Checklist

Checklist để đảm bảo bot được deploy thành công.

## 📋 Trước khi Deploy

### Chuẩn bị
- [ ] Đã có Telegram Bot Token từ [@BotFather](https://t.me/BotFather)
- [ ] Đã có AI Gateway API Key (nếu muốn dùng AI games)
- [ ] Đã test bot ở local thành công
- [ ] Đã commit code lên Git repository
- [ ] Đã tạo file `.gitignore` để không commit `.env`

### Test Local

#### Với Docker:
```bash
# Build image
docker-compose build

# Start bot
docker-compose up -d

# Check logs
docker-compose logs -f

# Test health endpoint
curl http://localhost:8080/health

# Stop
docker-compose down
```

#### Với Python:
```bash
# Activate venv
source .venv/bin/activate

# Run bot
python main.py

# Test health endpoint (trong terminal khác)
curl http://localhost:8080/health
```

#### Test Bot Commands:
- [ ] `/start` - Bot trả lời với welcome message
- [ ] `/help` - Hiển thị danh sách commands
- [ ] `/balance` - Hiển thị số dư
- [ ] `/work` - Có thể làm việc và nhận tiền
- [ ] `/dice` - Chơi được game xúc xắc
- [ ] `/slots` - Chơi được slot machine
- [ ] `/daily` - Nhận quà hằng ngày
- [ ] `/fish` - Chơi game câu cá
- [ ] `/mine` - Chơi game khai mỏ
- [ ] `/wordchain` - (Nếu có AI key) Game nối từ hoạt động
- [ ] `/vietking` - (Nếu có AI key) Game tiếng Việt hoạt động

## 🚀 Deployment

### Railway

- [ ] Fork/push repository lên GitHub
- [ ] Tạo project mới trên Railway
- [ ] Connect với GitHub repository
- [ ] Set environment variables:
  - [ ] `TELEGRAM_TOKEN`
  - [ ] `WEBHOOK_ENABLED=true`
  - [ ] `WEBHOOK_URL` (sau khi có domain)
  - [ ] `AI_GATEWAY_API_KEY` (optional)
- [ ] Add volume mount tại `/app/data`
- [ ] Deploy thành công
- [ ] Kiểm tra logs
- [ ] Test bot trên Telegram

### Fly.io

- [ ] Install Fly CLI
- [ ] Login: `fly auth login`
- [ ] Run: `fly launch --no-deploy`
- [ ] Set secrets:
  ```bash
  fly secrets set TELEGRAM_TOKEN=xxx
  fly secrets set WEBHOOK_URL=https://your-app.fly.dev
  fly secrets set AI_GATEWAY_API_KEY=xxx
  ```
- [ ] Create volume: `fly volumes create telegram_bot_data --size 1`
- [ ] Deploy: `fly deploy`
- [ ] Check logs: `fly logs`
- [ ] Check status: `fly status`
- [ ] Test bot

### Render

- [ ] Push code lên GitHub
- [ ] Create Web Service trên Render
- [ ] Select Docker environment
- [ ] Configure environment variables
- [ ] Add disk storage (`/app/data`)
- [ ] Deploy
- [ ] Wait for deploy (5-10 phút)
- [ ] Check logs
- [ ] Test bot
- [ ] Note: Free tier có sleep sau 15 phút

### VPS/Droplet

- [ ] Create VPS/Droplet với Docker
- [ ] SSH vào server
- [ ] Clone repository
- [ ] Create `.env` file với token
- [ ] Run: `docker-compose up -d`
- [ ] Setup auto-restart: `docker update --restart unless-stopped telegram-game-bot`
- [ ] Test health: `curl localhost:8080/health`
- [ ] Test bot
- [ ] Setup backup cho data folder

## ✅ Post-Deployment

### Verification

- [ ] Bot online trên Telegram
- [ ] Health endpoint responding: `curl https://your-app/health`
- [ ] Webhook configured (nếu dùng webhook mode):
  ```bash
  curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo
  ```
- [ ] Logs không có error
- [ ] Data được persist sau restart
- [ ] All commands hoạt động

### Webhook Info Check

Nếu dùng webhook mode, verify:
```bash
curl https://api.telegram.org/bot<YOUR_TOKEN>/getWebhookInfo
```

Expected output:
```json
{
  "ok": true,
  "result": {
    "url": "https://your-app.com/webhook",
    "has_custom_certificate": false,
    "pending_update_count": 0,
    "max_connections": 40
  }
}
```

Check:
- [ ] `url` đúng với domain của bạn
- [ ] `pending_update_count` thấp (< 10)
- [ ] Không có `last_error_message`

### Monitoring

Setup monitoring:
- [ ] Health check endpoint được monitor
- [ ] Logs được theo dõi
- [ ] Disk space được kiểm tra (cho data folder)
- [ ] Uptime monitoring (UptimeRobot, Healthchecks.io, etc.)

### Backup

- [ ] Setup automated backup cho `data/users.json`
- [ ] Test restore từ backup
- [ ] Document backup procedure

### Security

- [ ] `.env` file không commit vào Git
- [ ] Token được lưu trong secrets/environment variables
- [ ] Data folder có proper permissions
- [ ] HTTPS enabled cho webhook
- [ ] Rate limiting enabled (đã có trong code)

## 🐛 Troubleshooting

### Bot không start

**Check:**
1. Logs có error gì không?
   ```bash
   docker-compose logs -f
   # hoặc
   fly logs
   ```
2. Token có đúng không?
3. Environment variables đã set đầy đủ chưa?

**Common errors:**
- `Missing TELEGRAM_TOKEN` → Chưa set token
- `Invalid token` → Token sai
- `Port already in use` → Port conflict, đổi port

### Bot không trả lời

**Check:**
1. Bot có đang chạy không?
   ```bash
   curl http://your-app/health
   ```
2. Webhook có đúng không? (nếu dùng webhook)
   ```bash
   curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo
   ```
3. Logs có error không?

**Fixes:**
- Restart bot
- Xóa webhook và set lại:
  ```bash
  # Xóa webhook
  curl https://api.telegram.org/bot<TOKEN>/deleteWebhook
  
  # Set lại (bot sẽ tự set khi restart)
  docker-compose restart
  ```
- Check network/firewall

### Data bị mất

**Check:**
1. Volume/disk có được mount đúng không?
2. File `users.json` có tồn tại không?
3. Permissions có đúng không?

**Fixes:**
- Verify volume mount trong docker-compose.yml
- Restore từ backup
- Restart bot

### Webhook errors

**Check:**
1. HTTPS có hoạt động không?
2. SSL certificate có valid không?
3. Port có mở không?

**Fixes:**
- Verify WEBHOOK_URL có `https://`
- Check SSL certificate
- Ensure port forwarding đúng

## 📊 Performance Checks

### Resource Usage

Monitor:
- [ ] CPU usage < 50% thường xuyên
- [ ] Memory usage < 80%
- [ ] Disk space đủ cho data
- [ ] Response time < 1s

### Optimization

Nếu cần optimize:
- [ ] Enable caching
- [ ] Optimize database queries (nếu chuyển từ JSON)
- [ ] Scale horizontally (thêm instances)
- [ ] Use CDN cho assets

## 🎉 Success Criteria

Bot được coi là deploy thành công khi:
- ✅ Bot online 24/7
- ✅ Tất cả commands hoạt động
- ✅ Data được persist sau restart
- ✅ Health check passing
- ✅ Logs clean (không có persistent errors)
- ✅ Response time tốt (< 1-2s)
- ✅ Users có thể chơi game bình thường

## 📝 Notes

- Backup data trước khi update code
- Test thoroughly ở local trước khi deploy
- Monitor logs trong 24h đầu sau deploy
- Document mọi thay đổi config
- Keep credentials secure

---

## 🆘 Need Help?

Nếu gặp vấn đề:
1. Check logs đầu tiên
2. Verify configuration
3. Test health endpoint
4. Check Telegram webhook info
5. Xem DEPLOY.md để biết chi tiết platform-specific
6. Open GitHub issue nếu cần support

**Happy deploying! 🚀**
