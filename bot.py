import os
import telegram
from dotenv import load_dotenv
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from main import Main


def start(update, context):
    username = update.message.from_user.username
    if username == None:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Привет! У тебя не задан @username в Telegram. Для корректной работы бота тебе нужно задать его настройках профиля и снова нажать /start.",
            reply_markup=create_menu(),
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Привет! Я помогу тебе обменять что-то ненужное на очень нужное. Чтобы разместить вещь к обмену нажми - 'Добавить вещь'." 
                "После этого тебе станут доступны вещи других пользователей. Нажми 'Найти вещь' и я пришлю тебе фотографии вещей для обмена." 
                "Понравилась вещь - нажми 'Обменяться', нет - снова нажимай 'Найти вещь'. Нажал “обменяться”? - если владельцу вещи понравится"
                "что-то из твоих вещей, то я пришлю контакты вам обоим.",
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


def message_handler(update, context):
    if update.message.text == "Добавить вещь":
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Загрузите, пожалуйста, фото и подпись (caption) к предмету.",
            reply_markup=create_menu()
        )
    elif update.message.text == "Найти вещь":
        find_handler(update, context)
    elif update.message.text == "Обменяться":
        user_id = update.message.from_user.id # получаем user_id
        username = update.message.from_user.username
        main_class = Main(user_id)
        match = main_class.change_stuff()
        if match:
            user_stuff_card, owner_index, owner_username, owner_stuff_card = match
            user_msg_text = "BINGO!!! Вашу {0} хотят обменять на {1}".format(user_stuff_card['name'], owner_stuff_card['name'])
            owner_msg_text = "BINGO!!! Вашу {0} хотят обменять на {1}".format(owner_stuff_card['name'], user_stuff_card['name'])
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"{user_msg_text}. Напишите @{owner_username}", 
                reply_markup=create_menu()
            )
            update.message.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo = user_stuff_card["image_id"],
                caption = user_stuff_card["name"],
                reply_markup=create_menu(),
            )
            update.message.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo = owner_stuff_card["image_id"],
                caption = owner_stuff_card["name"],
                reply_markup=create_menu(),
            )
            context.bot.send_message(
                chat_id=owner_index, 
                text=f"{owner_msg_text}. Напишите @{username}", 
                reply_markup=create_menu()
            )
            update.message.bot.send_photo(
                chat_id=owner_index,
                photo = owner_stuff_card["image_id"],
                caption = owner_stuff_card["name"],
                reply_markup=create_menu(),
            )
            update.message.bot.send_photo(
                chat_id=owner_index,
                photo = user_stuff_card["image_id"],
                caption = user_stuff_card["name"],
                reply_markup=create_menu(),
            )
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text="Успешно добавлено в список желаний", 
                reply_markup=create_menu()
            )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Вы ввели неверную команду. Нажмите, пожалуйста, одну из кнопок ниже.",
            reply_markup=create_menu()
        )


def photo_handler(update, context):
    user_id = update.message.from_user.id # получаем user_id
    user = update.message.from_user # получаем юзера
    first_name = user.first_name # получаем имя
    username = user.username 
    main_class = Main(user_id, username, first_name)
    os.makedirs(f'users_img/{user_id}', exist_ok=True) # создаем категорию по user_id
    photo = update.message.photo[-1].get_file() # получаем фотку
    photo_id = photo.file_id
    path = 'users_img/{0}/{1}.jpg'.format(user_id, photo.file_unique_id) # путь к фотке
    caption = update.message.caption # получаем описание к фотке
    photo.download(path) # сохраняем фотку
    context.bot.send_message(
            chat_id=update.effective_chat.id,
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
            caption = stuff_card['name'], # caption из photo_handler
            reply_markup=create_menu(),
        )


def main():
    load_dotenv()
    tg_token = os.environ['TG_TOKEN']
    updater = Updater(tg_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=message_handler))
    dispatcher.add_handler(MessageHandler(filters=Filters.photo, callback=photo_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()