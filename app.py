import os
import json
import requests
import gradio as gr
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained("inu-ai/alpaca-guanaco-japanese-gpt-1b", use_fast=False)
model = AutoModelForCausalLM.from_pretrained("inu-ai/alpaca-guanaco-japanese-gpt-1b").to(device)

def predict(system_msg, inputs, top_p, temperature, chat_counter, chatbot=[], history=[]):
    # ここでモデルを使って応答を生成する処理を実装します。
    # 必要に応じて、system_msg, top_p, temperature などのパラメータを使用して、
    # モデルの挙動を調整できます。

    # 以下のコードは、最初のコードの generate_response 関数を参考にしています。
    # 必要に応じて、この部分を変更してください。

    # 入力トークン数1024におさまるようにする
    for _ in range(8):
        input_text = prepare_input(system_msg, history, inputs)
        token_ids = tokenizer.encode(input_text, add_special_tokens=False, return_tensors="pt")
        n = len(token_ids[0])
        if n + MAX_ASSISTANT_LENGTH <= MAX_INPUT_LENGTH:
            break
        else:
            history.pop(0)
            history.pop(0)

    with torch.no_grad():
        output_ids = model.generate(
            token_ids.to(model.device),
            min_length=n,
            max_length=min(MAX_INPUT_LENGTH, n + MAX_ASSISTANT_LENGTH),
            temperature=temperature,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            bad_words_ids=[[tokenizer.unk_token_id]]
        )

    output = tokenizer.decode(output_ids.tolist()[0])
    formatted_output_all = format_output(output)

    response = f"Assistant:{formatted_output_all.split('応答:')[-1].strip()}"
    history.append(f"User:{inputs}".replace("\n", "\\n"))
    history.append(response.replace("\n", "\\n"))

    chat = [(history[i], history[i + 1]) for i in range(0, len(history) - 1, 2)]  # convert to tuples of list
    chat_counter += 1

    return chat, history, chat_counter

# 以下のコードは、最初のコードの Gradio インターフェイス部分を参考にしています。
# 必要に応じて、この部分を変更してください。

iface = gr.Interface(fn=predict, inputs=["text", "text", "slider", "slider", "number"], outputs=["text", "text", "number"])
iface.launch()
