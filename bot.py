import discord
import re
import random
import os
import json
from dotenv import load_dotenv

# Use local models with the OpenAI library and a custom baseurl
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# LLM Configuration
llm_config = {
    "api_key": os.getenv("LLM_API_KEY", "sk-no-key-required"),
    "base_url": os.getenv("LLM_BASE_URL"),
    "model": os.getenv("LLM_MODEL")
}

# Bot Configuration
bot_config = {
    "identity": os.getenv("BOT_IDENTITY"),
    "history_lines": int(os.getenv("BOT_HISTORY_LINES", "5")),
    "discord_token": os.getenv("DISCORD_TOKEN"),
    "question_prompt": os.getenv("BOT_QUESTION_PROMPT")
}

# Configure discord intent for chatting
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Removes discord IDs from strings
def remove_id(text):
    return re.sub(r'<@\d+>', '', text)

# Remove @ from broadcast mentions but keep the words
def filter_mentions(text):
    pattern = r'@(\b(here|everyone|channel)\b)'
    filtered_text = re.sub(pattern, r'\1', text)
    return filtered_text

def format_prompt(prompt, user, question, history):
    formatted_prompt = prompt.replace("{user}", user)
    formatted_prompt = formatted_prompt.replace("{question}", question)
    formatted_prompt = formatted_prompt.replace("{history}", history)
    return formatted_prompt

# Split messages into 2000 character chunks (discord's message limit)
def split_message(message):
    return [message[i:i+2000] for i in range(0, len(message), 2000)]

# Call llm using the llm configuration
def llm_local(prompt):
    client = OpenAI(api_key=llm_config["api_key"], base_url=llm_config["base_url"])
    messages=[{"role": "system", "content": bot_config["identity"]},{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model=llm_config["model"], messages=messages)
    return response.choices[0].message.content

@client.event
async def on_ready():
    print(f'Bot logged in as {client.user}')

@client.event
async def on_message(message):

    # Never reply to yourself
    if message.author == client.user:
        return
    
    # Grab the channel history and format as JSON with user/message pairs
    history_list = []
    channel_history = [user async for user in message.channel.history(limit=bot_config["history_lines"] + 1)]
    for history in channel_history:
        if remove_id(history.content) != remove_id(message.content):
            history_list.append({
                "user": history.author.name,
                "message": remove_id(history.content)
            })

    # Reverse the order of the history so it looks more like the chat log
    # Then convert to JSON string
    history_list.reverse()
    history_text = json.dumps(history_list)

    # Only respond when mentioned directly
    if client.user.mentioned_in(message):
        content = remove_id(message.content).strip().lower()
        if content.startswith('summarize'):
            prompt = format_prompt(bot_config["question_prompt"], message.author.name, remove_id(message.content), history_text)
            bot_response = filter_mentions(llm_local(prompt))
            message_chunks = split_message(bot_response)
            for chunk in message_chunks:
                await message.channel.send(chunk)
        else:
            await message.channel.send("I can summarize the discord channel - mention me with the word 'summarize'")

# Run the main loop
client.run(bot_config["discord_token"])
