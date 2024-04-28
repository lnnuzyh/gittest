from modelscope.hub.snapshot_download import snapshot_download

model_dir = snapshot_download('ClueAI/PromptCLUE-base-v1-5', cache_dir='/home/zyh/NLP/model', revision='master')
#
# model_dir = snapshot_download('damo/nlp_structbert_zero-shot-classification_chinese-large', cache_dir='/home/zyh/NLP/model', revision='master')