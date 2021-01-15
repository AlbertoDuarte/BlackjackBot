import os
import time

import discord
from discord.ext import commands
from dotenv import load_dotenv
from game import Game

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = '!'
TIMEOUT_INTERVAL = 15

bot = commands.Bot(command_prefix = PREFIX)
t = time.time()
game = Game()
game.seed(int(time.time()))
game_done = True

@bot.event
async def on_ready():
    print('{} has connected to Discord!'.format(bot.user))

@bot.command(name='play')
async def play(ctx, arg : str):
    global game_done

    if arg == 'start':
        game_done = False
        state = game.reset()
        render_string = game.render(mode='ansi')
        await ctx.send(render_string)

        return

    elif arg == 'hit':
        action = 'h'
    elif arg == 'stand':
        action = 's'
    else:
        await ctx.send('Invalid command')
        return

    if game_done:
        await ctx.send('Game finished! Start a new game with {}play start'.format(PREFIX))
        return

    state, reward, game_done, _ = game.step(action)
    render_string = game.render(mode='ansi')

    await ctx.send(render_string)

@bot.command(name='rules')
async def rules(ctx):
    await ctx.send('Not implemented')

bot.run(TOKEN)
