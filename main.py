import asyncio
import os
import discord
import requests
import random
import youtube_dl
import ffmpeg
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from discord.ext import tasks, commands
# imports all of depenancies 

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# sets bot token to access the discord servers

intents = discord.Intents().all()
client = discord.Client(8)
bot = commands.Bot(command_prefix='!',intents=intents)
# defines the client and bots as well as set its intents to all because its a req to use if you want it in more than one server

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': False,
    'download': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': False,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
# download settings might use for high quality audio

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}
# sets up youtube stream settings

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="tango! help"))
    bot_info = await client.application_info()
    # When it connects to discord it sets the bots status and prints that it has connected in the console


@client.event
async def on_message(message):
    split_message = message.content.split()
    # splits the message to check for call
    sender_id = message.author.discriminator
    #identifier number to check if bot sent the message
    if not message.author.voice:
        donothing = True
    else:
        channel = message.author.voice.channel
        voice_client = message.guild.voice_client 
    # Checks if the message sender is in a voice channel if it isnt sets a null and if they are sets what vc they are in to join
    if split_message[0] == 'tango!':
        # if you start your message with "!tango" check these
        if split_message[1] == 'help' or split_message[1] == 'Help':
            # print("made it to section 2")
            response = "*This is the help page for the bot\n\nList of cmds:\n\"tango! help\"\nThis gets you to where you are now\n\n\"tango! gif <search query>\"\nThis searches a word and pulls a gif that matches\n\n\"tango! GLaDOS\"\nPrints out a random GLaDOS quote from the Portal games\n\n\"tango! xkcd <Optional specific number>\"\n This prints either a random xkcd comic or a specified one\"tango! join\"\nMakes the bot join the voice channel you are in\n\n\"tango! play <Youtube link>\"\nPlays the audio of the youtube video in a voice chat\n\n\"tango! pause\"\nPauses the audio in the voice chat\n\n\"tango! resume\"\nResumes the music where you paused it\n\n\"tango! stop\"\nStops the audio entirely\n\n\"tango! leave\"\nMakes the bot leave the voice channel*"
            await message.channel.send(response)
        # if message says "tango! help" print this

        if split_message[1] == 'gif':
            search_Query = split_message[2]
            URL = "https://gfycat.com/gifs/search/" + search_Query
            # searches the word following "gif"
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            # get page and set a html parser on the page
            img_elem = soup.find_all('img')
            # gets all elements that are img
            ron = len(img_elem)
            # puts them in an array
            nor = random.randrange(0, ron)
            # picks a random one from the array 
            gotten_img = img_elem[nor].get('src')
            # gets the image
            await message.channel.send(gotten_img)
        
        if split_message[1] == 'GLaDOS':
            URL = "https://theportalwiki.com/wiki/GLaDOS_voice_lines"
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            # gets page and sets it as a html parser
            listed_quotes = soup.find_all('i')
            # finds all elements 'i'
            quo = len(listed_quotes)
            # puts them in an array 
            tes = random.randrange(0, quo)
            # picks a random one
            quoted = listed_quotes[tes].text.strip()
            # makes sure that the text isnt wonky
            await message.channel.send(quoted)

        if split_message[1] == 'xkcd':
            if len(split_message) == 3:
                # if message has three parts
                URL = "https://xkcd.com/" + split_message[2]
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, "html.parser")
                x_img = soup.find('div', {'id' : "comic"})
                y_img = x_img.findChildren("img", recursive=False)[0]
                xkcd_img = y_img.get('src')
                got_img = "https:" + xkcd_img
                await message.channel.send(got_img)
            else:
                rando = random.randrange(1, 2624)
                randod = str(rando)
                numOutput = "Comic number: "+ randod
                URL = "https://xkcd.com/" + randod
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, "html.parser")
                x_img = soup.find('div', {'id' : "comic"})
                y_img = x_img.findChildren("img", recursive=False)[0]
                xkcd_img = y_img.get('src')
                got2_img = "https:" + xkcd_img
                await message.channel.send(got2_img)
                await message.channel.send(numOutput)
        
        if split_message[1] == 'join':
            if not message.author.voice:
                await message.channel.send("{} is not connected to a voice channel".format(message.author.name))
                return
            else:
                await channel.connect()

        
        if split_message[1] == 'leave':
            if voice_client.is_connected():
                await voice_client.disconnect()
            else:
                await message.channel.send("The bot is not connected to a voice channel.")
        
        if split_message[1] == 'play':
            url = split_message[2]

            with youtube_dl.YoutubeDL(ytdl_format_options):
                info = ytdl.extract_info(url, download=False)
                # gets the page and does NOT download it
                url2 = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                # get ffmpeg audio
                voice_client.play(source)
                # start playing the ffmpeg audio in vc
        
        if split_message[1] == 'pause':
            if voice_client.is_playing():
                await voice_client.pause()
            else:
                await message.channel.send("The bot is not playing anything at the moment.")

        if split_message[1] == 'resume':
            if voice_client.is_paused():
                await voice_client.resume()
            else:
                await message.channel.send("The bot was not playing anything before this. Use play_song command")

        if split_message[1] == 'stop':
            if voice_client.is_playing():
                await voice_client.stop()
            else:
                await message.channel.send("The bot is not playing anything at the moment.")

client.run(TOKEN)
# starts up everything with the bot token