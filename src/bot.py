import discord
from discord.ext import commands

import logging

import db.sqldb as database

class client(commands.Bot):
    def __init__(self, default_cogs : list[str] = []):
        self.default_cogs = default_cogs
        self.logger = logging.getLogger()
        self.db : database.ScorekeeperDB = database.ScorekeeperDB()
        intents = discord.Intents.default()
        intents.members = True  # Server Members intent (privileged)
        intents.moderation = True  # Moderation events (ban, kick, etc.)
        intents.bans = True
        super().__init__(command_prefix="f!", intents=intents, help_command=None)
        
    async def cog_enable(self, cog : str):
        """
        Enable a cog by its path (Python module path).
        Example: "cogs.example_cog"
        
        This method loads the cog and syncs the application commands.
        
        Args:
            cog (str): The path to the cog to be loaded.
        Raises:
            commands.ExtensionAlreadyLoaded: If the cog is already loaded.
            commands.ExtensionNotFound: If the cog is not found.
            Exception: For any other exceptions that may occur.
        Returns:
            None        
        """
        try:
            self.logger.debug(f"Attempting to load {cog}...")
            await self.load_extension(cog)
            self.logger.info(f"Loaded {cog} successfully.")
            self.logger.debug(f"Syncing application commands for {cog}...")
            await self.tree.sync()
            self.logger.info(f"Synced application commands for {cog}.")
        except commands.ExtensionAlreadyLoaded:
            self.logger.warning(f"{cog} is already loaded.")
        except commands.ExtensionNotFound:
            self.logger.error(f"{cog} not found.")
        except Exception as e:
            self.logger.error(f"Failed to load {cog}: {e}")
            
    async def batch_cog_enable(self, cogs : list[str]):
        """
        Enable multiple cogs by their paths (Python module paths).
        Example: ["cogs.example_cog", "cogs.another_cog"]
        
        This method loads the cogs and syncs the application commands.
        Avoids more Syncs.
        
        Args:
            cogs (list): A list of paths to the cogs to be loaded.
        Raises:
            commands.ExtensionAlreadyLoaded: If any cog is already loaded.
            commands.ExtensionNotFound: If any cog is not found.
            Exception: For any other exceptions that may occur.
        Returns:
            None
        """
        self.logger.debug(f"Attempting to load {len(cogs)} cogs...")
        self.logger.debug(f"Cog list: {cogs}")
        self.logger.debug("Loading cogs...")
        for cog in cogs:
            try:
                self.logger.debug(f"Loading {cog}...")
                await self.load_extension(cog)
                self.logger.info(f"Loaded {cog} successfully.")
            except commands.ExtensionAlreadyLoaded:
                self.logger.warning(f"{cog} is already loaded.")
            except commands.ExtensionNotFound:
                self.logger.error(f"{cog} not found.")
            except Exception as e:
                self.logger.error(f"Failed to load {cog}: {e}")
        self.logger.info(f"Batch loaded {len(cogs)} cogs successfully.")
        self.logger.debug("Syncing application commands...")
        await self.tree.sync()
        self.logger.debug("Synced application commands.")
            
    async def cog_disable(self, cog : str):
        """
        Disable a cog by its path (Python module path).
        Example: "cogs.example_cog"
        
        This method unloads the cog and syncs the application commands.
        
        Args:
            cog (str): The path to the cog to be unloaded.
        Raises:
            commands.ExtensionNotLoaded: If the cog is not loaded.
            commands.ExtensionNotFound: If the cog is not found.
            Exception: For any other exceptions that may occur.
        Returns:
            None
        """
        self.logger.debug(f"Attempting to unload {cog}...")
        try:
            self.logger.debug(f"Unloading {cog}...")
            await self.unload_extension(cog)
            self.logger.info(f"Unloaded {cog} successfully.")
            self.logger.debug(f"Syncing application commands after unloading {cog}...")
            await self.tree.sync()
            self.logger.info(f"Synced application commands after unloading {cog}.")
        except commands.ExtensionNotLoaded:
            self.logger.warning(f"{cog} is not loaded.")
        except commands.ExtensionNotFound:
            self.logger.error(f"{cog} not found.")
        except Exception as e:
            self.logger.error(f"Failed to unload {cog}: {e}")
            
    async def batch_cog_disable(self, cogs : list[str]):
        """
        Disable multiple cogs by their paths (Python module paths).
        Example: ["cogs.example_cog", "cogs.another_cog"]
        
        This method unloads the cogs and syncs the application commands.
        Avoids more Syncs.
        
        Args:
            cogs (list): A list of paths to the cogs to be unloaded.
        Raises:
            commands.ExtensionNotLoaded: If any cog is not loaded.
            commands.ExtensionNotFound: If any cog is not found.
            Exception: For any other exceptions that may occur.
        Returns:
            None
        """
        self.logger.debug(f"Attempting to unload {len(cogs)} cogs...")
        self.logger.debug(f"Cog list: {cogs}")
        self.logger.debug("Unloading cogs...")
        for cog in cogs:
            try:
                self.logger.debug(f"Unloading {cog}...")
                await self.unload_extension(cog)
                self.logger.info(f"Unloaded {cog} successfully.")
            except commands.ExtensionNotLoaded:
                self.logger.warning(f"{cog} is not loaded.")
            except commands.ExtensionNotFound:
                self.logger.error(f"{cog} not found.")
            except Exception as e:
                self.logger.error(f"Failed to unload {cog}: {e}")
        self.logger.info(f"Batch unloaded {len(cogs)} cogs successfully.")
        self.logger.debug("Syncing application commands...")
        await self.tree.sync()
        self.logger.debug("Synced application commands.")
        
    async def cog_reload(self, cog : str ):
        """
        Reload a cog by its path (Python module path).
        Example: "cogs.example_cog"
        
        This method reloads the cog and syncs the application commands.
        
        Args:
            cog (str): The path to the cog to be reloaded.
        Raises:
            commands.ExtensionNotLoaded: If the cog is not loaded.
            commands.ExtensionNotFound: If the cog is not found.
            Exception: For any other exceptions that may occur.
        Returns:
            None
        """
        try:
            await self.reload_extension(cog)
            self.logger.info(f"Reloaded {cog} successfully.")
            await self.tree.sync()
        except commands.ExtensionNotLoaded:
            self.logger.warning(f"{cog} is not loaded.")
        except commands.ExtensionNotFound:
            self.logger.error(f"{cog} not found.")
        except Exception as e:
            self.logger.error(f"Failed to reload {cog}: {e}")
            
    async def batch_cog_reload(self, cogs : list[str]):
        """
        Reload multiple cogs by their paths (Python module paths).
        Example: ["cogs.example_cog", "cogs.another_cog"]
        
        This method reloads the cogs and syncs the application commands.
        Avoids more Syncs.
        
        Args:
            cogs (list): A list of paths to the cogs to be reloaded.
        Raises:
            commands.ExtensionNotLoaded: If any cog is not loaded.
            commands.ExtensionNotFound: If any cog is not found.
            Exception: For any other exceptions that may occur.
        Returns:
            None
        """
        for cog in cogs:
            try:
                await self.reload_extension(cog)
                self.logger.info(f"Reloaded {cog} successfully.")
            except commands.ExtensionNotLoaded:
                self.logger.warning(f"{cog} is not loaded.")
            except commands.ExtensionNotFound:
                self.logger.error(f"{cog} not found.")
            except Exception as e:
                self.logger.error(f"Failed to reload {cog}: {e}")
        self.logger.info(f"Batch reloaded {len(cogs)} cogs successfully.")
        await self.tree.sync()
        
    async def on_ready(self):
        self.db.initialize_db()
        self.logger.info(f"Logged in as {self.user.name} - {self.user.id}") # type: ignore | self.user is not None unless called manually.
        self.logger.info("Latency: %s", self.latency)
        self.logger.info("Active Commands: %s", len(self.tree.get_commands()))
        self.logger.info("Active Guilds: %s", len(self.guilds))
        self.logger.info("Active Users: %s", len(self.users))
        self.logger.debug("Guilds: %s", [guild.name for guild in self.guilds])
        self.logger.debug("Cogs: %s", [cog for cog in self.cogs])
        self.logger.debug("Commands: %s", [command.name for command in self.tree.get_commands()])
        self.logger.info("------")
        await self.change_presence(activity=discord.Game(name="f!help"), status=discord.Status.dnd)
        self.logger.debug("Presence set to 'Playing f!help' with DND status.")
        self.logger.info("Bot is ready.")
        await self.batch_cog_enable(self.default_cogs)