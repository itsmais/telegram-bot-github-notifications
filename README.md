# Send Telegram messages on GitHub push events ⚡

Tutorial on configuring GitHub Actions to notify on new code pushes in a Telegram bot.

<a href = "https://github.com/itsmais/telegram-bot-github-notifications">
<img src = "./header.png"/ alt="telegram and github logos">
</a>

## Table of content

- [Introduction and use case](#introduction-and-use-case)
- [Steps](#steps)
  - [1. Create a Telegram bot](#1-create-a-telegram-bot)
  - [2. Get the `chat_id`](#2-get-the-chat_id)
  - [3. Code: Telegram bot](#3-code-telegram-bot)
  - [4. Code: GitHub Action](#4-code-github-action)
  - [5. Passing secrets to Python](#5-passing-secrets-to-python)
- [Final notes](#final-notes)
- [References](#references)

## Introduction and use case

I am learning GitHub Actions. As I implemented them, I wrote this tutorial and left it here for future reference. GitHub Actions make a perfect use for my side project that involves a couple of people. We have a Telegram group where we would love to receive notifications when someone pushes new code.

## Steps

### 1. Create a Telegram bot

Go to [@botfather](https://t.me/botfather) and create a bot using the `/newbot` command. Go through the steps (naming the bot, adding description, etc.) Save the `token`.

### 2. Get the `chat_id`

In my case, I added the bot to a group and I want it to send updates there. So, to get the `chat_id` of that group, I go to
`https://api.telegram.org/botPUTYOURTOKENHERE/getUpdates` and look for the group id (e.g. `12345`) by matching the group name with `title` field.

```json
my_chat_member: {
    chat: {
    id: 12345,
    title: "Coding project",
    type: "group",
    all_members_are_administrators: true
}
```

### 3. Code: Telegram bot

I am not using a fancy Telegram python wrapper since the requirement is simple; only send a single notification message to a group chat. It is in written in Python. You can make it more customized to your use case, but remember that you need to add all new dependencies to the action's `yaml` steps file.

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

### 4. Code: GitHub Action

I placed the above script in `auto/main.py` in my project where I intend for the GitHub Action to run. Place the below `.yaml` file in `.github/workflows` under any name. For more on this, see the official documentation mentioned in the references below.

```yaml
name: Learning GitHub Actions
run-name: ${{ github.actor }} is sending a telegram notification ⚡
on: [push]
jobs:
  Learning-GitHub-Actions:
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

### 5. Passing secrets to Python

We should be storing the Telegram bot API token in an environment variable. If you choose to do that using GitHub Actions, you can first add it to the repository's Settings (see references below) and then pass it as an env variable to the script in the execution step. Example:

```yaml
jobs:
  Explore-GitHub-Actions:
    runs-on: ubuntu-latest
    steps:
      - name: execute py script
        env:
          SECRET_API_KEY: ${{ secrets.TELEGRAM_BOT_TOKEN }}
        run: python3 ./auto/main.py
```

In Python, you can do the usual `.get()` on env:

```py
import os

API_KEY = os.environ.get('SECRET_API_KEY')
```

## Final notes

Both the script `main.py` and the action `github-action.yml` can be found in this repo.

This project could improve in many areas. This includes the notification message that we receive on Telegram. For now, it is only `Your project NAME has a new code push!`. It would be nice to include details like the commit message, the author, commit id, and the branch.

## References

- [Official GitHub Actions tutorial](https://docs.github.com/en/actions/quickstart)
- [Finding `chat_id`](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id)
- [Adding secrets to GitHub Actions](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository)
