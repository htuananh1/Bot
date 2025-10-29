# 🏗️ Architecture Overview

## Tổng quan kiến trúc Discord Game Bot

Bot được thiết kế theo mô hình **modular** với **main.py làm orchestrator trung tâm**.

## 📐 Kiến trúc tổng thể

```
┌─────────────────────────────────────────────────────────┐
│                      main.py                            │
│                  (Orchestrator)                         │
│  - Load configuration                                   │
│  - Initialize all modules                               │
│  - Start webhook server                                 │
│  - Start Discord bot                                    │
│  - Coordinate lifecycle                                 │
└────────┬──────────────┬──────────────┬──────────────────┘
         │              │              │
         ▼              ▼              ▼
┌────────────┐  ┌─────────────┐  ┌──────────────┐
│   Config   │  │  Webhook    │  │  Discord     │
│   Module   │  │   Server    │  │    Bot       │
└────────────┘  └─────────────┘  └──────┬───────┘
                                        │
                        ┌───────────────┼───────────────┐
                        │               │               │
                        ▼               ▼               ▼
                 ┌──────────┐   ┌─────────────┐  ┌──────────┐
                 │  Game    │   │   Storage   │  │  Games   │
                 │  Engine  │◄──┤   Module    │  │  Module  │
                 └────┬─────┘   └─────────────┘  └──────────┘
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐
    │  Work   │ │  Dice   │ │  Slots  │
    │  Game   │ │  Game   │ │  Game   │
    └─────────┘ └─────────┘ └─────────┘
          ▼           ▼           ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐
    │ Daily   │ │ Fishing │ │ Mining  │
    │  Game   │ │  Game   │ │  Game   │
    └─────────┘ └─────────┘ └─────────┘
```

## 🔄 Data Flow

### 1. Startup Flow

```
main.py
  ├─> Load config from environment variables
  ├─> Initialize webhook server (Flask)
  │   └─> Start on port 8080 with /health endpoint
  ├─> Build language oracle (if AI key available)
  ├─> Create Discord bot client
  │   ├─> Initialize intents
  │   ├─> Setup command handlers
  │   └─> Initialize game engine
  │       ├─> Load user store
  │       └─> Initialize all game modules
  └─> Start Discord bot (async)
```

### 2. Command Flow

```
User sends: !work
  │
  ├─> Discord.py receives message
  │
  ├─> Command parser matches "work"
  │
  ├─> discord_bot.py: work_command()
  │   │
  │   ├─> Call GameEngine.play_work(user_id)
  │   │   │
  │   │   ├─> WorkGame.play()
  │   │   │   ├─> Check cooldown
  │   │   │   ├─> Calculate payout
  │   │   │   └─> Update user state
  │   │   │
  │   │   └─> Return (message, coins_delta)
  │   │
  │   ├─> Create Discord Embed
  │   └─> Send response to channel
  │
  └─> User sees result
```

### 3. Data Persistence Flow

```
Game Module (e.g., WorkGame)
  │
  ├─> await store.get(user_id)
  │   ├─> Read from in-memory cache
  │   └─> Or load from JSON file
  │
  ├─> Modify user state (coins, streak, etc.)
  │
  └─> await store.save()
      ├─> Write to in-memory cache
      └─> Async write to JSON file
```

## 📦 Module Details

### main.py (Orchestrator)
**Trách nhiệm:**
- Entry point của toàn bộ ứng dụng
- Load configuration
- Khởi tạo tất cả modules
- Điều phối lifecycle (startup/shutdown)
- Error handling cấp cao

**Key Functions:**
- `main()` - Entry point chính
- `main_async()` - Async orchestration
- `build_language_oracle()` - Initialize AI module

### bot/config.py
**Trách nhiệm:**
- Load environment variables
- Validate configuration
- Provide config object

**Key Classes:**
- `BotConfig` - Configuration dataclass
- `ConfigError` - Custom exception

**Environment Variables:**
```python
DISCORD_TOKEN          # Required
DISCORD_WEBHOOK_URL    # Optional
DATA_PATH              # Default: bot/data/users.json
WEBHOOK_PORT           # Default: 8080
WEBHOOK_PATH           # Default: /discord-webhook
COMMAND_PREFIX         # Default: !
AI_GATEWAY_API_KEY     # Optional
```

### bot/discord_bot.py
**Trách nhiệm:**
- Discord bot client implementation
- Command registration và handling
- Message formatting (embeds)
- Error handling cho commands

**Key Classes:**
- `DiscordGameBot` - Custom bot client
- Command functions: `start_command()`, `work_command()`, etc.

**Key Methods:**
- `setup_hook()` - Called when bot ready
- `on_ready()` - Bot connection established
- `on_command_error()` - Handle command errors
- `send_webhook_message()` - Send via webhook

### bot/webhook_server.py
**Trách nhiệm:**
- HTTP server cho webhooks
- Health check endpoint
- Discord interaction webhooks (extensible)

**Endpoints:**
- `GET /health` - Health check
- `POST /discord-webhook` - Discord webhooks
- `GET /` - Root info endpoint

