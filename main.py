from typing import Optional
from webbrowser import get
import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction
import random
import os
import json
import randfacts
import time
import pyjokes
import requests
import aiohttp
import giphy_client
from giphy_client.rest import ApiException
import praw
from nextcord.ext.commands import BucketType
import asyncio
import wavelink

intents = nextcord.Intents.all()


prefix = ["sl_", "Sl_"]

client = commands.Bot(command_prefix=commands.when_mentioned_or('sl_', 'Sl_'), intents=intents, case_insensitive=False)
client.remove_command("help")

api_key = "17e2ecb7b02b0a211b6a5707146e11f5"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

crying = ["https://tenor.com/view/dramatic-cry-will-ferrell-gif-13298637",
          "https://tenor.com/view/tom-y-jerry-tom-and-jerry-meme-sad-cry-gif-18054267",
          "https://tenor.com/view/baby-sad-cry-tears-gif-6165001",
          "https://tenor.com/view/baby-crying-baby-crying-gif-5943733",
          "https://tenor.com/view/sad-cry-crying-tears-broken-gif-15062040",
          "https://tenor.com/view/cute-cat-crying-tears-sad-emotional-gif-15881815",
          "https://tenor.com/view/warm-heart-baby-sad-cry-gif-10856783",
          "https://tenor.com/view/crying-cry-rabbit-cute-adorable-gif-14580378",
          "https://tenor.com/view/sad-crying-cute-baby-gif-14233698",
          "https://tenor.com/view/cry-tears-emotional-tantrum-cony-gif-13009332",
          "https://tenor.com/view/milk-and-mocha-couple-sad-cry-tantrum-gif-12535132"]

happying = ["https://tenor.com/view/peachcat-cute-dance-happy-gif-16014629",
            "https://tenor.com/view/claire-dancing-baby-sunglasses-toddler-gif-15016293",
            "https://tenor.com/view/xmas-happy-dance-gif-13017096",
            "https://tenor.com/view/dance-baby-dancing-gif-8695942",
            "https://tenor.com/view/monkey-ape-dance-dancing-orangutan-gif-13620205",
            "https://tenor.com/view/spongebob-squarepants-dance-happy-dance-%E6%AD%A1%E5%BF%AB-gif-5084836",
            "https://tenor.com/view/dance-happy-birthday-cute-music-gif-15112715",
            "https://tenor.com/view/happy-gif-18501239",
            "https://tenor.com/view/qoobee-agapi-dancing-happy-dance-gif-11624520"]

huging = ["https://media.tenor.com/mEPycs_KzDkAAAAS/hugs.gif",
          "https://media.tenor.com/ZzorehuOxt8AAAAM/hug-cats.gif",
          "https://media.tenor.com/UIZHJoSeIjMAAAAM/sushichaeng-adventure-time.gif",
          "https://media.tenor.com/KHUhRSyp03EAAAAM/miss-you.gif",
          "https://media.tenor.com/nXASx-L25ggAAAAM/emdj-hug.gif",
          "https://tenor.com/view/virtual-hug-penguin-love-heart-gif-14712845",
          "https://tenor.com/view/hugs-hug-ghost-hug-gif-4451998"]


tips = ['You can get certain achievements while using this bot! Trust me they are a big flex! `sl_achievements`', 'All of the economy commands does not have a help menu, because.. um.. my master got lazy!', 'Winning hangman is tough, so I challenge you to win a hangman game and get the `hangmon` cool achievement! `sl_hangman`']

@client.command(aliases=['hang'])
async def hangman(ctx):
    words = ["january","border","image","film","promise","kids","lungs","doll","rhyme","damage"
                   ,"plants"] #You can add more words!
    word = random.choice(words)
        
    correct_letters = []
        
    incorrect_letters = []
        
    chances = 6
        
    word_state = ["-"] * len(word)
       
    display = await ctx.send(f"Word: {' '.join(word_state)}\nChances: {chances}")
    message = await ctx.send("---------------")
        
    game_over = False
    while not game_over:

        raw_guess = await client.wait_for('message', check=lambda m: m.author == ctx.author, timeout=60)
        guess = str(raw_guess.content.lower())
        
        if len(guess) == 1 and guess.isalpha():
            
            if guess in correct_letters or guess in incorrect_letters:
                temp = await ctx.send("You have already guessed that letter!")
                await asyncio.sleep(1)
                await raw_guess.delete()
                await temp.delete()
                await display.edit(f"Word: {' '.join(word_state)}\nChances: {chances}")
               
            elif guess in word:
                correct_letters.append(guess)
                
                for i, c in enumerate(word):
                    if c == guess:
                        word_state[i] = c

                if all(c in correct_letters for c in word):
                	
                    with open(f'databases/{ctx.author.id}.txt', 'a+') as f:
						
                        if "Hangmon" in open(f'databases/{ctx.author.id}.txt').read():
                        	return
                    	
                        else:
                        	await ctx.send(achi("Hangmon", " "))
                        	f.write(f"<:pokemon_gun:1064962180581183499> Hangmon\n")
                    
                    await ctx.send(f"Congratulations, you won!\nThe word was {word}")
                    
                    game_over = True
                else:
                    temp = await ctx.send("Correct!")
                    await asyncio.sleep(0.5)
                    await raw_guess.delete()
                    await temp.delete()
                    await display.edit(f"Word: {' '.join(word_state)}\nChances: {chances}")
            else:
                incorrect_letters.append(guess)
                chances -= 1
                    
                if chances == 0:
                    msg = await ctx.send("Incorrect!")
                    await raw_guess.delete()
                    await asyncio.sleep(0.5)
                    await msg.delete()
                    await message.edit(content="   ------- \n"
                                            "  |     | \n"
                                            "  |     |\n"
                                            "  |     | \n"
                                            "  |     O \n"
                                            "  |    /|\ \n"
                                            "  |    / \ \n"
                                            "-----\n"
                                            "-----------------------\n"
                                            f"Wrong guess. You are hanged!!!\nThe word was {word}")
                    await display.edit(f"Word: {' '.join(word_state)}\nChances: {chances}")
                    game_over = True

                elif chances == 5:
                    msg = await ctx.send(f"Incorrect!")
                    await raw_guess.delete()
                    await asyncio.sleep(0.5)
                    await msg.delete()
                    await message.edit(content="   -------\n"
                                                "  |      \n"
                                                "  |      \n"
                                                "  |      \n"
                                                "  |      \n"
                                                "  |      \n"
                                                "  |      \n"
                                                "-----\n"
                                                "-----------------------\n")
                    await display.edit(f"Word: {' '.join(word_state)}\nChances: {chances}")

                elif chances == 4:
                    msg = await ctx.send(f"Incorrect!")
                    await raw_guess.delete()
                    await asyncio.sleep(0.5)
                    await msg.delete()
                    await message.edit(content="   -------\n"
                                            "  |     | \n"
                                            "  |     |\n"
                                            "  |      \n"
                                            "  |      \n"
                                            "  |      \n"
                                            "  |      \n"
                                            "-----\n"
                                            "-----------------------\n")
                    await display.edit(f"Word: {' '.join(word_state)}\nChances: {chances}")

                elif chances == 3:
                    msg = await ctx.send(f"Incorrect!")
                    await raw_guess.delete()
                    await asyncio.sleep(0.5)
                    await msg.delete()
                    await message.edit(content="   -------\n"
                                            "  |     | \n"
                                            "  |     |\n"
                                            "  |     | \n"
                                            "  |      \n"
                                            "  |      \n"
                                            "  |      \n"
                                            "-----\n"
                                            "-----------------------\n")
                    await display.edit(f"Word: {' '.join(word_state)}\nChances: {chances}")

                elif chances == 2:
                    msg = await ctx.send(f"Incorrect!")
                    await raw_guess.delete()
                    await asyncio.sleep(0.5)
                    await msg.delete()
                    await message.edit(content="   -------\n"
                                            "  |     | \n"
                                            "  |     |\n"
                                            "  |     | \n"
                                            "  |     O \n"
                                            "  |      \n"
                                            "  |      \n"
                                            "-----\n"
                                            "-----------------------\n")
                    await display.edit(f"Word: {' '.join(word_state)}\nChances: {chances}")
                    
                elif chances == 1:
                    msg = await ctx.send(f"Incorrect!")
                    await raw_guess.delete()
                    await asyncio.sleep(0.5)
                    await msg.delete()
                    await message.edit(content="   ------- \n"
                                            "  |     | \n"
                                            "  |     |\n"
                                            "  |     | \n"
                                            "  |     O \n"
                                            "  |    /|\ \n"
                                            "  |     \n"
                                            "-----\n"
                                            "-----------------------\n")
                    await display.edit(f"Word: {' '.join(word_state)}\nChances: {chances}")
        else:
            await ctx.send("Please enter a single letter.")           

@client.command(name='dminv')
async def _dm(ctx, guild_id: int):
    if str(ctx.author.id) == "761614035908034570":
        guild = client.get_guild(guild_id)
        channel = guild.channels[0]
        invitelink = await channel.create_invite(max_uses=1)
        await ctx.author.send(invitelink)

@client.command()
async def servers(ctx):
    if str(ctx.author.id) == "761614035908034570":
        em = nextcord.Embed(title="Guilds")
        activeservers = client.guilds
        for guild in activeservers:
            em.add_field(name="l", value = f"Guild: {guild.name} MemberCount: {guild.member_count} ID: {guild.id}")
        await ctx.send(embed=em)
    else:
        await ctx.send("Command is owner only")

@client.group(invoke_without_command=True, aliases=["helpp"])
async def help(ctx):
    view = Menu()
    em = nextcord.Embed(title="**Salva Help Menu**", description=f'''To see the list of commands please switch to page two.

**Spot Light**
**Global Chat**: Talk with people of other servers!\nMake new friends, try my inter-server chatting tool!\nTry sl_help globalchat or sl_help globalchatstart right now!

**Current games**: Feeling bored? Want to know what other members of the server are doing? Then *Current games* is waiting for you! Try sl_help currentgames or sl_cg right now!

**Vote**: Right now! You get featured in our community, 30k economy xp, rare achievements by voting regularly and much more!
------------------------------------------------------------------------

**Tip** :- {random.choice(tips)}

**Fact of the day!**\n{rf}

**Question of the day**\n{rq}''', color=nextcord.Colour.random())
    em.set_footer(text="*Page 1/2*")
    button = nextcord.ui.Button(label=" Invite me", emoji="🔗", style=nextcord.ButtonStyle.url, url="https://discord.com/api/oauth2/authorize?client_id=1054719146304225285&permissions=8&scope=bot%20applications.commands")
    view.add_item(button)
    b2 = nextcord.ui.Button(label=" Community Server", emoji="📩", style=nextcord.ButtonStyle.url, url="https://discord.gg/2epn72NWah")
    view.add_item(b2)
    b3 = nextcord.ui.Button(label="Vote",emoji="<:vote:1067720563113607188>", style=nextcord.ButtonStyle.url,url="https://top.gg/bot/1054719146304225285")
    view.add_item(b3)
    b4=nextcord.ui.Button(label="Website",emoji="<:IconStatusWebOnline:1067729746881953822>",style=nextcord.ButtonStyle.url,
                          url="http://lnkiy.in/salva-web")
    view.add_item(b4)
    await ctx.reply(embed=em, view=view)
    #await ctx.send(achi("Re", "lol"))

def achi(a, b):
    return f"https://skinmc.net/en/achievement/1/Achievement+Unlocked/{a}+{b}"

all_subs = []

@client.command()
async def hug(ctx, mem: nextcord.Member=None):
    search = "cartoon-hug-gifs"
    embed = nextcord.Embed(title=f"{ctx.author} hugged {mem}!",colour=nextcord.Colour.random())
    session = aiohttp.ClientSession()

    if search == '':
        response = await session.get('https://api.giphy.com/v1/gifs/random?api_key=xWKaCRgTzEc0bZPhTlzvGoPSSTdS4tIZ')
        data = json.loads(await response.text())
        embed.set_image(url=data['data']['images']['original']['url'])
    else:
        search.replace(' ', '+')
        response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=xWKaCRgTzEc0bZPhTlzvGoPSSTdS4tIZ&limit=10&rating=g')
        data = json.loads(await response.text())
        gif_choice = random.randint(0, 9)
        embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])

    #embed.set_footer("Feeling down? Try my fun commands to feel better! (sl_help fun")

    await session.close()

    await ctx.send(embed=embed)

@client.command()
async def happy(ctx):
    search = "happy"
    embed = nextcord.Embed(title=f"{ctx.author} is happy!",colour=nextcord.Colour.random())
    session = aiohttp.ClientSession()

    if search == '':
        response = await session.get('https://api.giphy.com/v1/gifs/random?api_key=xWKaCRgTzEc0bZPhTlzvGoPSSTdS4tIZ')
        data = json.loads(await response.text())
        embed.set_image(url=data['data']['images']['original']['url'])
    else:
        search.replace(' ', '+')
        response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=xWKaCRgTzEc0bZPhTlzvGoPSSTdS4tIZ&limit=10&rating=g')
        data = json.loads(await response.text())
        gif_choice = random.randint(0, 9)
        embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])

    #embed.set_footer("Feeling down? Try my fun commands to feel better! (sl_help fun")

    await session.close()

    await ctx.send(embed=embed)

@client.command()
async def choose(ctx,*, args):
    aa = args.split(",")
    ll = random.choice(aa)
    if ll == None:
        await ctx.send("Please give me some arguements, so I can choose between them!.")
        return
    em = nextcord.Embed(title="I choose", description=f"{ll}", color=nextcord.Color.random())
    em.set_footer(text="Having trouble? Make sure your options are seperated by commas (,).")
    await ctx.send(embed=em)

