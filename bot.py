import os
import discord
from discord.ext import commands
from discord import app_commands

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable is not set.")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Change this if you want a different category name.
CATEGORY_NAME = "Tickets"

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Create Ticket",
        style=discord.ButtonStyle.green,
        emoji="🎫",
        custom_id="ticket:create"
    )
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        if guild is None:
            return await interaction.response.send_message(
                "This button only works inside a server.", ephemeral=True
            )

        category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
        if category is None:
            category = await guild.create_category(CATEGORY_NAME)

        channel_name = f"ticket-{interaction.user.name}".lower().replace(" ", "-")
        existing = discord.utils.get(guild.text_channels, name=channel_name)

        if existing:
            return await interaction.response.send_message(
                f"You already have a ticket: {existing.mention}", ephemeral=True
            )

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),
            guild.me: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_channels=True,
                read_message_history=True
            ),
        }

        channel = await guild.create_text_channel(
            channel_name,
            category=category,
            overwrites=overwrites,
            topic=f"Ticket created by {interaction.user} ({interaction.user.id})"
        )

        embed = discord.Embed(
            title="🎫 Support Ticket",
            description=(
                f"Welcome {interaction.user.mention}!\\n\\n"
                "Please explain what you need help with. A staff member will assist you."
            )
        )

        await channel.send(embed=embed, view=CloseTicketView())
        await interaction.response.send_message(
            f"Ticket created: {channel.mention}", ephemeral=True
        )

class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Close Ticket",
        style=discord.ButtonStyle.red,
        emoji="🔒",
        custom_id="ticket:close"
    )
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.channel

        if not isinstance(channel, discord.TextChannel):
            return await interaction.response.send_message(
                "This isn't a ticket channel.", ephemeral=True
            )

        if not channel.name.startswith("ticket-"):
            return await interaction.response.send_message(
                "This doesn't look like a ticket channel.", ephemeral=True
            )

        await interaction.response.send_message("🔒 Closing this ticket...")
        await channel.delete(reason=f"Ticket closed by {interaction.user}")

@bot.event
async def on_ready():
    bot.add_view(TicketView())
    bot.add_view(CloseTicketView())
    try:
        synced = await bot.tree.sync()
        print(f"Logged in as {bot.user}. Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"Slash command sync failed: {e}")

@bot.tree.command(name="ticket", description="Post the ticket creation panel.")
@app_commands.checks.has_permissions(manage_guild=True)
async def ticket(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎫 Support Tickets",
        description="Click **Create Ticket** to open a private support ticket."
    )
    await interaction.response.send_message(embed=embed, view=TicketView())

@ticket.error
async def ticket_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        if not interaction.response.is_done():
            await interaction.response.send_message(
                "You need Manage Server permission to use this command.",
                ephemeral=True
            )

bot.run(TOKEN)
