# telegram-bot-github-notifications
GitHub Actions to notify on new code pushes in a Telegram bot.

## Introduction and use case
I am learning about GitHub Actions. They make a perfect use for my side project with a couple of people. We have a Telegram group where we would love to receive notifications when someone pushes new code.

## Steps
#### 1. Create a Telegram bot
Go to [@botfather](https://t.me/botfather) and create a bot using the `/newbot` command. Go through the steps (naming the bot, adding description, etc.) Save the `token`.

#### 2. Get the `chat_id`
In my case, I added the bot to a group and I want it to send updates there. So, to get the `chat_id` of that group, I go to
`https://api.telegram.org/botPUTYOURTOKENHERE/getUpdates` and look for the group id (e.g. `12345`) by matching the group name with `title` field.

```
my_chat_member: {
    chat: {
    id: 12345,
    title: "Coding project",
    type: "group",
    all_members_are_administrators: true
},
```

#### 3. Code: Telegram bot
```py
import requests
API_KEY = 'TELEGRAM_BOT_API_KEY_GOES_HERE'
BASE_URL = f'https://api.telegram.org/bot{API_KEY}/'

def send_message(chat_id, text):
    url = BASE_URL + 'sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, json=data)
    return response.json()

def main():
    chat_id = 'CHAT_ID_GOES_HERE'
    text = 'Your project _____INSERT NAME_____ has a new code push!'
    send_message(chat_id, text)

if __name__ == '__main__':
    main()
```

#### 4. Code: GitHub Action
I placed the above script in `auto/main.py` in my project where I intend for the GitHub Action to run. Place the below `.yaml` file in `.github/workflows` under any name. For more on this, see the official documentation mentioned in the references below.

```yaml
name: GitHub Actions Demo
run-name: ${{ github.actor }} is sending a telegram notification ⚡
on: [push]
jobs:
  Explore-GitHub-Actions:
    runs-on: ubuntu-latest
    steps:
      - run: echo "The job was automatically triggered by a ${{ github.event_name }} event."
      - run: echo "The name of your branch is ${{ github.ref }} and your repository is ${{ github.repository }}."
      - name: Check out repository code
        uses: actions/checkout@v2
      - run: echo "The ${{ github.repository }} repository has been cloned to the runner."

      - name: start python
        uses: actions/setup-python@v2
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install requests

      - name: execute py script 
        run: python3 ./auto/main.py
```

#### 5. TODO: Explain how to use secrets instead of hardcoding the key

## References
- Official GitHub Actions tutorial https://docs.github.com/en/actions/quickstart
- Finding `chat_id` https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id
