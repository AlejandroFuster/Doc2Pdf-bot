from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import logging
import subprocess
import re
import os
from Secrets import TOKEN

logging.basicConfig(
    format=u'%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


def convert_to(folder, source):
    args = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', folder, source]
    process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=None)
    file = re.search('-> (.*?) using filter', process.stdout.decode())
    if file is None:
        raise Process(process.stdout.decode())
    else:
        return file.group(1)


class Process(Exception):
    def __init__(self, output):
        self.output = output


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='Hello! Send me a DOC or DOCX file and I will try to convert it to PDF :)')


def error(bot, update, e):
    logger.warning(u'Update "%s" caused error "%s"' % (update, e))
    update.message.reply_text(e)


def listener(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="I'm sorry, I don't understand you!"
                    "\nI'm able to reply with a PDF when you send me a DOC or DOCX file")


def check_document(file_name):
    return file_name.endswith('.docx') or file_name.endswith('.doc')


def get_destination_path(path, file_url):
    down_file = os.path.join(path, os.path.basename(file_url))
    new_file = os.path.join(path, os.path.splitext(
                os.path.basename(file_url))[0]) + '.pdf'
    return down_file, new_file


def document_saver(bot, update):
    if update.message.document and check_document(update.message.document.file_name):
        last_document = update.message.document
        try:
            doc_file = bot.getFile(last_document.file_id)
            my_path = os.path.abspath(os.path.dirname(__file__))
            down, new = get_destination_path(my_path, update.message.document.file_name)
            doc = doc_file.download(down)
            convert_to(my_path, update.message.document.file_name)
            bot.sendMessage(chat_id=update.message.chat_id,
                            text='Converting "%s"!' % update.message.document.file_name)
            bot.send_document(chat_id=update.message.chat_id,
                              document=open(new, 'rb'))
            if os.path.exists(doc):
                os.remove(doc)
            if os.path.exists(new):
                os.remove(new)
        except Exception as e:
            logger.error('Error:%s' % e)
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="Error! :(")
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="I'm only able to convert DOCX and DOC files!")


def main():

    # Create handler
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Log errors
    dp.add_error_handler(error)

    # Handle messages
    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(MessageHandler(Filters.document, document_saver))
    dp.add_handler(MessageHandler(Filters.text, listener))

    # Start the Bot
    updater.start_polling()
    logger.info('Bot started')
    updater.idle()


if __name__ == '__main__':
    main()
