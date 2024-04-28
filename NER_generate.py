from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from flask import Flask, request
from loguru import logger
import gradio as gr

def load_model():
    global ner_pipeline
    ner_pipeline = pipeline(Tasks.named_entity_recognition, './model/damo/nlp_raner_named-entity-recognition_chinese-base-cmeee')


def greet(input_text):
    logger.info(input_text)
    input_text = input_text.replace("\n", " ")
    logger.info(input_text)
    length = len(input_text)
    pre_end = 0
    pre_key = ""


    result = ner_pipeline(input_text.strip())
    output = result['output']
    # logger.info(output)
    out = dict()
    for item in output:
        if pre_end == 0:
            pre_key = item['span']
            pre_end = item['end']
            continue
        if pre_key in out:
            while pre_key in out:
                pre_key = pre_key + '@'
        out[pre_key] = input_text[pre_end:item['start']]
        pre_key = item['span']
        pre_end = item['end']

    out[pre_key] = input_text[pre_end:length]
    # return out
    outline = ""
    for key in out:
        outline += key
        outline += ' : '
        outline += out[key]
        outline += '\n'
    return outline

if __name__ == '__main__':
    load_model()
    # app.run(host="0.0.0.0", port=4110)

    demo = gr.Interface(fn=greet, inputs="text", outputs="text", title="易侕科研NLP平台-数值抽取")
    demo.launch(show_api=False,server_name='0.0.0.0', server_port=4113)