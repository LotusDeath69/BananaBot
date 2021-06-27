from replit import db
import discord
from ticket_system.GuildApp import guildApp, uuid, checkWeight, applicationInfo, applicationForm
import os 
from ticket_system.message import config_help_message
import asyncio
import requests
from DiscordChatExporterPy.chat_exporter.chat_exporter import quick_export
from dotenv import load_dotenv
key = load_dotenv('API')
GUILD_REQUIREMENT = 4500


def checkRoles(ctx, roles):
  for i in list(ctx.author.roles):
    for r in list(roles):
      if i.id == int(r):
        return True
  return False


async def addTicketSee(ctx, arg):
  guild = ctx.message.guild.id
  try:
    roles_required = db[f'{guild}_ticket_roles_allow_to_config']

    if checkRoles(ctx, roles_required):
      try:
        role_list = db[f'{guild}_ticket_roles_allow_to_see']
        if arg in role_list:
          await ctx.reply(f'{ctx.guild.get_role(int(arg))} role can already see tickets.')
        else: 
          role_list.append(arg)
          db[f'{guild}_ticket_roles_allow_to_see'] = role_list
          await ctx.reply(f'Now users with {ctx.guild.get_role(int(arg))} will be able to see tickets.')


      except KeyError:
        db[f'{guild}_ticket_roles_allow_to_see'] = [arg]
        await ctx.reply(f'Now users with {ctx.guild.get_role(int(arg))} will be able to see tickets.')


    else:
      role_name = []
      for i in list(db[f'{guild}_ticket_roles_allow_to_config']):
        role_name.append(ctx.guild.get_role(int(i)))
      if role_name != []:
        await ctx.reply(f'Roles Required: {str(role_name)} to use this command.')
      else:
        await ctx.reply('You need to do %ticket addrole config <role id> first.')


  except KeyError:
    await ctx.reply('You need to do %ticket addrole config <role id> first.')


async def addTicketConfig(ctx, arg):
  guild = ctx.message.guild.id
  try: 
    roles_required = db[f'{guild}_ticket_roles_allow_to_config']
    if checkRoles(ctx, roles_required):
      role_list = db[f'{guild}_ticket_roles_allow_to_config']
      if arg in role_list:
        await ctx.reply(f'{ctx.guild.get_role(int(arg))} role can already config tickets.')
      else:
        role_list.append(arg)
        db[f'{guild}_ticket_roles_allow_to_config'] = role_list
        await ctx.reply(f'Now users with {ctx.guild.get_role(int(arg))} role will be able to config tickets.')
      

    else:
        role_name = []
        for i in db[f'{guild}_ticket_roles_allow_to_config']:
          role_name.append(ctx.guild.get_role(int(i)))
        if role_name != []:
          await ctx.reply(f'Roles Required: {str(role_name)} to use this command.')
        else:
          if ctx.author.guild_permissions.administrator:
            db[f'{guild}_ticket_roles_allow_to_config'] = [arg]
            await ctx.reply(f'Now users with {ctx.guild.get_role(int(arg))} role will be able to config tickets.')

  except KeyError:
    if ctx.author.guild_permissions.administrator:
      db[f'{guild}_ticket_roles_allow_to_config'] = [arg]
      await ctx.reply(f'Now users with {ctx.guild.get_role(int(arg))} role will be able to config tickets.')

    else:
      await ctx.reply("You don't have permissions to run this command.")


async def ticketOverwrite(ctx):
  guild = ctx.message.guild.id
  num = 0
  overwrites = {
    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
    await ctx.message.guild.fetch_member(ctx.author.id): discord.PermissionOverwrite(read_messages=True)

  }
  try:
    for i in db[f'{guild}_ticket_roles_allow_to_config']:
      overwrites[ctx.guild.get_role(int(i))] = discord.PermissionOverwrite(read_messages=True)
  except KeyError:
    num += 1
  try:
    for i in db[f'{guild}_ticket_roles_allow_to_see']:
      overwrites[ctx.guild.get_role(int(i))] = discord.PermissionOverwrite(read_messages=True)
  except KeyError:
    num += 1
  if num == 2:
    await ctx.reply("Created a public ticket since no one has the perms to see the private channel\n"\
    "If you're the owner, please set up by using %ticket addrole config <role id> (to config) and ticket addrole <role id> (to see)")
    return {}
  return overwrites