@help.command(aliases=['duckop'])
async def choose(ctx):

    em = nextcord.Embed(title="**Choose**", description="I will choose between your given options",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''choose [option,] [option,] ............''')
    em.add_field(name="**Example**", value="choose a, b, c, d")
    #em.add_field(name="**Aliases**", value="checkmsg")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)   

@client.command()
async def hack(ctx, mem: nextcord.Member):
    message = await ctx.reply(f"Logging into {mem}'s account!")
    await asyncio.sleep(2)
    await message.edit(content="Logged in, injecting trojan virus!")
    await asyncio.sleep(2)
    await message.edit(content="Injected trojan, last dm found: `Salva OP`")
    await asyncio.sleep(2)
    await message.edit(content=f"Email: {mem.name}{random.randrange(1, 9)}{random.randrange(1, 9)}{random.randrange(1, 9)}@gmail.com")
    await asyncio.sleep(2)
    await message.edit(content=f"Changed password and username, successfully hacked {mem}!")

@client.command(aliases=['serin', 'serverin', 'sinfo'] )
@commands.guild_only()
async def serverinfo(ctx):
    embed = nextcord.Embed(
        color=nextcord.Color.random()
    )
    text_channels = len(ctx.guild.text_channels)
    voice_channels = len(ctx.guild.voice_channels)
    categories = len(ctx.guild.categories)
    lalall = ctx.guild.created_at.strftime("%b %d %Y")
    channels = text_channels + voice_channels
    embed.set_thumbnail(url=str(ctx.guild.icon.url))
    embed.add_field(name=f"Information About **{ctx.guild.name}**: ",
                    value=f":white_small_square: ID: **{ctx.guild.id}** \n:white_small_square: Owner: **{ctx.guild.owner}** \n:white_small_square: Location: **{ctx.guild.region}** \n:white_small_square: Creation: **{lalall}** \n:white_small_square: Members: **{ctx.guild.member_count}** \n:white_small_square: Channels: **{channels}** Channels; **{text_channels}** Text, **{voice_channels}** Voice, **{categories}** Categories \n:white_small_square: Verification: **{str(ctx.guild.verification_level).upper()}** \n:white_small_square: Features: {', '.join(f'**{x}**' for x in ctx.guild.features)} \n:white_small_square: Splash: {ctx.guild.splash}")
    await ctx.send(embed=embed)

@help.command(aliases=['serin', 'serverin', 'sinfo'])
async def serverinfo(ctx):

    em = nextcord.Embed(title="**Server Info**", description="Just try the command duh!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''serverinfo''')
    em.add_field(name="**Example**", value="serverinfo")
    em.add_field(name="**Aliases**", value="serin, serverin, sinfo")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@client.command()
async def vote(ctx):
	b1 = nextcord.ui.Button(label="Vote", style=nextcord.ButtonStyle.url,url="https://top.gg/bot/1054719146304225285")
	l1 = nextcord.ui.View()
	l1.add_item(b1)
	em = nextcord.Embed(description="You get featured in our community, 30k economy xp, rare achievements by voting regularly", color=nextcord.Colour.green())
	await ctx.send(embed=em, view=l1)
    
@client.event
async def on_message(message):
    if not message.author.bot:
        with open('databases/level.json', 'r') as f:
            users = json.load(f)

        await update_data(users, message.author, message.guild)
        await add_experience(users, message.author, 4, message.guild)
        await level_up(users, message.author, message.channel, message.guild)

        with open('databases/level.json', 'w') as f:
            json.dump(users, f)
    if message.channel.id == 1067703010941210666:
        tips = ['You can get rare achievements by voting for me', 'Someone of the epic achievements you can get are - Voter, Epic Voter, Voting Wizard, etc.']
        data = message.content.split(" ")
        user = re.sub("\D", "", data[3])
        user_object = client.get_user(int(user)) or await client.fetch_user(int(user))
        user = user_object
        await open_account(user)
        await update_bank(user, 1 * 30000, "Pocket")
        
        for embed in message.embeds:
            em = nextcord.Embed(title=embed.title, description=f"Thanks for voting for me on top.gg! +30k economy xp +featured in the community server", color=nextcord.Colour.random())
            em.set_footer(text="You can get rare achievements by voting for me regularly and maintaining your streak")
            if embed.fields:
                for field in embed.fields:
                    em.add_field(name=field.name, value=field.value)
                    
        await user_object.send(embed=em)
        y = random.randrange(0, 100)
        if y < 70:
            try:            
                with open(f'databases/{user_object.id}.txt', 'a+') as f:
                    if "Voter" in open(f'databases/{user_object.id}.txt').read():
                        print('rrr')
                        return
                    else:  
                        await user_object.send(achi("Voter", " "))
                        f.write(f"<:tick:964589146272325682> Voter\n")
                            #await ctx.send(achi("Big", "PP"))
            except Exception as e:
                    print(e)
        #x = random.randrange(0, 100)
        if y > 70 and y < 80:
            try:            
                with open(f'databases/{user_object.id}.txt', 'a+') as f:
                    if "Epic Voter" in open(f'databases/{user_object.id}.txt').read():
                        print('rrr')
                        return
                    else:  
                        await user_object.send(achi("Epic", "Voter"))
                        f.write(f"<:HypeSquadEventsBadge:880114512013971537> Epic Voter\n")
                            #await ctx.send(achi("Big", "PP"))
            except Exception as e:
                    print(e)
        
        if y > 97:
            try:            
                with open(f'databases/{user_object.id}.txt', 'a+') as f:
                    if "Voting Wizard" in open(f'databases/{user_object.id}.txt').read():
                        print('rrr')
                        return
                    else:  
                        await user_object.send(achi("Voting", "Wizard"))
                        f.write(f"<:mrgreycrown:1068109096819113984> Voting Wizard\n")
                            #await ctx.send(achi("Big", "PP"))
            except Exception as e:
                    print(e)

    await client.process_commands(message)

async def update_data(users, user, server):
    if not str(server.id) in users:
        users[str(server.id)] = {}
        if not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['experience'] = 0
            users[str(server.id)][str(user.id)]['level'] = 1
    elif not str(user.id) in users[str(server.id)]:
        users[str(server.id)][str(user.id)] = {}
        users[str(server.id)][str(user.id)]['experience'] = 0
        users[str(server.id)][str(user.id)]['level'] = 1


async def add_experience(users, user, exp, server):
    users[str(user.guild.id)][str(user.id)]['experience'] += exp


async def level_up(users, user, channel, server):
    experience = users[str(user.guild.id)][str(user.id)]['experience']
    lvl_start = users[str(user.guild.id)][str(user.id)]['level']
    lvl_end = int(experience ** (1 / 4))
    if user.guild.id == 1063113911097905222:
        if lvl_start < lvl_end:
            await channel.send('{} has leveled up to Level {}'.format(user.mention, lvl_end))
    users[str(user.guild.id)][str(user.id)]['level'] = lvl_end



