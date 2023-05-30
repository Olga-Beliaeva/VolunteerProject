"""
If you are experiensing a kind of
you-do-not-have-rights-sending-message-to-this-group problem
while message back to https://t.me/voluneer_project, try following:

- run Volunteer_project_Find_id.py

- find id of https://t.me/voluneer_project

- replace all https://t.me/voluneer_project by its id in Volunteer_project_Main.py

"""

from telethon import TelegramClient

api_id = '****'                 # your api_id
api_hash = '******************' # your api_hash
client = TelegramClient('my', api_id, api_hash)

async def main():

    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)


with client:
    client.loop.run_until_complete(main())