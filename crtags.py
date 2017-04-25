import requests
import os
import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from .utils.chat_formatting import escape_mass_mentions, italics, pagify
import json
from bs4 import BeautifulSoup
from .utils import checks
import urllib
import urllib.request
from urllib.request import Request, urlopen
import asyncio
import aiohttp
statscr_url = "http://statsroyale.com/profile/"
soup = 1
PATH = os.path.join("data", "crtags")
SETTINGS_JSON = os.path.join(PATH, "settings.json")
validChars = ['0', '2', '8', '9', 'C', 'G', 'J', 'L', 'P', 'Q', 'R', 'U', 'V', 'Y']
tags= {}
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

class JSONObject:
     def __init__(self, d):
             self.__dict__ = d
class Player:

    def __init__(self, bot):
        self.settings = dataIO.load_json(SETTINGS_JSON)
        self.bot = bot

    def is_valid(self, tag):
        for letter in tag:
            if letter not in validChars:
                return False
        return True

    @commands.command(pass_context=True)
    async def test(self, ctx):
        """test cmd"""
        await self.bot.say("the test worked")

    @commands.command(pass_context=True )
    async def myid(self, ctx):
        """show your discord ID"""
        print(html_doc)
        await self.bot.say("ID: {}".format(ctx.message.author.id))

    @commands.command(pass_context=True)
    async def settag(self, ctx, tag):
        """Save user tag. If not given a user, save tag to author"""
        tag = tag.upper()
        valid = True
        for letter in tag:
            if letter not in validChars:
                valid = False
        if valid: #self.is_valid(tag):
            author = ctx.message.author
            await self.bot.say("Saving {} for {}".format(tag, italics(author.display_name)))
            self.settings[author.id] = str(tag)
            dataIO.save_json(SETTINGS_JSON, self.settings)
        else:
            await self.bot.say("Invalid tag {}, it must only have the following characters {}".format(italics(author.mention), validChars)) 

    @commands.command(pass_context=True)
    @checks.mod_or_permissions()
    async def setusertag(self, ctx, user: discord.Member, tag):
        """Save user tag. If not given a user, save tag to author"""
        if user == None:
            user = ctx.message.author
        tag = tag.upper()
        valid = True
        for letter in tag:
            if letter not in validChars:
                valid = False
        if valid: #self.is_valid(tag):
            author = ctx.message.author
            await self.bot.say("Saving {} for {}".format(tag, italics(user.display_name)))
            self.settings[user.id] = str(tag)
            dataIO.save_json(SETTINGS_JSON, self.settings)
        else:
            await self.bot.say("Invalid tag {}, it must only have the following characters {}".format(italics(ctx.message.author.mention), validChars)) 

    @commands.command(pass_context=True)
    async def gettag(self, ctx, user: discord.Member=None):
        """Get user tag. If not given a user, get author's tag"""
        tags = dataIO.load_json(SETTINGS_JSON)
        if(user==None):
            if tags[ctx.message.author.id]:
                await self.bot.say("Your tag is {}.".format(tags[ctx.message.author.id]))
            else:
                await self.bot.say("You, {} do not have a tag set.".format(ctx.message.author.display_name))
        else:
            if tags[user.id]:
                await self.bot.say("{}'s tag is {}.".format(user.mention, tags[user.id]))
            else:
                await self.bot.say("User {} does not have a tag set.".format(user.display_name))

    @commands.command(pass_context=True)
    async def profile(self, ctx, user: discord.Member=None):
        """Get user profile. If not given a user, get author's profile"""
        tags = dataIO.load_json(SETTINGS_JSON)
        if user == None:
            user = ctx.message.author
        user_url = (statscr_url)
        
        r = requests.get(user_url, headers)
        print("\n\nraw html:\n\n")
        print(html) 
        # opener = AppURLopener()
        # response = opener.open(user_url)
        # html=response.read()
        #req = Request(user_url, headers={'User-Agent': 'Mozilla/5.0'})
        #html = urlopen(req).read()
        #print(html)
        # print(user_url)
        # with urllib.request.urlopen() as response:
        #     html = response.read()
        #     # and if you wanna verify that you have loaded the html correctly
        #     # you can just print it to console
        #     print(html)
        #soup = BeautifulSoup(html_doc, 'html.parser')
        #print(soup.title.string)

def check_folder():
    if not os.path.exists(PATH):
        os.makedirs(PATH)

def check_file():
    defaults = {}
    if not dataIO.is_valid_json(SETTINGS_JSON):
        dataIO.save_json(SETTINGS_JSON, defaults)

def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Player(bot))
