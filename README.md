 ChannelMaker

ChannelMaker is a command-line utility for managing Discord channels and roles using CSV files. It allows you to delete existing categories, channels, and roles, as well as create new roles and channels with specified permissions from CSV files.

## Installation

1. Install Python 3.6 or newer: https://www.python.org/downloads/
2. Install the `discord.py` library:

pip install discord.py
    Clone or download this repository.
Usage
To use ChannelMaker, you'll need a Discord bot token. Follow these instructions to create a bot and obtain its token.

Create your CSV files with the channels and roles you want to create. The expected format for the files is as follows:
Channels CSV
channel_name,channel_type,allowed_roles,category,topic
    channel_name: The name of the channel.
    channel_type: The type of the channel, either text or voice.
    allowed_roles: A semicolon-separated list of role names that are allowed to access the channel.
    category: The name of the category the channel belongs to.
    topic: (Optional) The topic of the channel, if it's a text channel.

Roles CSV
role_name,permissions
    role_name: The name of the role.
    permissions: A semicolon-separated list of permission names for the role. The list of available permissions can be found in the Discord API documentation.

Run ChannelMaker using the following command:
bash
python channelmaker.py GUILD_ID --token TOKEN [--channels-csv CHANNELS_CSV] [--roles-csv ROLES_CSV] [--delete-categories] [--delete-channels] [--delete-roles] [--create-roles] [--create-channels]
Replace GUILD_ID with the ID of the Discord guild (server) you want to manage and TOKEN with the Discord bot token. For more information on the available command-line options, see the man page provided in a previous response.

License
This program is licensed under the GNU General Public License version 3 (or later). See the LICENSE file for more details.