from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from flask import Flask, request
from loguru import logger
import gradio as gr


semantic_cls = pipeline(Tasks.siamese_uie,
                          './model/iic/nlp_structbert_siamese-uninlu_chinese-base', model_revision='v1.0')

# out = semantic_cls(
#     input='标本类型:(右叶)部分肝切除标本 标本大小:13.1*12.0*6.5cm 肿瘤部位:距烧灼面切缘0.7cm，紧邻被膜 肿瘤大小:2灶，4.2*3.7*3.0cm 及2.1*1.5*1.4c 组织学类型:肝内见大片坏死、纤维组织增生及泡沫细胞聚集,局部见少量肝细胞肝癌残留，符合治疗后改变，待免疫组化 脉管内癌栓:有nMVI分级:M1 卫星结节:有n切缘:烧灼面切缘阴性 纤维化分级:S4 肿瘤病理分期(AJCC第8版):ypT2NxMxn其他:慢性胆囊炎，胆固醇性息肉，胆囊颈部淋巴结未见癌转移(0/1)',
#     schema={
#         '肿瘤大小是多少？': None
#     }
# )

out = semantic_cls(
	input='标本类型:(右叶)部分肝切除标本 标本大小:13.1*12.0*6.5cm 肿瘤部位:距烧灼面切缘0.7cm，紧邻被膜 肿瘤大小:2灶，4.2*3.7*3.0cm 及2.1*1.5*1.4c 组织学类型:肝内见大片坏死、纤维组织增生及泡沫细胞聚集,局部见少量肝细胞肝癌残留，符合治疗后改变，待免疫组化 脉管内癌栓:有nMVI分级:M1 卫星结节:有n切缘:烧灼面切缘阴性 纤维化分级:S4 肿瘤病理分期(AJCC第8版):ypT2NxMxn其他:慢性胆囊炎，胆固醇性息肉，胆囊颈部淋巴结未见癌转移(0/1)',
  	schema={
        '肿瘤大小是多少？': None
        }
)
print(out)