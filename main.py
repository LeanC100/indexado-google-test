from enum import Flag
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
import requests
from datetime import date, datetime
import time
import pymysql
# local 
import db
import articles
import search

def main():
    # crea una lista de articulos
    list_article= articles.createList()

    # inicia el programa
    PROGRAM=True
    while PROGRAM:    
        # bucle que se repetira hasta que se publique un nuevo articulo 
        new_article_published = False  
        while new_article_published == False:
            
            # crea una nueva lista de articulos
            new_list_article = articles.createList()

            # realiza una comparacion entre los 2 articulos para saber si se publico un nuevo articulo
            new_article_published = articles.comparationArticles(list_article,new_list_article)

            # si se publico un nuevo articulo
            if new_article_published:
                # 
                list_article = new_list_article.copy()

                # se definen las variables de los articulos
                article_title = new_list_article[1]
                article_publication_date =  new_list_article[0]     
                article_indexed= "NULL"
                article_indexed_difference= "NULL"

                sql = """INSERT INTO google_index_time (nota,date_pub,date_indx,diff) VALUES(""" + "'" + article_title + "','" + str(article_publication_date) + "'," + article_indexed  + "," + article_indexed_difference +  """)"""
                
                # conecta a base de datos
                cursor,con= db.connectDatabase()

                retorno_query = False
                while retorno_query != True:
                    
                    # ejecuta la query
                    retorno_query = db.executeQuery(cursor,con,sql)

                    if retorno_query == True:
                        indexed_google = False
                        
                        # bucle que se repetira hasta que el articulo se publique en Google 
                        while indexed_google == False:

                            indexed_google = search.google(article_title)

                            # si el articulo se indexo correctamente en google
                            if indexed_google:
                                article_indexed = datetime.now()

                                # hace una resta entre el tiempo indexado y el tiempo publicado del nuevo articulo
                                article_indexed_difference = article_indexed - article_publication_date
                            
                                # guarda en un archivo los datos time_article_indexed y time_article_index_google 
                                sql= """UPDATE google_index_time SET date_indx = """ + "'" + str(article_publication_date) + "'," + """ diff = """ + "'" + str(article_indexed_difference) + "'" + """ WHERE nota =""" + "'" + article_title + "'"

                                # conecta a base de datos
                                cursor,con= db.connectDatabase()

                                # chekea que todo se publicuque correctamente
                                db.executeQuery(cursor,con,sql)

    print("the end")

if __name__ == "__main__":
    main()