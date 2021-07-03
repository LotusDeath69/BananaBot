import discord
from discord.ext import commands
from replit import db 
import os 
from flask import Flask
from threading import Thread
prefix = '%'

app = Flask('')

@app.route('/')
def home():
  return 'success!'

def run():
  app.run(host='0.0.0.0', port=8080)

def keepAlive():
  t = Thread(target=run)
  t.start()

client = commands.Bot(command_prefix=prefix, help_command=None)

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Activity(
    type=discord.ActivityType.listening, name=f'%help in {len(client.guilds)} servers'
  ))
  print('logged in')


@client.command()
async def count(ctx, arg):
  counting_channel_name = 'counting'
  guild = ctx.message.guild.id
  if arg.lower() == 'reset':
    db[f'{guild}_counting_number'] = 1
    await ctx.reply('Sucessfully reseted counting number.')
  
  if arg.lower() == 'help':
    await ctx.reply('How to use: \nCreate a channel call counting\nDo %count <number> to count\nDo %count reset to rest the number.')
  try:
    int(arg) 
    if str(ctx.message.channel.name) == counting_channel_name: 
      try:
        current_number = db[f'{guild}_counting_number'] 
      except KeyError:
        current_number = 1
        db[f'{guild}_counting_number'] = 1

      if str(arg) != str(current_number):
        await ctx.send('Incorrect number. :clown:')
      else:
        await ctx.send(current_number)
        await ctx.message.delete()
        db[f'{guild}_counting_number'] = current_number + 1
    else:
      await ctx.reply(f'Wrong channel go to #{counting_channel_name} :clown:')
  except ValueError:
    pass

keepAlive()# only works if use Replit. Keep the bot running. 
client.run(os.environ['TOKEN'])