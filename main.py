import math
import time
import random
import os
import discord

TOKEN = os.environ.get('TOKEN')
THUMBSUP_CODE_POINT = 128077
THUMBSDOWN_CODE_POINT = 128078
EYES_CODE_POINT = 128064
CLAP_CODE_POINT = 128079
PRAY_CODE_POINT = 128591

message_id = ''
member_cache = []

reaction_message_id = ''
is_reaction_method = False
reaction_group_count = 0
reaction_member = []

group_header_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']

client = discord.Client()

print(TOKEN)


async def grouping(member, num, channel):
    member_count = len(member)
    if member_count < num:
        await channel.send('※※人数に対してグループ数が多すぎます※※')
        return

    group_count = num
    group_number = math.ceil(member_count / num)
    random.shuffle(member)

    global group_header_list

    count = 0
    notify_message = ''
    for i in range(num):
        group_number = math.ceil(member_count / group_count)
        notify_message += '```[{0}グループ]\n'.format(group_header_list[i])
        for j in range(group_number):
            if (member[count:count+1]):
                notify_message += '・{0}\n'.format(member[count])
                count += 1
                member_count -= 1
        notify_message += '```\n'
        group_count -= 1
    notify_message += ''
    await channel.send(notify_message)

    global member_cache
    member_cache = member


async def clear_reaction_method(is_force=False, channel=None):
    global is_reaction_method
    global reaction_member
    global reaction_group_count
    is_reaction_method = False
    reaction_member.clear()
    reaction_group_count = 0
    if is_force:
        if channel != None:
            await channel.send('※※リアクショングルーピングを停止しました※※\n')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_raw_reaction_add(payload):
    global is_reaction_method
    if not is_reaction_method:
        return
    if payload.message_id != reaction_message_id:
        return

    ch = client.get_channel(payload.channel_id)
    if ord(payload.emoji.name) == THUMBSUP_CODE_POINT:
        user = await client.fetch_user(payload.user_id)
        global reaction_member
        reaction_member.append(user.name)

    if ord(payload.emoji.name) == EYES_CODE_POINT:
        global reaction_group_count
        await grouping(reaction_member, reaction_group_count, ch)
        await clear_reaction_method()

    if ord(payload.emoji.name) == THUMBSDOWN_CODE_POINT:
        await clear_reaction_method(True, ch)


@client.event
async def on_raw_reaction_remove(payload):
    global is_reaction_method
    if not is_reaction_method:
        return
    if payload.message_id != reaction_message_id:
        return

    global THUMBSUP_CODE_POINT
    if ord(payload.emoji.name) == THUMBSUP_CODE_POINT:
        user = await client.fetch_user(payload.user_id)
        global reaction_member
        if user.name in reaction_member:
            reaction_member.remove(user.name)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    split = message.content.split(' ')
    trigger = split[0]
    if trigger == 'grouping':
        global is_reaction_method
        if is_reaction_method:
            await clear_reaction_method(True, message.channel)

        grouping_method = split[1] if split[1:2] else ''
        grouping_number = int(
            split[2]) if split[2:3] and split[2].isdecimal() else ''

        if not grouping_method or not grouping_number:
            await message.channel.send('※※入力が正しくありません※※\n')
            return

        if grouping_method == 'direct':
            member = split[3].split(',')
            await grouping(member, grouping_number, message.channel)

        elif grouping_method == 'reaction':
            is_reaction_method = True
            mes = 'リアクションしたメンバーを{0}チームに分けます。\n'\
                '下記表に従ってリアクションしてください。\n'\
                '--------------------------------\n'\
                ':thumbsup:　参加希望\n'\
                ':eyes:　グルーピングを開始\n'\
                ':thumbsdown:　グルーピングを停止\n'\
                '--------------------------------'\

            mes = mes.format(grouping_number)
            send_message = await message.channel.send(mes)
            global reaction_message_id
            reaction_message_id = send_message.id
            global reaction_group_count
            reaction_group_count = grouping_number

        elif grouping_method == 'voice':
            if message.author.voice == None:
                await message.channel.send('※※{0}はボイスチャンネルに入っていません※※\n'.format(message.author.name))
                return
            member_list = []
            for mem in message.author.voice.channel.members:
                member_list.append(mem.name)
            await grouping(member_list, grouping_number, message.channel)

        elif grouping_method == 're':
            global member_cache
            member = member_cache
            await grouping(member, grouping_number, message.channel)

        else:
            await message.channel.send('※※サブアクションを検知できませんでした※※\n')

client.run(TOKEN)
