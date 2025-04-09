import _json
import json
import random
from operator import index
from urllib.parse import uses_relative

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def update_vectorizer():
    global all_patterns, tfidf_vectorizer

    all_patterns = []
    for intent in conversations.get("intents", []):
        all_patterns.extend(intent["patterns"])

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_vectorizer.fit(all_patterns)

#Function to load conversations
def load_conversations(filename="dataset.json", encoding='utf 8'):
    try:
        with open(filename, 'r', encoding='utf 8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

#Load conversations earlier to allow for intent
conversations = load_conversations("dataset.json")

#List of all patterns from dataset
all_patterns = []
for intent in conversations.get("intents", []):
    for pattern in intent ["patterns"]:
        all_patterns.append(str(pattern))

# Initialise TFIDF and fit vectorizer
tfidf_vectorizer = TfidfVectorizer()
#tfidf_vectorizer.fit(all_patterns)

#Function to save conversations
def save_conversations(conversations, filename="dataset.json"):
    with open(filename, 'w') as file:
        json.dump(conversations, file, indent=4)

#Function to learn from conversations
def learn_conversation(user_input):
    print("I'm not sure how to respond to that. What would you recommend as a response? ")
    bot_response = input("Bot: ")

    # Check if the user input is already in the conversations
    intent_exists = False
    for intent in conversations.get("intents", []):
        if user_input in intent["patterns"]:
            intent["responses"].append(bot_response)
            break
    # If the user input is not found in any existing intent, add it as a new intent
    else:
        new_intent = {
            "tag": user_input.replace("", "_"),
            "patterns": [user_input],
            "responses": [bot_response],
        }

        conversations["intents"].append(new_intent)

    save_conversations(conversations)
    update_vectorizer()
    return  bot_response

tfidf_vectorizer.fit(all_patterns)

#Find response
def find_response(user_input):
    best_match = None
    highest_similarity = 0.0

    for intent in conversations.get("intents", []):
        for pattern in intent["patterns"]:
            similarity = cosine_similarity(
                tfidf_vectorizer.transform([user_input]),
                tfidf_vectorizer.transform([pattern])
            )[0][0]

            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = intent

    if best_match and highest_similarity > 0.8:
        return random.choice(best_match["responses"])

    return learn_conversation(user_input)


#Main loop
#conversations = load_conversations("dataset.json")

while True:
    user_input = input("You: ").lower()

    #Exit code and chat
    if user_input == "exit":
        print("Thanks for chatting!")
        break

    #Get response based on input
    response = find_response(user_input)

    print(f"Bot: {response}")





