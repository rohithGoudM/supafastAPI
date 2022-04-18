import requests
from bs4 import BeautifulSoup

url = 'https://karpathy.medium.com/software-2-0-a64152b37c35'
headers = {'User-Agent':'https://developers.whatismybrowser.com/useragents/parse/1302411chrome-windows-blink'}

r = requests.get(url, headers=headers)

soup = BeautifulSoup(r.content, features="html.parser")
#soup = BeautifulSoup('<p>Back to the <a rel="index">homepage</a></p>', 'html.parser')
article = soup.find('div',class_ = 'ib ic id ie if')

#print(len(article))

insertArticle = {}
content=[]
heading=''
paras=[]
for child in article.descendants:
    #print(child.name)
    if child.name == 'h1':
        singleContent={}
        singleContent['heading']=child.text
        singleContent['paras']=[]
        singleContent['sub_headings']=[]
        content.append(singleContent)
        paras = []
    if child.name == 'p':
        content[-1]['paras'].append(child.text)

for item in content:
    print(item['heading'])
    print(len(item['paras']))

insertArticle['title'] = content[0]['heading']
insertArticle['paras'] = content[0]['paras']
insertArticle['content'] = content[1:]

print(insertArticle)
