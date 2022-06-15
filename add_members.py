from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
import logging
import traceback
from telethon import errors

api_id = xxxxxxxxx
api_hash = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
phone = '+7xxxxxxxxxxx'
client = TelegramClient(phone, api_id, api_hash)

logging.basicConfig(filename='app.log', filemode='w', format='%(message)s')
 
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))
 
input_file = sys.argv[1]
users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
#        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)
 
chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)
 
for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue
 
print('Choose a group to add members:')
i=0
for group in groups:
    print(str(i) + '- ' + group.title)
    i+=1
 
g_index = input("Enter a Number: ")
target_group=groups[int(g_index)]
 
target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)
 
mode = int(input("Enter 1 to add by username or 2 to add by ID: "))
waittime = 10
print(len(users))
for user in users:
    
    try:
        print ("Adding {}".format(user['id']))
        logging.warning("Adding {} ,".format(user['id']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = client.get_entity(user['id'])
        else:
            sys.exit("Invalid Mode Selected. Please Try Again.")
        client(InviteToChannelRequest(target_group_entity,[user_to_add]))
        #client.send_message(user['id'], 'Hi! please join my group....')
        print("Waiting {} Seconds...".format(waittime))
        time.sleep(10)
    except PeerFloodError:
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        logging.warning("Flood")
        print(traceback.format_exc())
        exit()
    except UserPrivacyRestrictedError:
        print("The user's privacy settings do not allow you to do this. Skipping. Sending message")
        client.send_message(user['id'], 'Hi! please join my group....')
        logging.warning("privacy settings")
    except errors.FloodWaitError as e:
        print('Flood wait for ', e.seconds)
        time.sleep(e.seconds)
        
    except  errors.UsernameInvalidError:
        print('NAME ERROR')
    except:
        traceback.print_exc()
        print("Unexpected Error")
        logging.warning("Unexpected Error")
        print("Print traceback {} Seconds...".format(waittime))
        #print(traceback.format_exc())
        #exit()
        continue
        
        