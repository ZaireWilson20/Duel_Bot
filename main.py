# bot.py
import os

import discord
import asyncio
import random
import dotenv
from discord.ext import commands
from dotenv import load_dotenv


BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, 'token.env'))


TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = "VR Duel Prototype"
bot = commands.Bot(command_prefix='!')


client = discord.Client()


duel_running = False
winner = ""


@bot.command(name='Duel', help="This is you start a duel")
async def run_duel(ctx, user_challenged: discord.User):
    player2 = bot.get_user(user_challenged.id)
    global duel_running
    global winner
    print(user_challenged)

    def check(reaction, user):
        return user == user_challenged and str(reaction.emoji) in ['✅', '❌']
    
    def shotFirst(reaction,user):
        #winner = user.name
        return user == user_challenged or user == ctx.author and str(reaction.emoji) == '🔫'

    def checkReady(reaction, user):
        return reaction.count == 3 and str(reaction.emoji) == '✅'
    if(player2 == None):
        await ctx.send("You tryna start a duel with someone who doesn't hang round these parts. Try again bub.")
        return
   
    if(not duel_running):
        response = ctx.author.name + " has challenged " + user_challenged.name + " to a duel. " + user_challenged.name.capitalize() + " If you except the challenge, press the check mark reaction, however, if you value your life and would rather not entertain your challenger, press the X reaction."
        
        g = await ctx.send(response)
        await g.add_reaction("✅")
        await g.add_reaction("❌")
        

        try: 
            reaction, user = await bot.wait_for('reaction_add', check=check)
        except:
            print("yes")
        else:
            if(reaction.emoji == '✅'):
                await ctx.send(user_challenged.name + " has accepted the duel.")
                duel_running = True
            elif(reaction.emoji == '❌'):
                await ctx.send(user_challenged.name + " has declined the duel.")
                return
        if(duel_running):
            duel_message = await ctx.send("Now that everyone's on board, lets get this duel runnin. The rules are simple: Once both parties are ready, the duel will progress. After waiting some time I feel that's right, I'll react to this message with a gun emoji. AS SOON AS I SEND THE GUN REACTION, the first party to click the gun reaction shoots first, which in turn will win them the game. That is all. If you are ready, click the green check reaction.")
            await duel_message.add_reaction("✅")
            try: 
                reaction, user = await bot.wait_for('reaction_add', check=checkReady)
            except:
                print("yes")
            else:
                await asyncio.sleep(random.randint(3,8))
                await duel_message.add_reaction("🔫")
            
            try: 
                reaction, user = await bot.wait_for('reaction_add', check=shotFirst)
                winner = user.name
            except:
                print("yes")
            else:
                await ctx.send(winner.capitalize() + " pulled the trigger first. Congrats " + winner.capitalize() + "!")
                duel_running = False
                winner = ""

                
            

    else:
        response = "There is already a duel in progress, yur gunna have to settle yur conflict later"
        await ctx.send(response)

    




bot.run(TOKEN)