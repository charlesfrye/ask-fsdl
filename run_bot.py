# This example requires the 'message_content' intent.
import os

import discord
from dotenv import load_dotenv

load_dotenv()

DISCORD_AUTH = os.environ["DISCORD_AUTH"]

import ask_fsdl

runner = ask_fsdl.get_runner()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)  # connection to Discord

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:  # ignore posts by self
        return

    if message.content.startswith('$ask-fsdl'):
        header, *content = message.content.split("$ask-fsdl")  # parse
        content =  "".join(content).strip()
        response = runner(content)  # execute
        await message.channel.send(f'{response}')  # respond

client.run(DISCORD_AUTH)
