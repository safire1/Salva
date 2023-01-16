from nextcord.ext import commands
from nextcord.ui import Button , View
import nextcord
import datetime


def calculate(exp):
    o = exp.replace('×', '*')
    o = o.replace('÷', '/')
    result = ''
    try:
        result = str(eval(o))
    except:
        result = 'An error occurred.'
    return result

class MyView(nextcord.ui.View):
    def __init__(self,ctx):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.expression = ""
        self.add_item(MyButton(label = "1" , style=nextcord.ButtonStyle.grey , row = 1))
        self.add_item(MyButton(label = "2" , style=nextcord.ButtonStyle.grey , row = 1))
        self.add_item(MyButton(label = "3" ,style = nextcord.ButtonStyle.grey , row = 1))
        self.add_item(MyButton(label = "×" , style = nextcord.ButtonStyle.blurple , row = 1))
        self.add_item(MyButton(label = "Exit" , style = nextcord.ButtonStyle.red , row = 1))
        self.add_item(MyButton(label = "4" , style = nextcord.ButtonStyle.grey , row = 2))
        self.add_item(MyButton(label = "5" , style = nextcord.ButtonStyle.grey , row = 2))
        self.add_item(MyButton(label = "6" , style = nextcord.ButtonStyle.grey , row = 2))
        self.add_item(MyButton(label = "÷" , style = nextcord.ButtonStyle.blurple , row = 2))
        self.add_item(MyButton(label = "←" , style = nextcord.ButtonStyle.red , row = 2))
        self.add_item(MyButton(label = "7" , style = nextcord.ButtonStyle.grey , row = 3))
        self.add_item(MyButton(label = "8" , style = nextcord.ButtonStyle.grey , row = 3))
        self.add_item(MyButton(label = "9" , style = nextcord.ButtonStyle.grey , row = 3))
        self.add_item(MyButton(label = "+" , style = nextcord.ButtonStyle.blurple , row = 3))
        self.add_item(MyButton(label = "C" , style = nextcord.ButtonStyle.red , row = 3))
        self.add_item(MyButton(label = "00" , style = nextcord.ButtonStyle.grey , row = 4))
        self.add_item(MyButton(label = "0" ,style = nextcord.ButtonStyle.grey , row = 4))
        self.add_item(MyButton(label = "." , style = nextcord.ButtonStyle.grey , row = 4))
        self.add_item(MyButton(label = "-" ,style = nextcord.ButtonStyle.blurple , row = 4))
        self.add_item(MyButton(label = "=" , style = nextcord.ButtonStyle.green , row = 4))
    
    async def interaction_check(self, interaction):
       return self.ctx.author == interaction.user

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(embed=nextcord.Embed(description = "__**Timeout , You can't react with the button**__" , color = nextcord.Colour.red()), view=self)

class MyButton(nextcord.ui.Button):
    async def callback(self, interaction : nextcord.Interaction):
        assert self.view is not None
        view: MyView = self.view
        if str(self.label) == "Exit":
            view.clear_items()
        elif view.expression == 'None' or view.expression == 'An error occurred.':
            view.expression = ''
        elif str(self.label) == "←":
            view.expression = view.expression[:-1]
        elif str(self.label) == "C":
            view.expression = ''
        elif str(self.label) == "=":
            view.expression = calculate(view.expression)
        else:
            view.expression += self.label
        
        e = nextcord.Embed(title=f'| {interaction.user.name}\'s calculator | ', description=f"```fix\n{view.expression}```",timestamp=nextcord.utils.utcnow() , color = nextcord.Colour.green())
        await interaction.response.edit_message(view = view, embed=e , content = None)
    

   
class Calculator(commands.Cog, name="buttoncalc"):
    """Calculation Commands"""
    COG_EMOJI = "🧮"
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases= ["buttoncal" , "bcal", "calculator" , "cal"])
    async def calculate(self,ctx):
        view = MyView(ctx)
        m = await ctx.send(content='Loading Calculator...')
        expression = 'None'
        delta = nextcord.utils.utcnow() + datetime.timedelta(minutes=5)
        e = nextcord.Embed(title=f'{ctx.author.name}\'s calculator | {ctx.author.id}', description=expression,timestamp=delta , color = nextcord.Colour.blurple())
        e.set_footer(text = f"The button calculator will be expired in 2 minutes")
        view.message = await m.edit(view = view, embed=e , content = None)

def setup(bot: commands.Bot):
    bot.add_cog(Calculator(bot))