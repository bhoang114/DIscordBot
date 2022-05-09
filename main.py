import discord
import asyncio
import os
from discord.ext import commands, tasks
intents = discord.Intents.all()
client = commands.Bot(command_prefix = '?', intents=intents)

@client.event
async def on_ready():
  print('bot is online')

@client.command()
async def hello(ctx):
  await ctx.send('hello')

@client.command()
async def schedule(ctx, * ,args):
  channel = client.get_channel(966844677842157608)

  # Adds people's name into a dictionary if they have a pinned message there.
  DISCORD_USERSNAMES = {}
  for member in ctx.guild.members:
    DISCORD_USERSNAMES[member.name.casefold().capitalize()] = member.id

  # Used to find a schedule based on a person's discord username.
  if args.casefold().capitalize() in list(DISCORD_USERSNAMES.keys()):
      for message in await channel.pins():
          if message.author.id == DISCORD_USERSNAMES[args.casefold().capitalize()]:
              return await ctx.send(file=await message.attachments[0].to_file())


@client.command()
async def remind(ctx, *, arg):
    time = 0
    single_number = False
    sentence = arg.split(" ")

    # Checks if the first argument has any duration words.
    if sentence[0][-1] != "s" and sentence[0][-1] != "m" and sentence[0][-1] != "h":
        try:
            time = int(sentence[0]) # Converts the first argument into an integer to be converted into time.
            single_number = True
        except:
              return await ctx.send("Enter a number and/or its duration.") 
    time_value = "0"
    counter = -1
    sec_open = True
    min_open = True
    hr_open = True
    for argument in sentence:
        # Checks if an argument has 2 or more characters (to see a number and a letter).
        if len(argument) > 1 and not(single_number) and counter < 2:
            try:
                time_value = int(argument[-2])
            except ValueError:
                pass
            else:
                if argument.endswith("s") and type(time_value) == int and sec_open:
                    time += int(argument[:-1])
                    counter += 1
                    sec_open = False
                if argument.endswith("m") and type(time_value) == int and min_open:
                    time += 60 * int(argument[:-1])
                    counter += 1
                    min_open = False
                if argument.endswith("h") and type(time_value) == int and hr_open:
                    time += 60 * 60 * int(argument[:-1])
                    counter += 1
                    hr_open = False

    # Conversions.
    hours = time // 60 // 60
    minutes = time // 60 % 60
    seconds = time % 60 % 60

    # Formatting output.
    hour_statement = ""
    minute_statement = ""
    second_statement = ""
    aand_statement = ""
    band_statement = ""
    comma = ""
    if hours > 0 and minutes > 0 and seconds > 0:
        band_statement = " and "
        comma = ","
    elif hours > 0 and minutes > 0 and seconds == 0:
        aand_statement = " and "
    elif (hours > 0 or minutes > 0) and seconds > 0:
        band_statement = " and "
    if seconds == 1:
        second_statement = " second"
    elif seconds == 0:
        seconds = ""
        second_statement = ""
    else:
        second_statement = " seconds"

    if minutes == 1:
        minute_statement = " minute"
    elif minutes == 0:
        minutes = ""
        minute_statement = ""
    else:
        minute_statement = " minutes"

    if hours == 1:
        hour_statement = " hour"
    elif hours == 0:
        hours = ""
        hour_statement = ""
    else:
        hour_statement = " hours"

    # Message formatter.
    message_output = "{0.author.mention}"
    if len(sentence) > 1:
        for index in range(len(sentence)):
            if single_number:
                if index != 0:
                    message_output += " " + sentence[index]
            else:
                if counter < index:
                    message_output += " " + sentence[index]
    message_output = message_output.format(ctx)

    await ctx.send("Reminding {0.author.mention} in {hour}{hrs}{comma}{aand}{minute}{mins}{comma}{band}{second}{secs}.".format(
            ctx, hour = hours, hrs = hour_statement, comma = comma, aand = aand_statement, minute = minutes, mins = minute_statement, band = band_statement, second = seconds, secs = second_statement))

    async def reminder(time, message):
      await asyncio.sleep(time),
      await ctx.send(message)

    await asyncio.ensure_future(reminder(time, message_output))

client.run('OTY3MTMxOTU2MTMzMzcxOTE0.YmL10g.od3K3JSoUIQah5PRQIPqOepVt-A')