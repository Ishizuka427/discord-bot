import discord
import traceback
from discord.ext import commands
from os import getenv
import openai

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

messages = [
    {"role": "system", "content": "You are a helpful assistant. The AI assistant's name is AI Qiitan."},
    {"role": "user", "content": "こんにちは。あなたは誰ですか？"},
    {"role": "assistant", "content": "私は AI アシスタントの AI Qiitan です。なにかお手伝いできることはありますか？"}
]

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user in message.mentions:
        # メッセージからボットへのメンションを削除
        content = message.content.replace(f'<@!{bot.user.id}>', '').strip()
        messages.append({"role": "user", "content": content})

        openai_api_key = getenv('OPENAI_API_KEY')
        openai.api_key = openai_api_key

        response = openai.chat.models.davinci.Codex.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        print(response['choices'][0]['message']['content'])
        await message.channel.send(response['choices'][0]['message']['content'])

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
