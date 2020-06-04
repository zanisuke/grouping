import math,random
import discord


TOKEN = 'NzE3NzMzMjE4MzEyMjU3NTY3.Xteniw.VAJi41wKYuH9uV9h8xJlnSsppsg'

message_id = ''
member_cache = []

group_header_list = ['A','B','C','D','E','F','G','H','I','J','K']

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
    ch = client.get_channel(payload.channel_id)
    await ch.send("reaction!")
    await ch.send(message_id)
    await ch.send(payload.message_id)
    if (message_id == ''):
        return

    if payload.message_id == message_id:
        ch = client.get_channel(payload.channel_id)
        await ch.send("sample!")
        

# @client.event
# async def on_raw_reaction_remove(payload):
#     if payload.message_id == ID:
#         print(payload.emoji.name)

#         guild_id = payload.guild_id
#         guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
#         role = discord.utils.find(lambda r: r.name == payload.emoji.name, guild.roles)

#         if role is not None:
#             member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
#             await member.remove_roles(role)
#             print("done")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    split = message.content.split(' ')
    trigger = split[0]
    if trigger == 'grouping':
        grouping_method = split[1] if split[1:2] else ''
        grouping_number = int(split[2]) if split[2:3] and split[2].isdecimal() else ''

        if not grouping_method or not grouping_number:
            await message.channel.send('入力が正しくありません')
            return

        if grouping_method == 'direct':
            member = split[3].split(',')
            await grouping(member, grouping_number, message.channel)
        elif grouping_method == 'reaction':
            await message.channel.send('リアクショングルーピング')
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