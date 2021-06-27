import discord
import asyncio
import requests
import os
key = os.environ['API']
GUILD_REQUIREMENT = 4500


def preliminaryFailed(weight):
  embed = discord.Embed(
    title = 'Preliminary Failed',
    colour = discord.Colour.blue()
  )
  embed.add_field(name='Reason:', value=f'Your weight ({weight}) does not meet our requirement ({GUILD_REQUIREMENT}).')
  embed.add_field(name="Do not close this ticket.", value="If you're closed to our requirement, we might make an exception.")
  embed.set_footer(text='Created by ThatBananaKing')
  return embed


def uuid(ign):
    data = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{ign}').json()
    x = data["id"]
    return x


def checkWeight(uuid, key):
  data = requests.get(f'https://hypixel-api.senither.com/v1/profiles/{uuid}/weight?key={key}').json()
  return data['data']['weight'] + data['data']['weight_overflow']


def applicationInfo():
  embed = discord.Embed(
    title = 'Guild Application Process',
    colour = discord.Colour.blue()
  )
  embed.add_field(name='#1', value='Submit Your Application', inline=False)
  embed.add_field(name='#2', value='Application reviewed by our staff steam', inline=False)
  embed.add_field(name='#3', value='Application is Accepted or Rejected', inline=False)
  embed.add_field(name='Note:', value='IF the guild is full, you will be placed in a waiting list while we resolved said issue.\n'\
  'All decisions made by the staff team are FINAL.'
  )
  embed.set_footer(text='Created by ThatBananaKing')
  return embed



def applicationForm():
  embed = discord.Embed(
    title = 'Guild Application Form',
    colour = discord.Colour.blue()
  )
  embed.add_field(name='Please fill in', value='❂ Application For Lunar Guard ❂\n'\
'IGN:\n'\
'Catacombs level:\n'\
'Link your sky.shiiyu.moe here:\n'\
'What is your approximate net worth (Use NEU if unsure):\n'\
'How active are you?:\n'\
'Previous skyblock guilds (if any):\n'\
'Why do you want to join?:\n'\
'Anything else you would like us to know?', inline=False)
  embed.set_footer(text='Created by ThatBananaKing')
  return embed

  
async def guildApp(ctx, client, channel):

  sent = await channel.send(f'Hello {ctx.author.mention},\nPlease Enter Your IGN')
  try:
      msg = await client.wait_for(
        "message",
        timeout = 3600,
        check = lambda message: message.author == ctx.author and message.channel == channel
      )
      if msg: 
        await sent.delete()
        try:
          weight = checkWeight(uuid(msg.content), key)
          try: 
            data = requests.get(f'https://api.hypixel.net/player?uuid={uuid(msg.content)}&key={key}').json()
            mc_discord_username = data['player']['socialMedia']['links']['DISCORD']
            discord_name = ctx.author.name + '#' + ctx.author.discriminator
            if str(discord_name) != str(mc_discord_username):
              await channel.send(f'Your minecraft account seems to be verified to a different discord name: {mc_discord_username}\nPlease check!')
            if weight >= GUILD_REQUIREMENT:
              await channel.send(f'Your weight from the account {msg.content}({round(weight)}) meet our requirement ({GUILD_REQUIREMENT})')
              await channel.send(embed=applicationInfo())
              await channel.send(embed=applicationForm())
            else:
              await channel.send(embed=preliminaryFailed(round(weight)))
          except KeyError:
            await channel.send(f'You discord account is not verified with the ign: {msg.content}')
        except ValueError:
          await channel.send('Invalid IGN \nPlease Try Again with %ticket verifyweight <name>')
        
  except asyncio.TimeoutError:
    await channel.send("Preliminary Failed\nReason: User hasn't enter their IGN")
    await sent.delete()
