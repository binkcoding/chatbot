import _json
import json
import random
from operator import index
from urllib.parse import uses_relative

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#Function to load conversations
def load_conversations(filename="dataset.json", encoding='utf 8'):
    try:
        with open(filename, 'r', encoding='utf 8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
#Function to save conversations
def save_conversations(conversations, filename="conversations.json"):
    with open(filename, 'w') as file:
        json.dump(conversations, file, indent=4)

#Function to learn from conversations
def learn_conversation(user_input):
    print("I'm not sure how to respond to that. What would you recommend as a response? ")
    bot_response = input("Bot: ")

    if user_input not in conversations:
        conversations[user_input] = []

    conversations[user_input].append(bot_response)
    save_conversations(conversations)

    return  bot_response

#Find response
def find_response(user_input):
    if user_input in conversations:
        return random.choice(conversations[user_input])

    #Not found in conversations
    return learn_conversation(user_input)

#Main loop
conversations = load_conversations("dataset.json")

while True:
    user_input = input("You: ").lower()

    #Exit code and chat
    if user_input == "exit":
        print("Thanks for chatting!")
        break

    #Get response based on input
    response = find_response(user_input)

    print(f"Bot: {response}")





