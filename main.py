# -*- coding: utf-8 -*-
import os
import time
import cv2
import telebot
from ping3 import ping
from urllib.parse import urlparse

def get_screenshot(rtsp_url: str, filename: str):
    try:
        cap = cv2.VideoCapture(rtsp_url)

        ret, frame = cap.read()
        if cap.isOpened():
            _,frame = cap.read()
            cap.release() 
            if _ and frame is not None:
                # Создаем папку если вдруг нет
                try:
                    os.mkdir('images')
                except:
                    pass

                cv2.imwrite(f'images/{filename}.jpg', frame)
    except Exception as e:
        print(e)

def get_all_screenshots(cam_list: list):
    try:
        if len(cam_list) > 0:
            cam_num = 1
            for cam in cam_list:
                get_screenshot(cam, str(cam_num))
                cam_num += 1
        else:
            print('Нет списка видеокамер')
    except Exception as e:
        print(e)

def check_camera(rtsp_url: str) -> bool:
    # Функция чекает камеру на доступность
    try:
        o = urlparse(rtsp_url)
        res = ping(o.hostname)

        if (res != False) & (res != None):
            return True
        else:
            return False
    except:
        return False

if __name__ == "__main__":
    cam_list = [
        'rtsp://192.168.57.62:554',
        'rtsp://10.0.0.59:556',
    ]

    try:
        bot = telebot.TeleBot('1717737934:AAGUbRSwF0n3Mgm_kUs52B6MxYixFXd8MQM')
        
        @bot.message_handler(commands=['start'])
        def start_message(message):
            bot.send_message(message.chat.id, 'Привет! Напиши мне что угодно, я дам тебе обстановку в столовой')

        @bot.message_handler(content_types=['text'])
        def send_text(message):
            try:
                if message.text.lower() == 'игорь гей?':
                    bot.send_message(message.chat.id, 'Да')
                else:
                    bot.send_message(message.chat.id, 'Я не понял что ты мне написал, но сейчас скину тебе фотки со столовой')

                    # Убеждаемся что есть камеры которые надо скриншотить
                    if len(cam_list) > 0:
                        cam_num = 1
                        for cam in cam_list:
                            # Проверяем камеру на доступность, иначе переходим к следующей
                            if check_camera(cam):
                                filename = str(cam_num) + '.jpg'

                                # Проверяем есть ли файл на диске
                                if os.path.isfile(os.path.join('images', filename)):
                                    createdat = os.path.getmtime(os.path.join('images', filename))

                                    if (time.time() - createdat) > 60:
                                        print('Файл протух, делаем новый')
                                        get_screenshot(cam, str(cam_num))
                                
                                # Если файла нет, то делаем новый
                                else:
                                    get_screenshot(cam, str(cam_num))
                                
                                # Грузим файл в телегу
                                photo = open(os.path.join('images', filename), 'rb')
                                bot.send_photo(message.chat.id, photo)
                                photo.close()
                            else:
                                print(f'{cam} мертвая, пропускаем ее')
                            cam_num += 1
                    # Иначе ругаемся на пустой список камер
                    else:
                        bot.send_message(message.chat.id, 'Нет камер в списке для стопкадров')
            except Exception as e:
                pass

        bot.polling()
    except Exception as e:
        print(e)