# Discord Ticket Bot

A simple Discord ticket bot for Render using an environment variable named `DISCORD_TOKEN`.

## Features

- `/ticket` posts a ticket panel.
- `Create Ticket` makes a private ticket channel.
- `Close Ticket` deletes the ticket channel.
- Creates a `Tickets` category automatically if it does not exist.
- No Discord token is stored in the code.

## Render setup

1. Create a new **Background Worker** on Render.
2. Upload/connect this project.
3. Build command:
   `pip install -r requirements.txt`
4. Start command:
   `python bot.py`
5. Add an Environment Variable:
   - Key: `DISCORD_TOKEN`
   - Value: your Discord bot token
6. Deploy.

## Discord bot permissions

Invite the bot with the permissions it needs to:
- View Channels
- Send Messages
- Embed Links
- Read Message History
- Manage Channels

The `/ticket` command requires the person using it to have **Manage Server** permission.

## Important

Never put your actual Discord token in `bot.py`, GitHub, or this ZIP. Use Render's `DISCORD_TOKEN` environment variable.
