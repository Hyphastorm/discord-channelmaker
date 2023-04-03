#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
channelmaker.py: Create, modify, or delete Discord channels and roles using CSV files.
Copyright (C) 2023 Hyphastorm <luke@hyphastorm.com>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import discord
from discord.ext import commands
import csv
import sys
import argparse

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

def read_channels_csv():
    channels_list = []
    with open('channels.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row:
                channel_name, channel_type, allowed_roles, category, topic = row[:5]
                channels_list.append({
                    'name': channel_name,
                    'type': channel_type,
                    'allowed_roles': allowed_roles.split(';'),
                    'category': category,
                    'topic': topic,
                })
    return channels_list



def read_roles_csv():
    roles_list = []
    with open(roles_csv, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            role_name, permissions = row
            permissions = permissions.split(';')
            roles_list.append((role_name, permissions))
    return roles_list

async def create_roles(guild, roles_list):
    created_roles = {}
    for role_name, permissions in roles_list:
        if role_name == "@everyone":
            role = guild.default_role
            print(f"Role found: {role.name}")
        else:
            role = await guild.create_role(name=role_name)
            print(f"Role created: {role.name}")
        created_roles[role_name] = role
    return created_roles

async def set_channel_permissions(channel, allowed_roles, created_roles):
    print(f"Setting channel permissions for channel {channel.name}")
    # Set the channel permissions for each allowed role
    for role_name in allowed_roles:
        role = created_roles.get(role_name)
        if role:
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = True
            await channel.set_permissions(role, overwrite=overwrite)
    print(f"Finished setting channel permissions for channel {channel.name}")

async def delete_all_categories(guild):
    for category in guild.categories:
        try:
            await category.delete()
            print(f"Category deleted: {category.name}")
        except Exception as e:
            print(f"Failed to delete category: {category.name}. Error: {e}")

async def delete_all_channels(guild):
    for channel in guild.channels:
        try:
            await channel.delete()
            print(f"Channel deleted: {channel.name}")
        except Exception as e:
            print(f"Failed to delete channel: {channel.name}. Error: {str(e)}")

async def delete_all_roles(guild):
    for role in guild.roles:
        if role != guild.default_role and role != guild.me.top_role:
            try:
                await role.delete()
                print(f"Role deleted: {role.name}")
            except Exception as e:
                print(f"Failed to delete role: {role.name}. Error: {str(e)}")
        else:
            print(f"Skipping deletion of role: {role.name}")

async def get_or_create_category(guild, category_name):
    category = discord.utils.get(guild.categories, name=category_name)
    if category is None:
        category = await guild.create_category(name=category_name)
    return category


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    # Replace GUILD_ID with the actual ID of the guild you want to create channels in
    guild = bot.get_guild(args.guild_id)

    if args.delete_categories:
        # Delete all existing categories
        await delete_all_categories(guild)    

    if args.delete_channels:
        # Delete all existing channels
        await delete_all_channels(guild)

    if args.delete_roles:
        # Delete all existing roles
        await delete_all_roles(guild)

    if args.create_roles:
        # Create roles
        roles_list = read_roles_csv(args.roles_csv)
        created_roles = await create_roles(guild, roles_list)

        if args.create_channels:
            # Create channels and set permissions
            channels_list = read_channels_csv(args.channels_csv)
            for channel_info in channels_list:
                channel_name = channel_info['name']
                channel_type = channel_info['type']
                allowed_roles = channel_info['allowed_roles']
                category_name = channel_info['category']
                topic = channel_info['topic']

                category = await get_or_create_category(guild, category_name)

                if channel_type == 'text':
                    channel = await guild.create_text_channel(name=channel_name, category=category, topic=topic)
                elif channel_type == 'voice':
                    channel = await guild.create_voice_channel(name=channel_name, category=category)
                else:
                    print(f"Invalid channel type '{channel_type}' for channel '{channel_name}'. Skipping channel creation.")
                    continue

                if channel is None:
                    print(f"Unable to find channel with name {channel_name}")
                else:
                    await set_channel_permissions(channel, allowed_roles, created_roles)

        await bot.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create Discord channels and roles from CSV files.")
    parser.add_argument('guild_id', type=int, help="The ID of the Discord guild.")
    parser.add_argument('--token', required=True, help="The Discord bot token.")
    parser.add_argument('--channels-csv', default='channels.csv', help="The path to the channels CSV file.")
    parser.add_argument('--roles-csv', default='roles.csv', help="The path to the roles CSV file.")
    parser.add_argument('--delete-categories', action='store_false', help="Delete all existing categories.")
    parser.add_argument('--delete-channels', action='store_false', help="Delete all existing channels.")
    parser.add_argument('--delete-roles', action='store_false', help="Delete all existing roles.")
    parser.add_argument('--create-roles', action='store_true', help="Create roles from the CSV file.")
    parser.add_argument('--create-channels', action='store_true', help="Create channels from the CSV file.")
    args = parser.parse_args()

    bot.run(args.token)