import discord
import traceback
from discord.ext import commands
from os import getenv
from openai import OpenAI

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

client = OpenAI(api_key=getenv('OPENAI_API_KEY'))

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

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": content}
            ]
        )

        print(response.choices[0].message['content'])
        await message.channel.send(response.choices[0].message['content'])

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
