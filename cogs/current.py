import nextcord, random, operator, json
from nextcord.ext import commands

#with open("vnreports.json") as f:
 #   config = json.load(f)

class WhosPlaying(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command(no_pm=True, aliases=["wp"])
    async def whosplaying(self, ctx, *, game):
        if len(game) <= 1:
            await ctx.send("```The game should be at least 2 characters long...```", delete_after=5.0)
            return

        guild = ctx.message.guild
        members = guild.members
        playing_game = ""
        count_playing = 0

        for member in members:
            if not member:
                continue
            if not member.activity or not member.activity.name:
                continue
            if member.bot:
                continue
            if game.lower() in member.activity.name.lower():
                count_playing += 1
                if count_playing <= 15:
                    emote = random.choice([":trident:", ":high_brightness:", ":low_brightness:", ":beginner:", ":diamond_shape_with_a_dot_inside:"])
                    playing_game += f"{emote} {member.name} ({member.activity.name})\n"

        if playing_game == "":
            await ctx.send("```Search results:\nNo users are currently playing that game.```")
        else:
            msg = playing_game
            if count_playing > 15:
                showing = "(Showing 15/{})".format(count_playing)
            else:
                showing = "({})".format(count_playing)

            em = nextcord.Embed(description=msg, colour= nextcord.Colour.random())
            em.set_author(name=f"""Who's playing "{game}"? {showing}""")
            await ctx.send(embed=em)
    
    @commands.command(no_pm=True, aliases=["cg"])
    async def currentgames(self, ctx):

        guild = ctx.message.guild
        members = guild.members

        freq_list = {}
        for member in members:
            if not member:
                continue
            if not member.activity or not member.activity.name:
                continue
            if member.bot:
                continue
            if member.activity.name not in freq_list:
                freq_list[member.activity.name] = 0
            freq_list[member.activity.name] += 1

        sorted_list = sorted(freq_list.items(),
                             key=operator.itemgetter(1),
                             reverse=True)

        if not freq_list:
            await ctx.send("```Search results:\nNo users are currently playing any games.```")
        else:
            msg = ""
            max_games = min(len(sorted_list), 10)

            em = nextcord.Embed(description=msg, colour=nextcord.Colour.random())
            for i in range(max_games):
                game, freq = sorted_list[i]
                if int(freq_list[game]) < 2:
                    amount = "1 person"
                else:
                    amount = f"{int(freq_list[game])} people"
                em.add_field(name=game, value=amount)
            em.set_thumbnail(url=guild.icon)
            em.set_footer(text="Do sl_whosplaying <game> to see whos playing a specific game")
            em.set_author(name="Top games being played right now in the server:")
            await ctx.send(embed=em) 

def setup(bot):
    bot.add_cog(WhosPlaying(bot))