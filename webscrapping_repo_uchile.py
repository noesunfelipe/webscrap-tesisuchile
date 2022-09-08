#Import needed libraries
from bs4 import BeautifulSoup as bs
import requests as rq
import pygal
from IPython.display import display, HTML
import pandas as pd

a = "https://repositorio.uchile.cl/discover?rpp=100&etal=0&scope=/&group_by=none&page="
b = "&sort_by=score&order=desc&filtertype_0=type&filter_relational_operator_0=equals&filter_0=Tesis"

chunks = [(1,100),(100,200),(200,300),(300,412)]
#chunks = [(200,300),(300,412)]

for x,y in chunks:
  lista_pags = []
  final_link_list = []
  list_links = []
  titles = []
  autores = []
  descriptions =[]

  for i in range(x,y):
      lista_pags.append(a+str(i)+b)
      

  for list_link in lista_pags:
    try:
      page = rq.get(list_link).text
      soup = bs(page)
      for link in soup.find_all('a'):
          l = link.get('href')
          try:
              if len(l)==19:
                  list_links.append("https://repositorio.uchile.cl" + str(l))
          except:
              pass
      #print(len(list_links))
    except:
      pass


  lista_tesis = []

  for l_ in list_links:
      if l_ not in lista_tesis:
          lista_tesis.append(l_)

  for li in lista_tesis:
        try:
              page_te = rq.get(li).text
              soup_te = bs(page_te)
        except:
          "Error de conexión"
        
        try:
          for title in soup_te.find('h2', itemprop='name'):
            if title in titles:
              #print("record already in list")
              pass
            else:
              final_link_list.append(li)
              titles.append(title)
              #print(title)

              desc = soup_te.find('div', itemprop = 'description')


              author = soup_te.find('a', itemprop ="author")
              if author == None:
                author_none = "el documento " + str(title) + " no indica autor"
                if author_none in autores:
                  pass
                else:
                  autores.append(author_none)
              else: 
                author = author.get_text()
                if author in autores:
                  pass
                else:
                  autores.append(author + " ## " + title)

              if desc == None:
                texto_desc_none = "el documento " + str(title) + " no posee descripción"
                if texto_desc_none in descriptions:
                  #print("el texto ya se encuentra")
                  pass
                else:
                  descriptions.append(texto_desc_none)
              else:    
                if desc in descriptions:
                  #print("description already in list")
                  pass
                else:
                  descriptions.append(str(desc))
                  print(author + " ## " + title)

        except:
          #print("N/A")
          pass


  fixed_descriptions = []
  for i in descriptions:
    i = i.replace('''<div itemprop="description">''','')
    i = i.replace('''</div>''','')
    fixed_descriptions.append(i)



  df = pd.DataFrame(zip(titles, final_link_list, fixed_descriptions, autores), columns=['Títulos', 'Link al archivo', 'descripción de la tesis', "Autor/a"])

  path = "C:/Users/Felipe/df_final_" + str(x) + ".xlsx"
  df.to_excel(path)
