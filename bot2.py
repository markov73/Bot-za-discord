# bot.py
import os
import time
import asyncio
import discord
import urllib.request
import re
import random
from tube_dl import Youtube
from discord.ext import commands

#upišite ime servera
server = 'Drugovi'

svirac = commands.Bot(command_prefix='b')
q = []
trenutni = 0


#lista
def muzika(vc):
    global trenutni
    while True:
        if vc.is_playing():
            print('Sviram')
            time.sleep(1)
            return
        elif len(q) >= 1:
            try:
                pesma = "/home/jakov/Documents/muzickibot/muzika/" + q[trenutni]
                pesma = pesma + ".mp3"
                trenutni = trenutni+1
                print('Trebal bi svirati ' + pesma)
                vc.play(discord.FFmpegOpusAudio(pesma), after=lambda m: muzika(vc))
            except:
                print('Kju je prazan!')
                return
        else:
            return

#spajanje na server
@svirac.event
async def on_ready():
    for guild in svirac.guilds:
        if guild.name == server:
             break
    print(
        f'{svirac.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

#muzika s kompa
@svirac.command(name='sviraj', help='svira muziku s kompjutera')
async def sviraj(ctx, *ime):
    channel = ctx.message.author.voice.channel
    try: await channel.connect()
    except:
        print('Already connected.')
        await ctx.send('Sviram pesmu ' + q[trenutni-1])

#    fajl = "/home/jakov/Documents/muzickibot/muzika/"
    fajl = ime[0]
    duljina = len(ime)
    for x in range(1,duljina):
        fajl = fajl + ' ' + ime[x]
#    fajl = fajl + ".mp3"

    q.append(fajl)
    print(fajl)
    await ctx.send('Dodana je pesma ' + fajl)
    vc = ctx.voice_client
    try: muzika(vc)
    except: print('Vec nekaj sviram.')

#    response = 'Sviram ' + fajl

#    vc = ctx.voice_client
#    vc.play(discord.FFmpegPCMAudio(fajl)
#    ctx.send(response)

#muzika s interneta
@svirac.command(name='download', help='skida muziku s interneta')
async def download(ctx, *query):
    trazi = "https://www.youtube.com/results?search_query="
    trazi = trazi + query[0]
    for x in range(1, len(query)):
        trazi = trazi + '+' + query[x]
    print(trazi)
    html = urllib.request.urlopen(trazi)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    rezultat = "https://www.youtube.com/watch?v=" + video_ids[0]

    channel = ctx.message.author.voice.channel
    try: await channel.connect()
    except:
        print('Already connected.')
        await ctx.send('Sviram pesmu ' + q[trenutni-1])

    upis = query[0]
    for i in range(1,len(query)):
       if i == len(query): upis = upis + query[i]
       else: upis = upis + " " + query[i]
    naredba = 'youtube-dl -x --audio-format mp3 --output "' + upis + '.mp3" ' + rezultat
    os.system(naredba)
    await ctx.send('Skinuto je')

    #sviranje
    q.append(upis)
    print(upis)
    await ctx.send('Dodana je pesma ' + upis)
    vc = ctx.voice_client
    try: muzika(vc)
    except: print('Vec nekaj sviram.')


#pauziranje
@svirac.command(name='pauza', help='pauira muziku')
async def pauziraj(ctx):
    vc = ctx.voice_client
    try: vc.pause()
    except:
        response = 'Vec je pauzirano. Jebo ti pas mater glupu'
        await ctx.send(response)

#resume
@svirac.command(name='nastavi', help='nastavlja muziku nakon pauziranja')
async def nastavak(ctx):
    vc = ctx.voice_client
    try: vc.resume()
    except:
        response = 'Nikaj je ne pauzirano. Naj me jebati'
        await ctx.send(response)

#skip
@svirac.command(name='skip', help='preskace trenutni track')
async def skip(ctx):
    vc = ctx.voice_client
    try: vc.stop()
    except:
        response = 'Nist ne sviram'
        await ctx.send(response)

#remove from queue
@svirac.command(name='remove', help='brise pesmu sa kjua (index obavezan)')
async def remove(ctx, *imena):
    upis = imena[0]
    for x in range(1,len(imena)):
        upis = upis + ' ' + imena[x]
    try:
        q.remove(upis)
        trenutni = trenutni -1
    except:
        response = 'Nema pesme na tom mestu u kjuu'
        await ctx.send(response)

#disconnect
@svirac.command(name='disconnect', help='diskonektuje sa servera')
async def disconnect(ctx):
    try:
        kanal = ctx.voice_client.channel
        await ctx.voice_client.disconnect()
    except:
        await ctx.send('Nisam spojen. Koji ti je kurac?')

@svirac.command(name='lista', help='ispisuje kaj je na listi')
async def lista(ctx):
    for x in range(trenutni,len(q)):
        response = str(x-trenutni+1) + " " + q[x]
        await ctx.send(response)

@svirac.command(name='miks', help='shuffle')
async def miks(ctx):
    global q
    global trenutni
    pizda = []
    for x in range(trenutni,len(q)):
        pizda.append(q[x])
    random.shuffle(pizda)
    
    print(pizda)

    for x in range(0,len(pizda)):
        q.append(str(pizda[x]))

    trenutni=trenutni+len(pizda)

#upišite token s discordove stranice
svirac.run('ODIwNjIzMTY4MzE3NDIzNjM2.YE324Q.dM3h8q57JPTT698Jdz9NyV39Gbg')
