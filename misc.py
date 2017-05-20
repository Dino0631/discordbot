```python
import requests
import os
import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from .utils.chat_formatting import escape_mass_mentions, italics, pagify
import json
from random import randint
from random import choice
PATH = os.path.join("data", "misc")
SETTINGS_JSON = os.path.join(PATH, "settings.json")
RPSLS = { 0 : "rock", 1 : "paper", 2 : "scissors", 3 : "lizard", 4 : "spock"}
RPSLSemoji = {"rock" : ":moyai:", "paper" : ":page_facing_up:", "scissors" : ":scissors:", "lizard" : ":lizard:", "spock" : ":vulcan:"}

class Misc:

    def __init__(self, bot):
        self.settings = dataIO.load_json(SETTINGS_JSON)
        self.bot = bot

    @commands.command(pass_context=True)
    async def rpsls(self, ctx, player_choice):
        """rock paper scissors lizard spock"""
        if player_choice == '<@!164047737648709632>' or player_choice.lower() == 'spike' or player_choice.lower() == 'inferno lizard': 
        #if spike is mentioned the choice is lizard
            player_choice = 'lizard'
        if player_choice not in RPSLS.values():
            await self.bot.say("{} is not a valid choice. Please pick {}, {}, {}, {}, or {}".format(player_choice, RPSLS[0], RPSLS[1], RPSLS[2], RPSLS[3], RPSLS[4]))
            return
        player_choice = player_choice.lower()
        bot_choice = randint(0, 4)
        cond = {("rock", "paper") : False,
            ("rock",  "scissors") : True,
            ("rock",  "lizard") : True,
            ("rock",  "spock") : False,
            ("paper", "rock") : True,
            ("paper", "scissors") : False,
            ("paper", "lizard") : False,
            ("paper", "spock") : True,
            ("scissors", "rock") : False,
            ("scissors", "paper") : True,
            ("scissors", "lizard") : True,
            ("scissors", "spock") : False,
            ("lizard", "rock") : False,
            ("lizard", "paper") : True,
            ("lizard", "scissors") : False,
            ("lizard", "spock") : True, 
            ("spock", "rock") : True,
            ("spock", "paper") : False,
            ("spock", "scissors") : True,
            ("spock", "lizard") : False,
            ("rock", "rock") : None,
            ("paper", "paper") : None,
            ("scissors", "scissors") : None,
            ("lizard", "lizard") : None,
            ("spock", "spock") : None
            }
        if cond[(player_choice, RPSLS[bot_choice])] == True:
            await self.bot.say("You won! {}{} vs {}{}.".format(player_choice, RPSLSemoji[player_choice], RPSLS[bot_choice], RPSLSemoji[RPSLS[bot_choice]]))
        elif cond[(player_choice, RPSLS[bot_choice])] == False:
            await self.bot.say("You lost! {}{} vs {}{}.".format(player_choice, RPSLSemoji[player_choice], RPSLS[bot_choice], RPSLSemoji[RPSLS[bot_choice]]))
        else:
            await self.bot.say("You tied! {}{} vs {}{}.".format(player_choice, RPSLSemoji[player_choice], RPSLS[bot_choice], RPSLSemoji[RPSLS[bot_choice]]))

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
    bot.add_cog(Misc(bot))
```
