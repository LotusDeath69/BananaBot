import os
from discord.ext import commands 
import discord
from minigames.bedwars import checkBedwarsStats
from minigames.fkdr import checkFKDR
from minigames.bridge import checkBridgeStats
from minigames.murderMystery import getMurderMysteryStats
from skyblock_misc.player import checkStats
from skyblock_misc.friends import getFriends
from skyblock_misc.skyblock import getBalance, getDungeonStats, getSkillAV, getSkillLvl, getSlayer
from skyblock import getSkillAV, getSlayer, getBalance, getSkillLvl, getDungeonStats
from minigames.skywars import getSkywarsStats
from server import keepAlive
from ticket_system import ticket, GuildApp
from message import ticket_help_message, command_help_message, ticket_setup_guide


intents = discord.Intents.default()
intents.members = True
GUILD_REQUIREMENT = 4500
key = os.environ['API']
prefix = '%'
client = commands.Bot(command_prefix=prefix, help_command=None)
todo_list = ['Optional chaining(refer to #dev)',"automatically get stats of player's discord name if no args is provided", 'add patchnotes', 'revamped getDungeonStats', 'make a emote for users to react to open tickets']


def checkRoles(ctx, roles):
  
  for i in list(ctx.author.roles):
    for r in list(roles):
      if i.id == int(r):
        return True
  return False


def createEmbed(ign, title, value):
  embed = discord.Embed(
    title = title,
    colour = discord.Colour.blue()
  )
  embed.add_field(name=ign, value=value)
  embed.set_footer(text='Created by ThatBananaking')
  return embed 


@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Activity(
    type=discord.ActivityType.listening, name=f'%help in {len(client.guilds)} servers'
  ))
  print('logged in')


@client.command()
async def fkdr(ctx, *args):
  if len(args) == 0:
    await ctx.reply('Please enter a name')
  else:
    title = 'FKDR - Bedwars'
    value = checkFKDR(args[0], key)
    await ctx.reply(embed=createEmbed(args[0], title, value))
    

@client.command()
async def prefix(ctx):
  await ctx.reply('Prefix: %')


@client.command()
async def player(ctx, *args):
  if len(args) == 0:
    await ctx.reply('Please enter a name')
  else:
    title = 'Hypixel Stats'
    value = checkStats(args[0], key)
    await ctx.reply(embed=createEmbed(args[0], title, value))


@client.command()
async def bedwars(ctx, *args):
  if len(args) == 0:
    await ctx.reply('Please enter a name')

  else:
    title = 'Bedwars Stats'
    value = checkBedwarsStats(args[0], key)
    await ctx.reply(embed=createEmbed(args[0], title, value))


@client.command()
async def bridge(ctx, *args):
  if len(args) == 0:
    await ctx.reply('Please enter a name')

  else:
    title = 'Bridge Stats'
    value = checkBridgeStats(args[0], key)
    await ctx.reply(embed=createEmbed(args[0], title, value))


@client.command()
async def skillav(ctx, *args):
  if len(args) == 0:
    await ctx.reply('Please enter a name')

  else:
    title = 'Skill Average'
    value = getSkillAV(args[0], key)
    await ctx.reply(embed=createEmbed(args[0], title, value))


@client.command()
async def slayer(ctx, *args):
  if len(args) == 0:
    await ctx.reply('Please enter a name')

  else:
    title = 'Slayer'
    value = getSlayer(args[0], key)
    await ctx.reply(embed=createEmbed(args[0], title, value))


@client.command()
async def dungeon(ctx, *args):
  if len(args) == 0:
    await ctx.reply('Please enter a name')

  else:
    title = 'Dungeon Stats'
    value = getDungeonStats(args[0], key)
    await ctx.reply(embed=createEmbed(args[0], title, value))


@client.command()
async def skilllvl(ctx, *args):
  if len(args) == 0:
    await ctx.reply('Please enter a name')

  else:
    title = 'Skill Level'
    value = getSkillLvl(args[0], key)
    await ctx.reply(embed=createEmbed(args[0], title, value))


@client.command()
async def balance(ctx, *args):
  if len(args) == 0:
    await ctx.reply('Please enter a name')

  else:
    title = 'Net Worth'
    value = getBalance(args[0], key)
    await ctx.reply(embed=createEmbed(args[0], title, value))

@client.command()
async def friends(ctx, *args):
  if len(args) == 0:
    await ctx.reply('Please enter a name.')
  else:
    await ctx.reply(f"{args[0]}'s friends in Lunar Guard: {getFriends(args[0], key)}")

@client.command()
async def skywars(ctx, *args):
  if len(args) == 0:
    await ctx.reply('Please enter a name')

  else:
    title = 'Skywars'
    value = getSkywarsStats(args[0], key)
    await ctx.reply(embed=createEmbed(args[0], title, value))


@client.command()
async def mm(ctx, *args):
  if len(args) == 0:
    await ctx.reply('Please enter a name')
  
  else:
    title = 'Murder Mystery'
    value = getMurderMysteryStats(args[0], key)
    await ctx.reply(embed=createEmbed(args[0], title, value))


@client.command()
async def todo(ctx):
  for i in todo_list:
    await ctx.send(f"-{i}")


@client.command()
async def help(ctx, *args):
  if len(args) == 0:
   await ctx.reply(embed=command_help_message())


@client.group(invoke_without_command=True)
async def ticket(ctx):
  await ctx.reply(embed=ticket_help_message())


@ticket.command()
async def create(ctx, *args):
  arg = ' '.join(args).lower()
  await ticket.createChannel(ctx, client, arg)


@ticket.command()
async def config(ctx, *args):
  try:
    if args[0].lower() == 'category':
      await ticket.configCategory(ctx, args[1])
    elif args[0].lower() == 'channel':
      await ticket.configChannel(ctx, args[1])
    elif args[0].lower() == 'help':
      await ticket.configHelp(ctx)
    elif args[0].lower() == 'restart':
      await ticket.configRestart(ctx, client)
  except IndexError:
    await ticket.configHelp(ctx)


@ticket.command()
async def verifyweight(ctx, arg):
  await ticket.verifyWeight(ctx, arg)


@ticket.command()
async def addrole(ctx, *args):
  if args[0].lower() == 'config':
    await ticket.addTicketConfig(ctx, args[1])
  else:
    await ticket.addTicketSee(ctx, args[0])

  
@ticket.command()
async def deleterole(ctx, *args):
  if args[0].lower() == 'config':
    await ticket.deleteTicketConfig(ctx, args[1])
  else:
    await ticket.deleteTicketSee(ctx, args[0])


@ticket.command()
async def delete(ctx):
  await ticket.deleteChannel(ctx)


@ticket.command()
async def rename(ctx, *args):
  arg = ' '.join(args)
  await ticket.renameChannel(ctx, arg)


@ticket.command()
async def perms(ctx):
  await ticket.ticketPerms(ctx)


@client.command()
async def test(ctx, args):
  pass


@ticket.command()
async def guide(ctx):
  await ctx.reply(embed=ticket_setup_guide())


@ticket.command()
async def adduser(ctx, arg): 
  await ticket.addUser(ctx, arg)
  

@client.command()
async def balls(ctx):
  await ctx.reply(f'{ctx.author.name} has no balls')


@client.command()
async def dababy(ctx):
  await ctx.reply("Let's GOO")


@client.event
async def on_raw_reaction_add(payload):
  if payload.member.bot:
    return
  if str(payload.emoji) == '\U0001F4AF':
    pass


keepAlive()
client.run(os.environ['TOKEN'])