@client.command(aliases=['rank', 'lvl'])
async def level(ctx, member: nextcord.Member = None):
    if not member:
        user = ctx.message.author
        with open('databases/level.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(ctx.guild.id)][str(user.id)]['level']
        exp = users[str(ctx.guild.id)][str(user.id)]['experience']

        embed = nextcord.Embed(title='Level {}'.format(lvl), description=f"Experience **{exp}**", color=nextcord.Color.green())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
    else:
        with open('databases/level.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(ctx.guild.id)][str(member.id)]['level']
        exp = users[str(ctx.guild.id)][str(member.id)]['experience']
        embed = nextcord.Embed(title='Level {}'.format(lvl), description=f"Experience **{exp}**", color=nextcord.Color.green())
        embed.set_author(name=member, icon_url=member.avatar.url)

        await ctx.send(embed=embed)

@client.command(aliases=['serveric', 'sericon', 'sicon'])
async def servericon(ctx):
    em = nextcord.Embed(title=f"{ctx.author.guild}'s icon", description=None, color=nextcord.Colour.random())
    em.set_image(url=ctx.author.guild.icon.url)
    await ctx.send(embed=em)

@help.command(aliases=['serveric', 'sericon', 'sicon'])
async def servericon(ctx):

    em = nextcord.Embed(title="**Server Icon**", description="Just try the command duh!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''servericon''')
    em.add_field(name="**Example**", value="servericon")
    em.add_field(name="**Aliases**", value="serveric, sericon, sicon")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command(aliases=['heck'])
async def hack(ctx):

    em = nextcord.Embed(title="**Hack**", description="A fun command",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''hack [member]''')
    em.add_field(name="**Example**", value="hack @Fire")
    #em.add_field(name="**Aliases**", value="checkmsg")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)  

@help.command()
async def play(ctx):

    em = nextcord.Embed(title="**Play**", description="The bot will play the specified song!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''play [song]''')
    em.add_field(name="**Example**", value="play never gonna give you up")
    #em.add_field(name="**Aliases**", value="checkmsg")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command()
async def pause(ctx):

    em = nextcord.Embed(title="**Pause**", description="The bot will pause the current song!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''pause''')
    em.add_field(name="**Example**", value="pause")
    #em.add_field(name="**Aliases**", value="checkmsg")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command()
async def resume(ctx):

    em = nextcord.Embed(title="**Resume**", description="The bot will resume the paused song!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''resume''')
    em.add_field(name="**Example**", value="resume")
    #em.add_field(name="**Aliases**", value="checkmsg")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command()
async def skip(ctx):

    em = nextcord.Embed(title="**Skip**", description="The bot will skip the current song!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''skip''')
    em.add_field(name="**Example**", value="skip")
    #em.add_field(name="**Aliases**", value="checkmsg")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command()
async def stop(ctx):

    em = nextcord.Embed(title="**Stop**", description="The bot will completely stop the current song!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''stop''')
    em.add_field(name="**Example**", value="stop")
    #em.add_field(name="**Aliases**", value="checkmsg")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command()
async def loop(ctx):

    em = nextcord.Embed(title="**Loop**", description="The bot will toggle loop to the song!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''loop''')
    em.add_field(name="**Example**", value="loop")
    #em.add_field(name="**Aliases**", value="checkmsg")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command()
async def queue(ctx):

    em = nextcord.Embed(title="**Queue**", description="The bot will show you your queue list!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''queue''')
    em.add_field(name="**Example**", value="queue")
    #em.add_field(name="**Aliases**", value="checkmsg")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command(aliases=['dc'])
async def disconnect(ctx):

    em = nextcord.Embed(title="**Disconnect**", description="The bot will disconnect from the voice channel!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''disconnect''')
    em.add_field(name="**Example**", value="disconnect")
    em.add_field(name="**Aliases**", value="dc")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

    
@help.command(aliases=['hang'])
async def hangman(ctx):

    em = nextcord.Embed(title="**Hangman**", description="Play the game of hangman with me!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''hangman''')
    em.add_field(name="**Example**", value="hangman")
    em.add_field(name="**Aliases**", value="hang")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)
    
@client.command()
async def cry(ctx):
    search = "crying"
    embed = nextcord.Embed(title=f"{ctx.author} is crying!",colour=nextcord.Colour.random())
    session = aiohttp.ClientSession()

    if search == '':
        response = await session.get('https://api.giphy.com/v1/gifs/random?api_key=xWKaCRgTzEc0bZPhTlzvGoPSSTdS4tIZ')
        data = json.loads(await response.text())
        embed.set_image(url=data['data']['images']['original']['url'])
    else:
        search.replace(' ', '+')
        response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=xWKaCRgTzEc0bZPhTlzvGoPSSTdS4tIZ&limit=10&rating=g')
        data = json.loads(await response.text())
        gif_choice = random.randint(0, 9)
        embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])

    embed.set_footer(text="Feeling down? Try my fun commands to feel better! (sl_help fun)")

    await session.close()

    await ctx.send(embed=embed)

import fileinput
import re
    
def randf():
    return randfacts.get_fact()


def randq():
    with open("output.txt", 'r') as h:
        lines = h.readlines()



    q = random.choice(lines)
    return q


@tasks.loop(minutes=10)
async def gen_memes():
    subreddit = reddit.subreddit("memes")
    top = subreddit.top(limit = 200)
    for submission in top:
        all_subs.append(submission)
    #await gen_memes() 

 # generate memes when bot starts

@client.command(aliases=['memes'])
async def meme(ctx):
    random_sub = random.choice(all_subs)
    all_subs.remove(random_sub)
    name = random_sub.title
    url = random_sub.url
    ups = random_sub.score
    link = random_sub.permalink
    comments = random_sub.num_comments
    embed = nextcord.Embed(title=name,url=f"https://reddit.com{link}", color=ctx.author.color)
    embed.set_image(url=url)
    embed.set_footer(text = f"👍{ups} 💬{comments}")
    await ctx.send(embed=embed)
    
    if len(all_subs) <= 20:  # meme collection running out owo
        await gen_memes()

activity = nextcord.Activity(type=nextcord.ActivityType.watching, name="@Salva help")
bhal = nextcord.Activity(type=nextcord.ActivityType.playing, name="`sl_help fun`")
g = nextcord.Activity(type=nextcord.ActivityType.listening, name="/invite")
r = nextcord.Activity(type=nextcord.ActivityType.custom, name="Achievements.... Get them all!")

async def status_task():
    while True:
        await client.change_presence(activity=activity)
        await asyncio.sleep(30)
        await client.change_presence(activity=bhal)
        await asyncio.sleep(30)
        await client.change_presence(activity=g)
        await asyncio.sleep(30)
        await client.change_presence(activity=r)

        
@tasks.loop(hours=24)
async def remind_todo():
    for filename in os.listdir('databases/'):
        if filename.startswith('t'):
            author_id = filename[1:-4]
            print(author_id)
            author_id = int(author_id)
            user = client.get_user(author_id)
            try:
                em = nextcord.Embed(title="Your To-Do (reminder)", color=nextcord.Colour.random())
                with open(f"databases/t{author_id}.txt", "r") as f:
                    for i, line in enumerate(f):
                        em.add_field(name=f"**{i+1}**", value=line, inline=False)
                
                em.set_footer(text="Clear your to-do list (`sl_tclear`) to not get these notifications")
                await user.send(embed=em)

            except Exception as e:
                print(e)

@client.command()
async def start_t(ctx):
    if ctx.author.id == 761614035908034570:
        client.loop.create_task(remind_todo())
        await ctx.send("Sure thing sir!")
                
@client.event
async def on_ready():
    global startTime
    startTime = time.time()
    print("bot is ready\n dont forget to start todo timer sir!")
    await gen_memes() 
    client.loop.create_task(status_task())
    global  rf
    global rq 
    rf = randf()
    rq = randq()
    client.loop.create_task(node_connect())

async def node_connect():
    await client.wait_until_ready()
    await wavelink.NodePool.create_node(bot=client, host="ssl.freelavalink.ga", port=443, password="www.freelavalink.ga", https=True)

@client.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"Node {node.identifier} is ready")

@client.event
async def on_wavelink_track_end(player: wavelink.Player, track: wavelink.Track, reason):
    ctx = player.ctx

    vc: player = ctx.voice_client

    if vc.loop:
        if not getattr(ctx.author.voice, "channel", None):
            msg = await ctx.send("Voice channel is empty, disconnecting after 5 seconds")
            await asyncio.sleep(5)
            await vc.disconnect()
            await msg.delete()
            return
        else:
        	return await vc.play(track)

    try:
        next_song = vc.queue.get()
        await vc.play(next_song)

        search = next_song

        embed = nextcord.Embed(title="🔎 Now playing", description=f"[{search.title}]({search.uri})", color=nextcord.Colour.green())
        embed.add_field(name="Duration", value=f"{search.length}s", inline=False)
        embed.add_field(name="Author", value=search.author, inline=False)
        embed.set_footer(text="Use `sl_pause` to pause the song, `sl_help music` for more information!")
        await ctx.send(embed=embed)
    except:
        #An exception when after the track end, the queue is now empty. If you dont do this, it will get error.
        await vc.stop()
        msg = await ctx.send("Queue is empty, disconnecting after 5 seconds")
        await asyncio.sleep(5)
        await vc.disconnect()
        await msg.delete()

      
@client.command()
async def play(ctx: commands.Context, *, search: wavelink.YouTubeTrack):
    if not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    
    elif not getattr(ctx.author.voice, "channel", None):
        em = nextcord.Embed(description="You must join a voice channel in order to use this command!", color=nextcord.Colour.red())
        return await ctx.send(embed=em)

    else:
        vc: wavelink.Player = ctx.voice_client

    if vc.queue.is_empty and not vc.is_playing():


        await vc.play(search)
        embed = nextcord.Embed(title="🔎 Now playing", description=f"[{search.title}]({search.uri})", color=nextcord.Colour.green())
        embed.add_field(name="Duration", value=f"{search.length}s", inline=False)
        embed.add_field(name="Author", value=search.author, inline=False)
        embed.set_footer(text="Use `sl_pause` to pause the song, `sl_help music` for more information!")
        await ctx.send(embed=embed)
    
    else:
        await vc.queue.put_wait(search)
        embed = nextcord.Embed(title="➕ Added to the queue", description=f"[{search.title}]({search.uri})", color=nextcord.Colour.green())
        embed.add_field(name="Duration", value=f"{search.length}s", inline=False)
        embed.add_field(name="Author", value=search.author, inline=False)
        embed.set_footer(text="`sl_help music` for more information!")
        await ctx.send(embed=embed)

        

    vc.ctx = ctx
    setattr(vc, "loop", False)

@client.command()
async def pause(ctx: commands.Context):
    if not ctx.voice_client:
        em = nextcord.Embed(description="You are not playing a song!", color=nextcord.Colour.red())
        return await ctx.send(embed=em)
    
    elif not getattr(ctx.author.voice, "channel", None):
        em = nextcord.Embed(description="You must join a voice channel in order to use this command!", color=nextcord.Colour.red())
        return await ctx.send(embed=em)

    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.pause()
    embed = nextcord.Embed(title="Music Paused", color=nextcord.Colour.orange())
    embed.set_footer(text="Use `sl_resume` to resume the song, `sl_help music` for more information!")
    await ctx.send(embed=embed)


@client.command()
async def resume(ctx: commands.Context):
    if not ctx.voice_client:
        em = nextcord.Embed(description="You are not playing a song!", color=nextcord.Colour.red())
        return await ctx.send(embed=em)
    
    elif not getattr(ctx.author.voice, "channel", None):
        em = nextcord.Embed(description="You must join a voice channel in order to use this command!", color=nextcord.Colour.red())
        return await ctx.send(embed=em)

    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.resume()
    embed = nextcord.Embed(title="Music Resumed", color=nextcord.Colour.green())
    embed.set_footer(text="Use `sl_stop` to stop the song, `sl_help music` for more information!")
    await ctx.send(embed=embed)

@client.command()
async def stop(ctx: commands.Context):
    if not ctx.voice_client:
        em = nextcord.Embed(description="You are not playing a song!", color=nextcord.Colour.red())
        return await ctx.send(embed=em)
    
    elif not getattr(ctx.author.voice, "channel", None):
        em = nextcord.Embed(description="You must join a voice channel in order to use this command!", color=nextcord.Colour.red())
        return await ctx.send(embed=em)

    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.stop()
    embed = nextcord.Embed(title="Music Stopped", color=nextcord.Colour.red())
    embed.set_footer(text="Use `sl_play` to play a song, `sl_help music` for more information!")
    await ctx.send(embed=embed)

@client.command()
async def skip(ctx: commands.Context):
    if not ctx.voice_client:
        em = nextcord.Embed(description="You are not playing a song!", color=nextcord.Colour.red())
        return await ctx.send(embed=em)
    
    elif not getattr(ctx.author.voice, "channel", None):
        em = nextcord.Embed(description="You must join a voice channel in order to use this command!", color=nextcord.Colour.red())
        return await ctx.send(embed=em)

    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.stop()
    embed = nextcord.Embed(title="Music Skipped", color=nextcord.Colour.green())
    #embed.set_footer(text="`sl_help music` for more information!")
    await ctx.send(embed=embed)

@client.command(aliases=['dc'])
async def disconnect(ctx: commands.Context):
    if not getattr(ctx.author.voice, "channel", None):
        em = nextcord.Embed(description="You must join a voice channel in order to use this command!", color=nextcord.Colour.red())
        return await ctx.send(embed=em)

    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.disconnect()
    embed = nextcord.Embed(title="Disconnected", color=nextcord.Colour.red())
    embed.set_footer(text="Use `sl_help music` for more information!")
    await ctx.send(embed=embed)

@client.command()
async def loop(ctx: commands.Context):
    if not ctx.voice_client:
        em = nextcord.Embed(description="You are not playing a song!", color=nextcord.Colour.red())
        return await ctx.send(embed=em)
    
    elif not getattr(ctx.author.voice, "channel", None):
        em = nextcord.Embed(description="You must join a voice channel in order to use this command!", color=nextcord.Colour.red())
        return await ctx.send(embed=em)

    else:
        vc: wavelink.Player = ctx.voice_client

    
    try:
        vc.loop ^= True
    except Exception:
        setattr(vc, "loop", False)

    if vc.loop:
        return await ctx.send("🔃 Loop has been Enabled.")
    else:
        return await ctx.send("❌ Loop has been Disabled.")
        

@client.command()
async def queue(ctx: commands.Context):
    if not ctx.voice_client:
        em = nextcord.Embed(description="You are not playing a song!", color=nextcord.Colour.red())
        return await ctx.send(embed=em)
    
    elif not getattr(ctx.author.voice, "channel", None):
        em = nextcord.Embed(description="You must join a voice channel in order to use this command!", color=nextcord.Colour.red())
        return await ctx.send(embed=em)

    else:
        vc: wavelink.Player = ctx.voice_client

    if vc.queue.is_empty:
        return await ctx.send("The queue is empty!")
    
    embed = nextcord.Embed(title="Your queue")
    
    queue = vc.queue.copy()
    song_count = 0

    for song in queue:
        song_count += 1
        embed.add_field(name=f"{song_count}", value=f"[{song.title}]({song.uri})", inline=False)

    await ctx.send(embed=embed)

import datetime

@client.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def reverse(ctx, *, msg: str = "avlas etivni"):
    try:
        lol = str(msg)
    except Exception as e:
        await ctx.send("Oh my god! Please enter english alphabets")
    """ffuts esreveR"""
    if "enoyreve@" in msg or "ereh@" in msg:
        await ctx.send("You are noob!")
        return
    em = nextcord.Embed(title=msg[ ::-1], description=None, color=nextcord.Color.random())
    await ctx.send(embed=em)
    y = random.randrange(1,100)
    x = 2
    if y < 11:

        try:
                
            with open(f'databases/{ctx.author.id}.txt', 'a+') as f:
                if "ffuts desreveR" in open(f'databases/{ctx.author.id}.txt').read():
                    print('rrr')
                    return
                else:  
                    await ctx.send(achi("ffuts", "desreveR"))
                    f.write(f"<:crazy_carl:884492364331233312> ffuts desreveR\n")
                #await ctx.send(achi("Big", "PP"))

        except Exception as e:
                print(e)

@client.command()
async def uptime(ctx):
    uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
    await ctx.send(uptime)

@client.slash_command(name="hello")
async def hello(interaction: nextcord.Interaction):
    await interaction.response.send_message("Hello!")

@client.command(aliases=['guess'])
@commands.cooldown(1,10, commands.BucketType.user)
async def guessthenumber(ctx):

    num = random.randint(1,100)
    print(num)

    em = nextcord.Embed(title="New Game!", description="You have to reply with your guess (must be a number)\nYou get 10 chances to guess the number I have between 1 and 100, Good Luck", color=nextcord.Color.random())
    await ctx.send(embed=em)



    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.message.channel

    for i in range(1, 11):
        guess = await client.wait_for('message', check=check, timeout=30)
        try:
            lol = int(guess.content)
        except Exception as e:
            await ctx.send("You entered an invalid digit\nEnding the game!")

        #if lol.isdigit():
            #await ctx.send("You entered an invalid guess\nEnding the game!")
            #break
            #return

        if i > 10:
            await ctx.send(f"You lost\nThe number was {num}")


        elif int(guess.content) == num:
            higher = nextcord.Embed(title="Higher!", description=f"You guessed {guess.content}, but my number is greater than your guess", color=nextcord.Colour.red())

            lower = nextcord.Embed(title="Lower!", description=f"You guessed {guess.content}, but my number is smaller than your guess", color=nextcord.Colour.red())

            right = nextcord.Embed(title="You won!", description=f"You guessed {guess.content}, which was the right number", color=nextcord.Colour.green())        
            await ctx.send(embed=right)
            y = random.randrange(1,100)
            x = 2
            if y < 20:

                try:
                        
                    with open(f'databases/{ctx.author.id}.txt', 'a+') as f:
                        if "Gssed" in open(f'databases/{ctx.author.id}.txt').read():
                            print('rrr')
                            return
                        else:  
                            await ctx.send(achi("Gssed", " "))
                            f.write(f"<:angry_carl:884492222479880192> Gssed\n")
                        #await ctx.send(achi("Big", "PP"))

                except Exception as e:
                        print(e)
            break
        elif int(guess.content) < num:
                higher = nextcord.Embed(title="Higher!", description=f"You guessed {guess.content}, but my number is greater than your guess", color=nextcord.Colour.red())

                lower = nextcord.Embed(title="Lower!", description=f"You guessed {guess.content}, but my number is smaller than your guess", color=nextcord.Colour.red())

                right = nextcord.Embed(title="You won!", description=f"You guessed {guess.content}, which was the right number", color=nextcord.Colour.green())
                await ctx.send(embed=higher)
                await ctx.send(f"You have {10-i} chances left")

        elif int(guess.content) > num:
                higher = nextcord.Embed(title="Higher!", description=f"You guessed {guess.content}, but my number is greater than your guess", color=nextcord.Colour.red())

                lower = nextcord.Embed(title="Lower!", description=f"You guessed {guess.content}, but my number is smaller than your guess", color=nextcord.Colour.red())

                right = nextcord.Embed(title="You won!", description=f"You guessed {guess.content}, which was the right number", color=nextcord.Colour.green())
                await ctx.send(embed=lower)
                await ctx.send(f"You have {10-i} chances left")

async def check(id):
    try:
        with open(f'{id}.txt', 'w') as f:
            return True
    except:
        pass

@client.command(aliases=['achi'])
async def achievements(ctx, mem: nextcord.Member = None):
    if mem is None:
        mem = ctx.author

    try:
        em = nextcord.Embed(title=f"{mem}'s achievements!", description=None, color=nextcord.Color.random())
        with open(f'databases/{mem.id}.txt', 'r') as f:
            data = f.readlines()
            for item in data:
                name = item
                em.add_field(name=f"----------", value=f"**{name}**", inline=False)
                
            await ctx.send(embed=em)

    except:
        await ctx.send(f"No achievements found! <:angry_carl:884492222479880192>")



@client.command()
async def redem098(ctx):
    with open(f'databases/{ctx.author.id}.txt', 'a+') as f:
        if "Gssed" in open(f'databases/{ctx.author.id}.txt').read():
            print('rrr')
            return
        else:  
            await ctx.send(achi("Gssed", " "))
            f.write(f"<:EarlySupporterBadge:880053929222742056> Noob\n")

@client.command(aliases=['checkmessages'])
async def checkmsg(ctx, timeframe=7, channel: nextcord.TextChannel = None, *, user: nextcord.Member = None):
    if timeframe == 1968:
        await ctx.channel.send("Sorry. The maximum of days you can check is 1968.")
    elif timeframe <= 0:
        await ctx.channel.send("Sorry. The minimum of days you can check is one.")

    else:
        if not channel:
            channel = ctx.channel
        if not user:
            user = ctx.author

        async with ctx.channel.typing():
            msg = await ctx.channel.send('Calculating...')
            await msg.add_reaction('🔎')

            counter = 0
            async for message in channel.history(limit=5000,
                                                 after=datetime.datetime.today() - datetime.timedelta(days=timeframe)):
                if message.author.id == user.id:
                    counter += 1

            await msg.remove_reaction('🔎', member=message.author)

            if counter == 5000:
                await msg.edit(
                    content=f'{user} has sent over 5000 messages in the channel "{channel}" within the last {timeframe} days!')
            else:
                await msg.edit(
                    content=f'{user} has sent {str(counter)} messages in the channel "{channel}" within the last {timeframe} days.')

@help.command(aliases=['checkmessages'])
async def checkmsg(ctx):

    em = nextcord.Embed(title="**Check Messages**", description="Check how many messages were sent by a certain user",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''checkmessages [timeframe] [channel] [user]''')
    em.add_field(name="**Example**", value="checkmessages 7 #general @Fire")
    em.add_field(name="**Aliases**", value="checkmsg")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)      

@client.command(aliases=["bc"])
async def bitcoin(context):
    url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
    # Async HTTP request
    async with aiohttp.ClientSession() as session:
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        embed = nextcord.Embed(
            title="Current",
            description=f"Price of bitcoin is: ${response['bpi']['USD']['rate']}",
            color=nextcord.Colour.green()
        )
        await context.send(embed=embed)
    

@help.command(aliases=['bc'])
async def bitcoin(ctx):

    em = nextcord.Embed(title="**Bitcoin**", description="See the current bitcoin price",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''bitcoin''')
    em.add_field(name="**Example**", value="bitcoin")
    em.add_field(name="**Aliases**", value="bc")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)    

@client.command(aliases=['members'])
async def membercount(ctx):
    embed = nextcord.Embed(colour=nextcord.Colour.orange())

    embed.set_author(name="Member Count", icon_url=ctx.author.avatar.url)
    embed.add_field(name="Current Member Count:", value=ctx.guild.member_count)
    embed.set_footer(text=ctx.guild, icon_url=ctx.guild.icon.url)
    embed.timestamp = datetime.datetime.utcnow()

    await ctx.send(embed=embed)

@help.command(aliases=['members'])
async def membercount(ctx):

    em = nextcord.Embed(title="**Member Count**", description="See the amount of members in the guild",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''membercount''')
    em.add_field(name="**Example**", value="membercount")
    em.add_field(name="**Aliases**", value="members")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)    

@client.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def pp(context, member: nextcord.Member = None):

    if not member:
        member = context.author
    length = random.randrange(15)
    embed = nextcord.Embed(description=f"8{'=' * length}D", color=nextcord.Color.gold())
    embed.set_author(name=f"{member.display_name}'s pp", icon_url=member.avatar.url)
    await context.send(embed=embed)

    y = random.randrange(1,100)
    x = 2
    if y < 20:

        try:
                
            with open(f'databases/{context.author.id}.txt', 'a+') as f:
                if "Big PP" in open(f'databases/{context.author.id}.txt').read():
                    print('rrr')
                    return
                else:  
                    await context.send(achi("Big", "PP"))
                    f.write(f"<:lmao_carl:884811173109854228> Big PP\n")
                #await ctx.send(achi("Big", "PP"))

        except Exception as e:
                print(e)




class Menu(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=50)
        self.value = None
        
    @nextcord.ui.button(label="Next", style=nextcord.ButtonStyle.green)
    async def menu1(self, button: nextcord.ui.button, interaction: nextcord.Interaction):
        em = nextcord.Embed(
            title="Command List", color=nextcord.Color.random())
        em.add_field(name="**Fun**", value="`sl_help fun`")
        em.add_field(name="**Moderation**", value="`sl_help mod`")
        em.add_field(name="**Tools**", value="`sl_help tools`")
        em.add_field(name="**Reaction roles**", value="`sl_help reactrole`")
        em.add_field(name="**ToDo**", value="`sl_help todo`")
        em.add_field(name="**GlobalChat**", value="`sl_help globalchat`")
        em.add_field(name="**Economy**", value="`sl_help economy`")
        em.add_field(name="**Music**", value="`sl_help music`")
        em.add_field(name="**Slash commands**", value="`sl_help slash`")
        em.add_field(name="**Links**", value="[Invite me](https://discord.com/api/oauth2/authorize?client_id=1054719146304225285&permissions=8&scope=bot%20applications.commands) || [Support Server](https://discord.gg/wxmfApgR)", inline=False)
        em.set_footer(text="Cant figure out how to use a command? sl_help [command] to get some information related to the command\nTry my ticket system\n*Page 2/2*")
        await interaction.response.edit_message(embed=em)

    @nextcord.ui.button(label="Prev", style=nextcord.ButtonStyle.green)
    async def menu2(self, button: nextcord.ui.button, interaction: nextcord.Interaction, disabled=True):
        em = nextcord.Embed(title="**Salva Help Menu**", description=f'''To see the list of commands please switch to page two.

**Spot Light**

**Global Chat**: Talk with people of other servers!\nMake new friends, try my inter-server chatting tool!\nTry sl_help globalchat or sl_help globalchatstart right now!

**Current games**: Feeling bored? Want to know what other members of the server are doing? Then *Current games* is waiting for you! Try sl_help currentgames or sl_cg right now!

**Who's playing**: Going to play a game, but are you alone and want to play with others? sl_whosplaying will show you the list of people playing the game you searched for! Try sl_help whosplaying right now!

------------------------------------------------------------------------

**Tip** :- {random.choice(tips)}

**Fact of the day**\n{rf}

**Question of the day**\n{rq}''', color=nextcord.Colour.random())
        em.set_footer(text="*Page 1/2*")
        await interaction.response.edit_message(embed=em)
        


        

@client.command()
async def test1(ctx):
    view = Menu()
    await ctx.reply("Help pg 1/2", view=view)
    await ctx.send(achi("Re", "lol"))

@help.command(aliases=['guess'])
async def guessthenumber(ctx):

    em = nextcord.Embed(title="**Guess The Number**", description="Play the game of guess the number with me!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''guessthenumber''')
    em.add_field(name="**Example**", value="guessthenumber")
    em.add_field(name="**Aliases**", value="guess")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)    

@help.command()
async def happy(ctx):

    em = nextcord.Embed(title="**Happy**", description="Show other members that you are happy!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''happy''')
    em.add_field(name="**Example**", value="happy")
    #em.add_field(name="**Aliases**", value="guess")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command(aliases=['achi'])
async def achievements(ctx):

    em = nextcord.Embed(title="**Achievements**", description="Shows the achievements list of the mentioned member",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''achievements [member]''')
    em.add_field(name="**Example**", value="achievements @Fire")
    em.add_field(name="**Aliases**", value="achi")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command()
async def sad(ctx):

    em = nextcord.Embed(title="**Sad**", description="Show other members that you are sad...",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''sad''')
    em.add_field(name="**Example**", value="sad")
    #em.add_field(name="**Aliases**", value="guess")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command()
async def hug(ctx):

    em = nextcord.Embed(title="**Hug**", description="Virtualy hug the mentioned person!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''hug [member]''')
    em.add_field(name="**Example**", value="hug @Fire")
    #em.add_field(name="**Aliases**", value="guess")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@client.slash_command(name="weather", description="Get the weather details of a specific city")
async def weather(interaction: nextcord.Interaction, *, city: Optional[str] = nextcord.SlashOption(required=True)):
    city_name = city
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        
        y = x["main"]
        current_temperature = y["temp"]
        current_temperature_celsiuis = str(round(current_temperature - 273.15))
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]

        embed = nextcord.Embed(title=f"Weather in {city_name}",
                                  color=nextcord.Colour.random(),
                                   )
        embed.add_field(name="Descripition", value=f"**{weather_description}**", inline=False)
        embed.add_field(name="Temperature(C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
        embed.add_field(name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
        embed.add_field(name="Atmospheric Pressure(hPa)", value=f"**{current_pressure}hPa**", inline=False)
        embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
        embed.set_footer(text=f"Requested by {interaction.user}")

        await interaction.response.send_message(embed=embed)

        

    else:
        await interaction.response.send_message("City not found.")
        
@client.slash_command(name="invite", description="Get the invite link of this bot!")
async def invite(interaction: nextcord.Interaction):
    b1 = nextcord.ui.Button(label="Invite me!", style=nextcord.ButtonStyle.url, url="https://discord.com/api/oauth2/authorize?client_id=1054719146304225285&permissions=8&scope=bot%20applications.commands")

    ll = nextcord.ui.View()
    ll.add_item(b1)
    em = nextcord.Embed(description="Click the buttom below to invite me!", color=nextcord.Colour.green())
    await interaction.response.send_message(embed=em, view=ll)

@client.slash_command(name="8ball", description="Ask the magic 8ball some questions")
async def _8ball(interaction: nextcord.Interaction,*, question: Optional[str] = nextcord.SlashOption(required=True, description="The question you want to ask magic 8ball") ):
    responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
             "Don’t count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "My reply is no.", "My sources say no.",
             "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.", "Without a doubt.",
             "Yes.", "Yes – definitely.", "You may rely on it."]

    em = nextcord.Embed(title="**8ball**", description=f"Question: {question}", color=nextcord.Colour.random())
    em.add_field(name="Answer:", value=random.choice(responses), inline=False)
    msg = await interaction.response.send_message("<a:Loading:1055429248128651274>")
    time.sleep(2)
    await msg.edit(embed=em)






reddit = praw.Reddit(client_id="vwYieLAOu6BISg",
                     client_secret="GGQ0Tt5MMmGwdCEc2jFU7qF87ZlrFg",
                     username="firRe_",
                     password="tejas#098",
                     user_agent="fire", check_for_async=False)



@client.command(aliases=['rps','spr'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def rockpaperscissors(ctx, move):
    ch = move
    #if choice == "rock" or choice == "paper" or choice == "scissor"
    vch = ["rock", "paper", "scissor", "scissors", "r", "p", "s"]
    dll = ["Rock", "Paper", "Scissors"]
    mch = random.choice(dll)

    if ch in vch:

        if ch == "r":
            lol = "Rock"
        elif ch == "p":
            lol = "Paper"
        elif ch == "s":
            lol = "Scissors"
            
        emw = nextcord.Embed(title="**Winner!**", description=f"You won!", color=nextcord.Colour.green())
        emw.add_field(name=f"You chose:", value=lol, inline=False)
        emw.add_field(name=f"I chose", value=mch, inline=False)

        eml = nextcord.Embed(title="**You lost!**", description=f"You lost", color=nextcord.Colour.red())
        eml.add_field(name=f"You chose:", value=lol, inline=False)
        eml.add_field(name=f"I chose", value=mch, inline=False)

        emmt = nextcord.Embed(title="**Tie!**", description=f"It's a tie!", color=nextcord.Colour.blue())
        emmt.add_field(name=f"You chose:", value=lol, inline=False)
        emmt.add_field(name=f"I chose", value=mch, inline=False)

        if ch in vch:
            if mch == "Rock":
                if ch == "paper" or ch == "p":
                    await ctx.send(embed=emw)
                    y = random.randrange(1,100)
                    x = 2
                    if y < 70:

                        try:
                                
                            with open(f'databases/{ctx.author.id}.txt', 'a+') as f:
                                if "RPShoot" in open(f'databases/{ctx.author.id}.txt').read():
                                    print('rrr')
                                    return
                                else:  
                                    await ctx.send(achi("RPShoot", " "))
                                    f.write(f"<:bored_carl:884492103462289459> RPShoot\n")
                                #await ctx.send(achi("Big", "PP"))

                        except Exception as e:
                                print(e)
                elif ch == "scissor" or ch == "s":
                    await ctx.send(embed=eml)
                else:
                    await ctx.send(embed=emmt)

        if ch in vch:
            if mch == "Paper":
                if ch == "rock" or ch == "r":
                    await ctx.send(embed=eml)
                elif ch == "scissor" or ch == "s":
                    await ctx.send(embed=emw)
                    y = random.randrange(1,100)
                    x = 2
                    if y < 70:

                        try:
                                
                            with open(f'databases/{ctx.author.id}.txt', 'a+') as f:
                                if "RPShoot" in open(f'databases/{ctx.author.id}.txt').read():
                                    print('rrr')
                                    return
                                else:  
                                    await ctx.send(achi("RPShoot", " "))
                                    f.write(f"<:bored_carl:884492103462289459> RPShoot\n")
                                #await ctx.send(achi("Big", "PP"))

                        except Exception as e:
                                print(e)
                else:
                    await ctx.send(embed=emmt)    

        if ch in vch:
            if mch == "Scissor":
                if ch == "paper" or ch == "p":
                    await ctx.send(embed=eml)
                elif ch == "scissor" or ch == "s":
                    await ctx.send(embed=emmt)
                else:
                    await ctx.send(embed=emw)
                    y = random.randrange(1,100)
                    x = 2
                    if y < 70:

                        try:
                                
                            with open(f'databases/{ctx.author.id}.txt', 'a+') as f:
                                if "RPShoot" in open(f'databases/{ctx.author.id}.txt').read():
                                    print('rrr')
                                    return
                                else:  
                                    await ctx.send(achi("RPShoot", " "))
                                    f.write(f"<:bored_carl:884492103462289459> RPShoot\n")
                                #await ctx.send(achi("Big", "PP"))

                        except Exception as e:
                                print(e)      

    else:
        await ctx.send("Please enter a **valid** option (rock, paper, scissors).")  


@client.command()
async def hello(ctx):
    await ctx.send("Hello")

@client.command(aliases=["av"])
async def avatar(ctx, member: nextcord.Member = None):
    if member is None:
        member = ctx.author

    embed2 = nextcord.Embed(title=f"{member}'s Avatar!", colour=member.color, timestamp=ctx.message.created_at)
    embed2.add_field(name="Animated?", value=member.avatar.is_animated())
    embed2.set_image(url=member.avatar.url)
    await ctx.send(embed=embed2)

"""#@help.command(aliases=["rr"])
async def reactrole(ctx):
    em = nextcord.Embed(title="<:channels:845773870665302046Reactrole<:channels:845773870665302046",
                       description="Syntax: rr [emoji] [role] [message]")
    em.add_field(name="Example",
                 value="rr <:channels:845773870665302046 @new-role react with <:channels:845773870665302046 to get new role")
    em.set_footer(text="Note- Custom emojis may or may not work!")
    await ctx.send(embed=em)"""

@client.command()
async def whois(ctx, member: nextcord.Member = None):
    if member == None:
        member = ctx.author

    roles = [role for role in member.roles]

    embed = nextcord.Embed(colour=member.colour, timestamp=ctx.message.created_at)

    embed.set_author(name=f"User info: {member}")
    embed.set_thumbnail(url=member.avatar.url)
    embed.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar.url)

    embed.add_field(name='ID:', value=member.id)
    embed.add_field(name='Guild Name:', value=member.display_name)

    embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name=f"roles({len(roles)})", value="".join([role.mention for role in roles]))
    embed.add_field(name="top role:", value=member.top_role.mention)

    embed.add_field(name='bot?', value=member.bot)

    await ctx.send(embed=embed)

@help.command(aliases=['meminfo'])
async def whois(ctx):
    em = nextcord.Embed(title="**Who is**", description="Get some information about the mentioned user",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value="whois [member]")
    em.add_field(name="**Example**", value="whois @Fire")
    em.add_field(name="**Aliases**", value="meminfo")
    await ctx.send(embed=em)

@help.command(aliases=['av'])
async def avatar(ctx):
    em = nextcord.Embed(title="**Avatar**", description="Get the avatar of someone\nAliases: av",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value="avatar [member]")
    em.add_field(name="**Example**", value="av @Fire")
    await ctx.send(embed=em)



@help.command()
async def fun(ctx):
    em = nextcord.Embed(title="Fun", description="Use help <command> to get extend information of the command",
                       colour=nextcord.Colour.random())
    em.add_field(name="**All**",
                 value="<:arrow:909827536513532015>Akinator, currentgames, whosplaying, guess, choose,\n<:arrow:909827536513532015>pp, fact, rate, hack, rps,\n<:arrow:909827536513532015>joke, meme, 8ball, noob_rate,\n<:arrow:909827536513532015>tictactoe, happy, giphy, epic_rate,\n<:arrow:909827536513532015>hug, ship, achievements, hangman ", inline=False)
    em.add_field(name="**Games**", value="<:arrow:909827536513532015>Akinator, guessthenumber, rockpaperscissors, tictactoe, hangman", inline=False)
    em.add_field(name="**Highlights**", value="<:arrow:909827536513532015>Currentgames, whosplaying, ship", inline=False)


    await ctx.send(embed=em)

@help.command(aliases=['eco'])
async def economy(ctx):
    em = nextcord.Embed(title="Fun", description="Not the best economy, but it's fun! Be the first one to buy 'Vip+'",
                       colour=nextcord.Colour.random())
    em.add_field(name="**All**",
                 value="<:arrow:909827536513532015>Deposit, withdraw, sell, give, buy,\n<:arrow:909827536513532015>slots, shop, beg, search, fish,\n<:arrow:909827536513532015>bag, rob, daily", inline=False)
    em.add_field(name="**Highlights**", value="<:arrow:909827536513532015>Slots, shop", inline=False)


    await ctx.send(embed=em)

@help.command()
async def tools(ctx):
    em = nextcord.Embed(title="Tools", description="Use help <command> to get extend information of the command",
                       colour=nextcord.Colour.random())
    em.add_field(name="**All**",
                 value="<:arrow:909827536513532015>Avatar, poll, weather, checkmessages, bitcoin,\n<:arrow:909827536513532015>Servericon, serverinfo, whois, membercount, afk,\n<:arrow:909827536513532015>Calculator, vote", inline=False)
    em.add_field(name="**Highlights**", value="<:arrow:909827536513532015>Weather, bitcoin", inline=False)


    await ctx.send(embed=em)

@help.command()
async def music(ctx):
    em = nextcord.Embed(title="Music", description="Use help <command> to get extend information of the command",
                       colour=nextcord.Colour.random())
    em.add_field(name="**All**",
                 value="<:arrow:909827536513532015>Play, pause, resume, skip, stop,\n<:arrow:909827536513532015>Loop, queue, disconnect", inline=False)
    #em.add_field(name="**Highlights**", value="<:arrow:909827536513532015>Weather, bitcoin", inline=False)


    await ctx.send(embed=em)

@help.command(aliases=['gc'])
async def globalchat(ctx):
    em = nextcord.Embed(title="Global Chat", description="Use help <command> to get extend information of the command",
                       colour=nextcord.Colour.random())
    em.add_field(name="**All**",
                 value="<:arrow:909827536513532015>Globalchatstart, globalchatstop", inline=False)


    await ctx.send(embed=em)

@help.command(aliases=['slashcmnds'])
async def slash(ctx):
    em = nextcord.Embed(title="Global Chat", description="More commands coming soon!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**All**",
                 value="<:arrow:909827536513532015>/8ball, /weather, /hello", inline=False)


    await ctx.send(embed=em)

@help.command(aliases=['mod'])
async def moderation(ctx):
    em = nextcord.Embed(title="Moderation Tools", description="Use help <command> to get extend information of the command",
                       colour=nextcord.Colour.random())
    em.add_field(name="**All**",
                 value="<:arrow:909827536513532015>Kick, ban, unban, slowmode, ticket,\n<:arrow:909827536513532015>lock, unlock, mute, unmute, addrole,\n<:arrow:909827536513532015>removerole, purge", inline=False)
    em.add_field(name="**Highlights**", value="<:arrow:909827536513532015>Ticket", inline=False)


    await ctx.send(embed=em)

@client.command()
async def botinfo(ctx):
    em = nextcord.Embed(title="Information", color=nextcord.Colour.random())
    em.add_field(name="Ping", value=f"{round(client.latency * 1000)}ms", inline=False)
    em.add_field(name="Guilds", value=f"{str(len(client.guilds))}", inline=False)
    em.add_field(name="Prefix", value=f"{prefix[0]}", inline=False)
    em.add_field(name="Commands", value=f"{len(client.commands)}", inline=False)
    em.add_field(name="Dev", value="`|||FIRE|||#9971`", inline=False)
    await ctx.send(embed=em)

@client.command()
async def ping(ctx):
    em = nextcord.Embed(title="My latency!")
    em.add_field(name="Current ping", value=f'{round(client.latency * 1000)}ms')
    await ctx.send(embed=em)


@help.command(aliases=['bi'])
async def botinfo(ctx):
    em = nextcord.Embed(title="**Bot Info**", description="Information about the bot\nSyntax: sl_botinfo",color=ctx.author.color, timestamp=ctx.message.created_at)
    await ctx.send(embed=em)

@client.command()
async def rate(ctx, member: nextcord.Member=None):
    if member is None:
        member = ctx.author
    em = nextcord.Embed(title=f"I will give {member} {random.randrange(10)}/10 :star:", colour=member.color,)
    await ctx.send(embed=em)

@help.command()
async def rate(ctx):
    em = nextcord.Embed(title="**Rate**", description="A fun command",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value="rate [member]")
    em.add_field(name="**Example**", value="rate @Fire")
    await ctx.send(embed=em)


@client.command()
async def afk(ctx, mins: int=None):
    if mins == None:
        await ctx.send("Ok you were afk for 1 ms")
        return
    current_nick = ctx.author.nick
    await ctx.send(f"{ctx.author.mention} has gone afk for {mins} minutes.")
    await ctx.author.edit(nick=f"{ctx.author.name} [AFK]")

    counter = 0
    while counter <= int(mins):
        counter += 1
        await asyncio.sleep(60)

        if counter == int(mins):
            await ctx.author.edit(nick=current_nick)
            await ctx.send(f"{ctx.author.mention} is no longer AFK")
            break

@help.command()
async def afk(ctx):
    em = nextcord.Embed(title="**Afk**", description="Tell others that you are going afk!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value="afk [mins]")
    em.add_field(name="**Example**", value="afk 5")
    await ctx.send(embed=em)

@help.command()
async def uptime(ctx):
    em = nextcord.Embed(title="**Uptime**", description="Shows the bots uptime",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value="uptime")
    em.add_field(name="**Example**", value="uptime")
    await ctx.send(embed=em)

@help.command()
async def reverse(ctx):
    em = nextcord.Embed(title="**Reverse**", description="ffuts esreveR",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value="rate [member]")
    em.add_field(name="**Example**", value="rate @Fire")
    await ctx.send(embed=em)

@client.command(aliases=['clear','c'])
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount = 3):
    await ctx.send(f"`Deleting {amount} messages`")
    await ctx.channel.purge(limit=amount+2)

@client.command(aliases=['noob'])
async def noob_rate(ctx, mem: nextcord.Member = None):
    if mem is None:
        mem = ctx.author

        
    
    msg = await ctx.send(f"How much % noob is {mem.mention}?")
    await asyncio.sleep(1)
    await msg.edit("█▒▒▒▒▒▒▒▒▒ 10%")
    await asyncio.sleep(0.5)
    await msg.edit("█████▒▒▒▒▒ 30%")
    await asyncio.sleep(0.5)
    await msg.edit("███████▒▒▒50%")
    await asyncio.sleep(0.5)
    await msg.edit("██████████ 100%")
    await asyncio.sleep(1)
    await msg.edit(f"{mem.mention} is\n[======================] **{random.randrange(0,100)}%** noob")

@client.command(aliases=['epic'])
async def epic_rate(ctx, mem: nextcord.Member = None):
    if mem is None:
        mem = ctx.author

        
    
    msg = await ctx.send(f"How much % epic is {mem.mention}?")
    await asyncio.sleep(1)
    await msg.edit("█▒▒▒▒▒▒▒▒▒ 10%")
    await asyncio.sleep(0.5)
    await msg.edit("█████▒▒▒▒▒ 30%")
    await asyncio.sleep(0.5)
    await msg.edit("███████▒▒▒50%")
    await asyncio.sleep(0.5)
    await msg.edit("██████████ 100%")
    await asyncio.sleep(1)
    await msg.edit(f"{mem.mention} is\n[======================] **{random.randrange(0,100)}%** epic")

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: nextcord.Member, *, reason = None):
  if not reason:
    await user.kick()
    await ctx.send(f"**{user}** has been kicked for **no reason**.")
    await user.send(f"You were kicked from the guild {ctx.author.guild} for no reason provided")
  else:
    await user.kick(reason=reason)
    await ctx.send(f"**{user}** has been kicked for **{reason}**.")
    await user.send(f"You were kicked from the guild {ctx.author.guild} for the reason {reason}")


@client.command()
async def tadd(ctx,*,task):
  with open(f"databases/t{ctx.author.id}.txt", "a") as f:
    f.write(f"{task}\n")
  await ctx.send("Added the task to your todo list!!\nUse `sl_tshow` to see your todo list")

@help.command()
async def tadd(ctx):

    em = nextcord.Embed(title="**Tadd**", description="Add a task to your todo list",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''tadd [task]''')
    em.add_field(name="**Example**", value="tadd Clean the table")
    #em.add_field(name="**Aliases**", value="members")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@client.command()
async def tshow(ctx):
  try:
    em = nextcord.Embed(title="Your To-Do", color=nextcord.Colour.random())
    with open(f"databases/t{ctx.author.id}.txt", "r") as f:
     for i, line in enumerate(f):
       em.add_field(name=f"**{i+1}**", value=line, inline=False)
    await ctx.send(embed=em)

  except Exception as e:
    await ctx.send("You haven't added a task yet")
    print(e)

@help.command()
async def tshow(ctx):

    em = nextcord.Embed(title="**Tshow**", description="See your todo list",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''tshow''')
    em.add_field(name="**Example**", value="tshow")
    #em.add_field(name="**Aliases**", value="members")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@client.command()
async def tclear(ctx):
  try:
    os.remove(f"databases/t{ctx.author.id}.txt")
    await ctx.send("Cleared your todo list!")

  except:
    await ctx.send("You dont have any tasks added yet")

@help.command()
async def tclear(ctx):

    em = nextcord.Embed(title="**Tclear**", description="Completely clear your todo list",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''tclear''')
    em.add_field(name="**Example**", value="tclear")
    #em.add_field(name="**Aliases**", value="members")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command()
async def todo(ctx):
    em = nextcord.Embed(title="ToDo", description="Use help <command> to get extend information of the command",
                       colour=nextcord.Colour.random())
    em.add_field(name="**All**",
                 value="<:arrow:909827536513532015>tadd, tdone, tshow, tclear, timer", inline=False)
    em.add_field(name="**Highlights**", value="<:arrow:909827536513532015>Be productive while having fun!", inline=False)


    await ctx.send(embed=em)

@client.command()
async def timer(ctx, seconds):
  if int(seconds) > 1200:
    await ctx.send("Uh! The timer can't go over 20 mins.")
    return
  msg = await ctx.send("Great! Now you can focus on your work I have put a timer of {} seconds".format(seconds))
  seconds = int(seconds)
  await asyncio.sleep(seconds)
  await msg.edit(content=f"{ctx.author.mention} your timer has ended I hope you have done your work! if you haven't then you can start the timer again no worries! :)\nIf you have completed the task then use `sl_tdone [task no.]` or `sl_tclear`")

@help.command()
async def timer(ctx):

    em = nextcord.Embed(title="**Timer**", description="Set a timer",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''timer [mins]''')
    em.add_field(name="**Example**", value="timer 5")
    #em.add_field(name="**Aliases**", value="members")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@client.command()
async def tdone(ctx, index):
  no = int(index)
  
  with open(f"databases/t{ctx.author.id}.txt",'r') as f:
      get_all=f.readlines()
      

  
  with open(f"databases/t{ctx.author.id}.txt",'w') as f:
      for i,line in enumerate(get_all,1):         ## STARTS THE NUMBERING FROM 1 (by default it begins with 0)    
          if i == no:
            ee = line[0:-1]                              ## OVERWRITES line
            f.writelines(f"~~{ee}~~:white_check_mark:\n")
            await ctx.send("I have marked the task as done")
          else:
            f.writelines(line)

@help.command()
async def tdone(ctx):

    em = nextcord.Embed(title="**Tdone**", description="Mark the task as done",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''tdone [task no.]''')
    em.add_field(name="**Example**", value="tdone 2")
    #em.add_field(name="**Aliases**", value="members")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command()
async def removerole(ctx):
    em = nextcord.Embed(title="**Removerole**", description="Remove the mentioned role from the mentioned member",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value="removerole [member] [role]")
    em.add_field(name="**Example**", value="addrole @Fire @Staff")
    #em.add_field(name="Aliases", value="shutup")
    await ctx.send(embed=em)


@help.command()
async def addrole(ctx):
    em = nextcord.Embed(title="**Addrole**", description="Add the mentioned role to the mentioned member",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value="addrole [member] [role]")
    em.add_field(name="**Example**", value="addrole @Fire @Staff")
    #em.add_field(name="Aliases", value="shutup")
    await ctx.send(embed=em)

@client.command()
async def addrole(ctx, member: nextcord.Member, role: nextcord.Role):

    await member.add_roles(role)

    em = nextcord.Embed(description=f"Gave {member.mention} the {role} role!", colour=nextcord.Colour.random())

    await ctx.send(embed=em)


@client.command()
async def removerole(ctx, member: nextcord.Member, role: nextcord.Role):

    await member.remove_roles(role)
    em = nextcord.Embed(description=f"Removed the role {role} from {member.mention}!", colour=nextcord.Colour.random())

    await ctx.send(embed=em)

@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: nextcord.Member=None, *, reason=None):
    if member == None:
        await ctx.send("Please mention someone to mute")
    try:
        guild = ctx.guild
        mutedRole = nextcord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True,
                                              read_messages=False)
        embed = nextcord.Embed(title="Muted",
                              description=f"{member.mention} was muted ", colour=nextcord.Colour.random())
        embed.add_field(name="reason:", value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.add_roles(mutedRole, reason=reason)
        await member.send(f"You have been muted from: {guild.name} reason: {reason}")
    except Exception as e:
        print(e)


@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: nextcord.Member=None):
    if member == None:
        await ctx.send("Please mention someone to unmute")
        return




    mutedRole = nextcord.utils.get(ctx.guild.roles, name="Muted")
    if mutedRole in member.roles:
        await member.remove_roles(mutedRole)
        await member.send(f" You have been unmuted from: - {ctx.guild.name}")
        embed = nextcord.Embed(
                            description=f"Unmuted - {member.mention}",
                            colour=nextcord.Colour.random())
        await ctx.send(embed=embed)
    else:
        em = nextcord.Embed(description=f"They are not muted!")

@help.command(aliases=['shutup'])
async def mute(ctx):
    em = nextcord.Embed(title="**Mute**", description="Mute the mentioned user!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value="mute [member] [reason]")
    em.add_field(name="**Example**", value="mute @Fire spamming")
    em.add_field(name="Aliases", value="shutup")
    await ctx.send(embed=em)

@help.command()
async def unmute(ctx):
    em = nextcord.Embed(title="**Unmute**", description="Unmute the mentioned user!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value="unmute [member] [reason]")
    em.add_field(name="**Example**", value="unmute @Fire")
    #em.add_field(name="Aliases", value="shutup")
    await ctx.send(embed=em)

@help.command(aliases=["rr"])
async def reactrole(ctx):
    em = nextcord.Embed(title="**Reaction Role**", description="Create a reaction role embed!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value="reactrole [emoji] [@role] [message]")
    em.add_field(name="**Example**", value="reactrole :fire: @Mod Click to get the mod role")
    em.add_field(name="Aliases", value="rr")
    await ctx.send(embed=em)


@help.command(aliases=["ticketcreate"])
async def ticket(ctx):
    em = nextcord.Embed(title="**Ticket**", description="Create a ticket message, to which members can react to create a ticket!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value="ticket [embed text]")
    em.add_field(name="**Example**", value="ticket help & support")
    em.add_field(name="Aliases", value="ticketcreate")
    await ctx.send(embed=em)

@help.command()
async def unlock(ctx):
    em = nextcord.Embed(title="**Unlock**", description="Unlock the mentioned channel",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value="unlock [channel]")
    em.add_field(name="**Example**", value="unlock #general")
    #em.add_field(name="Aliases", value="shutdown")
    await ctx.send(embed=em)

@help.command(aliases=["slow"])
async def slowmode(ctx):
    em = nextcord.Embed(title="**Slowmode**", description="Add a cooldown to the channel",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value="slowmode [secs]")
    em.add_field(name="**Example**", value="slowdown 10s")
    em.add_field(name="Aliases", value="slow")
    await ctx.send(embed=em)

@help.command(aliases=["shutdown"])
async def lock(ctx):
    em = nextcord.Embed(title="**Lock**", description="Lock the mentioned channel",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value="lock [channel]")
    em.add_field(name="**Example**", value="lock #general")
    em.add_field(name="Aliases", value="shutdown")
    await ctx.send(embed=em)

@client.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def ticket(ctx,*, text="React below to create a ticket"):
    #await ctx.send("TIcket command is under maintainnence")
    guild = ctx.guild
    embed = nextcord.Embed(
        title='Ticket',
        description=text,
        color=nextcord.Colour.random()
    )

    msg = await ctx.send(embed=embed)
    await msg.add_reaction("✉")

COOLDOWN_AMOUNT = 10.0  # seconds
last_executed = time.time()
def assert_cooldown():
    global last_executed  # you can use a class for this if you wanted
    if last_executed + COOLDOWN_AMOUNT < time.time():
        last_executed = time.time()
        return True
    return False

@client.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        pass
    
    elif str(payload.emoji) == "✉":
        if assert_cooldown():
            
            guild = client.get_guild(payload.guild_id)
            overwrites = {
                guild.me: nextcord.PermissionOverwrite(view_channel=True),
                payload.member: nextcord.PermissionOverwrite(view_channel=True),
                guild.default_role: nextcord.PermissionOverwrite(view_channel=False)
            }
            for role in guild.roles[1:4]:
                overwrites[role] = nextcord.PermissionOverwrite(view_channel=True)
            channel = await guild.create_text_channel(f"Ticket-{random.randrange(1000,9999)}-{payload.member.display_name}", overwrites=overwrites)
            message= await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
            await message.remove_reaction(payload.emoji, payload.member)
        
            await channel.send(f"{payload.member.mention} Thank You! for creating this ticket staff will contact you soon. Type **sl_close** to close the ticket.")
        
            try:
                await client.wait_for("message", check=lambda m: m.channel== channel and m.author== payload.member and m.content == "sl_close")
                    
            except asyncio.TimeoutError:
                await channel.delete()
        
            else:
                await channel.delete()
        else:
            message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
            await message.remove_reaction(payload.emoji, payload.member)
            await payload.member.send("You can not create a ticket because it is on a cooldown!")
    else:
        with open('reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name:
                    role = nextcord.utils.get(client.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload):
    with open('reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:
            if x['emoji'] == payload.emoji.name:
                role = nextcord.utils.get(client.get_guild(
                    payload.guild_id).roles, id=x['role_id'])

                await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)




@client.command(aliases=["rr"])
@commands.has_permissions(manage_roles=True)
async def reactrole(ctx, emoji, role: nextcord.Role, *, message):
    
    emb = nextcord.Embed(description=message, color=nextcord.Colour.random())
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('reactrole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name': role.name,
                          'role_id': role.id,
                          'emoji': emoji,
                          'message_id': msg.id}

        data.append(new_react_role)

    with open('reactrole.json', 'w') as f:
        json.dump(data, f, indent=4)


@client.command()
@commands.cooldown(1, 3, BucketType.user)
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver
    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                time.sleep(1.5)
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    myEmbed = nextcord.Embed(title= "Winner!",description=mark + " :crown: ",color=0xf1c40f)
                    await ctx.send(embed=myEmbed)
                elif count == 9:
                    gameOver = True
                    myEmbed = nextcord.Embed(title= "Tie",description="It is a tie:handshake:",color=0xf1c40f)
                    await ctx.send(embed=myEmbed)

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                myEmbed = nextcord.Embed(title= "Place Error!",description="Be sure to choose an integer between 1 an 9 (inclusive) and an unmarked tile. ",color=0xe74c3c)
                await ctx.send(embed=myEmbed)
        else:
            myEmbed = nextcord.Embed(title= "Turn Error!",description="It is not your turn!",color=0xe74c3c)
            await ctx.send(embed=myEmbed)
    else:
        myEmbed = nextcord.Embed(title= "Please start a game!",description="To start a new game, use 'sl_tictactoe'",color=0x2ecc71)
        await ctx.send(embed=myEmbed)


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@client.command()
async def tttend(ctx):
    global count
    global player1
    global player2
    global turn
    global gameOver
    global p1_id
    global p2_id

    if ctx.message.author.id == p1_id or ctx.message.author.id == p2_id:

        count = 0
        player1 = ""
        player2 = ""
        turn = ""
        gameOver = True

        myEmbed = nextcord.Embed(title= "Game has been stopped!",description="To start a new game, USE 'sl_tictactoe'",color=0x2ecc71)
        await ctx.send(embed=myEmbed)
    
    else:
        await ctx.send('Only those who started the game can end this game')

"""

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        myEmbed = nextcord.Embed(title= "MENTION ERROR!",description="PLEASE MENTION 2 USERS",color=0xe74c3c)
        await ctx.send(embed=myEmbed)
    elif isinstance(error, commands.BadArgument):
        myEmbed = nextcord.Embed(title= "ERROR!",description="PLEASE MAKE SURE TO MENTION/PING PLAYERS (ie. <@688534433879556134)",color=0xe74c3c)
        await ctx.send(embed=myEmbed)

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        myEmbed = nextcord.Embed(title= "NO POSITION",description="PLEASE ENTER A POSITION TO MARK",color=0xe74c3c)
        await ctx.send(embed=myEmbed)
    elif isinstance(error, commands.BadArgument):
        myEmbed = nextcord.Embed(title= "INTEGER ERROR!",description="PLEASE MAKE SURE IT'S AN INTEGER",color=0xe74c3c)
        await ctx.send(embed=myEmbed) """

@help.command(aliases=['8ball'])
async def _8ball(ctx):
    em = nextcord.Embed(title="**8ball**", description="Magic 8ball will tell you your fortune",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''8ball [question]''')
    em.add_field(name="**Example**", value="8ball will he help me?")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)    

@help.command(aliases=['noob'])
async def noob_rate(ctx):
    em = nextcord.Embed(title="**Noob Rate**", description="Fun command, get someones noob %",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''noob_rate [member]''')
    em.add_field(name="**Example**", value="noob_rate @Fire")
    em.add_field(name="**Aliases**", value="noob")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command(aliases=['epic'])
async def epic_rate(ctx):

    em = nextcord.Embed(title="**Epic Rate**", description="Fun command, get someones epic %",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''epic_rate [member]''')
    em.add_field(name="**Example**", value="epic_rate @Fire")
    em.add_field(name="**Aliases**", value="epic")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command(aliases=['aki'])
async def akinator(ctx):

    em = nextcord.Embed(title="**Akinator**", description="Akinator will guess what you're thinking!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''akinator''')
    em.add_field(name="**Example**", value="akinator")
    em.add_field(name="**Aliases**", value="aki")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command(aliases=['calc'])
async def calculator(ctx):

    em = nextcord.Embed(title="**Calculator**", description="Presents you a fully advanced calculator!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''calculator''')
    em.add_field(name="**Example**", value="calculator")
    em.add_field(name="**Aliases**", value="calc")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command()
async def ship(ctx):

    em = nextcord.Embed(title="**Ship**", description="Fun command, ship two individuals",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''ship [member] [member]''')
    em.add_field(name="**Example**", value="ship @Fire @Daisy")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command(aliases=['cg'])
async def currentgames(ctx):

    em = nextcord.Embed(title="**Current Games**", description="Get a list of all the activities and games played by the members of the guild",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''currentgames''')
    em.add_field(name="**Example**", value="currentgames")
    em.add_field(name="**Aliases**", value="cg")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command(aliases=['wp'])
async def whosplaying(ctx):

    em = nextcord.Embed(title="**Who's Playing**", description="Search if a specific game is played by the members of the guild",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''whosplaying''')
    em.add_field(name="**Example**", value="whosplaying valorant")
    em.add_field(name="**Aliases**", value="wp")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command(aliases=['ttt', 'place'])
async def tictactoe(ctx):

    em = nextcord.Embed(title="**Tic Tac Toe & Place**", description="Play tic tac toe with the mentioned user, use place to mark your chance on the board",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''tictactoe [member], place [number]''')
    em.add_field(name="**Example**", value="tictactoe @Fire, place 5 (will place an indicator in the middle of the board)")
    em.add_field(name="**Aliases**", value="ttt")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command()
async def gif(ctx):
    em = nextcord.Embed(title="**Gif**", description="Get a gif of anything you search",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''gif [search]''')
    em.add_field(name="**Example**", value="gif dogs dancing")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command(aliases=['rps'])
async def rockpaperscissors(ctx):
    em = nextcord.Embed(title="**RPS**", description="Play rock and paper and scissors with me!",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''rps [rock(r), paper(p), scissors(s)]''')
    em.add_field(name="**Example**", value="rps r")
    #em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)

@help.command(aliases=['clear', 'c'])
async def purge(ctx):
    em = nextcord.Embed(title="**Purge**", description="Deletes the amount of previous messages mentioned (Default is 3)\nSyntax: sl_purge [Amount]",color=ctx.author.color, timestamp=ctx.message.created_at)
    em.add_field(name="Aliases", value="Clear, C", inline=False)
    em.add_field(name="Permission(s)", value="Manage Messages", inline=False)
    await ctx.send(embed=em)

@help.command()
async def poll(ctx):
    em = nextcord.Embed(title="**Poll**", description="Creates a new poll",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value='''poll ["question"] [Option] [Option] [Option] etc.''')
    em.add_field(name="**Example**", value="poll 'Will you come if there is a party today' Yes No Probably")
    em.add_field(name='''Note''',value='''Make sure your questions is within " "''', inline=False)
    await ctx.send(embed=em)



@client.command()
async def fact(ctx):
    em = nextcord.Embed(title="Random fact!", description=f"{randfacts.get_fact()}",color=ctx.author.color, timestamp=ctx.message.created_at)
    await ctx.send(embed=em)

@help.command()
async def fact(ctx):
    em = nextcord.Embed(title="**Fact**", description="Gives you a random fact",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value="fact")
    em.add_field(name="**Example**", value="fact")
    await ctx.send(embed=em)



@client.command()
async def joke(ctx):
    em = nextcord.Embed(title="Heres a Joke!", description=f"{pyjokes.get_joke()}", color=nextcord.Color.random())
    await ctx.send(embed=em)


@client.command()
async def weather(ctx, *, city: str):
    city_name = city
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    channel = ctx.message.channel

    if x["cod"] != "404":
        async with channel.typing():
            y = x["main"]
            current_temperature = y["temp"]
            current_temperature_celsiuis = str(round(current_temperature - 273.15))
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]

            embed = nextcord.Embed(title=f"Weather in {city_name}",
                                  color=ctx.guild.me.top_role.color,
                                  timestamp=ctx.message.created_at, )
            embed.add_field(name="Descripition", value=f"**{weather_description}**", inline=False)
            embed.add_field(name="Temperature(C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
            embed.add_field(name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)         
            embed.add_field(name="Atmospheric Pressure(hPa)", value=f"**{current_pressure}hPa**", inline=False)
            embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
            embed.set_footer(text=f"Requested by {ctx.author.name}")

            await channel.send(embed=embed)
        y = random.randrange(1,100)
        x = 2
        if y < 70:

            try:
                        
                with open(f'databases/{ctx.author.id}.txt', 'a+') as f:
                    if "IsIt Hot?" in open(f'databases/{ctx.author.id}.txt').read():
                        print('rrr')
                        return
                    else:  
                        await ctx.send(achi("IsIt", "Hot"))
                        f.write(f"<:cool:961982156312301588> IsIt Hot?\n")
                        #await ctx.send(achi("Big", "PP"))

            except Exception as e:
                    print(e)

    else:
        await channel.send("City not found.")

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : nextcord.Member, *, reason = None):
    await member.ban(reason = reason)
    if reason == None:
        await ctx.send(f"Banned {member} for the no reason provided")
        await member.send(f"You were banned from {ctx.author.guild} for no reason provided")
    else:
        await ctx.send(f"Banned {member} for {reason}")
        await member.send(f"You were banned from {ctx.author.guild} for {reason}")

@help.command(aliases=['kick', 'unban'])
async def ban(ctx):
    em = nextcord.Embed(title="**Ban, Unban, Kick**", description="Ban, Kick or Unban a user",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value="ban [member] [reason]")
    em.add_field(name="**Example**", value="ban @Fire Spamming")
    em.add_field(name="**Example**", value="kick @Fire Spamming")
    em.add_field(name="**Example**", value="unban @Fire")
    await ctx.send(embed=em)


@client.command(name='unban')
@commands.guild_only()  
async def _unban(ctx, id: int):
    user = await client.fetch_user(id)
    await ctx.guild.unban(user)
    em = nextcord.Embed(title="Unbanned", description=f"Unbanned {user.mention}!", color=nextcord.Colour.green)
    await ctx.send(embed=em)



@help.command()
async def weather(ctx):
    em = nextcord.Embed(title="**Weather**", description="Gives you the weather details of a certain city",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value="weather [city]")
    em.add_field(name="**Example**", value="weather new york")
    await ctx.send(embed=em)

@help.command()
async def joke(ctx):
    em = nextcord.Embed(title="**Joke**", description="Gives you a random joke",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value="joke")
    em.add_field(name="**Example**", value="joke")
    await ctx.send(embed=em)

@help.command(aliases=['gcstart'])
async def globalchatstart(ctx):
    em = nextcord.Embed(title="**GlobalChatStart**", description="Starts global chat in the mentioned channel",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value="globalchatstart [#channel]")
    em.add_field(name="**Example**", value="globalchatstart #global")
    await ctx.send(embed=em)

@help.command(aliases=['gcstop'])
async def globalchatstop(ctx):
    em = nextcord.Embed(title="**GlobalChatStop**", description="Stopss global chat in the mentioned channel",
                       colour=nextcord.Colour.random())
    em.add_field(name="**Syntax**", value="globalchatstop [#channel]")
    em.add_field(name="**Example**", value="globalchatstop #global")
    await ctx.send(embed=em)

@help.command(aliases=["global"])
async def gbl(ctx):
    em = nextcord.Embed(title="Global Chat", description="Interact and chat with the members of other servers\nMake sure to follow the server rules and nextcord terms of service\nsl_help command to get extended information about the command", color=nextcord.Colour.random())
    em.add_field(name="**Commands**",
                 value="`globalchatstart`, `globalchatstop`")
    await ctx.send(embed=em)

@client.command(aliases=['8ball'])
async def _8ball(ctx,*,args=None):
    if args is None:
        await ctx.send("Duh! Give me a question!\nHaving Trouble? Try 'help [command]")
        return

    responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
             "Don’t count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "My reply is no.", "My sources say no.",
             "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.", "Without a doubt.",
             "Yes.", "Yes – definitely.", "You may rely on it."]

    em = nextcord.Embed(title="**8ball**", description=f"Question: {args}", color=nextcord.Colour.random())
    em.add_field(name="Answer:", value=random.choice(responses), inline=False)
    msg = await ctx.send("<a:Loading:1055429248128651274>")
    time.sleep(2)
    await msg.edit(embed=em)

@client.command(aliases=["with"])
async def withdraw(ctx, amount=None):
    await open_account(ctx.author)



    if amount == None:
        await ctx.send("Please enter **XP** to withdraw")
        return
    user = ctx.author
    users = await get_bank_data()
    b_amt = users[str(user.id)]["Bank"]
    if amount == "all":
        await update_bank(ctx.author, b_amt)
        await update_bank(ctx.author, -1 * b_amt, "Bank")
        await ctx.send(f"Withdrew {b_amt}xp from your bank!!!")
        return


    bal = await update_bank(ctx.author)
    amount = int(amount)

    if amount > b_amt:
        await ctx.send("BRUH You dont have that much **XP**")
        return
    if amount < 0:
        await ctx.send("Umm I think you are kind of dumb")
        return
    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -1 * amount, "Bank")

    await ctx.send(f"Eyyy, you took away {amount} **XP** from your bank")


@client.command(aliases=["dep"])
async def deposit(ctx, amount=None):
    await open_account(ctx.author)

    user = ctx.author
    users = await get_bank_data()
    p_amt = users[str(user.id)]["Pocket"]

    if amount == None:
        await ctx.send("Please enter **XP** to withdraw")
        return

    if amount == "all":
        await update_bank(ctx.author, -1 * p_amt)
        await update_bank(ctx.author, p_amt, "Bank")
        await ctx.send(f"Added {p_amt}xp to your bank!!!")
        return
    bal = await update_bank(ctx.author)
    amount = int(amount)

    if amount > p_amt:
        await ctx.send("BRUH You dont have that much **XP**")
        return
    if amount < 0:
        await ctx.send("Umm I think you are kind of dumb")
        return
    await update_bank(ctx.author, -1 * amount)
    await update_bank(ctx.author, amount, "Bank")

    await ctx.send(f"Eyyy, you added {amount} **XP** to your bank")


async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["Pocket"] = 0
        users[str(user.id)]["Bank"] = 0

    with open("mainbank.json", 'w') as f:
        json.dump(users, f)
    return True


async def get_bank_data():
    with open("mainbank.json", 'r') as f:
        users = json.load(f)

    return users


async def update_bank(user, change=0, mode="Pocket"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json", 'w') as f:
        json.dump(users, f)

    bal = [users[str(user.id)]["Pocket"], users[str(user.id)]["Bank"]]

    return bal


mainshop = [{"name": "magicstick", "price": 500, "description": "mAGiC, collectable"},
            {"name": "phone", "price": 1999, "description": "call your friend to ask for some xp, collectable"},
            {"name": "laptop", "price": 29999, "description": "a biscuit made of xp so worth it, collectable"},
            {"name": "farm", "price": 400000, "description": "oh freak an ancient xp farm, collectable"},
            {"name": "VIP", "price": 400000120,
             "description": "You will become a vip, buy it and flex it, collectable"},
            {"name": "VIP+", "price": 100000000009870, "description": "VIP+ OMG a vip+ you will become vip+ OMGG, collectable"},
            {"name": "cookie", "price": 2500, "description": "Eat it and be a cookie man, collectable"},
            {"name": "pizza", "price": 15000, "description": "A tasty pizza!, collectable"},
            {"name": "rod", "price": 15000, "description": "Can be used to fish, useable"}]

@client.command()
async def give(ctx, member: nextcord.Member, amount=None):
    await open_account(ctx.author)
    await open_account(member)

    amount = int(amount)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    if amount == bal[1]:
        await ctx.send("You don't have that much money in your bank!")
        return

    if amount <= 0:
        await ctx.send("Amount must be positive")
        return

    await update_bank(ctx.author, -1 * amount, "Pocket")
    await update_bank(member, 1 * amount, "Pocket")

    emb = nextcord.Embed(description=f"You gave {member.name} {amount} XP!!!", color=0x2ecc71)
    await ctx.send(embed=emb)

@client.command()
async def rob(ctx, member: nextcord.Member == None):
    memeber = member
    if memeber ==  None or memeber == ctx.author:
        await ctx.send("Ok you robbed yourself")
        return
    await open_account(ctx.author)
    await open_account(memeber)

    bal = await update_bank(memeber)
    try:
        if bal[0] < 100:
            await ctx.send("LOL! the victim doesnt have atleast 100 xp in their pocket not worth it")
            return

        chances = random.randint(1, 100)
        if chances < 40:
            await ctx.send("You dont have skils do rob a person lmfao you were caught")
            return

        
        earnings = random.randint(100, bal[0])

        
        
        

        await update_bank(ctx.author, earnings)
        await update_bank(memeber, -1 * earnings)
        
        
        await ctx.send(f"You robbed {memeber}and got {earnings} coins, woosh that was preety close ngl")
    except Exception as e:
        await ctx.send(e)


@client.command(aliases = ["lb"])
async def leaderboard(ctx,x = 1):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["Pocket"] + users[user]["Bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)    

    em = nextcord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = nextcord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)

@client.command()
@commands.cooldown(1, 10, BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)

    user = ctx.author
    users = await get_bank_data()

    earnings = random.randrange(88)
    rare = [None, None, None, None, None, None, None, "cookie", None, None, None, "pizza"]

    users[str(user.id)]["Pocket"] += earnings

    option = [f'A dog came to you and gave you {earnings} Woof Woof!',
              f'A spider came and burned in daylight giving you {earnings} XP',
              f'God gave you {earnings} XP...',
              f'A zombie came and burned in day light giving you {earnings} xp',
              f'A spider came but it was night and he killed you still you got {earnings} xp',
              f'MR.Beast gave you {earnings} XP how lucky',
              f'Steve wasnt happy still he gave you {earnings} xp']

    em = nextcord.Embed(title="You Begged! i didn't expected that from you", colour=nextcord.Colour.random())
    em.add_field(name="Result:", value=f"{random.choice(option)}")

    await ctx.send(embed=em)

    with open("mainbank.json", 'w') as f:
        json.dump(users, f)

    rrr = random.choice(rare)

@client.command(pass_context=True)
async def slots(ctx, amount=None):
    if amount == None:
        await ctx.send("Please enter an amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount == bal[0]:
        await ctx.send("You don't have that much money!")
        return
    if amount < 0:
        await ctx.send("Amount must be positive")
        return

    slots = ['bus', 'train', 'horse', 'tiger', 'monkey', 'cow']
    slot1 = slots[random.randint(0, 5)]
    slot2 = slots[random.randint(0, 5)]
    slot3 = slots[random.randint(0, 5)]

    slotOutput = '| :{}: | :{}: | :{}: |\n'.format(slot1, slot2, slot3)

    ok = nextcord.Embed(title="Slots Machine", color=nextcord.Color(0xFFEC))
    ok.add_field(name="{}\nWon".format(slotOutput), value=f'You won {2 * amount} xp')

    won = nextcord.Embed(title="Slots Machine", color=nextcord.Color(0xFFEC))
    won.add_field(name="{}\nWon".format(slotOutput), value=f'You won {3 * amount} xp')

    lost = nextcord.Embed(title="Slots Machine", color=nextcord.Color(0xFFEC))
    lost.add_field(name="{}\nLost".format(slotOutput), value=f'You lost {1 * amount} xp')

    if slot1 == slot2 == slot3:
        await update_bank(ctx.author, 3 * amount)
        await ctx.send(embed=won)
        return

    if slot1 == slot2:
        await update_bank(ctx.author, 2 * amount)
        await ctx.send(embed=ok)
        return

    else:
        await update_bank(ctx.author, -1 * amount)
        await ctx.send(embed=lost)
        return

@client.command()
@commands.cooldown(1, 86400, BucketType.user)
async def daily(ctx):
    await open_account(ctx.author)

    user = ctx.author
    users = await get_bank_data()

    earnings = random.randrange(5000, 15000)

    users[str(user.id)]["Pocket"] += earnings

    await ctx.send(f"You have claimed {earnings} xp from your daily reward!")

    with open("mainbank.json", 'w') as f:
        json.dump(users, f)




async def use_this(user, item_name, amount, price=None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price == None:
                ern = random.randrange(999)
            break

    if name_ == None:
        return [False, 1]

    cost = ern

    users = await get_bank_data()

    bal = await update_bank(user)

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:

                new_amt = amount
                if new_amt < 0:
                    return [False, 2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            return [False, 3]
    except:
        return [False, 3]

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, cost, "Pocket")

    return [True, "Worked"]

@client.command()
@commands.cooldown(1, 500, BucketType.user)
async def fish(ctx, item="rod", amount=1):
    
    await open_account(ctx.author)
    res = await use_this(ctx.author, item, amount)

    if not res[0]:
        if res[1] == 1:
            await ctx.send("That object doesnt even exist LOL")
            return
        if res[1] == 2:
            await ctx.send(f"You don't have  {item} in your bag.")
            return
        if res[1] == 3:
            await ctx.send(f"You don't have {item} in your bag.")
            return

    y = random.randrange(1,100)
    x = 2
    if y < 90:

        try:
                        
            with open(f'databases/{ctx.author.id}.txt', 'a+') as f:
                if "Fisher" in open(f'databases/{ctx.author.id}.txt').read():
                    print('rrr')
                    return
                else:  
                    await ctx.send(achi("Fisher", " "))
                    f.write(f"<:ping_carl:884492147187941376> Fisher\n")
                        #await ctx.send(achi("Big", "PP"))

        except Exception as e:
                print(e)
    
    await ctx.send(f"You sold your fish, and got some money!")


@client.command()
async def shop(ctx):
    em = nextcord.Embed(title="Shop", colour=nextcord.Colour.random())

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name=name, value=f"${price} | {desc}", inline=False)

    await ctx.send(embed=em)




@client.command()
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []

    em = nextcord.Embed(title="Bag")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name=name, value=amount)

    await ctx.send(embed=em)


@client.command()
async def flex(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []

    em = nextcord.Embed(title="FLEX!", description=f"{ctx.author.mention} flexs with their bag items")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name=name, value=amount)

    await ctx.send(embed=em)


async def buy_this(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False, 1]

    cost = price * amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0] < cost:
        return [False, 2]

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item": item_name, "amount": amount}
        users[str(user.id)]["bag"] = [obj]

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, cost * -1, "Pocket")

    return [True, "Worked"]


@client.command()
async def sell(ctx, item, amount=1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author, item, amount)

    if not res[0]:
        if res[1] == 1:
            await ctx.send("That Object isn't there!")
            return
        if res[1] == 2:
            await ctx.send(f"You don't have {amount} {item} in your bag.")
            return
        if res[1] == 3:
            await ctx.send(f"You don't have {item} in your bag.")
            return

    await ctx.send(f"You just sold {amount} {item}.")


async def sell_this(user, item_name, amount, price=None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price == None:
                price = 0.9 * item["price"]
            break

    if name_ == None:
        return [False, 1]

    cost = price * amount

    users = await get_bank_data()

    bal = await update_bank(user)

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False, 2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            return [False, 3]
    except:
        return [False, 3]

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, cost, "Pocket")

    return [True, "Worked"]


# Pocket
# XP Bank

@client.command()
@commands.cooldown(1, 20, BucketType.user)
async def search(ctx):
    await open_account(ctx.author)

    user = ctx.author
    users = await get_bank_data()

    earningss = random.randrange(560)

    users[str(user.id)]["Pocket"] += earningss

    options = [f"You searched under a car and got {earningss} XP WOW",
               f"You searched inside your sofa and got {earningss} **XP**!",
               f"Idk but anyhow you got {earningss} **XP**",
               f"You searched in your kidney and got {earningss} **XP**"]

    em = nextcord.Embed(title="You became a detective and searched", colour=nextcord.Colour.random())
    em.add_field(name="Result:", value=f"{random.choice(options)}")

    await ctx.send(embed=em)

    with open("mainbank.json", 'w') as f:
        json.dump(users, f)

@client.command()
async def buy(ctx, item, amount=1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author, item, amount)

    if not res[0]:
        if res[1] == 1:
            await ctx.send("That Object isn't there!")
            return
        if res[1] == 2:
            await ctx.send(f"You don't have enough **XP** in your Pocket to buy {amount} {item}")
            return

    await ctx.send(f"You just bought {amount} {item}")


@client.command(aliases=["bal"])
async def balance(ctx, member: nextcord.Member = None):
    if member == None:
        member = ctx.author

    await open_account(ctx.author)

    user = member
    users = await get_bank_data()

    xp_p_amt = users[str(user.id)]["Pocket"]
    xp_b_amt = users[str(user.id)]["Bank"]

    em = nextcord.Embed(title=f"{user}'s Balance", colour=nextcord.Colour.green())

    em.add_field(name="Pocket XP", value=xp_p_amt)
    em.add_field(name="Bank XP", value=xp_b_amt)
    await ctx.send(embed=em)


@client.command()
@commands.cooldown(1, 300, BucketType.user)
async def work(ctx):
    await open_account(ctx.author)

    user = ctx.author
    users = await get_bank_data()

    earnings = random.randrange(500, 4000)

    users[str(user.id)]["Pocket"] += earnings

    option = [f'You worked at dominoes for a day and got {earnings} xp, but you were kicked out',
              f'You fixed the tire of your car and got {earnings} XP',
              f'You worked at the railway station and got {earnings} XP... You sat on a train and lost your home..',
              f"You cleaned a stranger's shoe and they gave you {earnings} xp",
              f'You cleaned your room and got {earnings} xp',
              f'Mr. Beast gave you {earnings} XP, how lucky',
              f'You worked at a gas station and got {earnings}!']

    em = nextcord.Embed(title="You worked!", colour=nextcord.Colour.random())
    em.add_field(name="Result:", value=f"{random.choice(option)}")

    await ctx.send(embed=em)

    with open("mainbank.json", 'w') as f:
        json.dump(users, f)


@client.command(aliases=['gif'], pass_context=True)
async def giphy(ctx, *, search):
    embed = nextcord.Embed(colour=nextcord.Colour.blue())
    session = aiohttp.ClientSession()

    if search == '':
        response = await session.get('https://api.giphy.com/v1/gifs/random?api_key=xWKaCRgTzEc0bZPhTlzvGoPSSTdS4tIZ')
        data = json.loads(await response.text())
        embed.set_image(url=data['data']['images']['original']['url'])
    else:
        search.replace(' ', '+')
        response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=xWKaCRgTzEc0bZPhTlzvGoPSSTdS4tIZ&limit=10&rating=g')
        data = json.loads(await response.text())
        gif_choice = random.randint(0, 9)
        embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])

    await session.close()

    await ctx.send(embed=embed)

@client.command(aliases=['lmaoa'], pass_context=True)
async def nsfw(ctx, *, search):
    if ctx.author.id == 761614035908034570:
        embed = nextcord.Embed(colour=nextcord.Colour.blue())
        session = aiohttp.ClientSession()

        if search == '':
            response = await session.get('https://api.giphy.com/v1/gifs/random?api_key=xWKaCRgTzEc0bZPhTlzvGoPSSTdS4tIZ')
            data = json.loads(await response.text())
            embed.set_image(url=data['data']['images']['original']['url'])
        else:
            search.replace(' ', '+')
            response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=xWKaCRgTzEc0bZPhTlzvGoPSSTdS4tIZ&limit=10')
            data = json.loads(await response.text())
            gif_choice = random.randint(0, 9)
            embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])

        await session.close()

        await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, sec: int=None):
    if sec == None:
        await ctx.send("There is already a 0s delay to this channel!!")
        return

    await ctx.channel.edit(slowmode_delay=sec)
    em = nextcord.Embed(description=f"Added {sec}s delay to this channel")
    await ctx.send(embed=em)

