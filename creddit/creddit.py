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
from random import randint
from random import choice
PATH = os.path.join("data", "misc")
SETTINGS_JSON = os.path.join(PATH, "settings.json")
redditUrl="https://www.reddit.com/"

headers = {
    'User-Agent': 'Bot(Rain), (https://github.com/Dino0631/discordbot/tree/master)',
    'From': '<youremailhere>'  
}
class Creddit:

    def __init__(self, bot):
        self.settings = dataIO.load_json(SETTINGS_JSON)
        self.bot = bot
    @commands.command()
    async def creddit(self, post=1, sort='hot', announce='no'):
        """Get top(sorted by "hot") reddit posts of r/CR
        If you want to get the #2 post do:
        !creddit 2
        If you want to get the top post sorted by "rising" do:
        !creddit 1 rising

        !creddit rising 
        will not work because it will assume you want the rising'th post 
        sorted by "hot"(default sort)
        
        If you want the top announcement do
        yes or y to say that you want just the announcements
        !creddit 1 hot yes
        """
        if(post<1 or post>20):
            post = 1
        if(sort == 'hot' or sort.lower() == 'new' or sort.lower() == 'rising' or 
            sort.lower() == 'controversial' or sort.lower() == 'top' or sort.lower() == 'gilded'):
            pass
        else:
            sort='hot'
        if sort=='hot':
            sort=''
        subreddit='cr'
        if(subreddit.lower() == "clashroyale" or subreddit.lower() == "cr"):
            url = redditUrl + "r/" + "ClashRoyale" +"/" + sort
            r = requests.get(url, headers=headers)
            html_doc = r.content
            soup = BeautifulSoup(html_doc, "html.parser")
            link3 = soup.find_all("p", "title")
            ifannounce = soup.find_all("p", "tagline ")
            bean = "url=\""
            bean2 = "rel>"
            bean3 = "tabindex=\"1\">"
            print("\n\nlink3s: {}\n\n".format(link3))
            print("\n\nifannounce: {}\n\n".format(ifannounce))
            print(link3[post-1])
            print(ifannounce[post-1])
            print("\n{} link3 posts".format(len(link3)))
            print("\n{} ifannounce posts".format(len(ifannounce)))

            print(type(str(ifannounce[1])[5 : 7]))
            print("b")

            bean6 = str(ifannounce[1])
            bean5 = bean6[bean6.find("\'s moderators\"") + len("\'s moderators\""): ]
            print(bean5)
            print(bean5[ : bean5.find("/span></p>")])


            amtannounce = 0
            if not (announce == 'yes' or announce == 'y'):
                for i in range( 0, len(ifannounce)-1):
                    bean6 = str(ifannounce[i])
                    bean5 = bean6[bean6.find("\'s moderators\"") + len("\'s moderators\""): ]

                    # print(bean5[ : bean5.find("/span></p>")])
                    if(bean5[ : bean5.find("/span></p>")]=='>announcement<'):
                        amtannounce+=1
            print("\n\n{}\n\n".format(amtannounce))
            topreddit = str(link3[post-1+amtannounce])


            bean4 = topreddit[topreddit.find(bean)+len(bean):]
            print("{} start, {} finish".format(topreddit.find(bean)+len(bean), topreddit.find(bean)+len(bean)+bean4.find("\" ")))
            toplink = topreddit[topreddit.find(bean)+len(bean) : topreddit.find(bean)+len(bean)+bean4.find("\" ")]
            toptitle = topreddit[topreddit.find(bean3)+len(bean3) : topreddit.find("</a>")]
            await self.bot.say("Top post on the `r/ClashRoyale` reddit: \n{}\nTitle: `{}`".format(redditUrl + toplink, toptitle))

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
    bot.add_cog(Creddit(bot))
