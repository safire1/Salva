import asyncio, random
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import clean_content

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ship(self, ctx, name1: clean_content, name2: clean_content):
        shipnumber = random.randint(0, 100)
        if name1 == "@//Fire" and name2 == "@miyah chan" or name1 == "@miyah chan" and name2 == "@//Fire":
            shipnumber = 100
	
 	
		
            
        if 0 <= shipnumber <= 10:
            status = "Really low! {}".format(random.choice(["Friendzone ;(",
                                                            'Just "friends"',
                                                            '"Friends"',
                                                            "Little to no love ;(",
                                                            "There's barely any love ;("]))
        elif 10 < shipnumber <= 20:
            status = "Low! {}".format(random.choice(["Still in the friendzone",
                                                     "Still in that friendzone ;(",
                                                     "There's not a lot of love there... ;("]))
        elif 20 < shipnumber <= 30:
            status = "Poor! {}".format(random.choice(["But there's a small sense of romance from one person!",
                                                      "But there's a small bit of love somewhere",
                                                      "I sense a small bit of love!",
                                                      "But someone has a bit of love for someone..."]))
        elif 30 < shipnumber <= 40:
            status = "Fair! {}".format(random.choice(["There's a bit of love there!",
                                                      "There is a bit of love there...",
                                                      "A small bit of love is in the air..."]))
        elif 40 < shipnumber <= 60:
            status = "Moderate! {}".format(random.choice(["But it's very one-sided OwO",
                                                          "It appears one sided!",
                                                          "There's some potential!",
                                                          "I sense a bit of potential!",
                                                          "There's a bit of romance going on here!",
                                                          "I feel like there's some romance progressing!",
                                                          "The love is getting there..."]))
        elif 60 < shipnumber <= 70:
            status = "Good! {}".format(random.choice(["I feel the romance progressing!",
                                                      "There's some love in the air!",
                                                      "I'm starting to feel some love!"]))
        elif 70 < shipnumber <= 80:
            status = "Great! {}".format(random.choice(["There is definitely love somewhere!",
                                                       "I can see the love is there! Somewhere...",
                                                       "I definitely can see that love is in the air"]))
        elif 80 < shipnumber <= 90:
            status = "Over average! {}".format(random.choice(["Love is in the air!",
                                                              "I can definitely feel the love",
                                                              "I feel the love! There's a sign of a match!",
                                                              "There's a sign of a match!",
                                                              "I sense a match!",
                                                              "A few things can be imporved to make this a match made in heaven!"]))
        elif 90 < shipnumber <= 100:
            status = "True love! {}".format(random.choice(["It's a match!",
                                                           "There's a match made in heaven!",
                                                           "It's definitely a match!",
                                                           "Love is truely in the air!",
                                                           "Love is most definitely in the air!"]))

        if shipnumber <= 33:
            shipColor = 0xE80303
        elif 33 < shipnumber < 66:
            shipColor = 0xff6600
        else:
            shipColor = 0x3be801

        emb = (nextcord.Embed(color=shipColor, \
                             title="Love test for:", \
                             description="**{0}** and **{1}** {2}".format(name1, name2, random.choice([
                                 ":sparkling_heart:",
                                 ":heart_decoration:",
                                 ":heart_exclamation:",
                                 ":heartbeat:",
                                 ":heartpulse:",
                                 ":hearts:",
                                 ":blue_heart:",
                                 ":green_heart:",
                                 ":purple_heart:",
                                 ":revolving_hearts:",
                                 ":yellow_heart:",
                                 ":two_hearts:"]))))
        emb.add_field(name="Results:", value=f"{shipnumber}%", inline=True)
        emb.add_field(name="Status:", value=(status), inline=False)
        emb.set_author(name="Shipping", icon_url="http://moziru.com/images/kopel-clipart-heart-6.png")
        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Fun(bot))