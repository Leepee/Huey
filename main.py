import random
import time
import os
import discord
from discord.ext import commands
from yeelight import Bulb
import webcolors
import aiohttp, asyncio, json
import urllib.parse
import urllib.request


TOKEN = open("token.txt", "r").readline()

bot_info = {
	'server_name' : 'Solent Media Technology',
	'_guild_obj' : None,
	'_members' : {},
	'_roles' : {},
	'_channels' : {}
}

emoji_index = {
	0 : '✔',
	1 : '❌',
	2 : '2\N{COMBINING ENCLOSING KEYCAP}',
	3 : '3\N{COMBINING ENCLOSING KEYCAP}',
	4 : '4\N{COMBINING ENCLOSING KEYCAP}',
	5 : '5\N{COMBINING ENCLOSING KEYCAP}',
	6 : '6\N{COMBINING ENCLOSING KEYCAP}',
	7 : '7\N{COMBINING ENCLOSING KEYCAP}',
	8 : '8\N{COMBINING ENCLOSING KEYCAP}',
	9 : '9\N{COMBINING ENCLOSING KEYCAP}',
	10 : '\U0001F52B',
	11 : '🏕️',
	12 : '🔥',
	13 : '🥎',
	14 : '🚓',
	15 : '🍺',
	16 : '🙈',
	17 : '💄',
	18 : '⛅',
	19 : '🙄',
	20 : '🎄'
}



bulb = Bulb("192.168.1.116")


def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)


client = commands.Bot(command_prefix='$')


# client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

    for guild in client.guilds:
        if guild.name == bot_info['server_name']:
            bot_info['_guild_obj'] = guild

            for member in guild.members:
                bot_info['_members'][member.id] = member

            for role in bot_info['_guild_obj'].roles:
                bot_info['_roles'][role.id] = role

            for channel in guild.channels:
                bot_info['_channels'][channel.name] = channel

@client.event
async def on_member_join(self, member):
    # Keep updating members.
    bot_info['_members'][member.id] = member

@client.event
async def talley_votes(self, reaction):
    channel = self.get_channel(reaction.channel_id)
    message = await channel.fetch_message(reaction.message_id)

    votes = {}

    for reaction in message.reactions:
        async for reactor in reaction.users():
            if not reaction.emoji in votes: votes[reaction.emoji] = 0

            votes[reaction.emoji] += 1

    leading_votes = {}
    all_votes = votes.values()
    highest_vote = max(all_votes)

    for emoji, vote in votes.items():
        if vote < highest_vote: continue
        leading_votes[emoji] = vote

    if not 'Current winning poll: ' in message.content:
        await message.edit(content=message.content + f'\nCurrent winning poll: {", ".join(leading_votes.keys())}')
    else:
        last_poll_result_pos = message.content.find('Current winning poll: ') - 1  # Remove pre-pended \n
        message_content = message.content[:last_poll_result_pos]
        await message.edit(content=message_content + f'\nCurrent winning poll: {", ".join(leading_votes.keys())}')

@client.event
async def on_raw_reaction_remove(self, reaction, *args, **kwargs):
    await self.talley_votes(reaction)

@client.event
async def on_raw_reaction_add(self, reaction, *args, **kwargs):
    await self.talley_votes(reaction)

@client.command()
async def poll(ctx):
    # Check if we're sending to a server (guild) and not a direct message/private message
    # if arg.guild:
    # print(arg)
    # print(arg2)
    # print(arg3)
        # Check if the message starts with !poll
        # if arg.content[:5] == '!poll':

            # Check if the user has a role called 'Admin' (case sensitive)
            # admin = False
            # for role in arg.author.roles:
            #     if role.name == 'Admin':
            #         admin = True
            #         break

            # if admin:
                # Split out the title and individual poll items.
    # cmd, title = arg.split(' ', 1)
    # title, *poll_items = title.split('\n')
    title, *poll_items = "Are you understanding?", "Yes", "No"

    # Build the new message that the bot will send out:
    poll = f'New poll: {title}\n'
    emojis = []
    for index, item in enumerate(poll_items):
        poll += f'{emoji_index[index]}: {item}\n'
        emojis.append(emoji_index[index])

        # Send it, and then add the reactions/emoji's as "buttons" below
        sent_message = await bot_info['_channels']["secret-bot-commands"].send(poll)
        for emoji in emojis:
            await sent_message.add_reaction(emoji)

            # await arg.delete()  # Delete the !poll message


async def on_message(self, message):
    # don't respond to ourselves
    if message.author == self.user:
        return


@client.command()
async def colour(ctx, arg):
    try:
        await ctx.send('Setting color to ' + arg + ' (' + str(webcolors.name_to_rgb(arg)) + ')')
        r, g, b = webcolors.name_to_rgb(arg)
        bulb.set_rgb(r + 1, g + 1, b + 1)
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
    r = random.randint(1, 255)
    g = random.randint(1, 255)
    b = random.randint(1, 255)

    bulb.set_rgb(r, g, b)

    await ctx.send('Setting a random colour! (' + str(r) + ',' + str(g) + ',' + str(b) + ')')


client.run(TOKEN)
