#Libraries______________________________________________________________
import discord
import numpy as np
from discord.ext import commands
import random

#Set Up______________________________________________________________________
bot = commands.Bot(command_prefix = '$')
rules = []
prules = []
fav = []

#Check if Author is bot__________________________________________________
def check(author):
    def inner_check(message):
        return ctx.message.author.bot

#Anounce_Arrival_______________________________________________________
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

#Intro____________________________________________________
@bot.event
async def on_message(message):
    if message.author == bot.user: return #Makes sure it can't loop itself when making messages
    await bot.process_commands(message)
    if message.content.startswith('$hello'):
        channel = message.channel
        await channel.send('Hello {}!'.format(message.author.name))

#Begin____________________________________________________
@bot.command(alliaces = ['go', 'start', 'commence'])
async def begin(ctx):
    rules.clear()
    prules.clear()
    players = []
    for i in bot.users:
        if i.bot == False:
            players.append(i)
    for p in players:
        x = 70*players.index(p)+35
        y = x//840
        pt = [30, 70*y + 35, x - 840*y]
        print(pt)
        rules.append([pt,p.name])
        prules.append(p.name)
    await ctx.send('I have perpared the Pizza Box')
            
#Flip_______________________________________________________        
@bot.command(alliases = ['flip', 'test'])
async def flip(ctx):
    #get x-axis
    await ctx.send('Pick a number between 1-840')
    msg = await bot.wait_for("message")
    #check input is number
    while msg.content.isdigit()== False:
        await ctx.send('It must be a number try again')
        msg = await bot.wait_for("message")
    x = int(msg.content)
    #checks number range
    while x < 1 or x > 840:
        await ctx.send('Pick a number between 1-840')
        msg = await bot.wait_for("message")
        while msg.content.isdigit()== False:
            await ctx.send('It must be a number try again')
            msg = await bot.wait_for("message")
        x = int(msg.content)
    #get y-axis
    await ctx.send('Pick a number between 1-420')
    msg = await bot.wait_for("message")
    #checks is it a number
    while msg.content.isdigit()== False:
        await ctx.send('It must be a number try again')
        msg = await bot.wait_for("message")
    y = int(msg.content)
    #checks is it in range
    while y < 1 or y > 420:
        await ctx.send('Pick a number between 1-420')
        msg = await bot.wait_for("message")
        while msg.content.isdigit()== False:
            await ctx.send('It must be a number try again')
            msg = await bot.wait_for("message")
        y = int(msg.content)    
    z = 0
    distance = 0
    radius = 0
    m_rad = min(x, y, 420-y, 840-x)
    #check if coin in rule circle
    for r in rules:
        pt = r[0]
        radius = pt[0]
        pt_y = pt[1]
        pt_x = pt[2]
        print(pt_x)
        y_diff= pt_y - y
        x_diff = x-pt_x
        distance = np.sqrt(float((y - pt_y)**2+(x-pt_x)**2))
        if distance <= radius:
            await ctx.send(r[1])
            z = 1;
        elif distance - radius < m_rad:
            m_rad = distance - radius
    #gets new rule
    if z==0:
        await ctx.send('What radius would you like? It must be less than {}'.format(int(m_rad)))
        msg = await bot.wait_for("message")
        while msg.content.isdigit()== False:
            await ctx.send('It must be a number try again')
            msg = await bot.wait_for("message")
        rad = int(msg.content)
        while (rad >= m_rad or rad < 0) and rad!=0:
            await ctx.send('What radius would you like? It must be less than {}'.format(int(m_rad)))
            msg = await bot.wait_for("message")
            while msg.content.isdigit()== False:
                await ctx.send('It must be a number try again')
                msg = await bot.wait_for("message")
            rad = int(msg.content)            
        point = [rad, y, x]
        await ctx.send('What rule would you like?')
        msg = await bot.wait_for("message")
        while msg.content.startswith('$') or msg.author.bot:
            msg = await bot.wait_for("message")
        rule = str(msg.content)
        rules.append([point, rule])
        prules.append(rule)
        await ctx.send('I have your rule')
           

#Add Fav___________________________________________________________    
@bot.command(alliases=['add like','add ideas','add fav', 'add'])
async def add_favorite(ctx):
    await ctx.send('What rule would you like to add to favorites?')
    msg = await bot.wait_for("message")
    f = str(msg.content)
    fav.append(f)
    await ctx.send('Rule has been added')

#Tell Favs___________________________________________________________
@bot.command(alliases=['ideas', 'like', 'fav'])
async def favorite(ctx):
    await ctx.send(fav)

#Tell Rules___________________________________________________________
@bot.command()
async def what_rules(ctx):
    await ctx.send(prules)

#End Game______________________________________________________________
@bot.command()
async def end_game(ctx):
    rules.clear()
    prules.clear()
    await ctx.send('I had fun. We should play again sometime. Bye!')

bot.run(token)
