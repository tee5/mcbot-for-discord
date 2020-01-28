#!/usr/bin/env python
# coding: utf-8

import re
import unicodedata
import logging
import socket
import requests
import discord
import datetime
import asyncio
import mcstatus
import conoha
from discord.ext import tasks


# TODO: あとで設定ファイルに書き出す
DISCORD_ACCESS_TOKEN = "XXXXXXXXXXXXXXXXXXXXX"
DISCORD_OAUTH2_URL = "https://discordapp.com/api/oauth2/authorize?client_id=XXXXXXXXXXXXXXX&permissions=8&scope=bot"
MINECRAFT_HOST_ADDRESS = "example.com"

# ログ出力に関する設定
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

class MinecraftStatus(object):
    def __init__(self, host_address):
        self.host_address = host_address
        self.server = mcstatus.MinecraftServer(host_address)

    def get_status(self):
        s = "```yaml\n"
        s += f"SERVER_ADDRESS: {self.server.host}\n"
        try:
            status = self.server.status()
            s += "SERVER_STATUS: ONLINE\n"
            s += f"SERVER_LATENCY: {int(status.latency)}ms\n"
            s += f"SERVER_VERSION: {status.version.name}\n"
            s += f"PLAYER_COUNT: {status.players.online}/{status.players.max}\n"
            s += "PLAYER_LIST:\n"
            if status.players.online:
                for player in status.players.sample:
                    s += f"- {player.name}\n"
        except Exception as e:
            s += "SERVER_STATUS: OFFLINE\n"
        s += "```"
        return s

    def get_activity(self):
        LARGE_GREEN_CIRCLE = '\U0001f7e2'
        LARGE_RED_CIRCLE   = '\U0001f7e5'
        status = self.server.status()
        if status == None:
            s = f"{LARGE_RED_CIRCLE} OFFLINE"
        else:
            s = f'{LARGE_GREEN_CIRCLE} ONLINE {status.players.online}/{status.players.max} {int(status.latency)}ms'
        return s


async def auto_update_activity(seconds=5):
    print(f"auto_update_activity() S")
    while True:
        print(f"auto_update_activity() loop S")
        activity = discord.Game(mc.get_activity())
        await client.change_presence(activity=activity)
        await asyncio.sleep(seconds)
        print(f"auto_update_activity() loop E")
    print(f"auto_update_activity() E")

@client.event
async def on_ready():
    print(f"on_ready() S")
    print(f"Logged in as [{client.user.name}][{client.user.id}]")
    await auto_update_activity()
    print(f"on_ready() E")

@client.event
async def on_message(message):
    print(f"on_message() S")

    # このBOTが投稿したメッセージは無視
    if message.author == client.user:
        print("message.author == client.user")
        return

    adjustesd_content = re.sub(" +", " ", message.content)
    words = adjustesd_content.split(" ")
    print(f"words: {words}")

    # このBOT宛のメンションの場合は、コマンドに応じた処理を実行
    if client.user in message.mentions:
        """ STATUS """
        if words[1].lower() in ("status", "s"):
            s = mc.get_status()
            await message.channel.send(s)
        """ REBOOT """
        if words[1].lower() in ("!start", "!s"):
            await message.channel.send(f"startは未実装。これから実装する。")
        if words[1].lower() in ("restart", "!r"):
            if mc.server.status().players.online:
                await message.channel.send("ログイン中のプレイヤーがいるため再起動できません")
            else:
                conoha_client = conoha.Conoha()
                conoha_client.restart()
                await message.channel.send("Minecraftサーバを再起動中")
        activity = discord.Game(mc.get_activity())
        await client.change_presence(activity=activity)
    print(f"on_message() E")

mc = MinecraftStatus(MINECRAFT_HOST_ADDRESS)
client.run(DISCORD_ACCESS_TOKEN)
