import pathlib
import datetime
import time
import csv
from dataclasses import dataclass

# Función para convertir milisegundos de la reproducción a formato de tiempo HH:MM:SS
def ms_to_time(ms):
    seconds = (ms / 1000) % 60
    minutes = (ms / (1000 * 60)) % 60
    hours = (ms / (1000 * 60 * 60)) % 24

    return "%02d:%02d:%02d" % (hours, minutes, seconds)

# Creamos clase DTO que representa una fila.
# Ver https://realpython.com/python-data-classes
@dataclass
class SongsDto:
    track: str
    artist: str
    album: str
    duration_ms: int
    views: int
    likes: int
    uri: str
    url: str


def parse_csv() -> list:
    songs = []
    try:
        # Abrir el archivo csv usando path relativo desde este archivo Python
        with open(f"{pathlib.Path(__file__).parent.absolute()}/music.csv", 'r', encoding='utf-8') as file:
            # Usamos csv.DictReader que permite leer el archivo y parsear cada fila a un diccionario Python.
            # ver https://realpython.com/python-csv/
            csv_reader = csv.DictReader(file, delimiter=',')
            for row in csv_reader:
            # Parseamos cada row a la clase DTO. Lo agregamos a la lista
                song = SongsDto(
                    row['Track'],
                    row['Artist'],
                    row['Album'],
                    row['Duration_ms'],
                    row['Views'],
                    row['Likes'],
                    row['Url_spotify'],
                    row['Url_youtube'],
                )
                songs.append(song)
        return songs
    except (FileNotFoundError):
        print("File not found")
        exit(1)

def research(callback):
    search = input("Quieres realizar una nueva busqueda o acción (si/no): ").lower()
    if search == "si":
        callback()
    elif search == "no":
        print("Volviendo al menu...")
        time.sleep(1)
        menu()
        return
    else:
        print("Opción no válida, intenta nuevamente")
        time.sleep(1)
        research(callback)

def menu():
    songs = parse_csv()
    print("Bienvenido al buscador de canciones🎶")
    print("1. Buscar canciones por titulo o artista")
    print("2. Buscar canciones más populares de un artista")
    print("3. Insertar canciones")
    print("4. Buscar albumes y sus canciones por artista")
    print("5. Salir")
    option = input("Introduce el número de la opción que deseas: ")
    if option == "1":
        search_songs(songs)
    elif option == "2":
        top_songs_by_artist(songs)
    elif option == "3":
        pass
        #Formula para agregar canciones 
    elif option == "4":
        pass
        #Formula para buscar albumes y sus canciones por artista
    elif option == "5":
        print("Saliendo...")
        time.sleep(1)
        return
    else:
        print("Opción no válida, intenta nuevamente")
        time.sleep(1)
        menu()

if __name__ == '__main__':
    # Obtenemos lista de películas como una lista de DTOs
    songs = parse_csv()
    menu()

# Función para buscar canciones por nombre de canción o artista
def search_songs(songs):
    search_text = input("Introduce el nombre de la canción o artista: ").lower()
    matching_songs = [song for song in songs if search_text in song.track.lower() or search_text in song.artist.lower()]
    if not matching_songs:
        print("No se encontraron canciones que coincidan con tu búsqueda")
        time.sleep(1)
        search_songs(songs)
        return
    matching_songs.sort(key=lambda song: int(float(song.views)), reverse=True)

    results = [(song.artist, song.track, ms_to_time(int(float(song.duration_ms)))) for song in matching_songs]
    for artist, track, duration in results:
        print(f"Artista: {artist}, Canción: {track}, Duración: {duration}")
    
    research(search_songs(songs))

# Función para buscar las diez canciones más populares de un artista
def top_songs_by_artist(songs):
    artist = input("Introduce el nombre del artista: ").lower()
    artist_songs = [song for song in songs if song.artist.lower() == artist.lower()]
    if not artist_songs:
        print("No se encontraron canciones de ese artista")
        time.sleep(1)
        top_songs_by_artist(songs)
        return
    top_songs = sorted(artist_songs, key=lambda song: int(float(song.views)), reverse=True)[:10]

    for song in top_songs:
        artist = song.artist
        track = song.track
        duration = ms_to_time(int(float(song.duration_ms)))
        views = round(int(float(song.views)) / 1000000)
        print(f"Artista: {artist}, Canción: {track}, Duración: {duration}, Reproducciones: {views} millones")

    research(top_songs_by_artist(songs))
    
