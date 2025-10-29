# Telegram Game Bot

Bot Telegram cày tiền với nhiều mini game giải trí như làm việc, xúc xắc, quay hũ
và nhận quà hằng ngày. Bot lưu dữ liệu người chơi để đảm bảo trải nghiệm mượt mà
không bị mất tiến trình.

## Tính năng chính

- **Làm việc** (`/work`): kiếm thêm tiền với thời gian hồi 20 phút.
- **Xúc xắc may rủi** (`/dice`): nhận thưởng lớn hoặc mất tiền tùy may mắn.
- **Quay hũ** (`/slots`): ba ô biểu tượng với mức thưởng đa dạng.
- **Quà hằng ngày** (`/daily`): chuỗi đăng nhập giúp tăng thưởng.
- **Chiến dịch câu cá** (`/fish`): nhiều lượt quăng lưới với khả năng gặp sinh vật huyền thoại.
- **Khai thác mỏ quy mô lớn** (`/mine`): khai phá nhiều mỏ, có cơ hội nhặt kho báu cổ đại.
- **Nối từ** (`/wordchain`): MC AI tạo chuỗi nối từ tiếng Việt sinh động.
- **Vua Tiếng Việt** (`/vietking`): thử thách tiếng Việt nâng cao do AI biên soạn.
- **Xem số dư** (`/balance`) và lệnh `/help` giải thích chi tiết.

## Yêu cầu

- Python 3.10 trở lên.
- Token bot Telegram (`TELEGRAM_TOKEN`).
- (Tuỳ chọn) Khóa AI Gateway (`AI_GATEWAY_API_KEY`) để kích hoạt các trò ngôn ngữ.

## Cài đặt

```bash
python -m venv .venv
source .venv/bin/activate  # Trên Windows dùng .venv\Scripts\activate
pip install -r requirements.txt
```

## Cấu hình

Tạo file `.env` (tuỳ chọn) hoặc đặt biến môi trường trước khi chạy:

```bash
export TELEGRAM_TOKEN="<TOKEN_CỦA_BẠN>"
export DATA_PATH="data/users.json"  # Không bắt buộc, mặc định bot/data/users.json
export AI_GATEWAY_API_KEY="<KHOA_GATEWAY>"  # Không bắt buộc nhưng cần cho game AI
```

## Chạy bot

```bash
python main.py
```

Bot sẽ tạo file lưu dữ liệu người chơi theo đường dẫn `DATA_PATH`. Đảm bảo tiến trình
chạy liên tục để bot phản hồi mượt mà và không mất dữ liệu.

## Triển khai gợi ý

- Triển khai trên VPS hoặc dịch vụ cloud chạy Python dài hạn (Railway, Fly.io, v.v.).
- Sử dụng `systemd`, `pm2` hoặc Docker để giữ bot luôn chạy.
- Sao lưu định kỳ file dữ liệu để phòng ngừa sự cố.

### Triển khai bằng Docker

1. Tạo file `.env` chứa `TELEGRAM_TOKEN` (và `AI_GATEWAY_API_KEY` nếu cần).
2. Xây dựng và chạy bot:

   ```bash
   docker compose up -d --build
   ```

   Container sẽ lưu dữ liệu người chơi tại volume `bot_data` (đường dẫn `/data/users.json`).
3. Xem log và trạng thái:

   ```bash
   docker compose logs -f
   docker compose ps
   ```

Khi cập nhật mã nguồn, chạy lại `docker compose up -d --build` để bot nhận thay đổi mới.
