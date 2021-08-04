import os
import discord
import random
from trie.Trie import Trie
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


client = discord.Client()
trie = Trie()
table = {
    "\"": None,
    "'": None,
    "-": None,
    "`": None,
    "~": None,
    ",": None,
    ".": None,
    ":": None,
    ";": None,
    "_": None
}


def buildTrie():
    file = open("trie/words.txt", 'r')

    for line in file:
        line = line.strip()
        trie.insert(line)


def punish_user(user_id):
    user_id = '<@' + str(user_id) + '>'
    responses = [
        "Hey {} shut up"
        "You pray with that mouth, {}?",
        "That's some colorful language, {}.",
        "Come on now, {}. Did you really need to say that?",
        "{} - It's not a good LANGUAGE!",
        "Hey now {}, watch your mouth.",
        "We don't use that kind of language here, {}."
        "Please {}, don't use this kind of slang"
        "Hey {}, Can you stop this"
        "{} You are not allowed to use that words here"
    ]

    choice = random.choice(responses)
    choice = choice.format(user_id)

    return choice


@client.event
async def on_ready():
    buildTrie()
    print("Trie is built. ready to read messages.")


@client.event
async def on_message(message):
    text = message.content
    text = text.translate(str.maketrans(table))
    author_id = message.author.id

    if author_id != 770954317926236160:
        isClean = True
        message_word_list = text.split()
        for word in message_word_list:
            if trie.search(word):
                isClean = False
                break
        if not isClean:
            await message.channel.send(punish_user(author_id))

keep_alive()
client.run(TOKEN)