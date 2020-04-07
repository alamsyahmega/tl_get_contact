from telethon.sync import TelegramClient
from telethon import functions, types
import csv

phone_number = "+62857xxx"

def create_csv(data):
    with open(f'{phone_number}_chat.csv', 'w', newline='') as f:
        fieldnames = ['room_id', 'room_name', 'sender_id', 'chat', 'time']
        thewritter = csv.DictWriter(f, fieldnames=fieldnames)
        thewritter.writeheader()

        for obj in data:
            thewritter.writerow({'room_id': obj['room_id'],'room_name': obj['room_name'], 'sender_id': obj['sender_id'], 'chat': obj['chat'], 'time': obj['time']})


client = TelegramClient(phone_number, api_id=1072074, api_hash="542c45e1f3b9417a974e6666d72051bf")


async def getChat():
    all_chat = []
    rooms = await client.get_dialogs()
    for room in rooms:
        async for message in client.iter_messages(room.id, limit=2500):
            res = {
                'room_id'   : room.id,
                'room_name' : room.name,
                'sender_id' : message.from_id,
                'chat'      : message.message if message.message != None else '',
                'time'      : message.date
            }
            all_chat.append(res)
    print('create and write to csv')
    create_csv(all_chat)


with client:
    client.loop.run_until_complete(getChat())
    print('finish')