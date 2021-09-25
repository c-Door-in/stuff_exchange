import os
import telegram
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from main import Main

#from dotenv import load_dotenv


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет! Я помогу тебе обменять что-то ненужное на очень нужное. Чтобы разместить вещь к обмену нажми - 'Добавить вещь'." 
             "После этого тебе станут доступны вещи других пользователей. Нажми 'Найти вещь' и я пришлю тебе фотографии вещей для обмена." 
             "Понравилась вещь - нажми 'Обменяться', нет - снова нажимай 'Найти вещь'. Если кому-то понравится предложенная тобой вещь, то я" 
             "пришлю тебе контакты владельца.",
        reply_markup=create_menu(),
    )


def create_menu():
    buttons = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Добавить вещь'),
                KeyboardButton(text='Найти вещь'),
                KeyboardButton(text='Обменяться')
            ],
        ],
        resize_keyboard=True
    )        
    return buttons


def create_upload_menu():
    buttons = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Загрузить фото'),
                KeyboardButton(text='Загрузить название вещи'),
            ],
            [
                KeyboardButton(text='Назад')
            ]
        ],
        resize_keyboard=True
    )        
    return buttons    


def message_handler(update, context):
    if update.message.text == "Добавить вещь":
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Загрузите фото и название предмета", 
            reply_markup=create_upload_menu()
        )
    elif update.message.text == "Найти вещь":
        find_handler(update, context)
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Тут будет случайное фото", 
            reply_markup=create_menu()
        )
    elif update.message.text == "Обменяться":
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Тут будут контакты для обмена (после взаимного нажатия кнопки 'Обменяться'", 
            reply_markup=create_menu()
        )    
    elif update.message.text == "Загрузить фото":
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Загрузите фото",
            reply_markup=create_upload_menu()
        )
    elif update.message.text == "Назад":
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Вы снова в главном меню.", 
            reply_markup=create_menu()
        )    



def photo_handler(update, context):
    user_id = update.message.from_user.id # получаем user_id
    user = update.message.from_user # получаем юзера
    name = user.first_name # получаем имя
    main_class = Main(user_id, name)
    os.makedirs(f'users_img/{user_id}', exist_ok=True) # создаем категорию по user_id
    photo = update.message.photo[-1].get_file() # получаем фотку
    photo_id = photo.file_id
    path = 'users_img/{0}/{1}.jpg'.format(user_id, photo.file_unique_id) # путь к фотке
    caption = update.message.caption # получаем описание к фотке
    photo.download(path) # сохраняем фотку
    context.bot.send_message(
            chat_id=update.effective_chat.id,
            # text='Фотография загружена.',
            text=main_class.add_stuff(photo_id, name=caption),
            reply_markup=create_menu(),
        )



def find_handler(update, context):
    user_id = update.message.from_user.id # получаем user_id
    main_class = Main(user_id)
    if not main_class.authorization():
        print(user_id, bool(main_class.authorization()))
        update.message.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Сперва нужно добавить свою вещь.", 
            reply_markup=create_menu()
        )
    else:
        stuff_card = main_class.find_stuff()
        if not stuff_card:
            update.message.bot.send_message(
                chat_id=update.effective_chat.id, 
                text="Это пока все. Нажмите Найти, чтобы начать заново", 
                reply_markup=create_menu()
            )
        update.message.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo = stuff_card['image_id'], # photo_id из photo_handler
            caption = stuff_card['name'] # caption из photo_handler
        )
        

TOKEN = '2030294717:AAHT1K9GSqCM_U1xEMRs8eYN1doY1Cltbzk'
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=message_handler))
dispatcher.add_handler(MessageHandler(filters=Filters.photo, callback=photo_handler))

updater.start_polling()
updater.idle()