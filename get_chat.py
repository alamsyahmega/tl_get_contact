from telethon.sync import TelegramClient
from telethon import functions, types
import csv

phone_number = "+62857xxx"

def create_csv():
    with open(f'{phone_number}_chat.csv', 'w', newline='') as f:
        fieldnames = ['room_id', 'room_name', 'sender_id', 'chat', 'time']
        thewritter = csv.DictWriter(f, fieldnames=fieldnames)
        thewritter.writeheader()

def insert_to_csv(data):
    with open(f'{phone_number}_chat.csv', 'a') as f:
        thewritter = csv.writer(f)
        thewritter.writerow(data)


client = TelegramClient(phone_number, api_id=1072074, api_hash="542c45e1f3b9417a974e6666d72051bf")


async def getChat():
    create_csv()
    rooms = await client.get_dialogs()
    for room in rooms:
        async for message in client.iter_messages(room.id, limit=2500):
            res = [room.id, room.name, message.from_id, message.message if message.message != None else '', message.date]
            insert_to_csv(res)
            

with client:
    client.loop.run_until_complete(getChat())
    print('finish')