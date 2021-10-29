from xml.etree import ElementTree
import requests
from datetime import date, datetime
import time

def createList():
    # obtengo los datos de los articulos de la URL y los transforma en XML
    articles_content = requests.get('https://www.clarin.com/sitemaps/sitemap_google_news.xml')
    articles_of_URL=ElementTree.fromstring(articles_content.content)

    time_today=datetime.today().strftime('%Y-%m-%d')

    # se crea una nueva iteracion de cada articulo
    list_article= []         
    for articles in articles_of_URL.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
        for article_data in articles.findall('{http://www.google.com/schemas/sitemap-news/0.9}news'):

            publication_date= article_data.find('{http://www.google.com/schemas/sitemap-news/0.9}publication_date').text

            day_update,b = publication_date.split('T')
            day_publication= datetime.strptime(day_update, '%Y-%m-%d')

            # pasa el publication_date(string) a un datetime
            hour_update,d = b.split('-')
            dia_y_hour_update=day_update+ ' ' + hour_update
            datetime_publication = datetime.strptime(dia_y_hour_update, '%Y-%m-%d %H:%M:%S')

            # si el articulo se publico hoy se añadira a una lista de articulos los datos => publication_date y title
            if str(day_update) == str(time_today):
                list_article.append(datetime_publication)
                title= article_data.find('{http://www.google.com/schemas/sitemap-news/0.9}title').text
                list_article.append(title)
        
    return list_article

def comparationArticles(art1, art2):

    if len(art1) != len(art2):
        print('¡¡¡new article published!!! ')
        return True
    else:
        print("Waiting for new articles ...")
        time.sleep(10)        
        return False
