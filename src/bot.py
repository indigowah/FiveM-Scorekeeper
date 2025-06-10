import discord
from discord.ext import commands

import logging

import db.sqldb as database

import json

class Config:
    """
    Configuration class for the bot.
    
    This class is used to store configuration settings for the bot, such as default cogs.
    It inherits from Dict to allow easy access to configuration values.
    
    Attributes:
        default_cogs (list): A list of default cogs to be loaded when the bot starts.
    """
    default_cogs: list[str] = []
    class debug:
        """
        Configuration for debug-related settings.
        
        Attributes:
            enabled (bool): Whether debug mode is enabled.
            debug_commands (bool): Whether debug commands are enabled.
            debug_cogs (list[str]): A list of cogs to be loaded in debug mode.
        """
        enabled: bool = False
        debug_commands: bool = False
        debug_cogs: list[str] = ["devtools.ping", "devtools.latency", "devtools.cogs"]
    class gangs:
        """
        Configuration for gang-related settings.
        
        Attributes:
            max_gangs (int): The maximum number of gangs allowed.
            max_members_per_gang (int): The maximum number of members allowed in a gang.
            max_gangs_per_user (int): The maximum number of gangs a user can be part of.
        """
        name_length_limit: int = 20
        max_gangs: int = 100
    class war:
        """
        Configuration for war-related settings.
        
        Attributes:
            max_wars (int): The maximum number of wars allowed.
            max_wars_per_gang (int): The maximum number of wars a gang can be involved in.
        """
        updates: bool = False
        update_channel_id: int = 0

    def json_to_dict(self, json_str: str):
        """
        Convert a JSON string to a dictionary and import configuration settings.
        
        Args:
            json_str (str): A JSON string containing configuration settings.
        Returns:
            None
        """
        import json
        config_dict = json.loads(json_str)
        self.import_from_dict(config_dict)
        
    def dict_to_json(self, config_dict: dict) -> str:
        """
        Convert a dictionary to a JSON string.
        
        Args:
            config_dict (dict): A dictionary containing configuration settings.
        Returns:
            str: A JSON string representation of the configuration settings.
        """
        import json
        return json.dumps(config_dict, indent=4)
 
    def import_from_dict(self, config_dict: dict):
        """
        Import configuration settings from a dictionary.
        
        Args:
            config_dict (dict): A dictionary containing configuration settings.
        Returns:
            None
        """
        self.default_cogs = config_dict.get("default_cogs", [])
        debug_config = config_dict.get("debug", {})
        self.debug.enabled = debug_config.get("enabled", False)
        self.debug.debug_commands = debug_config.get("debug_commands", False)
        self.debug.debug_cogs = debug_config.get("debug_cogs", [])
        gangs_config = config_dict.get("gangs", {})
        self.gangs.name_length_limit = gangs_config.get("name_length_limit", 20)
        self.gangs.max_gangs = gangs_config.get("max_gangs", 100)
        war_config = config_dict.get("war", {})
        self.war.updates = war_config.get("updates", False)
        self.war.update_channel_id = war_config.get("update_channel_id", 0)
            
    def export_to_dict(self) -> dict:
        """
        Export configuration settings to a dictionary.
        
        Returns:
            dict: A dictionary containing the configuration settings.
        """
        dict = {
            "default_cogs": self.default_cogs,
            "debug": {
                "enabled": self.debug.enabled,
                "debug_commands": self.debug.debug_commands,
                "debug_cogs": self.debug.debug_cogs
            },
            "gangs": {
                "name_length_limit": self.gangs.name_length_limit,
                "max_gangs": self.gangs.max_gangs
            },
            "war": {
                "updates": self.war.updates,
                "update_channel_id": self.war.update_channel_id
            }
        }
                
        return dict
    
    def store_to_file(self, file_path: str):
        """
        Store the configuration settings to a file.
        
        Args:
            file_path (str): The path to the file where the configuration will be stored.
        Returns:
            None
        """
        with open(file_path, 'w') as f:
            f.write(self.dict_to_json(self.export_to_dict()))
            
    def load_from_file(self, file_path: str):
        """
        Load configuration settings from a file.
        
        Args:
            file_path (str): The path to the file from which the configuration will be loaded.
        Returns:
            None
        """
        with open(file_path, 'r') as f:
            config_dict = json.load(f)
            self.import_from_dict(config_dict)

class client(commands.Bot):
    def __init__(self, config: Config):
        self.config = config
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
        await self.batch_cog_enable(self.config.default_cogs + (self.config.debug.debug_cogs if self.config.debug.enabled else []))