__author__ = "ME!"
"""uhh yeah so this is a discord bot b/c someone suggested it in 
the lecture channel (@Lord of Arbiters#9845) calling you out

Anyways, got bored and made a REALLY terrible one. Give it a look, or don't,
just made it for fun, thought I might share.

(Prolly buggy as heck, tested it like for like 10 mins and have no clue
what will happen when more than 2 people hammer it
prime example of technology compensating for terrible code :) )
"""

import discord
from discord.ext import commands
from datetime import date
from datetime import datetime
import io

bot = commands.Bot('!')
client = discord.Client() 

#keeping states
attend = []
oldDate = " "

#function lets you know when bot is ready
@bot.event
async def on_ready():
    print("Bot is ready")


#function triggers on message
"""
Every time someone messages in a server, it checks if it 
is in the lecture channel

If it is in the correct channel then it checks the date as well as the time to 
see if it is lecture time (every wednesdays and fridays 1:00pm - 2:30 pm)

if it is within lecture time, it then checks to see if the date has changed, 
if it has, the bot knows that it's a new lecture and will take attendance all
over again (resets). 
This checking is pretty redundent and probably a waste of time as it checks the
date and time for literally every single message

After all those "is it during lecture" checks pass it will check the 
messenger against the attendance list to see if the
messager is on the attendance list.

If messenger IS NOT on the list, add it to the a list and put their name in the
server in to a txt file. (name of txt file is the date)

If they are on the list, I suppose you just wasted some processing power on 
finding the dates and time and stuff, probablly not much, but some. 
(Hey, I never claimed this was good)

NOTES:
the date stuff is unnecessary if the bot is only turned on during lectures
the date stuff will only be usedful to determine the file name
easily abusable by people who use other peoples nicknames since it's modifiable
       -> can be patched with message.author.id
"""
@bot.event
async def on_message(message):
    if str(message.channel) == "lecture":
        #get states
        global oldDate
        global attend
        
        #grab the date and the time (system date and time)
        today = date.today()
        time = datetime.now()
        
        #grab the start times and end times for lecture
        startTime = time.replace(hour=13, minute=0, second=0, microsecond=0)
        endTime = time.replace(hour=14, minute=30, second=0, microsecond=0)
        #checks if it is a day in lecture 
        if (today.weekday() == 2 or 
            today.weekday() == 4) and (time > startTime and
                                       time < endTime) :
            #check if need reset
            if oldDate != today:
                oldDate = today
                attend = []
            #check if the sender is already checked off
            if not message.author.name in attend:
                # A SYNCHRONOUS FUNCTION CALL??? OH NO!!!
                # write person's name on server to txt file
                # needs encoding for special symbols
                with io.open(str(today)+".txt", "a", encoding="utf-8") as f:
                    print("wrote")
                    f.write(message.author.name + "\n")
                    f.close()
                attend.append(message.author.name)

#replace token with token of your bot
bot.run("BOT TOKEN HERE")