async def createChannel(ctx, client, arg):
  guild = ctx.message.guild.id
  try:
    desired_channel_location = db[f'{guild}_ticket_channel_id']
    if str(ctx.message.channel.id) != desired_channel_location:
      await ctx.reply('This is not the right channel to run this command.')
    else:
      try:
        category_id = db[f'{guild}_ticket_category_id']
        category = discord.utils.get(ctx.guild.categories, id=int(category_id))

        try:
          ticket_number = db[f'{guild}_ticket_number']
          db[f'{guild}_ticket_number'] = ticket_number + 1
        except KeyError:
          db[f'{guild}_ticket_number'] = 2
          ticket_number = 1
        channel = await ctx.guild.create_text_channel(f'{arg}-{ticket_number}', overwrites=await ticketOverwrite(ctx), category=category, reason='Created a ticket')
        await channel.edit(topic=f'ChannelType: Ticket, Type: {arg}, Number: {ticket_number}')

        await ctx.reply('Sucessfully created a channel.')
        if arg.lower() == 'guild app':
          await guildApp(ctx, client, channel)
      except KeyError:
        await ctx.reply('You need to do %ticket config category <category ID>')
  except KeyError:
    await ctx.reply('You need to do %ticket config channel <channel ID>')


def preliminaryFailed(weight):
  embed = discord.Embed(
    title = 'Preliminary Failed',
    colour = discord.Colour.blue()
  )
  embed.add_field(name='Reason:', value=f'Your weight ({weight}) does not meet our requirement ({GUILD_REQUIREMENT}).')
  embed.add_field(name="Do not close this ticket.", value="If you're close to our requirement, we might make an exception.")
  embed.set_footer(text='Created by ThatBananaKing')
  return embed

async def verifyWeight(ctx, arg):
  guild = ctx.message.guild.id
  category = db[f'{guild}_ticket_category_name']
  if str(ctx.message.channel.category) == category:
    try:
      weight = checkWeight(uuid(str(arg)), key)
      try: 
        data = requests.get(f'https://api.hypixel.net/player?uuid={uuid(str(arg))}&key={key}').json()
        mc_discord_username = data['player']['socialMedia']['links']['DISCORD']
        discord_name = ctx.author.name + '#' + ctx.author.discriminator
        if str(discord_name) != str(mc_discord_username):
          await ctx.reply(f'Your minecraft account seems to be verified to a different discord name: {mc_discord_username}\nPlease check!')
        if weight >= GUILD_REQUIREMENT:
          await ctx.reply(f'Your weight from the account {arg}({round(weight)}) meets our requirement ({GUILD_REQUIREMENT})')
          await ctx.reply(embed=applicationInfo())
          await ctx.reply(embed=applicationForm())
        else:
          await ctx.reply(embed=preliminaryFailed(round(weight)))
      except KeyError:
        await ctx.reply(f'You discord account is not verified with the ign: {arg}')
    except ValueError:
      await ctx.reply('Invalid IGN \nPlease Try Again with %ticket verifyweight <name>')
  else:
    await ctx.reply('You cannnot run this command here')


