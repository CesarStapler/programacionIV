import requests

def getAll(url):
    next = url
    data = []
    while next:
        res = requests.get(next)
        res = res.json()
        next = res['next']
        for item in res['results']:
            data.append(item)
    return data

def AridPlanets(clima = 'arid'):
    movies = getAll('https://swapi.dev/api/films/')
    data = []
    for film in movies:
        for j in film['planets']:
            planet = requests.get(j).json()
            if planet['climate'] == clima:
                data.append(film['title'])
                break    
    return data

def LargestShip(url = 'https://swapi.dev/api/starships/'):
    ships = getAll(url)
    data = ships[0]
    for item in ships:
        if float(item['length'].replace(',', '')) > float(data['length'].replace(',', '')):
            data = item
    return data


def WookieSixthMovie():
    wookieInFilm = []
    wookie = requests.get('https://swapi.dev/api/species/?search=wookie').json()
    wookie = wookie['results'][0]['people']
    peopleOfFilm = requests.get('https://swapi.dev/api/films/6/').json()
    peopleOfFilm = peopleOfFilm['characters']
    for item in peopleOfFilm:
        for j in wookie:
            if item == j:
                wookieInFilm.append(j)
    return wookieInFilm

if __name__ == '__main__':
    movie = AridPlanets()
    ships = LargestShip()
    WookieInMovie = WookieSixthMovie()
    print('a) ¿En cúantas peliculas aparecen planetas cuyo clima sea árido?')
    print(len(movie))
    print('b) ¿Cúantos wookies aparecen en la sexta pelicula?')
    print(len(WookieInMovie))
    print('c) ¿Cúal es el nombre de la aeronave mas grande en toda la saga?')
    print(ships['name'])