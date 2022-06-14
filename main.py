import random
import discord
from discord import Colour
from discord.ext import commands, tasks
from urllib import parse, request
import json

from discord.ext.commands import MissingPermissions, CommandNotFound, MissingRequiredArgument, MemberNotFound
from googleapiclient.discovery import build

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)


@bot.event
async def on_message(message):
    allCommands = list(bot.all_commands)
    if not message.author.bot:
        command = message.content.replace("!", "")
        variable = command.rsplit(" ")

        if message.channel.id == 924360190596362300 and variable[0] not in allCommands:
            await message.delete()
            await message.channel.send("Enter a  correct command. !help for commands")
            return
        else:
            await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send(f"{ctx.message.content} is not a valid command!")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("!Help"))
    print("bot is logged in")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(917385740667715615)
    await channel.send(f"Welcome! {member.mention} Write !joinServer to join.")


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(914517063844913215)
    await channel.send(f"{member.mention} left the server!")


@bot.command(brief="Writes hello to the channel.")
async def hello(ctx):
    if ctx.channel.id == 917120034642481202:
        await ctx.send("Hello")


@bot.command(brief="this searches the google images and gets a random photo from first 10 photos.", Hidden=True)
async def search(ctx, searchr=""):
    if searchr == "":
        await ctx.send("you need to write the search key")
        return
    apikey = "AIzaSyAJ8aw99Xleg04_CBn4ZizYfSgwyhIc-Sw"
    rand = random.randint(0, 9)
    resource = build("Customsearch", "v1", developerKey=apikey).cse()
    result = resource.list(q=f"{searchr}", cx="14010b84a50eb138d", searchType="image").execute()
    url = result["items"][rand]["link"]
    embedl = discord.Embed(title=f"Here is your image {searchr.title()}")
    embedl.set_image(url=url)
    await ctx.send(embed=embedl)


@bot.command(brief="Gets a random GIF according to the search parameter.")
async def gif(ctx, searchr=""):
    api_key = "hkDR42eZAUQoCcPYieHRmDfjKTGQgqfd"

    url = "https://api.giphy.com/v1/gifs/random"
    params = parse.urlencode({
        "api_key": api_key,
        "tag": searchr,
        "rating": "g"
    })
    with request.urlopen("".join((url, "?", params))) as response:
        data = json.loads(response.read())
    embedl = discord.Embed(colour=discord.Colour.blue())
    embedl.set_image(url=data['data']['images']['original']['url'])
    await ctx.send(embed=embedl)


# region Kick command
@bot.command(brief="Used to kick people from the server")
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, reason):
    await user.kick(reason=reason)
    await ctx.send(f"The user has been kicked for {reason}")


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to do that!")


# endregion
# region ban command
@bot.command(brief="used to ban people from the server.")
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, reason):
    await user.ban(reason=reason)
    await ctx.send(f"{user} has been banned for {reason}")


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to do that!")


# endregion
# region clear command
@bot.command(brief="clear a specific amount of message depending on the parameter.")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    if amount == 0:
        return
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"cleared {amount} messages!")


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to do that!")


# endregion
# region mute and unmute
@bot.command(brief="mutes the user")
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, reason=None):
    role = discord.utils.get(ctx.author.guild.roles, name="Muted")
    if role not in member.roles:
        await member.add_roles(role, reason=reason)
        await ctx.send(f"{member.mention} has been muted because of {reason}")
    else:
        await ctx.send(f"{member.mention} is already muted!")


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You dont have permission to do that!")


@bot.command(brief="Unmutes the user")
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.author.guild.roles, name="Muted")

    if role in member.roles:

        await member.remove_roles(role)
        await ctx.send(f"{member.mention} has been unmuted!")

    else:
        await ctx.send(f"{member.mention} is not muted!")


@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You dont have permission to do that!")


# endregion

@bot.command(name="start", brief="starts a counter", hidden=True)
async def counter(ctx):
    count.start()
    await ctx.send("counter started!")


_index = 0
_minutes = 0


@tasks.loop(seconds=1.0)
async def count():
    global _index
    global _minutes
    _index += 1
    if _index == 60:
        _minutes += 1
        _index = 0


@bot.command(hidden=True)
async def stop(ctx):
    count.cancel()
    global _index
    global _minutes
    await ctx.send(f"counter finished the timer is {_minutes} minutes and {_index} seconds!")
    _index = 0
    _minutes = 0


@bot.command(hidden=True)
async def ders(ctx):
    embed = discord.Embed(color=Colour.random())
    embed.description = "Identity and access managment pdf [click]" \
                        "(https://stuaydinedu-my.sharepoint.com/personal/muratmesum_stu_aydin_edu_tr/Documents" \
                        "/DESIGNING%20IDENTITY%20AND%20RES.%20MAN.%20SYSTEMS%20ARCH.pdf). "
    await ctx.send(embed=embed)


