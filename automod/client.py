import re
import traceback
import asyncio

from logger import get_logger
from filter import KeywordFilter, SyntaxFilter, SemanticFilter, FilterPipeline

logger = get_logger(__name__)

import discord

class AutomodClient():
    def __init__(self, **kwargs):
        self.client = discord.Client()
        self.kwargs = kwargs

        self.filters = [
            KeywordFilter(**kwargs),
            SyntaxFilter(**kwargs)
        ]
        self.filter_pipeline = FilterPipeline(self.filters)

        activity = None
        status = self.kwargs['client_args']['status']
        if status['type'] == 'playing':
            activity = discord.Activity(
                type=discord.ActivityType.playing,
                name=status['text']
            )
        elif status['type'] == 'listening':
            activity = discord.Activity(
                type=discord.ActivityType.listening,
                name=status['text']
            )
        elif status['type'] == 'watching':
            activity = discord.Activity(
                type=discord.ActivityType.watching,
                name=status['text']
            )        

        intents = discord.Intents().all()

        self.client = discord.Client(intents=intents, activity=activity, status=discord.Status.idle)
    
    async def on_ready(self):
        logger.info(f'Connected to Discord - ID: {self.client.user.id} - Name: {self.client.user.name}')
    
    async def on_message(self, message):
        # check if message comes from guilds that are in the config
        if message.guild.id not in self.kwargs['listening_guilds']:
            return
        
        # filter message - if true, delete message and log it in log channel
        if self.filter_pipeline(message.content):
            logger.info(f'Deleting message - Author ID: {message.author.id} - Guild ID: {message.guild.id} - Message ID: {message.id} - Content: {message.content}')
            await message.delete()
            channel = self.client.get_channel(self.kwargs['log_channel'])
            embed = discord.Embed(
                title=f'Automod Action',
                description=f'User: **``{message.author.name}#{message.author.discriminator}``**\nReason: **``Filtered message``**\nAction Type: **``Content Deleted``**\nMessage: **``{message.content}``**',
                color=discord.colour.Color(self.kwargs['embed_colour'])
            )
            await channel.send(embed=embed)

    def run(self):
        logger.info(f'Starting Discord Bot.')
        self.on_ready = self.client.event(self.on_ready)
        self.on_message = self.client.event(self.on_message)
        self.client.run(self.kwargs['client_args']['bearer_token'])
    
    def close(self):
        asyncio.run(self.client.close())