# def searchMovie_name():
#     name = input("Introduce el nombre de la plataforma o inicial de la misma: ")
#     movies = parse_csv()
#     name = name.lower()
#     count = 1
    
#     def research():
#         search = input("Quieres realizar una nueva busqueda (si/no): ").lower()
#         if search == "si":
#             searchMovie_name()
#         elif search == "no":
#             print("Volviendo al menu...")
#             time.sleep(1)
#             menu()
#         else:
#             print("Opción no válida, intenta nuevamente")
#             time.sleep(1)
#             research()
            
#     for movie in movies:
#         if movie.title.lower().startswith(name):
#             print(f"{count}. {movie.title}")
#             count += 1
#     research()
    
# def searchmovie_by_platform(movies):
#     platform = input("Introduce la plataforma a buscar (Netflix, Hulu, Prime Video, Disney Plus): ").lower()
#     matching_movies = []
#     for movie in movies:
#         if platform == "netflix" and movie.available_in_netflix:
#             matching_movies.append(movie)
#         elif platform == "hulu" and movie.available_in_hulu:
#             matching_movies.append(movie)
#         elif platform == "prime video" and movie.available_in_prime_video:
#             matching_movies.append(movie)
#         elif platform == "disney plus" and movie.available_in_disney_plus:
#             matching_movies.append(movie)
#     if not any([platform in ["netflix", "hulu", "prime video", "disney plus"]]):
#         print("Platarforma no encontrada, intenta nuevamente con una de las opciones válidas (Netflix, Hulu, Prime Video, Disney Plus)")
#         time.sleep(1)
#         searchmovie_by_platform(movies)
#         return
    
#     def get_movie_rating(movie):
#         if '/' in movie.rating:
#             rating = movie.rating.split('/')[0]
#             return int(rating)
#         else:
#             return 0


#     matching_movies.sort(key=get_movie_rating, reverse=True)
#     for movie in matching_movies[:10]:
#         print(f"{movie.title} está disponible en {platform.capitalize()} con una puntuación de {movie.rating}")
    
#     def research():
#         search = input("Quieres realizar una nueva busqueda (si/no): ").lower()
#         if search == "si":
#             searchmovie_by_platform(movies)
#         elif search == "no":
#             print("Volviendo al menu...")
#             time.sleep(1)
#             menu()
#             return
#         else:
#             print("Opción no válida, intenta nuevamente")
#             time.sleep(1)
#             research()
    
#     research()
    
# def searchmovie_by_age(movies):
#     age = input("Introduce la edad que quieres buscar (+7, +13, +16, +18, all): ").lower()
#     matching_movies = []
#     for movie in movies:
#         if age == "all" and movie.age == "all":
#             matching_movies.append(movie)
#         elif age in ["+7", "7+", "7"] and movie.age in ["+7", "7+"]:
#             matching_movies.append(movie)
#         elif age in ["+13", "13+", "13"] and movie.age in ["+13", "13+"]:
#             matching_movies.append(movie)
#         elif age in ["+16", "16+", "16"] and movie.age in ["+16", "16+"]:
#             matching_movies.append(movie)
#         elif age in ["+18", "18+", "18"] and movie.age in ["+18", "18+"]:
#             matching_movies.append(movie)
#     if not any([age in ["+7", "7+", "7", "+13", "13+", "13", "+16", "16+", "16", "+18", "18+", "18", "all"]]):
#         print("Edad no encontrada, intenta nuevamente con una de las opciones válidas (+7, +13, +16, +18, all)")
#         time.sleep(1)
#         searchmovie_by_age(movies)
#         return
#     def get_movie_rating(movie):
#         return movie.rating
    
#     matching_movies.sort(key=get_movie_rating, reverse=True)
#     for movie in matching_movies[:10]:
#         print(f"{movie.title} está disponible con una puntuación de {movie.rating}")
    
