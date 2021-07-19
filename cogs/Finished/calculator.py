import discord
from discord.ext import commands
import math
import datetime
import mpmath

def ErrorEmbed(title,reason):
  embed = discord.Embed(
      title = title,
      description = reason,
      color = discord.Color.red(),
      timestamp = datetime.datetime.utcnow()
    )
  embed.set_author(name = "Error")
  return embed

def ee(title,reason):
  embed = discord.Embed(
      title = title,
      description = reason,
      color = discord.Color.red(),
      timestamp = datetime.datetime.utcnow()
    )
  embed.set_author(name = "Error")
  return embed

class Calculator(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.group(invoke_without_command=True, aliases = ["maths"])
  async def math(self, ctx):
    embed = discord.Embed(title="Math Commands: ", name="`add <a> <b>` `subtract <a> <b>` `multiply <a> <b>` `divide <a><b>` `remainder <a> <b>` `power <a> <b>` `factorial <a>` `ceiling <a>` `floor <a>` `floordivision <a>` `squareroot <a>` `exponent <a>` `round <a>` `modulus <a>` `sin <a>` `cos <a>` `tan <a>` `cot <a>` `secant <a>` `cosecant <a>` `asine <a>` `acosine <a>` `atangent <a>` `acotangent <a>` `asecant <a>` `acosecant <a>` `sineh <a>` `cosineh <a>` `tangenth <a>` `asineh <a>` `acosineh <a>` `atangenth <a>` `pi` `e` `tau` `infinity` `nan`")
    await ctx.send(embed=embed)
      
  @math.command(aliases = ['addition', 'sum'])
  async def add(self, ctx, a = None, b = None):
    """Add two numbers together."""
    
    if a == None or b == None:
      embed = ee("Missing Command Arguments", "You need to specify two numbers to add.")
      await ctx.send(embed = embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ee("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return

      try:
        b = int(b)
      except:
        try:
          b = float(b)
        except:
          embed = ee("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return

      embed = discord.Embed(
        title = f"{a} + {b}",
        description = f"= {a + b}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)
      await msg.add_reaction("➕")

  @math.command(aliases = ['subtract', 'difference', 'diff', 'subtraction'])
  async def sub(self, ctx, a = None, b = None):
    """Subtract two numbers."""
    
    if a == None or b == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify two numbers to subtract.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      try:
        b = int(b)
      except:
        try:
          b = float(b)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"{a} - {b}",
        description = f"= {a - b}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)
      await msg.add_reaction("➖")

  @math.command(aliases = ['multiply', 'multiplication', 'product', 'multi'])
  async def mult(self, ctx, a = None, b = None):
    """Multiply two numbers together."""
    
    if a == None or b == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify two numbers to multiply.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      try:
        b = int(b)
      except:
        try:
          b = float(b)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"{a} x {b}",
        description = f"= {a * b}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)
      await msg.add_reaction("✖️")

  @math.command(aliases = ['divide', 'quo', 'quot', 'quotient'])
  async def div(self, ctx, a = None, b = None):
    """Divide two numbers."""
    
    if a == None or b == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify two numbers to divide.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      try:
        b = int(b)
      except:
        try:
          b = float(b)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"{a} / {b}",
        description = f"= {a / b}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)
      await msg.add_reaction("➗")

  @math.command(aliases = ['ceiling'])
  async def ceil(self, ctx, a = None):
    """Round a number up."""
    
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to ceiling.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"ceil({a})",
        description = f"= {math.ceil(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)

  @math.command()
  async def floor(self, ctx, a : int = None):
    """Round a number down."""
    
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to floor.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"floor({a})",
        description = f"= {math.floor(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)

  @math.command(aliases=['fd', 'floordivision'])
  async def floordiv(self, ctx, a = None, b = None):
    """Floor divide two numbers."""
    
    if a == None or b == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify two number to floor divide.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      try:
        b = int(b)
      except:
        try:
          b = float(b)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"{a} // {b}",
        description = f"= {a // b}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)
      await msg.add_reaction("➗")

  @math.command(aliases=['sr', 'squareroot'])
  async def sqrt(self, ctx, a = None):
    """Square root a number."""
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to square root.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"√{a}",
        description = f"= {math.sqrt(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)
      await msg.add_reaction("√")

  @math.command(aliases=['pow', 'exp', 'exponent'])
  async def power(self, ctx, a = None, b = None):
    """Raise a number to a power."""
    
    if a == None or b == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify two numbers; one to raise the other to. (ex. 2^6)")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      try:
        b = int(b)
      except:
        try:
          b = float(b)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"{a}^{b}",
        description = f"= {a ** b}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)

  @math.command(aliases=['rnd'])
  async def round(self, ctx, a = None):
    """Raise a number to a power."""
  
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to round.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"round({a})",
        description = f"= {round(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)

  @math.command(aliases=['fac'])
  async def factorial(self, ctx, a = None):
    """Perform the factorial function on a number."""
  
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to factorial.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"{a}!",
        description = f"= {math.factorial(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)

  @math.command(aliases=['mod'])
  async def modulus(self, ctx, a = None, b = None):
    """Find the modulus of two numbers."""
    
    if a == None or b == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify two numbers to modulus.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      try:
        b = int(b)
      except:
        try:
          b = float(b)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"{a} % {b}",
        description = f"= {a % b}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)

  @math.command(aliases=['sine'])
  async def sin(self, ctx, a = None):
    """Perform the sine function on a number."""
  
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to sine.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"sin({a})",
        description = f"= {mpmath.sin(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)

  @math.command(aliases=['cosine'])
  async def cos(self, ctx, a = None):
    """Perform the cosine function on a number."""
  
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to cosine.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"cos({a})",
        description = f"= {mpmath.cos(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)

  @math.command(aliases=['tangent'])
  async def tan(self, ctx, a = None):
    """Perform the tangent function on a number."""
  
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to tangent.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"tan({a})",
        description = f"= {mpmath.tan(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)

  @math.command(aliases=['cotangent'])
  async def cot(self, ctx, a = None):
    """Perform the cotangent function on a number."""
  
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to cotangent.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"cot({a})",
        description = f"= {mpmath.cot(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)

  @math.command(aliases=['secant'])
  async def sec(self, ctx, a = None):
    """Perform the secant function on a number."""
  
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to secant.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"sec({a})",
        description = f"= {mpmath.sec(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)

  @math.command(aliases=['cosecant', 'csc'])
  async def cosec(self, ctx, a = None):
    """Perform the cosecant function on a number."""
  
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to cosecant.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"csc({a})",
        description = f"= {mpmath.csc(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)


  @math.command(aliases=['asine'])
  async def asin(self, ctx, a = None):
    """Perform the asine function on a number."""
  
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to asine.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"asin({a})",
        description = f"= {mpmath.asin(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)

  @math.command(aliases=['acosine'])
  async def acos(self, ctx, a = None):
    """Perform the acosine function on a number."""
  
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to acosine.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"acos({a})",
        description = f"= {mpmath.acos(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)

  @math.command(aliases=['atangent'])
  async def atan(self, ctx, a = None):
    """Perform the atangent function on a number."""
  
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to atangent.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"atan({a})",
        description = f"= {mpmath.atan(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)

  @math.command(aliases=['acotangent'])
  async def acot(self, ctx, a = None):
    """Perform the acotangent function on a number."""
  
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to acotangent.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"acot({a})",
        description = f"= {mpmath.acot(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)

  @math.command(aliases=['asecant'])
  async def asec(self, ctx, a = None):
    """Perform the asecant function on a number."""
  
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to asecant.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"asec({a})",
        description = f"= {mpmath.asec(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)

  @math.command(aliases=['acosecant', 'acsc'])
  async def acosec(self, ctx, a = None):
    """Perform the cosecant function on a number."""
  
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to acosecant.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"acsc({a})",
        description = f"= {mpmath.acsc(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)


  ####################3
  
  @math.command(aliases=['sineh'])
  async def sinh(self, ctx, a = None):
    """Perform the sineh function on a number."""
  
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to sineh.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"sinh({a})",
        description = f"= {math.sinh(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)

  @math.command(aliases=['cosineh'])
  async def cosh(self, ctx, a = None):
    """Perform the cosineh function on a number."""
  
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to cosineh.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"cosh({a})",
        description = f"= {math.cosh(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)

  @math.command(aliases=['tangenth'])
  async def tanh(self, ctx, a = None):
    """Perform the tangent function on a number."""
  
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to tangenth.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"tanh({a})",
        description = f"= {math.tanh(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)

  @math.command(aliases=['asineh'])
  async def asinh(self, ctx, a = None):
    """Perform the asineh function on a number."""
  
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to asineh.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"asineh({a})",
        description = f"= {math.asinh(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)

  @math.command(aliases=['acosineh'])
  async def acosh(self, ctx, a = None):
    """Perform the acosineh function on a number."""
  
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to acosineh.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"acosh({a})",
        description = f"= {math.acosh(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)

  @math.command(aliases=['atangenth'])
  async def atanh(self, ctx, a = None):
    """Perform the atangenth function on a number."""
  
    if a == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to specify a number to atangenth.")
      await ctx.send(embed=embed)
    else:
      try:
        a = int(a)
      except:
        try:
          a = float(a)
        except:
          embed = ErrorEmbed.error("Invalid Command Arguments", "Make sure your numbers are either floats or integers.")
          await ctx.send(embed=embed)
          return
      embed = discord.Embed(
        title = f"atanh({a})",
        description = f"= {mpmath.atanh(a)}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)

  @math.command()
  async def pi(self, ctx):
    """Get the constant pi."""
    embed = discord.Embed(
      title = "Pi",
      description = math.pi,
      color = 0x5f10a3,
      timestamp = datetime.datetime.utcnow()
    )
    await ctx.send(embed=embed)

  @math.command()
  async def e(self, ctx):
    """Get the constant e."""
    embed = discord.Embed(
      title = "Euler's Constant",
      description = math.e,
      color = 0x5f10a3,
      timestamp = datetime.datetime.utcnow()
    )
    await ctx.send(embed=embed)

  @math.command()
  async def tau(self, ctx):
    """Get the constant tau."""
    embed = discord.Embed(
      title = "Tau",
      description = math.tau,
      color = 0x5f10a3,
      timestamp = datetime.datetime.utcnow()
    )
    await ctx.send(embed=embed)

  @math.command(aliases=['infinity'])
  async def inf(self, ctx):
    """Get the constant Infinity, or NaN."""
    embed = discord.Embed(
      title = "Infinity",
      description = math.inf,
      color = 0x5f10a3,
      timestamp = datetime.datetime.utcnow()
    )
    await ctx.send(embed=embed)

  @math.command()
  async def nan(self, ctx):
    """Get the constant pi."""
    embed = discord.Embed(
      title = "NaN",
      description = math.nan,
      color = 0x5f10a3,
      timestamp = datetime.datetime.utcnow()
    )
    await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Calculator(client))