from dotenv import load_dotenv
import os
from groq import Groq
from textblob import TextBlob


load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

client = Groq(api_key=GROQ_API_KEY)

def type_out_text(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.02)

def interact_with_user():
    print("Cai: Hi, I'm Cai! What's your name?")
    user_name = input("You: ")
    print(f"Cai: Nice to meet you, {user_name}! How are you doing today?")
    return user_name

def groq_prompt(prompt, user_name):
    sentiment = TextBlob(prompt).sentiment
    system_message = f"Hello, {user_name}! I'm here to support you."
    if sentiment.polarity > 0.5:
        system_message += "  That's great to hear! Let's explore that further."
    elif sentiment.polarity < -0.5:
        system_message += " I'm sorry to hear that. Let's work together to make things better."
    else:
        system_message += " How can I help you today?"

    convo = [
        {
            "role": "user",
            "content": prompt,
        },
        {
            "role": "system",
            "content": system_message
        }
    ]

    print("Cai is typing...")
    time.sleep(2)

    chat_completion = client.chat.completions.create(messages=convo, model='llama3-70b-8192', temperature=1.1)
    response = chat_completion.choices[0].message.content
    return response

if __name__ == "__main__":
    user_name = interact_with_user()
    print("By the way, whenever you feel like ending our chat, simply type 'exit'.")

    while True:
        prompt = input(f'{user_name}: ')
        response = groq_prompt(prompt, user_name)
        print('Cai:', end=' ')
        type_out_text(response)
        print()
        if prompt.lower() == "exit":
            print("Conversation ended.")
            break
