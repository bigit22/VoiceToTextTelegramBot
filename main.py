import speech_recognition
import telebot
import os

from datetime import datetime
from pydub import AudioSegment
from manage import API_TOKEN


class MyVoiceToTextTelegramBot:
    def __init__(self):
        self.token = API_TOKEN
        self.bot = telebot.TeleBot(self.token)
        print('VoiceToTextTelegramBot initialized.')
        print('Developed by Bigit22.')

        @self.bot.message_handler(commands=['help', 'start'])
        def say_hi(message):
            print(
                '---------------------------\n'
                f'Greetings with {message.chat.first_name} {message.chat.last_name}\n'
                f'Nickname: @{message.chat.username}\n'
                f'Premium: {message.from_user.is_premium}\n'
                f'IsBot: {message.from_user.is_bot}\n'
                f'Message received: {message.text}\n'
                '---------------------------\n'
            )
            print('Greetings')
            self.bot.send_message(message.chat.id, f'Sup, {message.chat.first_name}')

        @self.bot.message_handler(content_types=['text'])
        def say_hi(message):
            print(
                '---------------------------\n'
                f'Greetings with {message.chat.first_name} {message.chat.last_name}\n'
                f'Nickname: @{message.chat.username}\n'
                f'Premium: {message.from_user.is_premium}\n'
                f'IsBot: {message.from_user.is_bot}\n'
                f'Message received: {message.text}\n'
                '---------------------------\n'
            )
            self.bot.send_message(message.chat.id, f'Sup, {message.chat.first_name}')

        @self.bot.message_handler(content_types=['voice'])
        def transcript(message):
            filename = download_file(self.bot, message.voice.file_id)
            text = recognize_speech(filename)
            if text == 'Sup, try again, ':
                self.bot.send_message(message.chat.id, text + message.chat.first_name)
            else:
                self.bot.send_message(message.chat.id, text)
            print(
                '---------------------------\n'
                f'Time: {datetime.now().strftime("%I:%M%p %d %B %Y")}\n'
                f'Greetings with {message.chat.first_name} {message.chat.last_name}\n'
                f'Nickname: @{message.chat.username}\n'
                f'Premium: {message.from_user.is_premium}\n'
                f'IsBot: {message.from_user.is_bot}\n'
                f'Message received: {text} (voice message)\n'
                '---------------------------\n'
            )

    def run(self):
        self.bot.polling(none_stop=True)


def download_file(bot, file_id):
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    filename = file_id + file_info.file_path
    filename = filename.replace('/', '_')
    with open(filename, 'wb') as f:
        f.write(downloaded_file)
    return filename


def recognize_speech(oga_filename):
    wav_filename = oga_to_wav(oga_filename)
    recognizer = speech_recognition.Recognizer()
    with speech_recognition.WavFile(wav_filename) as source:
        wav_audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(wav_audio, language='ru')
    except Exception:
        try:
            text = recognizer.recognize_google(wav_audio, language='en')
        except Exception:
            text = 'Sup, try again, '
    delete_files(oga_filename, wav_filename)
    return text


def delete_files(oga, wav):
    if os.path.exists(oga):
        os.remove(oga)
    if os.path.exists(wav):
        os.remove(wav)


def oga_to_wav(filename):
    new_filename = filename.replace('.oga', '.wav')
    audio = AudioSegment.from_file(filename)
    audio.export(new_filename, format='wav')
    return new_filename
