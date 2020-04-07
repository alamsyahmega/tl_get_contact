from telethon.sync import TelegramClient
from telethon import functions, types
import csv
import re

phone_number = "+62857xxx"


def check_media_extension(mime_type):
    mimetype = ""
    media_type = mime_type
    try:
        if re.search("pdf", mime_type, re.IGNORECASE):
            mimetype=".pdf"
            media_type="document"
        elif re.search("webp", mime_type, re.IGNORECASE):
            mimetype=".webp"
            media_type="sticker"
        elif re.search("mpeg", mime_type, re.IGNORECASE):
            mimetype=".mp3"
            media_type="audio"
        elif re.search("mp3", mime_type, re.IGNORECASE):
            mimetype=".mp3"
            media_type="audio"
        elif re.search("mp4", mime_type, re.IGNORECASE):
            mimetype=".mp4"
            media_type="video"
        elif re.search("x-tgsticker", mime_type, re.IGNORECASE):
            mimetype=".x-tgsticker"
            media_type="sticker"
        elif re.search("png", mime_type, re.IGNORECASE):
            mimetype=".png"
            media_type="photo"
        elif re.search("ogg", mime_type, re.IGNORECASE):
            mimetype=".ogg"
            media_type="audio"
        elif re.search("spreadsheetml", mime_type, re.IGNORECASE):
            mimetype=".xlsx"
            media_type="document"
        elif re.search("excel", mime_type, re.IGNORECASE):
            mimetype=".xls"
            media_type="document"
        elif re.search("wordprocessingml", mime_type, re.IGNORECASE):
            mimetype=".docx"
            media_type="document"
        elif re.search("msword", mime_type, re.IGNORECASE):
            mimetype=".doc"
            media_type="document"
        elif re.search("ms-word", mime_type, re.IGNORECASE):
            mimetype=".docm"
            media_type="document"
        elif re.search("presentationml", mime_type, re.IGNORECASE):
            mimetype=".pptx"
            media_type="document"
        elif re.search("powerpoint", mime_type, re.IGNORECASE):
            mimetype=".ppt"
            media_type="document"
        elif re.search("zip", mime_type, re.IGNORECASE):
            mimetype=".zip"
            media_type="archive"
        elif re.search("rar", mime_type, re.IGNORECASE):
            mimetype=".rar"
            media_type="archive"
        elif re.search("7z", mime_type, re.IGNORECASE):
            mimetype=".7z"
            media_type="archive"
        elif re.search("text/plain", mime_type, re.IGNORECASE):
            mimetype=".txt"
            media_type="document"
        elif re.search("subrip", mime_type, re.IGNORECASE):
            mimetype=".srt"
            media_type="document"
        elif re.search("android.package", mime_type, re.IGNORECASE):
            mimetype=".apk"
            media_type="executable"
        elif re.search("executable", mime_type, re.IGNORECASE):
            mimetype=".exe"
            media_type="executable"
        else:
            mimetype=""
            media_type=mime_type
        
        return mimetype, media_type
    except:
        return mimetype, media_type


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
    try:
        create_csv()
        rooms = await client.get_dialogs()
        for room in rooms:
            async for message in client.iter_messages(room.id, limit=2500):
                try:
                    if message.media.document:
                        extension, media_type = check_media_extension(message.media.document.mime_type)
                        saved_file = f'{message.media.document.id}{extension}'
                except:
                    try:
                        if message.media.photo:
                            saved_file = f'{message.media.photo.id}.jpeg'
                    except:
                        pass

                try:
                    if message.media.document or message.media.photo:
                        await message.download_media(file=f"media/{saved_file}")
                        insert_to_csv([room.id, room.name, message.from_id, f'id_media: {saved_file}' ,message.date])
                except:
                    res = [room.id, room.name, message.from_id, message.message if message.message != None else '', message.date]
                    insert_to_csv(res)
    except  Exception as error:
        print(error)

with client:
    client.loop.run_until_complete(getChat())
    print('finish')