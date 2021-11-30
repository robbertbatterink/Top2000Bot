import discord
from discord import FFmpegPCMAudio
from discord.ext import commands as cmd
from top2000 import TOP2000
from dotenv import load_dotenv
import os

client = cmd.Bot(command_prefix = '/')

player = None
top2000Bool = False
load_dotenv()

@client.event
async def on_ready():
    print("Bot is ready!")

@client.command()
async def top2000(ctx, commando=None, int=5):
    global player, top2000Bool, top2000
    radio = TOP2000()

    if commando == "nu":
        song = radio.get_current_song()
        embed = discord.Embed(title="Top 2000", description="Nummer dat zich nu afspeelt", color=0xff0000)
        if "number" in song.keys():
            embed.add_field(name="Plaats in de lijst:", value=song['number'], inline=False)

        embed.add_field(name="Titel van het nummer:", value=song['title'], inline=False)
        embed.add_field(name="Gemaakt door artiest:", value=song['artist'], inline=True)
        if "thumbnail" in song.keys():
            if song['thumbnail'] is not None:
                    embed.set_thumbnail(url=song['thumbnail'])

        if "year" in song.keys():
            embed.add_field(name="Uit het jaar:", value=song['year'], inline=False)

        await ctx.send(embed=embed)

    elif commando == "lijst":
        songs = radio.get_future_song(int)
        for song in songs:
            embed = discord.Embed(title="Top 2000", description="Nummer uit de lijst", color=0xff0000)
            if "number" in song.keys():
                embed.add_field(name="Plaats in de lijst:", value=song['number'], inline=False)

            embed.add_field(name="Titel van het nummer:", value=song['title'], inline=False)
            embed.add_field(name="Gemaakt door artiest:", value=song['artist'], inline=True)
            if "thumbnail" in song.keys():
                if song['thumbnail'] is not None:
                    embed.set_thumbnail(url=song['thumbnail'])

            if "year" in song.keys():
                embed.add_field(name="Uit het jaar:", value=song['year'], inline=False)

            await ctx.send(embed=embed)

    elif commando is None and top2000Bool is False and player is None:
        channel = client.get_channel(ctx.message.author.voice.channel.id)
        player = await channel.connect()
        player.play(FFmpegPCMAudio("http://icecast.omroep.nl/radio2-bb-mp3"))
        top2000Bool = True
        
    elif commando is None and top2000Bool is False:
        player.stop()
        player.play(FFmpegPCMAudio("http://icecast.omroep.nl/radio2-bb-mp3"))
        top2000Bool = True

@client.command()
async def stop2000(ctx):
    global player, top2000Bool
    player.stop()
    await player.disconnect()
    player = None
    top2000Bool = False

client.run(os.getenv('BOT_TOKEN'))
