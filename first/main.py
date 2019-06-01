import os

from telegram import Bot, Update, User, Contact
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

from first.config import TG_TOKEN


FILE_NAME = 'audio_message'

def create_dir(dir_name):
    path_dir = os.path.join(os.getcwd(), dir_name)
    if not os.path.exists(path_dir):
        os.mkdir(path_dir)
    return path_dir


def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Wats up, bastard?!"
    )


def do_echo(bot: Bot, update: Update):
    text = update.message.text
    bot.send_message(
        chat_id=update.message.chat_id,
        text=f"'{ text }' and its all? You are pathetic! "
        f"And I know you ID - { update.message.from_user.id }. I'am coming."
    )


def do_voice(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text=f"{ update.message.from_user.first_name }, he-he, I got stuff to blackmailing on you."
    )
    file_id = update.message.voice.file_id
    newFile = bot.get_file(file_id)

    main_folder = create_dir('voice_messages')
    message_folder = create_dir(
        os.path.join(main_folder, f'{update.message.from_user.id}')
    )
    message_number = len([x for x in os.listdir(path=message_folder) if FILE_NAME in x])
    file_name = f'{ FILE_NAME }_{ message_number }.ogg'
    newFile.download(os.path.join(message_folder, file_name))


def unknown(bot: Bot, update: Update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Sorry, I didn't understand that command.")


def main():
    bot = Bot(
        token=TG_TOKEN,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler('start', do_start)
    message_handler = MessageHandler(Filters.text, do_echo)
    unknown_handler = MessageHandler(Filters.command, unknown)
    voice_handler = MessageHandler(Filters.voice, do_voice)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.dispatcher.add_handler(unknown_handler)
    updater.dispatcher.add_handler(voice_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
