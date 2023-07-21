from flask import Flask, render_template, request, jsonify
from characterai import PyCAI

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


# tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
# model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
client = PyCAI('c43e694469173dee86270d54d98fab46dee96885')

# Dog test: NOk05AzKadfMKlyLs5vFic1FSMtfZs-9oajfdf_An1g

char = 'NOk05AzKadfMKlyLs5vFic1FSMtfZs-9oajfdf_An1g'

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    return get_Chat_response(input)


def get_Chat_response(input):
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
        message = input

        data = client.chat.send_message(
            char, message, history_external_id=history_id, tgt=tgt
        )

        name = data['src_char']['participant']['name']
        text = data['replies'][0]['text']
        print(text)
        return text
    # Let's chat for 5 lines
    # for step in range(5):
    #     # encode the new user input, add the eos_token and return a tensor in Pytorch
    #     new_user_input_ids = tokenizer.encode(str(text) + tokenizer.eos_token, return_tensors='pt')
    #
    #     # append the new user input tokens to the chat history
    #     bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids
    #
    #     # generated a response while limiting the total chat history to 1000 tokens,
    #     chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    #
    #     # pretty print last ouput tokens from bot
    #     return tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)