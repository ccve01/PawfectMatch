import random
import json

import torch
from characterai import PyCAI
# client = PyCAI('c43e694469173dee86270d54d98fab46dee96885')
#
# # Dog test: NOk05AzKadfMKlyLs5vFic1FSMtfZs-9oajfdf_An1g
#
# char = 'NOk05AzKadfMKlyLs5vFic1FSMtfZs-9oajfdf_An1g'
#
# # Save tgt and history_external_id
# # to avoid making a lot of requests
# chat = client.chat.get_chat(char)
#
# history_id = chat['external_id']
# participants = chat['participants']
#
# # In the list of "participants",
# # a character can be at zero or in the first place
# if not participants[0]['is_human']:
#     tgt = participants[0]['user']['username']
# else:
#     tgt = participants[1]['user']['username']
#
# while True:
#     message = input('You: ')
#
#     data = client.chat.send_message(
#         char, message, history_external_id=history_id, tgt=tgt
#     )
#
#     name = data['src_char']['participant']['name']
#     text = data['replies'][0]['text']
#
#     print(f"{name}: {text}")
#     break
#


def get_response(msg):
    client = PyCAI('c43e694469173dee86270d54d98fab46dee96885')

    # Dog test: NOk05AzKadfMKlyLs5vFic1FSMtfZs-9oajfdf_An1g

    char = 'NOk05AzKadfMKlyLs5vFic1FSMtfZs-9oajfdf_An1g'

    # Save tgt and history_external_id
    # to avoid making a lot of requests
    chat = client.chat.get_chat(char)

    history_id = chat['external_id']
    participants = chat['participants']

    # In the list of "participants",
    # a character can be at zero or in the first place
    if not participants[0]['is_human']:
        tgt = participants[0]['user']['username']
    else:
        tgt = participants[1]['user']['username']

    while True:
        message = msg

        data = client.chat.send_message(
            char, message, history_external_id=history_id, tgt=tgt
        )

        name = data['src_char']['participant']['name']
        text = data['replies'][0]['text']

        # print(f"{name}: {text}")
        break
    return text



if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)