async def deleteTicketSee(ctx, arg):
  guild = ctx.message.guild.id
  try:
    role_required = db[f'{guild}_ticket_roles_allow_to_config']
    if checkRoles(ctx, role_required):
      try:
        role_list = db[f'{guild}_ticket_roles_allow_to_see']
        try:
          role_list.remove(arg)
          db[f'{guild}_ticket_roles_allow_to_see'] = role_list
          await ctx.reply(f'Users with {ctx.guild.get_role(int(arg))} will not be able to see tickets.')
        except ValueError:
          await ctx.reply('Role did not have perms to see channel in the first place.')
      except KeyError:
        await ctx.reply('There are no roles to be delete.')
    else:
      role_name = []
      for i in db[f'{guild}_ticket_roles_allow_to_config']:
        role_name.append(ctx.guild.get_role(int(i)))
      if role_name != []:
        await ctx.reply(f'Role Required: {str(role_name)} to use this command.')
      else:
        await ctx.reply('You must first do %ticket addrole <role id> to use this command')  
  except KeyError:
    await ctx.reply('You must first do %ticket addrole <role id> to use this command')


async def deleteTicketConfig(ctx, arg):
  guild = ctx.message.guild.id
  try:
    role_required = db[f'{guild}_ticket_roles_allow_to_config']
    if checkRoles(ctx, role_required):
      role_list = list(db[f'{guild}_ticket_roles_allow_to_config'])
      try:
        role_list.remove(arg)
        db[f'{guild}_ticket_roles_allow_to_config'] = role_list
        await ctx.reply(f'Now users with {ctx.guild.get_role(int(arg))} will not be able to config tickets.')
      except ValueError:
        await ctx.reply('Role did not have perms to see channel in the first place.')
    else:
      role_name = []
      for i in db[f'{guild}_ticket_roles_allow_to_config']:
        role_name.append(ctx.guild.get_role(int(i)))
      if role_name != []:
        await ctx.reply(f'Role Required: {str(role_name)} to run this command.')
      else:
        await ctx.reply('Do %ticket addrole config first.')
  except:
    await ctx.reply('Do %ticket addrole config first.')


async def configCategory(ctx, arg):
  guild = ctx.message.guild.id
  try: 
    roles_required = db[f'{guild}_ticket_roles_allow_to_config']
    if checkRoles(ctx, roles_required):
      ticket_category_id = arg
      db[f'{guild}_ticket_category_id'] = ticket_category_id
      category_name = discord.utils.get(ctx.guild.categories, id=int(arg))
      await ctx.reply(f'Sucessfully configured. Now all tickets location will be created in the {category_name} category.')
    else:
      role_name = []
      for i in db[f'{guild}_ticket_roles_allow_to_config']:
        role_name.append(ctx.guild.get_role(int(i)))
      if role_name != []:
        await ctx.reply(f'Role Required: {str(role_name)} to run this command.')
      else:
        await ctx.reply('Do %ticket addrole config <role id> first.')
  except KeyError:
    await ctx.reply('Do %ticket addrole config <role id> first. ')


async def configChannel(ctx, arg):
  guild = ctx.message.guild.id
  try:
    roles_required = db[f'{guild}_ticket_roles_allow_to_config']
    if checkRoles(ctx, roles_required):
      db[f'{guild}_ticket_channel_id'] = arg
      channel_name = discord.utils.get(ctx.guild.channels, id=int(arg))
      await ctx.reply(f'Sucessfully configured. Now all tickets can only be created in the {channel_name} channel.')
    else:
      role_name = []
      for i in db[f'{guild}_ticket_roles_allow_to_config']:
        role_name.append(ctx.guild.get_role(int(i)))
      if role_name != []:
        await ctx.reply(f'Role Required: {str(role_name)} to run this command.')
      else:
        await ctx.reply('Do %ticket addrole config <role id> first.')

  except KeyError:
    await ctx.reply('Do %ticket addrole config <role id> first. ')


async def configHelp(ctx):
  guild = ctx.message.guild.id
  try:
    roles_required = db[f'{guild}_ticket_roles_allow_to_config']
    if checkRoles(ctx, roles_required):
      await ctx.reply(embed=config_help_message())
    else:
      role_name = []
      for i in db[f'{guild}_ticket_roles_allow_to_config']:
        role_name.append(ctx.guild.get_role(int(i)))
      if role_name != []:
        await ctx.reply(f'Role Required: {str(role_name)} to run this command.')
      else:
        await ctx.reply('Do %ticket addrole config <role id> first.')
  except KeyError:
    await ctx.reply('Do %ticket addrole config <role id> first.')


