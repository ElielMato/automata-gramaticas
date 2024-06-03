import pathlib
import datetime
import time
import csv
import re
import pandas as pd
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

def research(callback, args):
    search = input("Quieres realizar una nueva busqueda o acción (si/no): ").lower()
    if search == "si":
        callback(args)
    elif search == "no":
        print("Volviendo al menu...")
        time.sleep(1)
        menu()
        return
    else:
        print("Opción no válida, intenta nuevamente")
        time.sleep(1)
        research(callback, args)

# Función para buscar canciones por nombre de canción o artista
def search_songs(songs):
    search_text = input("Introduce el nombre de la canción o artista: ").lower()
    matching_songs = [song for song in songs if search_text in song.track.lower() or search_text in song.artist.lower()]
    if not matching_songs or search_text.strip() == "":
        print("No se encontraron canciones que coincidan con tu búsqueda")
        time.sleep(1)
        search_songs(songs)
        return
    #Ordena las canciones de manera descendente por número de reproducciones
    matching_songs.sort(key=lambda song: int(float(song.views)) if song.views.strip() else 0, reverse=True)

    results = [(song.artist, song.track, ms_to_time(int(float(song.duration_ms)))) for song in matching_songs]
    for artist, track, duration in results:
        print(f"Artista: {artist}, Canción: {track}, Duración: {duration}")
    
    research(search_songs, songs)

# Función para buscar las diez canciones más populares de un artista
def top_songs_by_artist(songs):
    artist = input("Introduce el nombre del artista: ").lower()
    artist_songs = [song for song in songs if song.artist.lower() == artist.lower()]
    if not artist_songs or artist.strip() == "":
        print("No se encontraron canciones de ese artista")
        time.sleep(1)
        top_songs_by_artist(songs)
        return
    top_songs = sorted(artist_songs, key=lambda song: int(float(song.views)) if song.views.strip() else 0, reverse=True)[:10]

    for song in top_songs:
        artist = song.artist
        track = song.track
        duration = ms_to_time(int(float(song.duration_ms)))
        views = round(int(float(song.views)) / 1000000)
        print(f"Artista: {artist}, Canción: {track}, Duración: {duration}, Reproducciones: {views} millones")

    research(top_songs_by_artist, songs)

# Funciones de validación
def is_valid_spotify_uri(uri):
    pattern = r'spotify:track:[a-zA-Z0-9]{22}'
    return re.match(pattern, uri) is not None

def is_valid_spotify_url(url):
    pattern = r'https://open\.spotify\.com/track/[a-zA-Z0-9]{22}'
    return re.match(pattern, url) is not None

def is_valid_youtube_url(url):
    pattern = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+'
    return re.match(pattern, url) is not None

# Función para insertar un registro manualmente
def insert_manual_record(songs):
    new_song = []

    # Obtener el último índice del archivo CSV
    try:
        songs_df = pd.read_csv('music.csv')
        last_index = songs_df['Index'].max() + 1
    except (FileNotFoundError, pd.errors.EmptyDataError, KeyError):
        last_index = 0
    
    new_song.append(last_index)

    artist = input("Artista: ")
    new_song.append(artist)
    
    # Validar URL de Spotify
    while True:
        url_spotify = input("URL de Spotify: ")
        if is_valid_spotify_url(url_spotify):
            new_song.append(url_spotify)
            break
        else:
            print("La URL de Spotify no es válida. Inténtalo de nuevo.")

    track = input("Canción: ")
    new_song.append(track)
    
    album = input("Álbum: ")
    new_song.append(album)

    album_type = input("Tipo de álbum (album/single): ")
    new_song.append(album_type)

    # Validar URI de Spotify
    while True:
        uri = input("URI de Spotify: ")
        if is_valid_spotify_uri(uri):
            new_song.append(uri)
            break
        else:
            print("La URI de Spotify no es válida. Inténtalo de nuevo.")

    # Danceability
    new_song.append(0)
    
    # Energy
    new_song.append(0)
    
    # Key
    new_song.append(0)
    
    # Loudness
    new_song.append(0)
    
    # Speechiness
    new_song.append(0)
    
    # Acousticness
    new_song.append(0)
    
    # Instrumentalness
    new_song.append(0)
    
    # Liveness
    new_song.append(0)
    
    # Valence
    new_song.append(0)
    
    # Tempo
    new_song.append(0)

    # Validar duración en milisegundos
    while True:
        try:
            duration_ms = int(input("Duración en milisegundos: "))
            new_song.append(duration_ms)
            break
        except ValueError:
            print("La duración debe ser un número entero. Inténtalo de nuevo.")

    # Validar URL de YouTube
    while True:
        url_youtube = input("URL de YouTube: ")
        if is_valid_youtube_url(url_youtube):
            new_song.append(url_youtube)
            break
        else:
            print("La URL de YouTube no es válida. Inténtalo de nuevo.")

    # Title
    new_song.append(track)
    
    # Channel
    new_song.append(artist)

    # Validar vistas y likes
    views = int(input("Vistas: "))
    new_song.append(views)

    while True:
        try:
            likes = int(input("Likes: "))
            if likes > views:
                print("Los likes no pueden ser mayores que las vistas. Inténtalo de nuevo.")
            else:
                new_song.append(likes)
                break
        except ValueError:
            print("Los likes deben ser un número entero. Inténtalo de nuevo.")
    

    # Comentarios
    new_song.append(23542)

    # Licence
    new_song.append(True)

    # Official Video
    new_song.append(True)

    # Stream
    new_song.append(0)

    with open('music.csv', 'a', newline='', encoding='utf-8') as musics:
        music_csv = csv.writer(musics)
        if last_index == 0:
            # Escribir encabezados si el archivo está vacío o es nuevo
            headers = ["Index", "Artist", "Url_spotify", "Track", "Album", "Album_type", "Uri", "Danceability", "Energy", "Key", "Loudness", "Speechiness", "Acousticness", "Instrumentalness", "Liveness", "Valence", "Tempo", "Duration_ms", "Url_youtube", "Title", "Channel", "Views", "Likes", "Comments", "Licensed", "official_video", "Stream"]
            music_csv.writerow(headers)
        music_csv.writerow(new_song)
    print("Canción añadida con éxito.")

