import discord


commands_list = 'fkdr: fkdr of bedwars\nbedwars: Bedwars Stats\nskywars: Skywars Stats\nbridge: Bridge Stats\nplayer:'\
' Hypixel Stats\nskilllvl: Skill Level in Skyblock\nskillav: Skill Average in Skyblock\nslayer: Slayer level in Skyblock\n'\
'dungeon: Dungeon Stats in Skyblock\nbalance: The amount of money in your purse + bank\nhelp: Displayed this\n'


def config_help_message():
  embed = discord.Embed(
    title = 'Config Help',
    colour = discord.Colour.blue()
  )
  embed.add_field(name='Add role (to see tickets)', value='Usage: %ticket addrole <role ID>\nExample: %ticket addrole 834835390795218944', inline=False)
  embed.add_field(name='Add role Config (to use config commands and the above)', value='Usage: %ticket addrole config <role ID>\n'\
  'Example: %ticket addrole config 834835390795218944', inline=False)
  embed.add_field(name='Delete role (to see ticket)', value='Usage: %ticket deleterole <role ID>\nExample: %ticket deleterole 834835390795218944', inline=False)
  embed.add_field(name='Delete role Config (to use config commands)', value='Usage: %ticket deleterole config <role ID>\n'\
  'Example: %ticket deleterole config 834835390795218944', inline=False)
  embed.add_field(name='Config the channel where tickets can be created.', value='Usage: %ticket config channel <channel ID>\n'\
  'Example: %ticket config channel 838833852810002492', inline=False)
  embed.add_field(name='Config the locaiton of where tickets are created. (category)', value='Useage: %ticket config category <category ID>\n Example: %ticket config category 840207741636050996', inline=False)
  embed.add_field(name='Restart, WARNING: might break the ticket system', value='%ticket config restart (required admin perms)')
  embed.add_field(name='Help', value='Show this message', inline=False)
  embed.set_footer(text='Created by ThatBananaKing')
  return embed


def ticket_help_message():
  embed = discord.Embed(
      title = 'Ticket',
      colour = discord.Colour.blue()
    )
  embed.add_field(name='Commands:', value='%ticket create <type>\n%ticket delete\n%ticket rename <name>\n%ticket verifyweight <ign>', inline=False)
  embed.add_field(name='Type:', value='guild app\nstaff app\ncommittee app\nhelp', inline=False)
  embed.add_field(name='Config', value='Required: See %ticket perms\nUsage: %ticket config <*args>')
  embed.set_footer(text='Created by ThatBananaKing')
  return embed


def command_help_message():
  embed = discord.Embed(
    title = 'Help',
    colour = discord.Colour.blue()
  )
  embed.set_footer(text='Created by ThatBananaKing')
  embed.add_field(name='IMPORTANT:', value='Commands are case-sensitive\nPlease type in lower case\n\n', inline=False)
  embed.add_field(name='Available Commands: ', value=commands_list, inline=False)
  embed.add_field(name='Usage:', value='Prefix: %\nHow to use:\n<prefix><command> <name> \nExample: %bedwars thatbananaking\n')
  return embed


def ticket_setup_guide():
  embed = discord.Embed(
    title = 'Setup Guide',
    colour = discord.Colour.blue()
  )
  embed.add_field(name='Note:', value='Please be careful with entering ID(s), you will break the ticket system should you enter an invalid ID. In that case, please do %ticket config restart (required admin).')
  embed.add_field(name='#1 Set the role(s) that can config ticket', value='%ticket addrole config <role ID>', inline=False)
  embed.add_field(name='#2 Set the role(s) that can see tickets', value='%ticket addrole <role ID>', inline=False)
  embed.add_field(name='#3 Set the location of where tickets will be created', value='%ticket config category <category ID>', inline=False)
  embed.add_field(name='#4 Set the channel to allow users to create tickets', value='%ticket config channel <channel ID>', inline=False)
  embed.set_footer(text='Created by ThatBananaKing')
  return embed