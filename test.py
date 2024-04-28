import requests

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
    response = requests.get(url,params=params)
    if response.status_code == 200:
        # 打印响应内容
        for item in response.json()['data']['content']:
            one_text = item['sentence']
            one_text = one_text.replace('\t',' ')
            one_text = one_text.replace('<em>', '')
            one_text = one_text.replace('</em>', '')
            all_text.append(one_text)
        return all_text
    else:
        print("请求失败:", response.status_code)


print(get_text('cancer'))