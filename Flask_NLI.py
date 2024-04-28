# -*- coding: utf-8 -*-
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from flask import Flask, request
from loguru import logger
import gradio as gr
import re
import json
import collections


# app = Flask(__name__)

def load_model():
    global ner_pipeline
    ner_pipeline = pipeline(Tasks.named_entity_recognition, './model/damo/nlp_raner_named-entity-recognition_chinese-base-cmeee', device='gpu')
    global semantic_cls
    semantic_cls = pipeline(Tasks.nli,
                            './model/iic/nlp_structbert_nli_chinese-large', device='gpu')

def greet(text):
    logger.info(text)
    text.replace('"', '')
    sentences = text.split("。")

    # sentence_list = re.split(r'[，。]', text)
    # sentences = [sentence.strip() for sentence in sentence_list if sentence.strip()]
    res = []
    for sentence in sentences:
        sym_list = []
        dis_list = []
        result = ner_pipeline(sentence.strip())
        output = result['output']
        for item in output:
            if item['type'] == 'dis':
                dis_list.append(item['span'])
            if item['type'] == 'sym':
                sym_list.append(item['span'])
        for sym in sym_list:
            out = semantic_cls(input=('患者'+sentence,'患者'+sym))
            if out['labels'][out['scores'].index(max(out['scores']))]== '中立':
                res.append('患者'+ sym + '不明' + '\n')
            elif out['labels'][out['scores'].index(max(out['scores']))]== '蕴涵':
                res.append('患者' + sym + '\n')
            else:
                res.append('患者无' + sym + '\n')
        for dis in dis_list:
            out = semantic_cls(input=(sentence, '患者有' + dis))
            if out['labels'][out['scores'].index(max(out['scores']))]== '中立':
                res.append('患者'+ dis + '不明' + '\n')
            elif out['labels'][out['scores'].index(max(out['scores']))]== '蕴涵':
                res.append('患者有' + dis + '\n')
            else:
                res.append('患者无' + dis + '\n')

    # return res

    res_text = ""
    for sentence in res:
        res_text += sentence
    return res_text


if __name__ == '__main__':
    load_model()
    # app.run(host="0.0.0.0", port=4110)

    demo = gr.Interface(fn=greet, inputs="text", outputs="text", title="易侕科研NLP平台-信息抽取")
    demo.launch(show_api=False,server_name='0.0.0.0', server_port=4115)