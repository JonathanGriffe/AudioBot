import discord
from discord.ext import commands
import asyncio
import glob
import ffmpeg
import random
import time
import os
token = os.environ['DS_TOKEN']
absence_de_bot = 716741076920303627

#find quotes with name containing a string
# returns quote "no" if not found
def find(string):
    for str in file:
        if(str.lower().find(string.lower()) != -1):
            return str
    return "./quotes/2 no.mp3"

def init():
    client = commands.Bot('!')
    client.vc = None

    client.jointime = [0,0,0,0,0,0,0] #time where monitored user was last seen entering a voice chat
    client.nbquotes = 0 #amount of quotes
    client.voicenames = ["./quotes/j.mp3","./quotes/t.mp3","./quotes/s.mp3","./quotes/f.mp3","./quotes/lu.mp3","./quotes/lo.mp3","./quotes/c.mp3"] #samples to play when monitored user enters a voice chat
    client.ids = [493136445146184201,369134955931155906,193039217056604160,353977157139920896,179211720469626897,310337512755727361,222943156640905216] #monitored users id
    client.adminIDs = [493136445726184201,369134915932155906,179211720469626897,310337512755727361] # ids of users authorized to add samples

    file=[]
    while True:
        #searches for sample in quotes directory and creates a command to play each sample
        client.nbquotes += 1
        quoteNames = glob.glob('./quotes/'+str(client.nbquotes)+' *.mp3')
        if len(quoteNames) == 0:
            client.nbquotes -= 1
            break
        for fileName in quoteNames:
            file.append(fileName)
            print(fileName)
            print(client.nbquotes)

        print(client.nbquotes)
        @client.command(name=str(client.nbquotes))
        async def _(ctx):
            channel = ctx.author.voice.channel
            if(client.vc != None and client.vc.is_playing()):
                return
            if(channel==None):
                return
            if(client.vc != None):
                chanActuel = client.vc.channel
            else:
                chanActuel = None
            if(channel != chanActuel):
                if(chanActuel != None):
                    await client.vc.disconnect()
                client.vc= await channel.connect()
            print(file[int(ctx.command.name)-1])
            print(int(ctx.command.name)-1)
            source = discord.FFmpegPCMAudio(file[int(ctx.command.name)-1])
            client.vc.play(source)
            while client.vc.is_playing():
                await asyncio.sleep(1)

    #command to search and play a quotes using a extract of its name
    @client.command()
    async def q(ctx, nom):
        channel = ctx.author.voice.channel
        if(client.vc != None and client.vc.is_playing()):
            return
        if(channel==None):
            return
        if(client.vc != None):
            chanActuel = client.vc.channel
        else:
            chanActuel = None
        if(channel != chanActuel):
            if(chanActuel != None):
                await client.vc.disconnect()
            client.vc= await channel.connect()
        source = discord.FFmpegPCMAudio(find(nom))
        client.vc.play(source)
        while client.vc.is_playing():
            await asyncio.sleep(1)

    @client.command()
    async def yurop(ctx):
        await ctx.channel.send(":flag_eu:")
        await ctx.channel.send("YUROP")
        await ctx.channel.send(":flag_eu:")
        if(client.vc != None and client.vc.is_playing()):
            return
        channel = ctx.author.voice.channel
        if(channel == None):
            return
        if(client.vc != None):
            chanActuel = client.vc.channel
        else:
            chanActuel = None
        if(channel != chanActuel):
            if(chanActuel != None):
                await client.vc.disconnect()
            client.vc = await channel.connect()
        source = discord.FFmpegPCMAudio("quotes/yurop.mp3")
        client.vc.play(source)
        while client.vc.is_playing():
            await asyncio.sleep(1)
            
        
    #command playing a random sample
    @client.command()
    async def rand(ctx):
        if(client.vc != None and client.vc.is_playing()):
            return
        i = random.randint(1,client.nbquotes + 1)
        channel = ctx.author.voice.channel
        if(client.vc != None):
            chanActuel = client.vc.channel
        else:
            chanActuel = None
        if(channel != chanActuel):
            if(chanActuel != None):
                await client.vc.disconnect()
            client.vc= await channel.connect()
        source = discord.FFmpegPCMAudio(file[i-1])
        await ctx.channel.send(file[i-1][9:-4])
        client.vc.play(source)
        while client.vc.is_playing():
            await asyncio.sleep(1)


    @client.command()
    async def harass(ctx):
        if(client.vc != None and client.vc.is_playing()):
            return
        for channel in ctx.guild.voice_channels:
            if(len(channel.members) !=0):
                if(client.vc != None and channel != client.vc.channel):
                    await client.vc.disconnect()
                if(client.vc == None or client.vc.channel == None):
                    client.vc = await channel.connect()
                source = discord.FFmpegPCMAudio(file[52])
                client.vc.play(source)
                while client.vc.is_playing():
                    await asyncio.sleep(1)


    @client.command()
    async def cassetoi(ctx):
        if(client.vc != None):
            await client.vc.disconnect()
        client.vc = None

    #command adding a new sample
    @client.command()
    async def add(ctx):
        if(not ctx.author.id in client.adminIDs):
            return
        att = ctx.message.attachments[0]
        client.nbquotes += 1
        await att.save("./quotes/"+str(client.nbquotes)+" "+att.filename)
        file.append("./quotes/"+str(client.nbquotes)+" "+att.filename)
        @client.command(name=str(client.nbquotes))
        async def _(ctx):
            channel = ctx.author.voice.channel
            if(client.vc != None and client.vc.is_playing()):
                return
            if(channel==None):
                return
            if(client.vc != None):
                chanActuel = client.vc.channel
            else:
                chanActuel = None
            if(channel != chanActuel):
                if(chanActuel != None):
                    await client.vc.disconnect()
                client.vc= await channel.connect()
            print(file[int(ctx.command.name)-1])
            print(int(ctx.command.name)-1)
            source = discord.FFmpegPCMAudio(file[int(ctx.command.name)-1])
            client.vc.play(source)
            while client.vc.is_playing():
                await asyncio.sleep(1)
        await ctx.channel.send("Quote " + "./quotes/"+str(client.nbquotes)+" "+att.filename + " ajoutée")
            
    
    @client.event
    async def on_typing(channel, user, when):
        if(channel == client.get_channel(absence_de_bot)):
            await channel.send("Je suis là")

    #event to greet monitored members joining
    @client.event
    async def on_voice_state_update(member, before, after):
        if(after.channel != None and before.channel == None):
            for i in range(len(client.ids)):
                if(member.id == client.ids[i] and time.time() - client.jointime[i] > 60*60*5):
                    client.jointime[i] = time.time()
                    if(client.vc != None and client.vc.channel != after.channel):
                        await client.vc.disconnect()
                    if(client.vc == None):
                        client.vc = await after.channel.connect()
                    client.vc.play(discord.FFmpegPCMAudio(file[59]))   
                    while client.vc.is_playing():
                        await asyncio.sleep(1)
                    client.vc.play(discord.FFmpegPCMAudio(client.voicenames[i]))
                    while client.vc.is_playing():
                        await asyncio.sleep(1)
                    return
    return client

async def close():
    global bot
    await bot.close()

bot = init()
bot.run(token)