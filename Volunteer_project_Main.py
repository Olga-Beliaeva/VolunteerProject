
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
from datetime import date, datetime
from telethon import TelegramClient
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

def show_result(finding: list) -> str:
    " return a str from a list"
    if len(finding)==0:
        return 'we could not find anything on Volunteer.su'
    finding_str = ""
    for item in finding:
        finding_str += ' '.join(item)
        finding_str += '\n'
    return finding_str

class Telegram:

    api_id = env.int("API_ID")
    api_hash = env("API_HASH")

    def __init__(self, min_id: int = 0):
        self.messages_dict = {'ids':[], 'volunteer':{}}
        self.__min_id = min_id
        self.__max_id = min_id+50

    # connect to Telegram with your api and get data from the chat
    # by message id range
    async def main(self):
        async with TelegramClient('my', self.api_id, self.api_hash) as client:
            chat = await client.get_entity("https://t.me/voluneer_project")
            all_messages = await client.get_messages(chat,
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
                    show = show_result(pay_attention)
                    print(f'Main: check result is following: {show}')

                    # message back a result
                    # back notes marked with hashtag #verdict
                    if len(pay_attention) > 0:
                        # case where we found something
                        print('Main: sending message with INFO from Volunteer.su')
                        self.messages_dict['volunteer'].update(
                                                        {message.id: show}
                                                        )
                        message_back = f"#verdict Please pay attention to: {show}"
                        await client.send_message(chat,
                                                  message_back,
                                                  reply_to=message.id
                                                  )
                        print('Main: INFO message has been sent')
                    else:
                        # in case we did not find anything
                        print('Main: sending Ok message')
                        message_back = f"#verdict ОК.\
                        Nothing found for {person_full_name}"
                        await client.send_message(chat,
                                                  message_back,
                                                  reply_to=message.id
                                                  )
                        print('Main: OK message has been sent')
                except Exception as e:
                    # print(f'Main: {e}')
                    pass

    def ids(self) -> list:
        return self.messages_dict['ids']

min_ind = 0

# set a timer to collect messages from the chat
# with convinient time interval
@repeat(every().day().at("21:30"))
@repeat(every(1).minutes)
def main():
    global min_ind
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f'Main: request at {current_time}')
    print('Main: started checking procedure...')
    get_info = Telegram(min_ind)
    asyncio.run(get_info.main())
    ind_list = get_info.ids()
    min_ind = max(ind_list) if len(ind_list) > 0 else min_ind
    print(f'Main: min_id now is {min_ind}')
    print(f'Main: FYI -> {get_info.messages_dict["volunteer"]}')
    print()

if __name__ == '__main__':
    print('Date:', date.today())
    print('Main: please wait')
    while True:
        run_pending()