async def renameChannel(ctx, arg):
  guild = ctx.message.guild.id
  category = db[f'{guild}_ticket_category_id']
  if str(ctx.message.channel.category.id) == str(category):
    try:
      if 'Ticket' in ctx.channel.topic:
        await ctx.channel.edit(name=arg, topic=arg)
        await ctx.reply(f'Sucessfully renamed to {arg}')
      else:
        await ctx.reply("Cannot rename channel because it is not labeled as Ticket.")
    except TypeError:
      await ctx.reply("Cannot rename channel because it is not labeled as Ticket.")
  
  else:
    await ctx.reply(f'Cannot rename any channel except the ones in the {category} category.')


async def deleteChannel(ctx):
  await quick_export(ctx)  
  guild = ctx.message.guild.id
  category = db[f'{guild}_ticket_category_id']
  channel = db[f'{guild}_ticket_channel_id']
  if str(category) == str(ctx.message.channel.category.id):
    if int(ctx.message.channel.id) != int(channel):
      if 'Ticket' in ctx.channel.topic:
        await ctx.channel.delete(reason='Closed Ticket.')
      else:
        await ctx.reply('Cannot delete this channel because it is not labeled as Ticket.')
    else:
      await ctx.reply('Cannot delete this channel.')
  else:
    await ctx.reply(f'Cannot delete any channel except the ones in the {category} category.')
  
async def ticketPerms(ctx):
  guild = ctx.message.guild.id
  see_roles_id= []
  see_roles_names = []
  for i in db[f'{guild}_ticket_roles_allow_to_see']:
    see_roles_id.append(i)
  for i in see_roles_id:
    see_roles_names.append(str(ctx.guild.get_role(int(i))))

  config_roles_id = []
  config_roles_names = []
  for i in db[f'{guild}_ticket_roles_allow_to_config']:
    config_roles_id.append(i)
  for i in config_roles_id:
    config_roles_names.append(str(ctx.guild.get_role(int(i))))
  await ctx.reply(f'Roles allowed to see tickets: {see_roles_names}')
  await ctx.reply(f'Roles allowed to config tickets: {config_roles_names}')


async def configRestart(ctx, client):
  guild = ctx.message.guild.id
  await ctx.reply('Consequences: ticket system might not work properly after resetting its value.')
  sent = await ctx.reply('Please enter: I understand the consequences of this')
  try:
    msg = await client.wait_for(
      "message",
      timeout = 60,
      check = lambda message: message.author == ctx.author and ctx.author.guild_permissions.administrator == True and message.content == 'I '\
      'understand the consequences of this'
    )
    if msg:
      deleted = []
      stuff_to_delete = ['ticket_channel_id', 'ticket_category_id', 'ticket_roles_allow_to_config', 'ticket_roles_allow_to_see', 'ticket_number']
      for i in stuff_to_delete:
        try:
          del db[f'{guild}_{i}']
          deleted.append(i)
        except KeyError:
          await ctx.reply(f'FAILED to delete {i}')
      await ctx.reply(f'Sucessfully deleted {deleted}')
      await ctx.reply('Please set up your ticket system again. For more, do %ticket guide')
      await sent.delete()
  except asyncio.TimeoutError:
    await ctx.reply('Time out, Please try again')


async def addUser(ctx, arg):
  arg = int(arg.strip('<>!@'))
  overwrites = await ticketOverwrite(ctx)
  overwrites[await ctx.message.guild.fetch_member(arg)] = discord.PermissionOverwrite(read_messages=True)
  try:
    if "Ticket" in ctx.channel.topic:
      await ctx.channel.edit(overwrites=overwrites)
      await ctx.reply('Sucess')
    else:
      await ctx.reply('Cannot perform this operation.')      
  except TypeError:
    await ctx.reply('Cannot perform this operation.')


async def ticketSetup(ctx):
  embed = discord.Embed() 
  await ctx.channel.send()