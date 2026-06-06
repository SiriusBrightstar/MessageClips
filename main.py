"""
MessageClips v3.0.0
Bookmark Bot for Discord

By SiriusBrightstar
"""

import asyncio
import logging
import os
from datetime import datetime

import discord

# Configuration
BOOKMARK_EMOJI = "🔖"
DELETE_EMOJI = "❌"
MAX_CONCURRENT_TASKS = 5  # Limit concurrent API calls to avoid rate limits

# Configure logging for journalctl
logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")
log = logging.getLogger("MessageClips")
# Reduce noise from discord.py internal rate limit retries in logs
logging.getLogger("discord").setLevel(logging.WARNING)

TOKEN = os.environ.get("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Required for raw_reaction_add if fetching messages
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

# Semaphore to control concurrency
semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)


@tree.command(name="bot_info", description="Message Clipper Bot Details")
async def first_command(interaction: discord.Interaction):
    detailsEmbed = discord.Embed(
        title="Message Clipper Bot",
        description="Open Source Message Clipper Bot",
        color=0x002366,
    )
    detailsEmbed.set_author(
        name="SiriusBrightstar",
        url="https://github.com/siriusbrightstar",
        icon_url="https://avatars.githubusercontent.com/u/62252266?v=4",
    )

    await interaction.response.send_message(embed=detailsEmbed)


@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="Your Messages"
        ),
        status=discord.Status.online,
    )
    log.info(f"Bot has logged in as {client.user}")


@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    # Use semaphore to limit concurrent processing
    async with semaphore:
        message_id = payload.message_id
        channel_id = payload.channel_id
        channel = client.get_channel(channel_id)

        if channel is None:
            try:
                channel = await client.fetch_channel(channel_id)
            except (discord.NotFound, discord.Forbidden):
                return
            except discord.HTTPException as e:
                if e.status == 429:
                    log.warning(
                        "Rate limited while fetching channel, discord.py will retry."
                    )
                return

        if not isinstance(channel, discord.DMChannel):
            try:
                emoji = payload.emoji
                user = payload.member
                if user is None or user.bot:
                    return

                if emoji.name == BOOKMARK_EMOJI:
                    message = await channel.fetch_message(message_id)
                    authorName = message.author

                    log.info(f"Message Clip for User: {user.name}")
                    log.debug(f"Message Clip Content: {message.content}")
                    log.debug(f"Message Clip from Channel ID: {channel_id}")

                    dmEmbed = discord.Embed(
                        description=str(message.content),
                        color=0x002366,
                        url=message.jump_url,
                    )
                    dmEmbed.set_author(name=str(authorName))
                    dmEmbed.set_footer(
                        text=f"React with {DELETE_EMOJI} to delete this message"
                    )

                    await user.send(
                        f"**Message Clip Created** on {str(datetime.now())[:-7]}\nJump to Message: {message.jump_url}",
                        embed=dmEmbed,
                    )
            except discord.NotFound:
                pass
            except discord.Forbidden:
                log.warning(
                    f"Missing permissions in channel {channel_id} or cannot DM user {payload.user_id}"
                )
            except discord.HTTPException as e:
                if e.status == 429:
                    log.warning(
                        "Rate limited. Discord.py handles this, but operations are heavy."
                    )
                else:
                    log.error(f"HTTP error: {e}")
            except Exception as e:
                log.error(
                    f"Unexpected error in Server channel processing: {e}", exc_info=True
                )

        else:
            try:
                dm_message_id = payload.message_id
                dm_channel = channel
                dm_emoji = payload.emoji

                if dm_emoji.name == DELETE_EMOJI:
                    dm_message = await dm_channel.fetch_message(dm_message_id)
                    # Ensure we only delete bot's own messages in DM
                    if dm_message.author == client.user:
                        log.info("Deleted message in DM")
                        await dm_message.delete()
            except discord.NotFound:
                pass
            except discord.HTTPException as e:
                if e.status == 429:
                    log.warning("Rate limited in DM.")
                else:
                    log.error(f"HTTP error in DM: {e}")
            except Exception as e:
                log.error(
                    f"Unexpected error in DM channel processing: {e}", exc_info=True
                )


if __name__ == "__main__":
    if not TOKEN:
        log.error("TOKEN environment variable not set.")
    else:
        try:
            client.run(TOKEN)
        except discord.LoginFailure:
            log.error("Invalid Discord Token.")
        except Exception as e:
            log.critical(f"Bot failed to start: {e}")
