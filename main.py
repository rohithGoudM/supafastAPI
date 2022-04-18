#main.py
import string
from fastapi import FastAPI
from supabase import create_client, Client
from pydantic import BaseModel

app = FastAPI()

url = 'https://wfxqibzqdhmxfnumlkaw.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndmeHFpYnpxZGhteGZudW1sa2F3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY1MDE4MzAwMCwiZXhwIjoxOTY1NzU5MDAwfQ._aey16Mjl1m-hDJmM_H5kdv3PNmliJf1TS0cVf6zXCo'
supabase: Client = create_client(url, key)

class Heading(BaseModel):
    heading: str
    sub_headings: list[str] | None = None
    paras: list[str] | None = None

class Article(BaseModel):
    title: str
    content: list[Heading] | None = None
    paras: list[str] | None = None

@app.post("/createArticle/")
async def create_article(article: Article):
    s = article.title
    s = s.translate(str.maketrans('', '', string.punctuation))
    createdArticle = supabase.table('Articles').insert({'title':s}).execute()
    headings = []
    for item in article.content:
        contentItem = {}
        contentItem['title']=item.heading
        contentItem['article'] = createdArticle.data[0]['title']
        headings.append(contentItem)
    createdHeadings = supabase.table('Headings').insert(headings).execute()
    headingDictId = {}
    for head in createdHeadings.data:
        headingDictId[head['title']]=head['id']
    sub_headings = []
    paras = []
    for item in article.content:
        for paragraph in item.paras:
            paraItem = {}
            paraItem['body']=paragraph
            paraItem['heading_id']=headingDictId[item.heading]
            paras.append(paraItem)
        # for sub_head in item.sub_headings:
        #     sub_headingItem={}
        #     sub_headingItem['title'] = sub_head
        #     sub_headingItem['heading_id'] = headingDictId[item.heading]
        #     sub_headings.append(sub_headingItem)

    createdParas = supabase.table('Paragraphs').insert(paras).execute()
    # createdSubHeads = supabase.table('Headings').insert(sub_headings).execute()
    
    return {'art': createdArticle,'h1s':createdHeadings,'p':createdParas}

@app.get("/articles")
def themes():
    themes = supabase.table('Articles').select('*').execute()
    #print(themes['data'])
    return themes

@app.get("/textSearchArticles/{text}")
def textSearch(text: str = 'Software'):
    s = text
    s = s.translate(str.maketrans('', '', string.punctuation))
    s = '`'+s+'`'
    articles = supabase.table('Articles').select('*').textSearch('title',s)

@app.get("/aritcle/{title}")
def getArticle(title):
    s = title
    s = s.translate(str.maketrans('', '', string.punctuation))
    article = supabase.table('Articles').select('*').match({'title':s}).execute()
    return article

@app.get("/headings/{article_title}")
def monsters(article_title : str = None):
    s = article_title
    s = s.translate(str.maketrans('', '', string.punctuation))
    headings = supabase.table('Headings').select('*').eq('article',s).execute()
    return headings

@app.get("/paras/{heading_id}")
def paras(heading_id : int = 1):
    paras = supabase.table('Paragraphs').select('*').eq('heading_id',heading_id).execute()
    sub_headings = supabase.table('Headings').select('*').eq('heading_id',heading_id).execute();
    return {'paragraphs':paras,'sub_headings':sub_headings}
