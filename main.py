import xml.etree.ElementTree as ET
from xml.etree import ElementTree
import requests
from datetime import date, datetime
import time
from googlesearch import search
import csv

def main():
    # obtengo los dato de la URL y los trabformo en XML
    articles = requests.get('https://www.clarin.com/sitemaps/sitemap_google_news.xml')
    root=ElementTree.fromstring(articles.content)

    time_today=datetime.today().strftime('%Y-%m-%d')

    # itera cada articulo
    list_article= []
    for article in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
        for news in article.findall('{http://www.google.com/schemas/sitemap-news/0.9}news'):
            publication_date= news.find('{http://www.google.com/schemas/sitemap-news/0.9}publication_date').text

            day_update,b = publication_date.split('T')
            day_publication= datetime.strptime(day_update, '%Y-%m-%d').date()
            
            # si el articulo se publico hoy se añadira a una lista de articulos los datos => publication_date y title
            if str(day_publication) == str(time_today):
                list_article.append(publication_date)
                title= news.find('{http://www.google.com/schemas/sitemap-news/0.9}title').text
                list_article.append(title)

    # bucle que se repetira hasta que se publique un nuevo articulo en articles
    new_article = False  
    while new_article == False:
        articles = requests.get('https://www.clarin.com/sitemaps/sitemap_google_news.xml')
        root=ElementTree.fromstring(articles.content)

         # se crea una nueva iteracion de cada articulo
        list_article_aux=[]
        for article in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            for news in article.findall('{http://www.google.com/schemas/sitemap-news/0.9}news'):

                publication_date= news.find('{http://www.google.com/schemas/sitemap-news/0.9}publication_date').text
                day_update,b = publication_date.split('T')

                # pasa el publication_date(string) a un datetime
                hour_update,d = b.split('-')
                dia_y_hour_update=day_update+ ' ' + hour_update
                datetime_publication = datetime.strptime(dia_y_hour_update, '%Y-%m-%d %H:%M:%S')

                # si el articulo se publico hoy se añadira a una lista lista de articulos los datos => publication_date y title
                if str(day_update) == str(time_today):
                    list_article_aux.append(datetime_publication)
                    title= news.find('{http://www.google.com/schemas/sitemap-news/0.9}title').text
                    list_article_aux.append(title)

        # se compara el largo de los 2 articulos
        # en caso de que list_article_aux sea mas largo quiere decir que se publico un nuevo articulo
        if len(list_article) != len(list_article_aux):
            print("New article uploaded")
            index_google=False

            # bucle que se repetira hasta que el articulo se indexe en google 
            while index_google ==False:

                # realiza una busqueda especial en google 
                name_article= list_article_aux[1]
                google_query = str(f"site:www.clarin.com \" {name_article} \"")
                search_google = search(google_query, start=0,pause=2)

                # comprueba si se encontraron resultados en la busqueda realizada
                result = results_check(search_google)

                # guarda en un archivo los datos publication_date y title del nuevo articulo
                with open ('data.csv', 'w') as file:
                    writer = csv.writer(file, delimiter=';')
                    date=[str(list_article_aux[1]),str(list_article_aux[0])]
                    writer.writerows(date)

                # si no se encontro resultados seguira buscando
                if result is None:
                    print('Google indexed in process ...')
                else:
                    print('site indexed correctly')

                    time_article_indexed = datetime.now()

                    # hace una resta entre el tiempo indexado y el tiempo publicado del nuevo articulo
                    time_article_index_google = time_article_indexed - list_article_aux[0]
                
                    # guarda en un archivo los datos time_article_indexed y time_article_index_google 
                    with open ('data.csv', 'w') as file:
                        writer = csv.writer(file, delimiter=';')
                        date=[str(time_article_indexed),str(time_article_index_google)]
                        writer.writerows(date)

                    index_google=True

                    print(google_query)
                    print(time_article_indexed)
                    print(list_article_aux[0])
                    print( time_article_index_google)
                    return 0

                time.sleep(4) 
        else:
            print("Waiting for new articles ...")
            time.sleep(15) 


def results_check(result):
    try:
        return result
    except StopIteration:
        return None

if __name__ == "__main__":
    main()