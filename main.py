import logging
import discord
from dotenv import load_dotenv
import os
from discord.ext import commands

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)
server_role="admin"

@bot.event
async def on_ready():
    print(f"We are ready to start {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "shit" in message.content.lower() :
        await message.delete()
        await message.channel.send(f"{message.author.mention} - watch out before you text")

    # if "hello" in message.content.lower():
    #     await message.channel.send(f"{message.author.mention} - welcome")
    

    await bot.process_commands(message)

# $hello - use this command
@bot.command()
async def hello(context):
    await context.send(f"Hello {context.author.mention}!!!")

# $assign - use this command
@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=server_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {server_role}")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
async def removed(ctx):
    role = discord.utils.get(ctx.guild.roles, name=server_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention}'s role which is {server_role} is removed")
    else:
        await ctx.send("Role doesn't exist")

# $dm hello - this command for sending msg in dm
@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg}")
    
# $reply hello - this command for replying msg in sever
@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message!")

# $poll is this server good - command for poll
@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

@bot.command()
@commands.has_role(server_role)
async def secret(ctx):
    await ctx.send("Welcome to the club!")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to do that!")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)
