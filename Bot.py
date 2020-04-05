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
    args = ['libreoffice', '--headless', '--convert-to', 'pdf:writer_pdf_Export', '--outdir', folder, source]
    process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=None)
    file = re.search('-> (.*?) using filter', process.stdout.decode())
    if file is None:
        raise Process(process.stdout.decode())
    else:
        return file.group(1)


class Process(Exception):
    def __init__(self, output):
        self.output = output


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                    text="Send me .doc, .docx or .odt and I'll convert them into .pdf.")


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text(str(context.error))


def listener(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                    text="I'm sorry, I don't understand you!"
                    "\nI'm able to reply with a PDF when you send me a .doc, .odt or docx file.")


def check_document(file_name):
    return file_name.endswith(('.docx', '.doc', '.odt'))


def get_destination_path(path, file_url):
    down_file = os.path.join(path, os.path.basename(file_url))
    new_file = os.path.join(path, os.path.splitext(
                os.path.basename(file_url))[0]) + '.pdf'
    return down_file, new_file


def document_saver(update, context):
    if update.message.document and check_document(update.message.document.file_name):
        last_document = update.message.document
        try:
            doc_file = context.bot.getFile(last_document.file_id)
            my_path = os.path.abspath(os.path.dirname(__file__))
            down, new = get_destination_path(my_path, update.message.document.file_name)
            doc = doc_file.download(down)
            convert_to(my_path, update.message.document.file_name)
            context.bot.send_message(chat_id=update.message.chat_id,
                            text='🔃 conversion for "%s" in progress!' % update.message.document.file_name)
            context.bot.send_document(chat_id=update.message.chat_id,
                              document=open(new, 'rb'))
            if os.path.exists(doc):
                os.remove(doc)
            if os.path.exists(new):
                os.remove(new)
        except Exception as e:
            logger.error('Error:%s' % e)
            context.bot.send_message(chat_id=update.message.chat_id,
                            text="Uh, oh! An error occured. Please try again.")
    else:
        context.bot.send_message(chat_id=update.message.chat_id,
                        text="I can convert only .docx, .doc or .odt files!")


def main():

    # Create handler
    updater = Updater(TOKEN, use_context=True)
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
