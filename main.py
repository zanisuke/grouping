import math
import random
import discord

TOKEN = ''

message_id = ''
member_cache = []

reaction_message_id = ''
is_reaction_method = False

group_header_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']

client = discord.Client()


async def grouping(member, num, channel):
    member_count = len(member)
    if member_count < num:
        await channel.send('人数に対してグループ数が多すぎます')
        return

    group_count = num
    group_number = math.ceil(member_count / num)
    random.shuffle(member)

    global group_header_list

    count = 0
    notify_message = ''
    for i in range(num):
        group_number = math.ceil(member_count / group_count)
        notify_message += '[{0} チーム]\n'.format(group_header_list[i])
        for j in range(group_number):
            if (member[count:count+1]):
                notify_message += '・{0}\n'.format(member[count])
                count += 1
                member_count -= 1
        notify_message += '\n'
        group_count -= 1
    await channel.send(notify_message)

    global member_cache
    member_cache = member


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_raw_reaction_add(payload):
    if not is_reaction_method:
        return
    if payload.message_id != reaction_message_id:
        return


@client.event
async def on_raw_reaction_remove(payload):
    if not is_reaction_method:
        return
    if payload.message_id != reaction_message_id:
        return


@client.event
async def on_message(message):
    global is_reaction_method
    if message.author == client.user:
        return

    split = message.content.split(' ')
    trigger = split[0]
    if trigger == 'grouping':
        grouping_method = split[1] if split[1:2] else ''
        grouping_number = int(
            split[2]) if split[2:3] and split[2].isdecimal() else ''

        if not grouping_method or not grouping_number:
            await message.channel.send('入力が正しくありません')
            return

        if grouping_method == 'direct':
            member = split[3].split(',')
            await grouping(member, grouping_number, message.channel)
        elif grouping_method == 'reaction':
            global reaction_message_id
            is_reaction_method = True
            mes = 'リアクションしたメンバーを{0}チームに分けます\n参加する人は:thumbsup:でリアクションしてください'
            mes = mes.format(grouping_number)
            reaction_message_id = await message.channel.send(mes).id
        elif grouping_method == 'channel':
            await message.channel.send('チャンネルグルーピング')
        elif grouping_method == 're':
            global member_cache
            member = member_cache
            await grouping(member, grouping_number, message.channel)
        else:
            await message.channel.send('サブアクションを検知できませんでした')

        # global message_id
        # message_id = mes.id

client.run(TOKEN)