@bot.command(aliases=['user-info', 'uinf'], brief='belirtilen kullanıcının bilgilerini gösterir *Admin rolü*')
@commands.has_permissions(administrator=True)
@commands.guild_only()
async def user_info(ctx, member: discord.Member):
    user_info_txt = """
```diff
+ User info for {nick}:

- User ID: 
    {uid}

- Joined discord at:
    {created_at}

- Joined server at: 
    {joined_at}

- Server Permissions:
    {perms}
```
"""
    name = member.display_name
    uid = member.id
    created_at = member.created_at.ctime()
    joined_at = member.joined_at.ctime()
    perms = member.permissions_in(ctx.channel)
    perms_str = ''
    for i, perm in enumerate(dir(perms)):
        if not i == 1 and perms.__getattribute__(perm) and not perm.startswith('_'):
            perms_str += perm.replace('_', ' ').capitalize() + ', '

    await ctx.send(
        user_info_txt.format(nick=name, uid=uid, created_at=created_at, joined_at=joined_at, perms=perms_str[:-2]))


@bot.command(aliases=["mtnall"], brief="mentions all active users in the server")
async def mentionall(ctx, *args):
    if args is None:
        await ctx.send("Specify a message!")
    else:
        mentionstring = ""
        users = ctx.guild.members
        for user in users:
            if user.raw_status == "online" or user.raw_status == "online":
                if user is not ctx.author and not user.bot:
                    mentionstring += f"{user.mention} "
        for arg in args:
            mentionstring += " " + arg
        await ctx.send(mentionstring)


@bot.command(hidden=True)
async def photo(ctx):
    url = "https://meme-api.herokuapp.com/gimme"
    with request.urlopen("".join((url, "/1"))) as response:
        data = json.loads(response.read())

    embed = discord.Embed(colour=Colour.random())
    embed.set_image(url=data["memes"][0]["url"])
    await ctx.send(embed=embed)


@bot.command(hidden=True)
async def avatar(ctx, user: discord.Member):
    if user not in ctx.guild.members:
        return
    url = user.avatar_url
    embed = discord.Embed(title=f"image of {user.display_name}!")
    embed.set_image(url=url)
    await ctx.send(embed=embed)


@avatar.error
async def avatar_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("mention a name for the image!")
    if isinstance(error, MemberNotFound):
        await ctx.send("user can't be found!")


@bot.command(brief="Shows the project tasks")
async def tasks(ctx):
    with open("Todo.txt") as file:
        filelist = file.readlines()
        newstring = ""
        index = 1
        for string in filelist:
            newstring = newstring + str(index) + ". " + string
            index += 1

        embed = discord.Embed(title="Things to be done", description=newstring)
        await ctx.send(embed=embed)


@bot.command(brief="Add a task to the end of the list")
async def addtask(ctx, *args):
    with open("Todo.txt", "a") as file:
        task = ""
        for arg in args:
            task += arg + " "

        file.write(task + "\n")
        await ctx.channel.purge(limit=1)
        await ctx.send("Task added.")


@bot.command(brief="Take a task to do on the project")
async def taketask(ctx, message):
    with open("Todo.txt") as file:
        list = file.readlines()
    if not message.isnumeric():
        await ctx.send("Enter a valid integer! ")
        return
    if int(message) > len(list) or int(message) < 1:
        await ctx.send(f"Enter Between 1 to {len(list)}")
        return
    for member in ctx.guild.members:
        name = member.display_name.rstrip("#")
        if name in list[int(message) - 1]:
            await ctx.send("This task is already taken by someone!")
            return

    list[int(message) - 1].rstrip("\n")
    task = f"~~{list[int(message) - 1][:-1]}~~ -- Taken by **{ctx.author.display_name}**\n"

    list[int(message) - 1] = task
    with open("Todo.txt", "w") as file:
        file.writelines(list)
    await ctx.send("Task is taken!")


@bot.command(brief="Finish a taken task and delete it from the list")
async def finishtask(ctx, message):
    with open("Todo.txt") as file:
        list = file.readlines()
    if not message.isnumeric():
        await ctx.send("Enter a valid integer! ")
        return
    if int(message) > len(list) or int(message) < 1:
        await ctx.send(f"Enter Between 1 to {len(list)}")
        return
    if not list[int(message) - 1].startswith('~'):
        print(list[int(message) - 1].startswith("~~"))
        await ctx.send("You can only finish the tasks that are taken!")
        return
    member = list[int(message) - 1].split("by")[1].replace("**", "")[:-1].lstrip()
    if ctx.author.display_name != member:
        await ctx.send("You didn't take this task!")
        return
    list.pop(int(message) - 1)
    with open("Todo.txt", "w") as file:
        file.writelines(list)
        await ctx.send("Task is finished!")


bot.run("Discord's bot id goes here, all of them is different")