#     def research():
#         search = input("Quieres realizar una nueva busqueda (si/no): ").lower()
#         if search == "si":
#             searchmovie_by_age(movies)
#         elif search == "no":
#             print("Volviendo al menu...")
#             time.sleep(1)
#             menu()
#             return
#         else:
#             print("Opción no válida, intenta nuevamente")
#             time.sleep(1)
#             research()
    
#     research()

# def add_movie(movies):
#     new_movie = []
#     new_movie.append(input("Ingrese el título de la película: "))

#     def add_year():
#         year = input("Ingrese el año de la pelicula: ")
#         if not year.isdigit() or len(year) != 4:
#             print("Error: El año debe ser un número de cuatro dígitos..")
#             time.sleep(1)
#             add_year()
#         current_year = datetime.datetime.now().year
#         if not 1900 <= int(year) <= current_year:
#             print("Error: Año no válido. Por favor ingrese un año entre 1900 y el año actual.")
#             time.sleep(1)
#             add_year()
#         new_movie.append(year)
    
#     add_year()
    
#     def add_age_rating():
#         age_rating = input("Ingrese la clasificación por edad (+7, +13, +16, +18, or all): ")
#         if age_rating not in ['+7', '+13', '+16', '+18', '7+', '13+', '16+', '18+', 'all']:
#             print("Error: Clasificación de edad no válida. Ingrese +7, +13, +16, +18 o all")
#             time.sleep(1)
#             add_age_rating()
#         new_movie.append(age_rating)

#     add_age_rating()

#     def add_rating():
#         rating = input("Ingrese el rating de la película (de 1 a 100): ")
#         if rating.isdigit() and 1 <= int(rating) <= 100:
#             new_movie.append(f"{rating}/100")
#         else:
#             print("Error: El rating debe ser un número entero entre 1 y 100.")
#             time.sleep(1)
#             add_rating()

#     add_rating()
            
#     def add_netflix():
#         netflix = input("¿Disponible en Netflix? (si/no): ")
#         if netflix.lower() == "si":
#             new_movie.append("1")
#         elif netflix.lower() == "no":
#             new_movie.append("0")
#         else:
#             print("Opción no válida, intenta nuevamente")
#             time.sleep(1)
#             add_netflix()
    
#     add_netflix()
            
#     def add_hulu():
#         hulu = input("¿Disponible en Hulu? (si/no): ")
#         if hulu.lower() == "si":
#             new_movie.append("1")
#         elif hulu.lower() == "no":
#             new_movie.append("0")
#         else:
#             print("Opción no válida, intenta nuevamente")
#             time.sleep(1)
#             add_hulu()
    
#     add_hulu()
            
#     def add_prime_video():
#         prime_video = input("¿Disponible en Prime Video? (si/no): ")
#         if prime_video.lower() == "si":
#             new_movie.append("1")
#         elif prime_video.lower() == "no":
#             new_movie.append("0")
#         else:
#             print("Opción no válida, intenta nuevamente")
#             time.sleep(1)
#             add_prime_video()
    
#     add_prime_video()
            
#     def add_disney():
#         disney = input("¿Disponible en Disney+? (si/no): ")
#         if disney.lower() == "si":
#             new_movie.append("1")
#         elif disney.lower() == "no":
#             new_movie.append("0")
#         else:
#             print("Opción no válida, intenta nuevamente")
#             time.sleep(1)
#             add_disney()
    
#     add_disney()

#     new_movie[1] = int(new_movie[1])

#     with open('movies.csv', 'a', newline='', encoding='utf-8') as movies:
#         movies_csv = csv.writer(movies)
#         movies_csv.writerow(new_movie)

#     print("La película se ha insertado correctamente.")
#     time.sleep(1)
    
#     def research():
#         search = input("¿Quieres agregar otra pelicula? (si/no): ").lower()
#         if search == "si":
#             searchmovie_by_age(movies)
#         elif search == "no":
#             print("Volviendo al menu...")
#             time.sleep(1)
#             menu()
#             return
#         else:
#             print("Opción no válida, intenta nuevamente")
#             time.sleep(1)
#             research()

#     research()

