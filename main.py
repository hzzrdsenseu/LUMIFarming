import time
import random
import pyautogui
import pyperclip
import keyboard


def send_message(message):
    # сохраняем буфер
    old_clipboard = pyperclip.paste()

    # вставляем сообщение
    pyperclip.copy(message)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")

    # восстанавливаем буфер
    pyperclip.copy(old_clipboard)


def message_scheduler(message_configs, micro_pause=0.5):

    print("5 секунд на подготовку. ESC — остановка.")
    time.sleep(5)

    now = time.time()

    # инициализация времени отправки
    for msg in message_configs:
        msg["next_time"] = now + random.uniform(0, msg.get("jitter", 0))

    while True:
        if keyboard.is_pressed("esc"):
            print("Остановлено пользователем")
            return

        current_time = time.time()

        # собираем все сообщения, которые пора отправить
        ready_messages = [
            msg for msg in message_configs
            if current_time >= msg["next_time"]
        ]

        # отправляем по очереди
        for msg in ready_messages:
            if keyboard.is_pressed("esc"):
                print("Остановлено пользователем")
                return

            send_message(msg["text"])

            # планируем следующую отправку с jitter
            jitter = msg.get("jitter", 0)
            next_delay = msg["interval"] + random.uniform(-jitter, jitter)
            next_delay = max(0, next_delay)

            msg["next_time"] = current_time + next_delay

            time.sleep(micro_pause)  # микропаузa

        time.sleep(0.1)  # разгрузка CPU


if __name__ == "__main__":
    """
    message_configs:
    [
        {"text": "Привет", "interval": 5, "jitter": 1},
        {"text": "Редкое сообщение", "interval": 15, "jitter": 3}
    ]

    micro_pause: задержка между сообщениями (если совпали по времени)
    """
    
    messages = [
        {"text": "/инфо баланс кто:@hzzrdbot", "interval": 3.5, "jitter": 1},
        # {"text": "/кубик ", "interval": 5, "jitter": 1},
        # {"text": "/снежок кого:@kaponikis", "interval": 70, "jitter": 3},
    ]

    message_scheduler(messages, micro_pause=0.7)