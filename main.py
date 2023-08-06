import requests
import os

API_KEY = os.environ.get('SECRET_API_KEY')
BASE_URL = f'https://api.telegram.org/bot{API_KEY}/'


def send_message(chat_id, text):
    url = BASE_URL + 'sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, json=data)
    return response.json()


def main():
    chat_id = '12345'
    text = 'Your app has a new code push ⚡'
    send_message(chat_id, text)


if __name__ == '__main__':
    main()
