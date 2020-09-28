import random
import time
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from yeelight import Bulb
import webcolors

TOKEN = open("token.txt", "r").readline()

bulb=Bulb("192.168.1.116")

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)


client = commands.Bot(command_prefix='$')

# client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


async def on_message(self, message):
    # don't respond to ourselves
    if message.author == self.user:
       return


@client.command()
async def colour(ctx, arg):
    try:
        await ctx.send('Setting color to ' + arg + ' (' + str(webcolors.name_to_rgb(arg)) + ')')
        r, g, b = webcolors.name_to_rgb(arg)
        bulb.set_rgb(r+1,g+1,b+1)
    except ValueError as valError:
        await ctx.send('Failed: ' + str(valError))


@client.command()
async def brightness(ctx, arg):
    if str.isnumeric(arg):
        bulb.set_brightness(clamp(int(arg), 0, 100))
        await ctx.send('Setting brightness to ' + str(clamp(int(arg), 0, 100)))
    else:
        await ctx.send('Failed: Please give me an integer input')


@client.command()
async def colour_list(ctx):
        await ctx.send('Checkit: ' + 'https://css-tricks.com/snippets/css/named-colors-and-hex-equivalents/')

@client.command()
async def random_colour(ctx):

    r=random.randint(1, 255)
    g=random.randint(1, 255)
    b=random.randint(1, 255)

    bulb.set_rgb(r,g,b)

    await ctx.send('Setting a random colour! (' + str(r) + ',' + str(g) + ',' + str(b) + ')')

client.run(TOKEN)
