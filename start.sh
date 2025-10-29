#!/bin/bash
# Quick start script for Telegram Bot

set -e

echo "🤖 Telegram Game Bot - Quick Start"
echo "=================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  File .env không tồn tại!"
    echo "Tạo file .env từ template..."
    cp .env.example .env
    echo "✅ Đã tạo file .env"
    echo ""
    echo "📝 Vui lòng chỉnh sửa file .env và thêm TELEGRAM_TOKEN của bạn:"
    echo "   nano .env"
    echo ""
    echo "Sau đó chạy lại script này: ./start.sh"
    exit 1
fi

# Check if DISCORD_TOKEN is set
if ! grep -q "DISCORD_TOKEN=.*[^example]" .env; then
    echo "⚠️  DISCORD_TOKEN chưa được cấu hình!"
    echo "📝 Vui lòng chỉnh sửa file .env và thêm token của bạn:"
    echo "   nano .env"
    exit 1
fi

echo "✅ Đã tìm thấy file .env"
echo ""

# Check if running with Docker
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "🐳 Phát hiện Docker, bắt đầu với Docker Compose..."
    echo ""
    
    # Create data directory
    mkdir -p data
    
    # Start with docker-compose
    docker-compose up -d
    
    echo ""
    echo "✅ Bot đã khởi động với Docker!"
    echo ""
    echo "📊 Xem logs:"
    echo "   docker-compose logs -f"
    echo ""
    echo "🛑 Dừng bot:"
    echo "   docker-compose down"
    echo ""
else
    echo "🐍 Chạy với Python..."
    echo ""
    
    # Check if virtual environment exists
    if [ ! -d ".venv" ]; then
        echo "Tạo virtual environment..."
        python3 -m venv .venv
    fi
    
    # Activate virtual environment
    source .venv/bin/activate
    
    # Install dependencies
    echo "Cài đặt dependencies..."
    pip install -q -r requirements.txt
    
    # Create data directory
    mkdir -p bot/data
    
    echo ""
    echo "✅ Khởi động bot..."
    echo ""
    
    # Start bot
    python main.py
fi
