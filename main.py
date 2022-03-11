import os
import math
import asyncio
import discord as d
from discord.ext import commands
from datetime import date as dt
from urllib.request import Request, urlopen
import json
import nest_asyncio
import time
import aiohttp

from db_helper import *
from evy_helper import *

   
nest_asyncio.apply()
     
 
event_log = {}

def crt(data):
    log_file = open("data.json", "w")
    log_file = json.dump(data, log_file, indent = 4)
    return True     

def get_tasks(session,skill_name):
    tasks = []
    for k in range(0,6250):  
        url='https://www.curseofaros.com/highscores'
        tasks.append(asyncio.create_task(session.get(url+skill_name+'.json?p='+str(k))))
    return tasks


async def makelog() :
    event_log = {}
    start = time.time()
    name_list = []
    
    c_xp = ['combat_xp','mining_xp','smithing_xp','woodcutting_xp','crafting_xp','fishing_xp','cooking_xp']
    c_skill =['','-mining','-smithing','-woodcutting','-crafting','-fishing','-cooking']
    
    for skill_x in range(7):
        #connector = aiohttp.TCPConnector(limit=80)
        async with aiohttp.ClientSession() as session :
            to_do = get_tasks(session, c_skill[skill_x])
            responses = await asyncio.gather(*to_do)
            for response in responses:
                data = await response.json()
                for fdata in data:
                    member_temp = { 'ign' : 'name' , 'combat_xp' : 0 , 'mining_xp' : 0 , 'smithing_xp' : 0 , 'woodcutting_xp': 0 , 'crafting_xp' : 0 , 'fishing_xp' : 0 , 'cooking_xp' : 0 , 'total': 0}
                    player_name = fdata["name"]
                    xp = fdata["xp"]
                    tag = player_name.split()[0]                    
                    if tag.upper() == "GOD":
                        if player_name in name_list:
                            event_log[player_name][c_xp[skill_x]]=xp
                            event_log[player_name]["total"] += xp
                        else:
                            name_list.append(player_name)
                            event_log[player_name]=member_temp
                            event_log[player_name]["ign"] = player_name
                            event_log[player_name][c_xp[skill_x]]=xp
                            event_log[player_name]["total"] += xp
    end = time.time()
    total_time = math.ceil(end - start)
    return event_log, total_time







bot = commands.Bot(command_prefix='&')

bot.remove_command("help")
bot.remove_command("date")
bot.remove_command('random')
@bot.event
async def on_ready():
    #global lock_state
    print('Logging in as {0.user}'.format(bot))

    #settings = retrieve('settings')
    #lock_state = settings['lock']









@bot.command()
async def log(ctx):
    await ctx.send("logging members xp ... ")
    if os.path.exists("data.json"):
        os.remove("data.json")
    
    old_record = retrieve("0000")
    create = crt(old_record)
   
    if create :
        await ctx.send("logging finished \nsending log file ...")
        await ctx.channel.send('collected data!', file=d.File("data.json"))
    else:
        await ctx.send("logging failed")
    

@bot.command()
async def create(ctx):
    l = createT()
    if l :
        await ctx.send("table created")
    else:
        await ctx.send("error")

@bot.command()
async def start(ctx):
    msg1 = await ctx.send("Fetching records ...")
    a = asyncio.run(makelog())
    init_record = a[0] #dict object contain records
    init_log = jsing(init_record) #json object contain records

    await msg1.delete()
    msg2 = await ctx.send("saving init records to DB ...")

    await msg2.delete()
    await insert(ctx,'0000',init_log)

@bot.command()
async def end(ctx):

    a = asyncio.run(makelog())
    final_record = a[0] #dict object contain records
    final_log = jsing(final_record) #json object contain records

    msg2 = await ctx.send("saving final records to DB ...")

    msg2.delete()
    await insert(ctx,'9999',final_log)

@bot.command()
async def event(ctx,skill='total'):
    if skill.lower() == 'total' or skill.lower() in ['combat','mining','smithing','woodcutting','crafting','fishing','cooking'] :
        msg1 = await ctx.send("Fetching newest records")
        old_record = retrieve("0000")
        a = asyncio.run(makelog())
        new_record = a[0]
        unranked_data = SortUp(old_record,new_record)

        if skill.lower() == 'total':
            await msg1.delete()
            ranked_data = RankUp(unranked_data[2])[0]
            ranking = RankList(ranked_data)
            oa_xp = RankUp(unranked_data[2])[1]
            await ctx.send("Total Xp LeaderBoard")
            await ctx.send(ranking)
            await ctx.send("Overall Xp gain : " + "{:,}".format(oa_xp))
            
        else:
            await msg1.delete()
            ranked_data = RankUp(unranked_data[0])[0]
            oa_xp = RankUp(unranked_data[0])[1]
            ranking = RankList(ranked_data)
            await ctx.send(f"{skill.capitalize()} LeaderBoard")
            await ctx.send(ranking)
            await ctx.send("Overall Xp gain : " + "{:,}".format(oa_xp))
            
       
    else :
        await ctx.send("Invalid Input ! \nPlease use one from : total - combat - mining - smithing - woodcutting - crafting - fishing - cooking")



bot.run(os.getenv("TOKEN"))
