
"""
Main module

- connects to a specified Telegram chat
- goes through a given range of message ids
- filters relevant messages only
- checks names from filtered messages with Volunteer.su
- messages a result back to a message of origin

"""
import re
import asyncio
from environs import Env
from telethon import TelegramClient, events
from schedule import run_pending, repeat, every
from Volunteer_project_Parser import Parser                  # my modul
from Volunteer_project_Volunteer import volunteer            # my modul

env = Env()
env.read_env()

def relevant(message: str) -> str:
    """
    delete extra spaces and an empty lines
    return data from between to flags:
    #медосмотр and От:
    """
    message = re.sub(r' *\n *', ' ',  message.replace('ё', 'е'))
    regex = re.compile(r'(?<=#check).*(?=От:)')
    return regex.search(message).group()

class Telegram:

    api_id = env.int("API_ID")
    api_hash = env("API_HASH")

    def __init__(self, min_id:int =0):
        self.messages_dict = {'ids':[], 'volunteer':{}}
        self.__min_id = min_id
        self.__max_id = min_id+50

    # connect to Telegram with your api and get data by ids range
    async def main(self):
        async with TelegramClient('my', self.api_id, self.api_hash) as client:
            all_messages = await client.get_messages("https://t.me/voluneer_project",
                                                     min_id=self.__min_id,
                                                     max_id=self.__max_id,
                                                     reverse=True)
            for message in all_messages:
                self.messages_dict['ids'].append(message.id)
                try:
                    # extract needed data from each relevant message
                    fit = relevant(message.message)
                    # find name
                    person_full_name = Parser(fit).parser('names').pop().lower()
                    # check name with Volunteer.ru
                    pay_attention = volunteer(person_full_name)

                    # message back a result
                    # back notes marked with hashtag #verdict
                    if len(pay_attention) > 0:
                        # case where we found something
                        self.messages_dict['volunteer'].update({message.id:pay_attention})
                        message_back = f"#verdict автоматической проверки на Волонтере:{pay_attention}."
                        await client.send_message("https://t.me/voluneer_project",
                                                  message_back, reply_to=message.id
                                                  )
                    else:
                        # in case we did not find anything
                        message_back = f"#verdict это тестирование автоматической проверки на Волонтере: все ОК."
                        await client.send_message("https://t.me/voluneer_project",
                                                  message_back, reply_to=message.id
                                                  )
                except:
                    pass

    def ids(self) -> list:
        return self.messages_dict['ids']

min_ind = 0

# set a timer
@repeat(every(1).minutes)
def main():
    global min_ind
    print('Main: started checking procedure...')
    get_info = Telegram(min_ind)
    asyncio.run(get_info.main())
    ind_list = get_info.ids()
    min_ind = max(ind_list) if len(ind_list) > 0 else min_ind
    print(f'min_id now: {min_ind}')
    print()

if __name__ == '__main__':
    while True:
        run_pending()


