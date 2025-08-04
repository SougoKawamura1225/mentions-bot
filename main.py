import os, sys
import discord
from discord.ext import commands

# スケジュール停止用フラグ（Actionsで切替）
if os.getenv("ENABLE_BOT", "true").lower() != "true":
    print("Bot disabled by schedule")
    sys.exit(0)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ ログインしました: {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.mentions and len(message.content.split()) >= 2:
        mentioned_users = message.mentions
        parts = message.content.split()
        content = " ".join(parts[len(mentioned_users):]).strip() or "[本文が空です]"
        for u in mentioned_users:
            try:
                await u.send(
                    f"📩 **{message.author.display_name} さんからのメッセージ**:\n{content}"
                )
            except discord.Forbidden:
                print(f"⚠️ DM送信失敗: {u.display_name}")
    await bot.process_commands(message)

bot.run(os.environ["TOKEN"])
