# Discord Summary Bot

A Discord bot that provides channel summaries when mentioned with the "summarize" command.

## Features

- Responds only when directly mentioned with "summarize"
- Uses local LLM (via OpenAI-compatible API) for generating summaries
- Maintains conversation context using recent message history
- Handles message chunking for Discord's character limits
- Includes macOS SSL certificate fix

## Requirements

- Python 3.8+
- Discord developer account and bot token
- LLM API endpoint (local or remote)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/patw/tilldeer.git
cd tilldeer
```

2. Install dependencies:
```bash
python3 -m pip install -r requirements.txt
```

3. Copy `sample.env` to `.env` and modify:
```ini
DISCORD_TOKEN=your_discord_bot_token
LLM_API_KEY=your_llm_api_key
LLM_BASE_URL=http://localhost:1234/v1  # Change to your LLM endpoint
LLM_MODEL=your-model-name
BOT_IDENTITY=You are a helpful assistant that summarizes Discord channels.
BOT_QUESTION_PROMPT=User {user} asks: {question}\n\nRecent messages:\n{history}\n\nPlease provide a concise summary:
BOT_HISTORY_LINES=100  # Number of previous messages to include
```

## Usage

1. Start the bot:
```bash
python3 bot.py
```

2. In Discord, mention the bot with the "summarize" command:
```
@YourBot summarize the last few messages
```

## Configuration

You can customize these environment variables:

- `BOT_HISTORY_LINES`: Number of previous messages to include (default: 5)
- `BOT_QUESTION_PROMPT`: Template for the LLM prompt
- `BOT_IDENTITY`: System message for the LLM

## License

[MIT](LICENSE)
