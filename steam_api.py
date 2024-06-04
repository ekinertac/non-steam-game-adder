"""
steam_api.py
============

This module provides a class to interact with the Steam Web API for retrieving Steam IDs and app lists.

Classes
-------
SteamAPI
    A class to interact with the Steam Web API.

Functions
---------
None

Attributes
----------
BASE_URL : str
    The base URL for the Steam Web API.
APP_LIST_URL : str
    The URL for retrieving the list of all Steam applications.

Methods
-------
__init__(api_key)
    Initialize the SteamAPI class with the provided API key.

get_steam_id(username)
    Retrieve the Steam ID for a given username.

get_app_list()
    Retrieve the list of all Steam applications.

find_app_id(game_name)
    Find the Steam app ID for a given game name.

Notes
-----
- Ensure that the `requests` library is installed in your environment.
- The `get_app_list` method caches the app list after the first retrieval to optimize performance.

Example
-------
To retrieve the Steam ID for a username and find the app ID for a game:

from steam_api import SteamAPI

api_key = "your_steam_api_key"
steam_api = SteamAPI(api_key)

steam_id = steam_api.get_steam_id("username")
if steam_id:
    print(f"Steam ID: {steam_id}")
else:
    print("Steam ID not found.")

app_id = steam_api.find_app_id("game_name")
if app_id:
    print(f"App ID: {app_id}")
else:
    print("App ID not found.")
"""

import requests
import logging


class SteamAPI:
    """
    A class to interact with the Steam Web API for retrieving Steam IDs and app lists.
    """

    BASE_URL = "http://api.steampowered.com"
    APP_LIST_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"

    def __init__(self, api_key):
        """
        Initialize the SteamAPI class with the provided API key.

        Args:
            api_key (str): The API key for accessing the Steam Web API.
        """
        self.api_key = api_key
        self.app_list_cache = None

    def get_steam_id(self, username):
        """
        Retrieve the Steam ID for a given username.

        Args:
            username (str): The Steam username to retrieve the Steam ID for.

        Returns:
            str: The Steam ID if found, else None.
        """
        try:
            url = f"{self.BASE_URL}/ISteamUser/ResolveVanityURL/v0001/?key={self.api_key}&vanityurl={username}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            steam_id = data['response'].get('steamid')
            if steam_id:
                logging.info(
                    f"Retrieved Steam ID for username '{username}': {steam_id}"
                )
                return steam_id
            logging.warning(
                f"Steam ID not found for username '{username}'. Response: {data}"
            )
            return None
        except requests.RequestException as e:
            logging.error(f"Error retrieving Steam ID for username '{username}': {e}")
            return None

    def get_app_list(self):
        """
        Retrieve the list of all Steam applications.

        Returns:
            list: A list of dictionaries containing app information.
        """
        try:
            if not self.app_list_cache:
                response = requests.get(self.APP_LIST_URL)
                response.raise_for_status()
                data = response.json()
                self.app_list_cache = data['applist']['apps']
                logging.info("Retrieved Steam app list.")
            return self.app_list_cache
        except requests.RequestException as e:
            logging.error(f"Error retrieving Steam app list: {e}")
            return []

    def find_app_id(self, game_name):
        """
        Find the Steam app ID for a given game name.

        Args:
            game_name (str): The name of the game to find the app ID for.

        Returns:
            int: The app ID if found, else None.
        """
        if not game_name or game_name == "":
            return None

        apps = self.get_app_list()
        app_dict = {app['name'].lower(): app['appid'] for app in apps}

        app_id = app_dict.get(game_name.lower())
        if app_id:
            logging.info(f"Found app ID for game '{game_name}': {app_id}")
        else:
            logging.warning(f"App ID not found for game '{game_name}'.")

        return app_id


# Configure logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)
