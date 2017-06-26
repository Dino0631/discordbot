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
import math
PATH = os.path.join("data", "misc")
SETTINGS_JSON = os.path.join(PATH, "settings.json")
redditUrl = "https://www.reddit.com/"
max_desc_chars = 300 # max chars for the description in the embed


headers = {
    'User-Agent': 'Bot(Rain), (https://github.com/Dino0631/discordbot/tree/master)',
    'From': 'htmldino@gmail.com'  
}
class Reddit2:

    def __init__(self, bot):
        self.settings = dataIO.load_json(SETTINGS_JSON)
        self.bot = bot
    @commands.command(pass_context=True) #add author, link to author, date, u/d botes
    async def r(self, ctx, sub='r', post=1, sort='hot', announce='no'):
        """Get top(sorted by "hot") reddit posts of r/sub
        To get top post of the main page do 
        !r
        !r r
        !r r 1
        If you want to get the #2 post do:
        !r r 2
        If you want to get the top post sorted by "rising" do:
        !r 1 rising

        !r rising 
        will not work because it will assume you want the rising'th post 
        sorted by "hot"(default sort)
        
        If you want the top announcement do
        yes or y to say that you want just the announcements
        !r 1 hot yes

        If the sort is not "controversial," "hot," "rising," "top," "new," or "guilded"
        then it will default to "hot"
        """
        server = ctx.message.server
        # server.emojis = 
        if(post<1 or post>20):
            post = 1
        if(sort == 'hot' or sort.lower() == 'new' or sort.lower() == 'rising' or 
            sort.lower() == 'controversial' or sort.lower() == 'top' or sort.lower() == 'gilded'):
            pass
        else:
            sort='hot'
        if sort=='hot':
            sort=''
        if(sub=='r'):
            sub=''
        else:
            sub = 'r/'+sub
        if(1):
            url = redditUrl + sub +"/" + sort
            try:
            	r = requests.get(url, headers=headers)
            except:
            	await self.bot.say("Invalid subreddit")
            html_doc = r.content
            soup = BeautifulSoup(html_doc, "html.parser")
            # link = soup.find_all("a", "title may-blank outbound")
            # link2 = soup.find_all("a", "title may-blank ")
            link3 = soup.find_all("p", "title")
            ifannounce = soup.find_all("p", "tagline ")
            votes = soup.find_all("div", "score unvoted")
            commentFinder = soup.find_all("ul",  "flat-list buttons")
            bean = "url=\""
            bean2 = "rel>"
            bean3 = "tabindex=\"1\">"
            # print(url)
            # print("\n\nlinks: {}\n\n".format(link))
            # print(link[post-1])
            # print("\n{} posts".format(len(link)))
            # print("\n\nlink2s: {}\n\n".format(link2))
            # print(link2[post-1])
            # print("\n{} link2 posts".format(len(link2)))
            # print("\n\nlink3s: {}\n\n".format(link3))
            # print("\n\nifannounce: {}\n\n".format(ifannounce))
            # print(link3[post-1])
            # print(ifannounce[post-1])
            # print("\n{} link3 posts".format(len(link3)))
            # print("\n{} ifannounce posts".format(len(ifannounce)))
            # print(soup.prettify())

            # print(ifannounce[post-1])
            # print(type(str(ifannounce[1])[5 : 7]))
            # print("b")

            # bean6 = str(ifannounce[1])
            # bean5 = bean6[bean6.find("\'s moderators\"") + len("\'s moderators\""): ]
            # print(bean5)
            # print(bean5[ : bean5.find("/span></p>")])


            amtannounce = 0
            if not (announce.lower() == 'yes' or announce.lower() == 'y'):
                for i in range( 0, len(ifannounce)-1):
                    bean6 = str(ifannounce[i])
                    bean5 = bean6[bean6.find("\'s moderators\"") + len("\'s moderators\""): ]

                    # print(bean5[ : bean5.find("/span></p>")])
                    if(bean5[ : bean5.find("/span></p>")]=='>announcement<'):
                        amtannounce+=1
            # print("\n\n{}\n\n".format(amtannounce))
            try:
                topreddit = str(link3[post-1+amtannounce])
            except:
                await self.bot.say("Invalid subreddit")
                return #not a valid subreddit

            bean4 = topreddit[topreddit.find(bean)+len(bean):]
            # print("{} start, {} finish".format(topreddit.find(bean)+len(bean), topreddit.find(bean)+len(bean)+bean4.find("\" ")))
            toplink = topreddit[topreddit.find(bean)+len(bean) : topreddit.find(bean)+len(bean)+bean4.find("\" ")]
            toptitle = topreddit[topreddit.find(bean3)+len(bean3) : topreddit.find("</a>")]
            if(toplink[:4]=='http'):
                postlink = toplink
                isText=False
            else:
                postlink = redditUrl + toplink
                isText=True
            if(sub!=''):
                await self.bot.say("Post #{} on the **{}** subreddit:".format(post, sub))
            else:
                await self.bot.say("Post #{} on **Reddit**:".format(post, sub))
            # await self.bot.say('beans'.find('y'))
            # await self.bot.say('`{}`'.format(server.emojis[1]))
            if(isText):
                r = requests.get(postlink, headers=headers)
                html_doc = r.content
                soup = BeautifulSoup(html_doc, "html.parser")
                thing = soup.find_all("div", "md")
                thing2 = soup.find_all("div", "usertext-body may-blank-within md-container ")
                thing3 = soup.find_all("div", "score")
                # print("\n\n\n{}\n\n\n".format(thing3))

                # print("\n\n{}\n\n".format(thing[1])) # full desc
                fulldesc = str(thing2[1])
                fulldesc = fulldesc.replace('<div class=\"usertext-body may-blank-within md-container \">', '')
                fulldesc = fulldesc.replace('<div class=\"md\">', '')
                fulldesc = fulldesc.replace('<p>', '')
                fulldesc = fulldesc.replace('</p>', '')
                fulldesc = fulldesc.replace('</div>', '')
                if(len(fulldesc)<=max_desc_chars):
                	desc=fulldesc
                else:
                	desc = fulldesc[:max_desc_chars]+'...'
                postembed = discord.Embed(title=toptitle, description=(desc), url=postlink, color=0x2299fe)
                postembed.set_thumbnail(url='https://pbs.twimg.com/profile_images/868147475852312577/fjCSPU-a_400x400.jpg')

            else: #image or gif
                postembed = discord.Embed(title=toptitle, url=postlink, color=0x2299fe)
                if(postlink[-4:]=='.jpg' or postlink[-4:]=='.png' or postlink[-4:]=='.gif' or postlink[-4:]=='.mp4'
                    or postlink.find('.jpg') != -1 or postlink.find('.png') != -1 or postlink.find('.gif') or postlink.find('gfy') != -1 or postlink.find('.mp4') != -1):
                    if(postlink[-4:]=='.gif' or postlink[-4:]=='.mp4' or postlink.find('.gif') != -1 or postlink.find('.mp4') != -1 or postlink.find('.gif')):
                        postembed.set_thumbnail(url='https://pbs.twimg.com/profile_images/868147475852312577/fjCSPU-a_400x400.jpg')
                    else:
                        postembed.set_thumbnail(url=postlink)
                else:
                    r2 = requests.get(postlink, headers=headers)
                    html_doc2 = r2.content
                    # print(html_doc2)
                    soup2 = BeautifulSoup(html_doc2, "html.parser")
                    thing4 = soup2.find_all('img')
                    # print(thing4)
                    x = str(thing4[1])
                    # thing4 = x[x.find('src=\"')+len('src=\"'):x.find('\"/>')]
                    # print(thing4)
                postembed.set_image(url=postlink)
                if(announce.lower() == 'yes' or announce.lower() == 'y'):
                    tagline = ifannounce[post]
                else:
                    tagline = ifannounce[post-1+amtannounce]
                if(announce.lower() == 'yes' or announce.lower() == 'y'):
                    commenturl = str(commentFinder[post])
                else:
                    commenturl = str(commentFinder[post-1+amtannounce])
                commenturl = commenturl[commenturl.find('url=\"')+len('url=\"') : commenturl.find('\" data-inbound-url')]
                commenturl = redditUrl + commenturl
                r = requests.get(commenturl, headers=headers)
                html_doc = r.content
                soup = BeautifulSoup(html_doc, "html.parser")
            thing3 = soup.find_all("div", "score")
            # print("\n\n\n{}\n\n\n".format(thing3))
            upvoteperc = str(thing3[0])
            upvoteperc = upvoteperc.replace('<div class="score"><span class="number">', '')
            upvoteperc = upvoteperc[upvoteperc.find('</span>')+len('</span>'):upvoteperc.find('%'+' upvoted')]
            upvoteperc = upvoteperc[upvoteperc.find('</span> (')+len('</span> ('):]
            # print(upvoteperc)
            upvoteperc = int(upvoteperc)
            upvoteperc = upvoteperc/100


            ifannounce[post-1+amtannounce]
            upvotes = str(votes[post-1+amtannounce])
            upvotes = upvotes.replace('<div class=\"score unvoted\" title=\"', '')
            upvotes = upvotes.replace('\">', '')
            upvotes = upvotes.replace('</div>', '')
            length = len(upvotes)
            upvotes = upvotes[0:int(float(length/2))]

            try:
                netupvotes = int(upvotes)
                upvotes = (2*netupvotes - 2*netupvotes*upvoteperc)/(4*upvoteperc - 2)+netupvotes
                downvoteperc = str(int(round(1 - upvoteperc, 2)*100))+'%'
                upvoteperc = str(int(upvoteperc*100))+ '%'
                downvotes = upvotes - netupvotes
                totalvotes = upvotes + downvotes
                downvotes = str(round(downvotes))
                upvotes = str(round(upvotes))
                netupvotes = str(round(netupvotes))
                totalvotes = str(round(totalvotes))
            except:
                upvotes = '0'
                upvoteperc = '0.0%'
                downvoteperc = '0.0%'
                totalvotes = '0'
                downvotes = '0'
                netupvotes = '0'

            # print("{}\n{}\n{}\n{}\n{}\n{}".format(downvoteperc, upvoteperc, downvotes, upvotes, netupvotes, totalvotes))
            # print("{}\n{}\n{}\n{}\n{}\n{}".format(type(downvoteperc), type(upvoteperc), type(downvotes), type(upvotes), type(netupvotes), type(totalvotes)))
            

            if(announce.lower() == 'yes' or announce.lower() == 'y'):
                tagline = str(ifannounce[post-1])
            else:
                tagline = str(ifannounce[post-1+amtannounce])
            
            downvotegraph = ''
            # print("\n\n{}\n\n".format(downvoteperc[0:-1]))
            downvotecircles = float(downvoteperc[0:-1])/10
            if((downvotecircles)<(math.floor(downvotecircles)+.5)):
                downvotecircles = math.floor(downvotecircles)
            else:
                downvotecircles = math.ceil(downvotecircles)
            
            # print(downvotecircles)
            # print(((math.floor(downvotecircles)+.5)))
            
            upvotecircles = float(upvoteperc[0:-1])/10
            partupcircle = upvotecircles - int(upvotecircles)
            upvotecircles = int(upvotecircles)
            partupcircle = str(partupcircle)[2:3]
            downvotecircles = float(downvoteperc[0:-1])/10
            partdowncircle = downvotecircles - int(downvotecircles)
            downvotecircles = int(downvotecircles)
            partdowncircle = str(partdowncircle)[2:3]
            # print(downvotecircles, ' ', partdowncircle)
            # print(upvotecircles, ' ', partupcircle)
            # if(upvotecircles<(math.floor(upvotecircles)+.5)):
            #     upvotecircles = math.floor(upvotecircles)
            # else:
            #     upvotecircles = math.ceil(upvotecircles)
            # print(upvotecircles)
            # print(((math.floor(upvotecircles)+.5)))
            partbluesq=''
            partredsq=''
            netupvotegraph=''
            upvotegraph=''
            downvotegraph=''
            totalvotegraph=''
            server = self.bot.get_server('264119826069454849')
            if(upvotes=='0' and downvotes=='0' and totalvotes=='0' and netupvotes=='0'
                and upvoteperc=='0%' and downvoteperc=='0%'):
                pass
            else:
                if(partupcircle=='0'):
                    partbluesq = ''
                else:
                    for i in server.emojis:
                        if str(i).find(':'+partupcircle+'bluesq:')!=-1 :
                            partbluesq = str(i)

                if(partdowncircle=='0'):
                    partredsq = ''
                else:
                    for i in server.emojis:
                        if str(i).find(':'+partdowncircle+'redsq:')!=-1 :
                            partredsq = str(i)

                for i in server.emojis:
                    if str(i).find(':bluesq:')!=-1 :
                        bluesq = str(i)

                for i in server.emojis:
                    if str(i).find(':redsq:')!=-1 :
                        redsq = str(i)

                for i in range(0, 10):
                    netupvotegraph = netupvotegraph + bluesq
                for i in range(0, upvotecircles):
                    upvotegraph = upvotegraph + bluesq
                upvotegraph = upvotegraph + partbluesq

                totalvotegraph = netupvotegraph


                for i in range(0, downvotecircles):
                    downvotegraph = downvotegraph + redsq
                downvotegraph = downvotegraph + partredsq
                totalvotegraph = totalvotegraph +'\n'+ downvotegraph
