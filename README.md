# Simple Discord Tasks

A simple bot that allows assigning a work in progress task to yourself or another user and checking tasks for one or all users.

The goal of this is to facilitate checking work progress on hobbyist servers where time and effort are at a premium.

# Commands

| Command | Function |
| -- | -- |
| `/set {task}` | Set your current WIP |
| `/assign {user} {task}` | Set a task for another user |
| `/get {user?}` | Get the current task for another user or, if omitted, yourself |
| `/clear {user?}` | Clears the current task for a user or yourself |
| `/list` | Admin-only: List all the tasks and ping all users |

# Setup

## Environment File

The environment file requires two variables:

```
DISCORD_TOKEN = { your bot token }
DISCORD_GUILD_ID = { your guild (server) id }
```

You will also need to make a `tasks.txt` file in the project root and ensure the python app has read and write permissions to it.
