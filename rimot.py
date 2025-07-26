#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os, asyncio
import random as ra
from pyrogram import Client, filters, errors
from pyrogram.raw import functions, types

bot_token = "8460243173:AAG4OWkmIxG_zw1zIdPm4W-sZswifrJHDEU"
sudo = [8139598502]
login_temp_list = {}

if not os.path.isdir('Rimots') : os.mkdir('Rimots')
if not os.path.isdir('downloads') : os.mkdir('downloads')
if not os.path.exists('downloads/time.txt') :
    with open('downloads/time.txt', 'w', encoding="utf-8") as file :
        file.write('5')

async def sleep(time):
    await asyncio.sleep(time)


def app_info() :
    with open('app_info.txt', 'r') as file :
        return ra.choice(file.read().split('\n')).split()

def getAccount() :
    return [f.split('.')[0] for f in os.listdir('Rimots') if os.path.isfile(os.path.join('Rimots', f))]

bot = Client(
    "bot",
    bot_token = bot_token,
    api_id = "9699912",
    api_hash = "0f58a9f709c476a346a2c8db1fce99f1"
)

@bot.on_message(filters.command(["start"]) & filters.chat(sudo))
def __start__(client, message):
    bot.send_message(message.from_user.id, '''welcome to rimote F300
Coded: @liknat

➕Add account ➕ 
1 <code>/coding</code> ➡️+9800000000
2 <code>/code</code> ➡️ 12345
3 password ➡️ </code>/pass<code> 12345..

📊 Account List 📊 
<code>/list</code>

❌Remove the account For rimote ❌
/kick +123456789

￣⁠￣⁠￣⁠￣⁠￣⁠￣⁠￣⁠￣⁠￣⁠￣⁠￣⁠￣⁠￣⁠￣⁠￣⁠￣
⚠️Run commands⚠️

🗂file
<code>/typer</code> [replay] too file 

💬 Caption 💬 
<code>/cap</code> TEXT

❗️Delete Caption ❗️
<code>/delcap</code>

⚪️Operation Join ⚪️
<code>/join</code> LINK  OR  ID

⚫️Operation Left⚫️
<code>/left</code> ID

🕠Speed🕠
<code>/sleep</code> ....

📛Runing 📛
<code>/run<code> -ID
Group super <code>/run</code> -100 ID

📬 Forward post Run 📬
<code>/forward</code> ID postLink

🛑Stop runing 🛑
<code>/stop</code>

🔃 return account 🔃
<code>/getcode</code> +12054789865

✏️Account Name ✏️
<code>/name</code> NAME

🗽Profile Accounts 🗽
<code>/set</code> (reply on photo) 


await client.send_message(
chat_id=message.chat.id,
text="support : @Chmeist _ @liknat",
reply_to_message_id=message.id,
parse_mode='html'
)


#account............................




@bot.on_message(filters.command('list') & filters.chat(sudo))
def getAccountList(client, message):
    accounts = getAccount()
    for session in accounts:
        with open('sessionList.txt', 'a', encoding='utf-8') as file:
            file.write(str(session) + '\n')
    if os.path.isfile('sessionList.txt'):
        bot.send_document(chat_id=message.chat.id, document='./sessionList.txt', caption='<b>🔅 لیست اکانت ها</b>', reply_to_message_id=message.message_id)
        os.unlink('sessionList.txt')
    else:
        message.reply(f'<b>empty!</b>', quote=True)




@bot.on_message(filters.regex('/coding ') & filters.chat(sudo))
def sendCode(client, message):
    phone_number = message.text.replace('/coding ', '').replace(' ', '').replace('+', '').replace('-', '')
    if os.path.isfile(f'Rimots/{phone_number}.session') :
        message.reply('<b>این شماره قبلا افزوده شده است❗️.</b>', quote=True)
    else :
        global login_temp_list
        random_api = app_info()
        login_temp_list['api_id'] = random_api[1]
        login_temp_list['api_hash'] = random_api[0]
        login_temp_list['phone_number'] = phone_number
        login_temp_list['client'] = Client(f'Rimots/{phone_number}', int(login_temp_list['api_id']), login_temp_list['api_hash'])
        try :
            login_temp_list['client'].connect()
            login_temp_list['response'] = login_temp_list['client'].send_code(phone_number)
        except errors.BadRequest :
            message.reply('<b>error !</b>', quote=True)
        else:
            message.reply(f'<b>code successful sent to {phone_number}✅.</b>', quote=True)




@bot.on_message(filters.regex('/code ') & filters.chat(sudo))
def setCode(client, message):
    telegram_code = message.text.split()[1].replace(' ', '').replace('-', '')
    global login_temp_list
    if len(login_temp_list.values()) == 0 :
        message.reply('<b>first use #coding.</b>', quote=True)
    else :
        try :
            login_temp_list['client'].sign_in(login_temp_list['phone_number'], login_temp_list['response'].phone_code_hash, telegram_code)
            login_temp_list['client'].disconnect()
            login_temp_list = {}
        except errors.SessionPasswordNeeded :
            password_hint = login_temp_list['client'].get_password_hint()
            message.reply(f'''seted cloud to add account.
            
            [گذر اکانت را با دستور مربوطه وارد کنید.]''', quote=True)
        except errors.BadRequest :
            message.reply('<b>خطایی رخ داد !</b>', quote=True)
        else:
            message.reply('<b>account added successful✅</b>', quote=True)




@bot.on_message(filters.regex('/cloud ') & filters.chat(sudo))
def set2FA(client, message):
    telegram_2fa_password = message.text.split()[1]
    global login_temp_list
    if len(login_temp_list.values()) == 0 :
        message.reply('<b>first use #coding.</b>', quote=True)
    else :
        try :
            login_temp_list['client'].check_password(telegram_2fa_password)
        except errors.BadRequest :
            message.reply('<b>wrong cloud.enter right cloud...</b>', quote=True)
        else:
            login_temp_list['client'].disconnect()
            login_temp_list = {}
            message.reply('<b>account added successful✅</b>', quote=True)




@bot.on_message(filters.regex('/kick ') & filters.chat(sudo))
def deleteAccount(client, message):
    phone_number = message.text.replace('/kick ', '').replace(' ', '').replace('+', '').replace('-', '')
    main_path = f'Rimots/{phone_number}.session'
    if not os.path.isfile(main_path) :
        message.reply('<b>❗️شماره در لیست وجود ندارد.</b>', quote=True)
    else :
        os.unlink(main_path)
        message.reply('<b>number kicked.</b>', quote=True)

#run.............................



@bot.on_message(filters.command('typer') & filters.chat(sudo))
def __SAVE__(client, message) :
    try :
        if message.reply_to_message.document.file_size / 1024 / 1024 <= 5 :
            bot.download_media(message.reply_to_message.document.file_id, file_name='file.txt')
            bot.send_message(message.chat.id, '''<b>typer saved successful✅</b>''', reply_to_message_id=message.reply_to_message.message_id, parse_mode='html')
    except :
        bot.send_message(message.chat.id, '''<b>error from typer❗️</b>''', reply_to_message_id=message.message_id, parse_mode='html')


@bot.on_message(filters.regex('/cap ') & filters.chat(sudo))
def __ADD__(client, message) :
    add = message.text.replace('/cap ', '')
    with open('downloads/caption.txt', 'w', encoding="utf-8") as file :
        file.write(add)
    bot.send_message(message.chat.id, '''<b>caption added successful✅</b>''', reply_to_message_id=message.message_id, parse_mode='html')


@bot.on_message(filters.regex('/time ') & filters.chat(sudo))
def __ADD__(client, message) :
    time = message.text.replace('/time ', '')
    with open('downloads/time.txt', 'w', encoding="utf-8") as file :
        file.write(time)
    bot.send_message(message.chat.id, '''<b>time seted successful✅</b>''', reply_to_message_id=message.message_id, parse_mode='html')




@bot.on_message(filters.regex('/join ') & filters.chat(sudo))
def __join__(client, message):
    link = message.text.split()[1].replace('@', '').replace('+', 'joinchat/')
    if len(getAccount()) == 0 :
        bot.send_message(message.from_user.id, f'<b>لطفا ابتدا در ریموت اکانت وارد کنید !</b>', reply_to_message_id=message.message_id, parse_mode='html')
    else :
        accs = len(getAccount())
        bot.send_message(message.from_user.id, f'<b>joining at...♻️</b>', reply_to_message_id=message.message_id, parse_mode='html')
        id = ''
        title = ''
        for session in getAccount() :
            info = app_info()
            try :
                with Client(f'Rimots/{session}', info[1], info[0]) as cli :
                    cli.join_chat(link)
                    get_chat = cli.get_chat(link)
                    title = get_chat.title
                    bot.send_message(message.from_user.id, f'<b>account [ {session} ] successful join at [ {title} ]</b>', reply_to_message_id=message.message_id, parse_mode='html')
                    asyncio.run(sleep(1))
            except :
                bot.send_message(message.from_user.id, f'<b>error at join [ {session} ]  ❗️</b>', reply_to_message_id=message.message_id, parse_mode='html')
        bot.send_message(message.from_user.id, f'<b>join finished✅</b>', reply_to_message_id=message.message_id, parse_mode='html')





@bot.on_message(filters.regex('/left ') & filters.chat(sudo))
def __left__(client, message):
    link = message.text.split()[1]
    if len(getAccount()) == 0 :
        bot.send_message(message.from_user.id, f'<b>کانتی در ریموت وجود ندارید !</b>', reply_to_message_id=message.message_id, parse_mode='html')
    else :
        accs = len(getAccount())
        bot.send_message(message.from_user.id, f'<b>left successful finished at...</b>', reply_to_message_id=message.message_id, parse_mode='html')
        id = 0
        for session in getAccount() :
            info = app_info()
            try :
                with Client(f'Rimots/{session}', info[1], info[0]) as cli :
                    get_chat = cli.get_chat(link)
                    title = get_chat.title
                    cli.leave_chat(link, delete=True)
                    bot.send_message(message.from_user.id, f'<b>account [ {session} ] successful left at [ {title} ] ✅</b>', reply_to_message_id=message.message_id, parse_mode='html')
                    asyncio.run(sleep(1))
            except :
                bot.send_message(message.from_user.id, f'<b>error at lefting [ {session} ]❗️.</b>', reply_to_message_id=message.message_id, parse_mode='html')
        bot.send_message(message.from_user.id, f'<b>left successful finished✅</b>', reply_to_message_id=message.message_id, parse_mode='html')




@bot.on_message(filters.regex('/run ') & filters.chat(sudo))
def __attack__(client, message) :
    link = message.text.split()[1]
    time2sleep = int(open('downloads/time.txt', 'r').read())
    if os.path.exists('stop') :
        os.unlink('stop')
    if os.path.exists('downloads/file.txt') == False :
        bot.send_message(message.chat.id, '''<b>first add typer...!</b>''', reply_to_message_id=message.message_id, parse_mode='html')
    else :
        bot.send_message(message.chat.id, '''<b>running started...✅</b>''', reply_to_message_id=message.message_id, parse_mode='html')
        with open('downloads/file.txt', 'r', encoding="utf-8") as mf : data = mf.read()
        while True:
            if os.path.exists('stop') :
                break
            for session in getAccount() :
                if os.path.exists('stop') :
                    break
                else:
                    line = ra.choice(data.split('\n')).strip()
                    if os.path.exists('downloads/caption.txt') :
                        with open('downloads/caption.txt', 'r', encoding="utf-8") as tfile :
                            line += '\n\n' + tfile.read()
                    info = app_info()
                    if line == None or len(line) < 2 :
                        continue
                    try :
                        with Client(f'Rimots/{session}', info[1], info[0]) as cli :
                            cli.send_message(link, line, parse_mode='html')
                        asyncio.run(sleep(time2sleep))
                    except :
                        continue
        bot.send_message(message.chat.id, f'running stoped at {link} successful✅</b>', reply_to_message_id=message.message_id, parse_mode='html')



@bot.on_message(filters.regex('/forward ') & filters.chat(sudo))
def __forward__(client, message) :
    link = message.text.split()[1]
    channel = message.text.split()[2].split('/')[3]
    msg_id = int(message.text.split()[2].split('/')[4])
    time2sleep = int(open('downloads/time.txt', 'r').read())
    if os.path.exists('stop') :
        os.unlink('stop')
    bot.send_message(message.chat.id, '''<b> running started...✅</b>''', reply_to_message_id=message.message_id, parse_mode='html')
    while True:
        if os.path.exists('stop') :
            break
        for session in getAccount() :
            if os.path.exists('stop') :
                break
            else:
                info = app_info()
                try :
                    with Client(f'Rimots/{session}', info[1], info[0]) as cli :
                        cli.forward_messages(link, channel, msg_id)
                    asyncio.run(sleep(time2sleep))
                except :
                    continue
    bot.send_message(message.chat.id, f'running stoped at {link} successful✅</b>', reply_to_message_id=message.message_id, parse_mode='html')




@bot.on_message(filters.command('stop') & filters.chat(sudo))
def __stop__(client, message) :
    with open('stop', 'w', encoding="utf-8") as file :
        file.write('yes')
    bot.send_message(message.chat.id, '''<b>stoped successful✅</b>''', reply_to_message_id=message.message_id, parse_mode='html')


@bot.on_message(filters.command('delcap') & filters.chat(sudo))
def __stop__(client, message) :
    if os.path.exists('downloads/caption.txt') :
        os.unlink('downloads/caption.txt')
    bot.send_message(message.chat.id, '''<b>caption deleted✅</b>''', reply_to_message_id=message.message_id, parse_mode='html')




@bot.on_message(filters.regex('/getcode ') & filters.chat(sudo))
def __code__(client, message):
    number = message.text.split()[1].replace(' ', '').replace('+', '')
    if not os.path.exists(f'Rimots/{number}.session') :
        bot.send_message(message.from_user.id, '''<b>  شماره مورد نظر وجود ندارد.</b>''', reply_to_message_id=message.message_id, parse_mode='html')
    else :
        try :
            info = app_info()
            with Client(f'Rimots/{number}', info[1], info[0]) as cli :
                text = cli.get_history(777000, limit=1)[0]['text']
                if text :
                    bot.send_message(message.from_user.id, text, reply_to_message_id=message.message_id, parse_mode='html')
                else :
                    bot.send_message(message.from_user.id, '''no messeage from telegram!!!''', reply_to_message_id=message.message_id, parse_mode='html')
        except :
            bot.send_message(message.from_user.id, '''<b>هنگام فراخوانی سشن خطایی رخ داد ❗️</b>''', reply_to_message_id=message.message_id, parse_mode='html')




@bot.on_message(filters.regex('/name ') & filters.chat(sudo))
def __name__(client, message):
    name = message.text.replace('/name ', '')
    if len(getAccount()) == 0 :
        bot.send_message(message.from_user.id, f'<b> ابتدا به ریموت اکانت اضافه کنید!</b>', reply_to_message_id=message.message_id, parse_mode='html')
    else :
        accs = len(getAccount())
        bot.send_message(message.from_user.id, f'<b>changing started...♻️</b>', reply_to_message_id=message.message_id, parse_mode='html')
        for session in getAccount() :
            info = app_info()
            try :
                with Client(f'Rimots/{session}', info[1], info[0]) as cli :
                    cli.update_profile(first_name=name, last_name="")
                    bot.send_message(message.from_user.id, f'<b>name account [ {session} ] changed to [ {name} ] successful ✅</b>', reply_to_message_id=message.message_id, parse_mode='html')
                    asyncio.run(sleep(1))
            except :
                bot.send_message(message.from_user.id, f'<b>error account[ {session} ] from joining❗️.</b>', reply_to_message_id=message.message_id, parse_mode='html')
        bot.send_message(message.from_user.id, f'<b>changing name successful finished ✅</b>', reply_to_message_id=message.message_id, parse_mode='html')



@bot.on_message(filters.command('set'))
def __profile__(client, message) :
    if len(getAccount()) == 0 :
        bot.send_message(message.from_user.id, f'<b>add account to remote first !</b>', reply_to_message_id=message.message_id, parse_mode='html')
    else :
        try :
            bot.download_media(message.reply_to_message.photo.file_id, file_name='photo.png')
        except :
            bot.send_message(message.chat.id, '''<b>error ❗️</b>''', reply_to_message_id=message.message_id, parse_mode='html')
        if os.path.exists('downloads/photo.png') :
            accs = len(getAccount())
            bot.send_message(message.from_user.id, f'<b>changing started for...️♻️</b>', reply_to_message_id=message.message_id, parse_mode='html')
            for session in getAccount() :
                info = app_info()
                try :
                    with Client(f'Rimots/{session}', info[1], info[0]) as cli :
                        cli.set_profile_photo(photo='downloads/photo.png')
                        bot.send_message(message.from_user.id, f'<b>profile seted [ {session} ] successful ✅</b>', reply_to_message_id=message.message_id, parse_mode='html')
                        asyncio.run(sleep(1))
                except :
                    bot.send_message(message.from_user.id, f'<b>error [ {session} ] ❗️</b>', reply_to_message_id=message.message_id, parse_mode='html')
            os.unlink('downloads/photo.png')
            bot.send_message(message.from_user.id, f'<b>changing finished successful ✅</b>', reply_to_message_id=message.message_id, parse_mode='html')


bot.run()