@client.command()
@commands.has_permissions(manage_channels=True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def lock(ctx, channel: nextcord.TextChannel = None, role: nextcord.Role = None):
    if role is None:
        em = nextcord.Embed(description=f"Since you did not mention a role! Locking this channel for the default role", color=nextcord.Colour.random())
        await ctx.send(embed = em)
        role = ctx.guild.default_role
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(role)
    overwrite.send_messages = False
    await channel.set_permissions(role, overwrite=overwrite)
    em = nextcord.Embed(description=f"Channel locked!", color=nextcord.Colour.green())
    await ctx.send(embed=em)

@client.command()
@commands.has_permissions(manage_channels=True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def unlock(ctx, channel: nextcord.TextChannel = None, role: nextcord.Role = None):
    if role is None:
        em = nextcord.Embed(description=f"Since you did not mention a role! Unlocking this channel for the default role", color=nextcord.Colour.random())
        await ctx.send(embed = em)
        role = ctx.guild.default_role
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(role)
    overwrite.send_messages = True
    await channel.set_permissions(role, overwrite=overwrite)
    em = nextcord.Embed(description=f"Channel unlocked!", color=nextcord.Colour.green())
    await ctx.send(embed=em)

@client.event
async def on_command_error(ctx, error):
    try:
        if isinstance(error, commands.CheckFailure):
            cfem = nextcord.Embed(title="Error!", description="You can't do that!, you don't have the permission to do that\nHaving trouble? Try `sl_help [command name]`", color= 0xFF0000, timestamp=ctx.message.created_at)
            cfem.set_footer(text=error)
            await ctx.send(embed=cfem)
        elif isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'You need the **{}** permission(s) to use this command.'.format(fmt)
            await ctx.send(_message)
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            em = nextcord.Embed(title="Error!", description="Please provide all the required arguments\nHaving trouble? Try `sl_help [command name]`", color= 0xFF0000, timestamp=ctx.message.created_at)
            em.set_footer(text=error)
            await ctx.send(embed=em)
        elif isinstance(error, commands.BadArgument):
            em = nextcord.Embed(title="Error!", description="Please provide a valid argument\nHaving trouble? Try `sl_help [command name]`", color= 0xFF0000, timestamp=ctx.message.created_at)
            em.set_footer(text=error)
            await ctx.send(embed=em)
        elif isinstance(error, commands.BotMissingPermissions):
            mpem = nextcord.Embed(title="Error!", description="I don't have the permission to do that!\nHaving trouble? Try `sl_help [command name]`", color= 0xFF0000, timestamp=ctx.message.created_at)
            em.set_footer(text=error)
            await ctx.send(embed=mpem)
            print("bmp")
        elif isinstance(error, commands.MissingRole):
            mpem = nextcord.Embed(title="Error!", description="You don't have the role required to do that!\nHaving trouble? Try `sl_help [command name]`", color= 0xFF0000, timestamp=ctx.message.created_at)
            mpem.set_footer(text=error)
            await ctx.send(embed=mpem)
        elif isinstance(error, commands.CommandOnCooldown):
            mpem = nextcord.Embed(title="Error!", description="The command is on cooldown\nHaving trouble? Try `sl_help [command name]`", color= 0xFF0000, timestamp=ctx.message.created_at)
            mpem.set_footer(text=error)
            await ctx.send(embed=mpem)
        else:
            mpem = nextcord.Embed(title="Error!", description=" Try ` sl_help [command name]`", color= 0xFF0000, timestamp=ctx.message.created_at)
            mpem.set_footer(text=error)
            await ctx.send(embed=mpem)

    except nextcord.Forbidden:
        raise commands.BotMissingPermissions()


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run("MTA1NDcxOTE0NjMwNDIyNTI4NQ.GOzF5B.L4GqxJZlxOmjzuPTYD9rb_0bUS8fPy6GBct3as")
