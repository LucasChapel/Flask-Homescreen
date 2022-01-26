from flask import Flask
from flask import render_template, request, redirect, url_for, g
app = Flask(__name__)

import requests

from datetime import date
from datetime import datetime
import time as t

# Il faut installer la bibliothèque googlesearch dans le terminal
# grace à la commande pip3 install googlesearch-python
from googlesearch import search
from bs4 import BeautifulSoup


'''
#Les fonctions Google, get_page_tag et Resultats permettent le fonctionnement de la barre de recherche google
def Google(rech):
    """
    Cette fonction utilise la fonction search du module googlesearch et renvoie une
    liste d'url des 10 premiers résultats de la recherche ayant pout mot clé la
    chaine de caractères rech.
    str -> list
    """
    res=[]
    for j in search(rech, tld="co.in", num=10, stop=10, pause=2):
        res.append(j)
    return res

def get_page_tag(url):
    """
    Cette fonction renvoie le titre de la page dont l'url est mis en paramètre
    str -> str
    """
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    reqs.close()
    return soup.find_all('title')[0].get_text()



def Resultats(rech):
    """
    Cette fonction combine les fonctions Google(rech) et get_page_tag(url) pour renvoyer une
    liste de tuples contenant le titre et l'url des 10 premiers résultats de la recherche
    ayant pout mot clé la chaine de caractères rech.
    str -> list
    """
    rech=Google(rech)
    resultats=[]
    for e in rech[1:]:
        titre=get_page_tag(e)
        if titre is None or e is None:
            return resultats
        resultats.append((titre,e))
    return resultats
'''


def News():
    """
    Cette fonction utilise l'API de newsapi.org pour renvoyer un dictionnaire de tuples
    correspondant chacun à une actualité (chaque tuple comporte le titre et le lien vers
    la page de l'actualité en question)
    """

    dic_keys = {0 : "bc268229f63d4de19533cadf2f3b941f", 1: "6a5d80cb902049d593e3246e3e9831f4", 2: "ecb982394f5a48cb8872f382cce74f7a", 3: "4ebc93bdac1d453da78eaaf88fa22e9a"}

    query_params = {
      "country": "fr",
      "sortBy": "top",
      "apiKey": dic_keys[0]
    }
    titre_lien =[]
    url = 'https://newsapi.org/v2/top-headlines'

    i = 1
    while 'articles' not in requests.get(url, params=query_params).json().keys() and i<=(len(dic_keys)-1) :
        query_params["apiKey"] = dic_keys[i]
        i += 1

    if 'articles' in requests.get(url, params=query_params).json().keys():
        response = requests.get(url, params=query_params)
        response_json = response.json()
        for i in response_json['articles']:
            titre_lien.append((i['title'],i['url']))
            if len(titre_lien)==5:
                return titre_lien
        return titre_lien
    else:
        return [("erreur", "erreur")]


def Meteo():
    """
    Cette fonction utilise l'API de openweathermap.org pour renvoyer un dictionnaire comportant
    diverses données météorologiques de Paris (description, température, températures minimale et
    maximale, humidité, vitesse du vent, l'heure du coucher et du lever de soleil).
    """
    #METEO

    weather=requests.get('http://api.openweathermap.org/data/2.5/weather?q=Paris&appid=b3400d123044b7b491fe24e8aee5471d&lang=fr').json()

    description = weather['weather'][0]['description']
    description='Description : '+str(description)

    temp = weather['main']['temp'] #en kelvin
    temp-=273.15 #converti en celcius
    temp=round(temp,3)
    temp= str(temp)+'°C'

    temp_min = weather['main']['temp_min']
    temp_min-=273.15
    temp_min=round(temp_min,3)
    temp_min='Température minimale : '+str(temp_min)+'°C'

    temp_max = weather['main']['temp_max']
    temp_max-=273.15
    temp_max=round(temp_max,3)
    temp_max='Temérature maximale : '+str(temp_max)+'°C'

    humidity = weather['main']['humidity']
    humidity='Humidité : '+str(humidity)+'%'

    wind_speed = weather['wind']['speed']
    wind_speed='Vitesse du vent : '+str(wind_speed)+'m/s'

    sunrise = weather['sys']['sunrise']
    sunset = weather['sys']['sunset']

    #Dictionnaire METEO
    meteo = {"description": description, "temp": temp, "temp_min": temp_min, "temp_max": temp_max,  "humidity": humidity, "wind_speed": wind_speed, "sunrise": sunrise, "sunset": sunset}

    return meteo

def stats_covid():
    """
    Cette fonction utilise l'API de covid19api.com pour renvoyer un dictionnaire contenant
    le nombre de cas, le nombre de morts et le nombre de guérisons en rapport avec la COVID
    dans le monde.
    """
    #STATISTIQUES COVID
    donnees_Covid = requests.get('https://api.covid19api.com/summary').json()

    nb_cas = donnees_Covid["Global"]["TotalConfirmed"]
    nb_morts = donnees_Covid["Global"]["TotalDeaths"]
    nb_guerisons = donnees_Covid["Global"]["TotalRecovered"]

    #Dictionnaire Covid
    covid = {"cas": nb_cas, "morts": nb_morts, "guerisons": nb_guerisons}
    return covid


METEO  = Meteo()
NEWS = News()
STATS_COVID = stats_covid()
TIME_REF = 0

@app.route('/', methods = ['GET','POST'])
def index():
    global TIME_REF, METEO, NEWS, STATS_COVID

    if t.time() - TIME_REF >= 600:
        METEO = Meteo()
        NEWS = News()
        STATS_COVID = stats_covid()
        TIME_REF = t.time()

    #TEMPS
    today = date.today()
    today = today.strftime("%B %d, %Y")
    time = datetime.now()
    unixtime = t.time()
    current_time = time.strftime("%H:%M:%S")

    #Dictionnaire TEMPS
    time_dico = {"time": current_time, "date": today, "unixtime": unixtime}

    """
    #RECHERCHE GOOGLE
    form_res = request.form
    if "recherche" in form_res:
        rech = form_res["recherche"]
        results = Resultats(rech)
        return render_template("index.html", resultats_recherche = results, test1 = rech,test2 = results, time_dico = time_dico, meteo = METEO, covid = STATS_COVID, news = NEWS)
    """

    return render_template("index.html", time_dico = time_dico, meteo = METEO, covid = STATS_COVID, news = NEWS)


app.run(debug = True)
