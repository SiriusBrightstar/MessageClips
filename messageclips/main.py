"""
MessageClips v2.0.0
Bookmark Bot for Discord

By SiriusBrightstar#8223
"""

import os
import logging
import discord
from datetime import datetime
from customLogger import CustomFormatter


log = logging.getLogger("My_app")
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
log.addHandler(ch)


intents = discord.Intents.default()
intents.members = True
embed = discord.Embed()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


@tree.command(name="bot_info", description="Message Clipper Bot Details")
async def first_command(interaction):
    detailsEmbed = discord.Embed(
        title="Message Clipper Bot", description="Open Source Message Clipper Bot", color=0x002366)
    detailsEmbed.set_author(name="SiriusBrightstar#8223", url="https://github.com/siriusbrightstar",
                            icon_url="https://avatars.githubusercontent.com/u/62252266?v=4")

    await interaction.response.send_message(embed=detailsEmbed)


@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                           name="Your Messages"),
                                 status=discord.Status.online)
    log.info('Bot has logged in as {0.user}'.format(client))


@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    channel_id = payload.channel_id
    channel = client.get_channel(channel_id)

    if isinstance(channel, discord.channel.DMChannel) == False:
        try:
            emoji = payload.emoji
            user = payload.member
            message = await channel.fetch_message(message_id)
            authorName = message.author

            if emoji.name == "🔖":
                log.info(f'Message Clip for User: {user.name}')
                log.debug(f'Message Clip Content: {message.content}')
                log.debug("Message Clip from Channel ID: " + str(channel_id))
                log.info("-"*10)

                dmEmbed = discord.Embed(description=str(
                    message.content), color=0x002366, url=message.jump_url)
                dmEmbed.set_author(name=str(authorName))
                dmEmbed.set_footer(text="React with ❌ to delete this message")
                send = await user.send(f'**Message Clip Created** on {str(datetime.now())[:-7]}\nJump to Message: {message.jump_url}', embed=dmEmbed)
                # await send.add_reaction("❌")
        except Exception as e:
            log.error(
                f'Some error detected in Server channel:\n{e}', exc_info=True)

    elif isinstance(channel, discord.channel.DMChannel) == True:
        try:
            dm_message_id = payload.message_id
            dm_channel_id = payload.channel_id
            dm_channel = client.get_channel(dm_channel_id)
            dm_emoji = payload.emoji

            dm_message = await dm_channel.fetch_message(dm_message_id)
            if dm_emoji.name == "❌":
                log.info("Deleted message")
                await dm_message.delete()
        except Exception as e:
            log.error(
                f'Some error detected in DM channel:\n{e}', exc_info=True)

client.run(os.getenv('TOKEN_1'))
