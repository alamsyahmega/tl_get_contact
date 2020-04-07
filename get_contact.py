from telethon.sync import TelegramClient
from telethon import functions, types
import csv

phone_number = "+62896xxx"


def create_csv(contacts):
    with open(f'{phone_number}_contact.csv', 'w', newline='') as f:
        fieldnames = ['user_id','first_name', 'last_name', 'username', 'phone']
        thewritter = csv.DictWriter(f, fieldnames=fieldnames)
        thewritter.writeheader()

        for obj in contacts:
            thewritter.writerow({'user_id': obj['user_id'],'first_name': obj['first_name'], 'last_name': obj['last_name'], 'username': obj['username'], 'phone': obj['phone']})


with TelegramClient(phone_number, api_id=1072074, api_hash="542c45e1f3b9417a974e6666d72051bf") as client:
    result = client(functions.contacts.GetContactsRequest(hash=0))

    list_contact = []
    for user in result.users:
        obj = {
            'user_id': user.id,
            'first_name': user.first_name if user.first_name else '',
            'last_name': user.last_name if user.last_name else '',
            'username': user.username if user.username else '',
            'phone': user.phone if user.phone else ''
        }
        list_contact.append(obj)

    create_csv(list_contact)
    print('finish')