### bot/storage.py
**Trách nhiệm:**
- User data persistence
- JSON file I/O
- In-memory caching
- Async operations

**Key Classes:**
- `UserState` - User data model
- `UserStore` - Persistence manager

**Data Structure:**
```json
{
  "user_id": {
    "coins": 1000,
    "streak": 5,
    "last_daily": 1234567890
  }
}
```

### bot/games.py (Game Engine)
**Trách nhiệm:**
- Orchestrate tất cả game modules
- Provide unified interface
- Handle game errors
- Manage user locks

**Key Classes:**
- `GameEngine` - Central coordinator
- `GameResult` - Result data class
- `GameError` - Game exception
- `LanguageOracle` - AI integration

**Methods:**
```python
play_work(user_id)          # Work game
play_dice(user_id)          # Dice game
play_slots(user_id)         # Slots game
play_daily(user_id)         # Daily reward
play_fishing(user_id)       # Fishing game
play_mining(user_id)        # Mining game
play_word_chain(user_id)    # AI word chain
play_vietnamese_king(user_id) # AI Vietnamese
```

### bot/games/ (Individual Game Modules)

#### Common Pattern
Mỗi game module follow pattern:

```python
class GameName:
    def __init__(self, store: UserStore):
        self.store = store
    
    async def play(self, user_id: int) -> tuple[str, int]:
        # Game logic
        # Update user state
        return (message, coins_delta)
```

#### Modules:
- **work.py** - Work game với cooldown
- **dice.py** - Dice roll gambling
- **slots.py** - Slot machine
- **daily.py** - Daily rewards với streak
- **fishing.py** - Fishing với random catches
- **mining.py** - Mining với jackpot

## 🔐 Security & Best Practices

### Configuration
- ✅ Sensitive data trong environment variables
- ✅ No hardcoded secrets
- ✅ Validation at config load time

### Error Handling
- ✅ Try-catch ở mọi layer
- ✅ Proper error propagation
- ✅ User-friendly error messages
- ✅ Detailed logging

### Data Persistence
- ✅ Async I/O operations
- ✅ In-memory caching
- ✅ Atomic saves
- ✅ File locking via asyncio

### Concurrency
- ✅ User-level locks trong GameEngine
- ✅ Async/await throughout
- ✅ No blocking operations

## 🚀 Extension Points

### Thêm Game Mới

1. Tạo file mới trong `bot/games/`:
```python
# bot/games/new_game.py
class NewGame:
    def __init__(self, store):
        self.store = store
    
    async def play(self, user_id: int) -> tuple[str, int]:
        # Your game logic
        return ("Result message", coins_earned)
```

2. Import trong `bot/games/__init__.py`:
```python
from .new_game import NewGame
```

3. Initialize trong `GameEngine`:
```python
# bot/games.py
class GameEngine:
    def __init__(self, ...):
        self.new_game = NewGame(store)
```

4. Thêm method trong `GameEngine`:
```python
async def play_new_game(self, user_id: int) -> GameResult:
    message, coins = await self.new_game.play(user_id)
    return GameResult(message=message, coins_delta=coins)
```

5. Thêm command trong `discord_bot.py`:
```python
async def new_game_command(ctx: commands.Context):
    await _play_game(ctx, "new_game")

# Trong setup_commands():
bot.command(name="newgame")(new_game_command)
```

### Thêm Webhook Handler

Extend `webhook_server.py`:

```python
@self.app.route("/custom-webhook", methods=["POST"])
def custom_webhook():
    data = request.get_json()
    # Handle webhook
    return jsonify({"status": "ok"}), 200
```

### Thêm Storage Fields

Update `UserState` trong `storage.py`:

```python
@dataclass
class UserState:
    coins: int = 0
    streak: int = 0
    last_daily: int = 0
    new_field: int = 0  # Add this
```

## 📊 Performance Considerations

### Caching
- User states cached in-memory
- Disk I/O only on explicit save
- Lazy loading

### Async Operations
- Non-blocking I/O throughout
- Concurrent user operations
- Background webhook server

### Resource Usage
- **Memory**: ~50-100MB typical
- **CPU**: <5% typical, spikes on commands
- **Disk**: Minimal, JSON append-only

## 🔧 Debugging

### Enable Debug Logging

```python
# main.py
logging.basicConfig(level=logging.DEBUG)
```

### Common Debug Points

1. **Config loading:**
```python
# bot/config.py
LOGGER.debug("Loaded config: %s", config)
```

2. **Game execution:**
```python
# bot/games.py
LOGGER.debug("User %s playing %s", user_id, game_name)
```

3. **Data persistence:**
```python
# bot/storage.py
LOGGER.debug("Saving state: %s", self._users)
```

## 📈 Monitoring

### Health Check
```bash
curl http://localhost:8080/health
```

### Logs
```bash
# Docker
docker-compose logs -f discord-bot

# Direct
python main.py 2>&1 | tee bot.log
```

### Metrics to Monitor
- Command response time
- User count growth
- Error rate
- Uptime
- Memory usage

---

**Architecture Version:** 2.0  
**Last Updated:** 2025-10-29  
**Maintainer:** Bot Development Team