# finish totsl upvote part
# asdfadfasf
# sdf
# sf
# sd
# f
# s
            #
            # print(round((float(upvoteperc[0:-3]))/10, 0))
            



            # if(upvotecircles>=downvotecircles):
            #     beanz = (int(partupcircle)+upvotecircles)-(int(partdowncircle)+downvotecircles)
            #     print("\n\n\t{}\n\n".format(beanz))
            #     for i in range(0, int(beanz)):
            #         totalvotegraph = totalvotegraph + bluesq
            #     partbeanz = beanz-int(beanz)
            #     partbeanz = partbeanz*10
            #     parttotalsq=''
            #     if(partbeanz=='0'):
            #         parttotalsq = ''
            #     else:
            #         for i in server.emojis:
            #             if str(i).find(':'+str(partbeanz)+'redsq:')!=-1 :
            #                 parttotalsq = str(i)
            #     totalvotegraph = totalvotegraph + parttotalsq
            # else:
            #     for i in range(0, downvotecircles-upvotecircles):
            #         totalvotegraph = totalvotegraph + redsq

            # print(float(tagline)

            author = tagline[tagline.find('href=\"https://www.reddit.com/user/')+len('href=\"https://www.reddit.com/user/') : -1]
            author = author[0:author.find('\">')]
            posttime = tagline[tagline.find('UTC\">')+len('UTC\">') : tagline.find('</time>')]
            postembed.add_field(name="Points", value=netupvotes+'\n'+upvotegraph, inline=False)
            postembed.add_field(name="People who voted", value='Total '+totalvotes+' (100%)\n:arrow_up:'+
                upvotes+' ('+upvoteperc+')\n:arrow_down:'+downvotes+' ('+downvoteperc+')'+ '\n'+totalvotegraph, inline=False)
            postembed.set_footer(text='by '+author+'  posted '+posttime)
            await self.bot.say(embed=postembed)

    
    @commands.command(pass_context=True)
    async def rmulti(self, ctx, sub='', post=1, amtpost=1, sort='hot', announce='no'):
        """Get multiple top(sorted by "hot") reddit posts of r/CR
        If you want to get the #1 post do:
        This is the default setting for !rmulti (one post, starting from the top post):
        !rmulti
        This is saying to start from post 1 and defaults to showing 1 post
        !rmulti 1
        This is saying to start from post 1 and show 1 post
        !rmulti 1 1
        If you want to get the #1 post - #3 post (top 3) do:
        !rmulti 1 3
        If you want to get the top post sorted by "rising" do:

        This works just like "!cr" but has the ability to show more than 1 post.
        Like "!cr" you must have all the arguments in correct order or it won't work
        """
        if(post<1 or post>20):
            post=1
        if(sort == 'hot' or sort.lower() == 'new' or sort.lower() == 'rising' or 
            sort.lower() == 'controversial' or sort.lower() == 'top' or sort.lower() == 'gilded'):
            pass
        else:
            sort='hot'
        for i in range(post, post+(amtpost)):
            await ctx.invoke(self.cr, sub=sub, post=i, sort=sort, announce=announce)


        # if(None):
        #     pass
        # else:
        #     if (subreddit==''):
        #         url=redditUrl
        #     else:
        #         if(subreddit.lower() == "cr"):
        #             url=redditUrl + "r/" + "clashroyale" + "/" + ".json"
        #         else:
        #             url=redditUrl + "r/" + subreddit + "/" + ".json"
        #     print(url)
        #     r = requests.get(url, headers=headers)
        #     # redditstuff = dataIO.load_json(r.content)
        #     # print(redditstuff)
        #     # print(html_doc)
        #     bean = "url=\""
        #     bean2 = "rel>"
        #     print("\n\nlinks: {}\n\n".format(link))
        #     try:
        #         topreddit = str(link[0])
        #         toplink = topreddit[topreddit.find(bean)+len(bean) : topreddit.find("\" data-outbound")]
        #     except(IndexError):
        #         print(soup.prettify())
        #         link = soup.find_all("p", "title")
        #         print(link[0])
        #         topreddit = str(link)
        #         toplink = topreddit[topreddit.find(bean)+len(bean) : topreddit.find("\" data-inbound")]
        #     bean = "url=\""
        #     # print(topreddit.find("\" data-"))
        #     # print(type(topreddit))
        #     # print(topreddit.find(bean))
        #     # print(topreddit)
        #     # print(bean)
        #     # print(toplink)
        #     if (subreddit == ''):
        #         await self.bot.say("Top post on reddit: {}".format(toplink))
        #     else:
        #         await self.bot.say("Top post on the r/{} reddit: {}".format(subreddit, toplink))

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
    bot.add_cog(Reddit2(bot))
