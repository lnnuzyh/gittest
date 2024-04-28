from flask import Flask, request
import gradio as gr
import requests
from openai import OpenAI
from loguru import logger
import json

app = Flask(__name__)

static_history = [
    {"role": "system",
     "content": "你是一个医学研究领域的专家"}
]


def get_text(keyword, paragraph='Introduction', current=1, size=100, date=0, iFactor='0,12'):
    url = "https://www.pubmed.pro/api/pubmeddata/searchSentenceByParagraph"

    params = {
        "keyWord": keyword,
        "paragraph": paragraph,
        "current": current,
        "size": size,
        "date": date,
        "iFactor": iFactor
    }
    all_text = []
    idx = 1
    response = requests.get(url, params=params)
    if response.status_code == 200:
        # 打印响应内容
        for item in response.json()['data']['content']:
            one_text = item['sentence']
            one_text = one_text.replace('\t', ' ')
            one_text = one_text.replace('<em>', '')
            one_text = one_text.replace('</em>', '')
            all_text.append(str(idx) + '. ' + one_text + '\n')
            idx += 1
        return all_text
    else:
        print("请求失败:", response.status_code)


def load_model():
    global client
    client = OpenAI(
        api_key="sk-OuPRv7nTXTzVL7JJx40InNfCOjU8NXJwWnHCpFksSipe8epu",
        base_url="https://api.moonshot.cn/v1",
    )

    # static_history = [
    #     {"role": "system",
    #      "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"}
    # ]


@app.route("/generate", methods=["POST"])
def chat():
    data = request.get_json()
    keywords = data['keywords']
    paragraph = data['paragraph']
    current = data['current']
    size = data['size']
    date = data['date']
    iFactor = data['iFactor']

    history = static_history

    all_text = get_text(keywords, paragraph, current, size, date, iFactor)
    # out_text = ""
    logger.info(keywords + "语料请求成功，数量为" + str(len(all_text)))

    query = "下面是一些关于“" + keywords + "”的一些文献资料：\n"

    for one_text in all_text:
        query += one_text
        # out_text += one_text
    query = query + "请根据我提供的文献资料，总结一份关于“" + keywords + "”的文献汇总报告。包括：报告摘要、研究趋势分析、研究热点和争议点、未来研究方向、报告总结。用中文回答，字数尽量多一些，如果引用了我提供的参考文献，请在对应位置标注文献的编号。整个报告的末尾不要展示参考文献。"

    history += [{
        "role": "user",
        "content": query
    }]
    completion = client.chat.completions.create(
        model="moonshot-v1-128k",
        messages=history,
        temperature=0.3,
    )
    result = completion.choices[0].message.content
    logger.info("对话请求成功")
    logger.info(result)
    history += [{
        "role": "assistant",
        "content": result
    }]

    res = dict()
    res['message'] = '请求成功！'
    res['result'] = result
    res['all_text'] = all_text

    return json.dumps(res)


# def chat(keywords):
#     history = static_history
#
#     all_text = get_text(keywords)
#     out_text = ""
#     logger.info(keywords + "语料请求成功，数量为" + str(len(all_text)))
#
#     query = "下面是一些关于“"+ keywords +"”的一些文献资料：\n"
#
#     for one_text in all_text:
#         query += one_text
#         out_text += one_text
#
#     query = query + "请根据我提供的文献资料，总结一份关于“" + keywords + "”的文献汇总报告。包括：报告摘要、研究趋势分析、研究热点和争议点、未来研究方向、报告总结。用中文回答，字数尽量多一些，如果引用了我提供的参考文献，请在对应位置标注文献的编号。整个报告的末尾不要展示参考文献。"
#
#
#     history += [{
#         "role": "user",
#         "content": query
#     }]
#     completion = client.chat.completions.create(
#         model="moonshot-v1-128k",
#         messages=history,
#         temperature=0.3,
#     )
#     result = completion.choices[0].message.content
#     logger.info("对话请求成功")
#     logger.info(result)
#     history += [{
#         "role": "assistant",
#         "content": result
#     }]
#
#     return result, out_text


if __name__ == '__main__':
    load_model()
    # get_text('cancer','Introduction', 1, 100, 0, '0,12')
    app.run(host="0.0.0.0", port=4116)

    # demo = gr.Interface(fn=chat, inputs="text", outputs=["text","text"], title="易侕科研")
    # demo.launch(show_api=False,server_name='0.0.0.0', server_port=4116)