# Función para insertar registros desde un archivo CSV
def insert_records_from_csv(input_csv):
    try:
        input_df = pd.read_csv(input_csv)
    except (FileNotFoundError, pd.errors.EmptyDataError) as e:
        print(f"Error al leer el archivo de entrada: {e}")
        return

    # Obtener el último índice del archivo CSV principal
    try:
        songs_df = pd.read_csv('music.csv')
        last_index = songs_df['Index'].max() + 1
    except (FileNotFoundError, pd.errors.EmptyDataError, KeyError):
        last_index = 0

    new_songs = []

    for _, row in input_df.iterrows():
        new_song = []
        new_song.append(last_index)
        last_index += 1

        artist = row.get('Artist', '')
        new_song.append(artist)
        
        url_spotify = row.get('Url_spotify', '')
        if is_valid_spotify_url(url_spotify):
            new_song.append(url_spotify)
        else:
            print(f"La URL de Spotify '{url_spotify}' no es válida. Canción omitida.")
            continue

        track = row.get('Track', '')
        new_song.append(track)
        
        album = row.get('Album', '')
        new_song.append(album)

        album_type = row.get('Album_type', '')
        new_song.append(album_type)

        uri = row.get('Uri', '')
        if is_valid_spotify_uri(uri):
            new_song.append(uri)
        else:
            print(f"La URI de Spotify '{uri}' no es válida. Canción omitida.")
            continue

        # Añadir características con valores por defecto si no están en el CSV de entrada
        new_song.extend([
            row.get('Danceability', 0),
            row.get('Energy', 0),
            row.get('Key', 0),
            row.get('Loudness', 0),
            row.get('Speechiness', 0),
            row.get('Acousticness', 0),
            row.get('Instrumentalness', 0),
            row.get('Liveness', 0),
            row.get('Valence', 0),
            row.get('Tempo', 0)
        ])

        # Validar duración en milisegundos
        try:
            duration_ms = int(row.get('Duration_ms', 0))
            new_song.append(duration_ms)
        except ValueError:
            print(f"La duración '{row.get('Duration_ms')}' no es válida. Canción omitida.")
            continue

        url_youtube = row.get('Url_youtube', '')
        if is_valid_youtube_url(url_youtube):
            new_song.append(url_youtube)
        else:
            print(f"La URL de YouTube '{url_youtube}' no es válida. Canción omitida.")
            continue

        new_song.extend([
            row.get('Title', track),
            row.get('Channel', artist),
            row.get('Views', 0),
            row.get('Likes', 0),
            row.get('Comments', 0),
            row.get('Licensed', True),
            row.get('official_video', True),
            row.get('Stream', 0)
        ])

        new_songs.append(new_song)

    with open('music.csv', 'a', newline='', encoding='utf-8') as musics:
        music_csv = csv.writer(musics)
        if songs_df.empty:
            # Escribir encabezados si el archivo está vacío o es nuevo
            headers = ["Index", "Artist", "Url_spotify", "Track", "Album", "Album_type", "Uri", "Danceability", "Energy", "Key", "Loudness", "Speechiness", "Acousticness", "Instrumentalness", "Liveness", "Valence", "Tempo", "Duration_ms", "Url_youtube", "Title", "Channel", "Views", "Likes", "Comments", "Licensed", "official_video", "Stream"]
            music_csv.writerow(headers)
        music_csv.writerows(new_songs)
    print("Canciones añadidas con éxito.")

# Función para mostrar la cantidad de álbumes de un artista y detalles por álbum
def artist_albums_info(songs):
    artist = input("Introduce el nombre del artista: ").lower()
    artist_songs = [song for song in songs if song.artist.lower() == artist.lower()]
    if not artist_songs:
        print("No se encontraron canciones de ese artista")
        return

    albums = {}
    for song in artist_songs:
        if song.album not in albums:
            albums[song.album] = {'count': 0, 'duration': 0}
        albums[song.album]['count'] += 1
        albums[song.album]['duration'] += int(float(song.duration_ms))

    print(f"Artista: {artist.capitalize()}, Álbumes: {len(albums)}")
    for album, info in albums.items():
        duration = ms_to_time(info['duration'])
        print(f"Álbum: {album}, Canciones: {info['count']}, Duración total: {duration}")

# Menú principal
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
        print("Elije una opcion")
        print("1. Insertar cancion manualmente")
        print("2. Insertar por archivo csv")
        print("3. Volver")
        option = input("Introduce el número de la opción que deseas: ")
        if option == "1":
            insert_manual_record(songs)
        elif option == "2":
            archive = input("Escribe el nombre del archivo (csv): ")
            insert_records_from_csv(archive)
        elif option == "3":
            menu()
            return
        else:
            print("Opción no válida, intenta nuevamente")
            time.sleep(1)
            menu()
    elif option == "4":
        artist_albums_info(songs)
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