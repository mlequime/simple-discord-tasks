# bot.py
import os

import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext.commands import has_permissions, MissingPermissions

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name = "test", description = "My first application Command", guild=discord.Object(id=GUILD_ID))
async def first_command(interaction):
    await interaction.response.send_message("Hello!")

@tree.command(name = "echo", description = "Echoes your message", guild=discord.Object(id=GUILD_ID))
async def echo(interaction, *, message: str):
    try:
        message = message.replace("\n", " ")
        await interaction.response.send_message(message)
    except Exception as e:
        print (e)
        await interaction.response.send_message("Message is not valid!")

@tree.command(name = "set", description = "Sets your current task", guild=discord.Object(id=GUILD_ID))
async def set(interaction, *, task: str):
    try:
        task = task.replace("\n", " ")

        # Get the user's ID
        user_id = interaction.user.id

        # Get the user's name
        user_name = interaction.user.name

        # Store the user's ID and the task in a text file, updating it if it's already found
        with open("tasks.txt", "r") as f:
            lines = f.readlines()
            found = False
            for i in range(len(lines)):
                if lines[i].startswith(str(user_id)):
                    lines[i] = f"{user_id} {task}\n"
                    found = True
                    break
            if not found:
                lines.append(f"{user_id} {task}\n")

        with open("tasks.txt", "w") as f:
            f.writelines(lines)

        await interaction.response.send_message(f'OK, {user_name}! Your current task is now: {task}')
    except Exception as e:
        print (e)
        await interaction.response.send_message("Something went wrong while setting tasks. Sorry!")

@tree.command(name = "assign", description = "Assigns a task to someone", guild=discord.Object(id=GUILD_ID))
async def assign(interaction, user: discord.User, *, task: str):
    try:
        task = task.replace("\n", " ")

        # Get the user's details
        user_id = user.id
        user_name = user.name

        # Store the user's ID and the task in a text file, updating it if it's already found
        with open("tasks.txt", "r") as f:
            lines = f.readlines()
            found = False
            for i in range(len(lines)):
                if lines[i].startswith(str(user_id)):
                    lines[i] = f"{user_id} {task}\n"
                    found = True
                    break
            if not found:
                lines.append(f"{user_id} {task}\n")

        with open("tasks.txt", "w") as f:
            f.writelines(lines)

        await interaction.response.send_message(f'OK, {user_name}! Your current task is now: {task}')
    except Exception as e:
        print (e)
        await interaction.response.send_message("Something went wrong while setting tasks. Sorry!")

@tree.command(name = "get", description = "Gets your current task", guild=discord.Object(id=GUILD_ID))
async def get(interaction, *, user: discord.User = None):
    try:
        # Get the user's ID
        if user is None:
            user_id = interaction.user.id
        else:
            user_id = user.id

        # Store the user's ID and the task in a text file, updating it if it's already found
        with open("tasks.txt", "r") as f:
            lines = f.readlines()
            found = False
            for i in range(len(lines)):
                if lines[i].startswith(str(user_id)):
                    if user is None:
                        await interaction.response.send_message(f'Your current task is: {lines[i][len(str(user_id))+1:]}')
                    else:
                        await interaction.response.send_message(f'{user.name}\'s current task is: {lines[i][len(str(user_id))+1:]}')
                    found = True
                    break
            if not found:
                await interaction.response.send_message(f'You have no current task. Why not start something?')

    except Exception as e:
        print (e)
        await interaction.response.send_message("Something went wrong while fetching tasks. Sorry!")

@tree.command(name = "clear", description = "Clears your current task", guild=discord.Object(id=GUILD_ID))
async def clear(interaction, *, user: discord.User = None):
    try:
        # Get the user's ID
        if user is None:
            user_id = interaction.user.id
        else:
            user_id = user.id

        # Store the user's ID and the task in a text file, updating it if it's already found
        with open("tasks.txt", "r") as f:
            lines = f.readlines()
            found = False
            for i in range(len(lines)):
                if lines[i].startswith(str(user_id)):
                    lines[i] = ""
                    found = True
                    break

        with open("tasks.txt", "w") as f:
            f.writelines(lines)

        message = ""
        if found:
            if user is None:
                message = f'Your current task has been cleared.'
            else:
                message = f'{user.name}\'s current task has been cleared.'
        else:
            if user is None:
                message = f'You have no current task.'
            else:
                message = f'{user.name} has no current task.'

        await interaction.response.send_message(message)

    except Exception as e:
        print (e)
        await interaction.response.send_message("Something went wrong while clearing tasks. Sorry!")

@tree.command(name = "list", description = "Lists all current tasks", guild=discord.Object(id=GUILD_ID))
@has_permissions(administrator = True)
async def list(interaction):
    try:
        message = ""
        # Reads the list of tasks and maps the user IDs to names
        with open("tasks.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                user_id = line.split(" ")[0]
                user = await client.fetch_user(user_id)
                message += f"{user.mention}: {line[len(user_id)+1:]}"
        await interaction.response.send_message(message)
    except Exception as e:
        print (e)
        await interaction.response.send_message("Something went wrong while listing tasks. Sorry!")
@list.error
async def test_error(error, ctx):
    if isinstance(error, MissingPermissions):
        await ctx.send("Looks like you don't have the permissions.")

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print("Ready!")
    for guild in client.guilds:
        if guild.id == GUILD_ID:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

client.run(TOKEN)
