import re
import gradio as gr

def search_text_after_keyword(text, keyword):
    pattern = re.compile(rf"{re.escape(keyword)}:[^，。' ']*")  # 构造正则表达式模式
    match = re.search(pattern, text)

    pattern = re.compile(rf"{re.escape(keyword)}[^，。' ']*")
    match2 = re.search(pattern, text)
    if match:
        return match.group(0)
    elif match2:
        return match2.group(0)
    else:
        return None

# text = "标本类型:右半结肠切除标本 标本大小小肠长12cm，大肠长28cm 肿瘤部位:距上切23cm, 下切10.5cm 大体类型:溃病型 肿瘤大小:76.6cm 溃病大小:6.66m，深1.5-3cm 组织学类型 :粘液腺癌 漫润累犯 : 浆膜下层，累犯神经 切缘 :上下切缘 : 阴性 淋巴结 : 见转移(1+/27) : 自检大肠旁(1+/25 )，另见2枚结节:小肠旁( 0/2 ) 其他 :1.慢性阑尾炎:2.( 右半结肠)管状腺瘤"
# keyword = "肿瘤部位"
# result = search_text_after_keyword(text, keyword)
# print("关键词后面的文本：", result)


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=4110)

    demo = gr.Interface(fn=search_text_after_keyword, inputs=["text","text"], outputs="text", title="易侕科研-模式匹配")
    demo.launch(show_api=False,server_name='0.0.0.0', server_port=4113)