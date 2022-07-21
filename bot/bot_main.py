from aiogram import Bot, Dispatcher, types, executor
from pytube import YouTube
import os
from audio_cutter_bot.bot.config import token
import logging

logging.basicConfig(filename='audio_cutter_bot.log', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p',
                    encoding='utf-8', filemode='w', level=logging.INFO)

bot = Bot(token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def hello_message(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, f'Привет, {message.from_user.first_name}😉\nОтправь мне ссылку на YouTube видео🎬, '
                                    f'из которого ты хочешь вырезать ауодио дорожку.')


@dp.message_handler()
async def link_handler(message: types.Message):
    chat_id = message.chat.id
    message_user = message.text
    logging.info(f'Пользователь: {message.from_user.full_name}; id: {chat_id}; отправил: {message_user}')

    if message_user.startswith(('https://youtu.be/', 'https://www.youtube.com/')):
        url = message_user
        yt = YouTube(url)
        await bot.send_message(chat_id, f'*Начинаю загрузку*...⏱', parse_mode="Markdown")
        await run(yt, chat_id)
    else:
        await bot.send_message(chat_id, f'Извини, я умею вырезать аудио только из YouTube😉\n*Поделись ссылкой '
                                        f'на YouTube видео😎*', parse_mode="Markdown")


def editing_name_track(s: str):
    return ''.join([letter for letter in f'{s}' if letter not in '|/:;\?*!"<>'])


def download_audio(yt, path, name_audio):
    yt.streams.filter(only_audio=True).first().download(path, f'{name_audio}.mp3')


async def send_audio(chat_id, path, name_audio):
    with open(f"{path}\\{name_audio}.mp3", 'rb') as track:
        await bot.send_audio(chat_id, track)
        logging.info(f'id: {chat_id}; принял: {track}')
        await bot.send_message(chat_id,
                               f'Готово, наслаждайся😘\n\n<b>👨🏻‍💻Автор:</b> @RuslanGafarovEkb\n<b>💰Поддержать:</b> <code>2200700115793134</code> (Tinkoffbank)',
                               parse_mode='html')


def del_audio(path, name_audio):
    os.remove(f"{path}\\{name_audio}.mp3")


async def run(yt, chat_id):
    name_audio = editing_name_track(yt.title)
    path = "d:\\Python\\audio_cutter_bot"
    download_audio(yt, path, name_audio)
    await send_audio(chat_id, path, name_audio)
    del_audio(path, name_audio)


if __name__ == '__main__':
    logging.info('Старт')
    executor.start_polling(dp, skip_updates=True)
