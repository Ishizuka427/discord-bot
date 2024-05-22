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
    if bot.user.id in [member.id for member in message.mentions]:
        print(message.content)
        content = message.content.split('>')[1].lstrip()

        openai_api_key = getenv('OPENAI_API_KEY')
        openai.api_key = openai_api_key

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=content,
            max_tokens=150
        )

        print(response['choices'][0]['text']['content'])
        await message.channel.send(response['choices'][0]['text']['content'])

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
