import pathlib
import datetime
import time
import csv
import re
from dataclasses import dataclass

# Función para convertir milisegundos de la reproducción a formato de tiempo HH:MM:SS
def ms_to_time(ms):
    seconds = (ms / 1000) % 60
    minutes = (ms / (1000 * 60)) % 60
    hours = (ms / (1000 * 60 * 60)) % 24

    return "%02d:%02d:%02d" % (hours, minutes, seconds)

#Codigo para abrir y manejar el archivo CSV
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
        with open(f"{pathlib.Path(__file__).parent.absolute()}/music.csv", 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=',')
            for row in csv_reader:
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

# Función para realizar una nueva búsqueda o acción
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
        print("Opción no válida, intenta nuevamente.")
        time.sleep(1)
        research(callback, args)

# Función para buscar canciones por nombre de canción o artista
def search_songs(songs):
    search_text = input("Introduce el nombre de la canción o artista: ").lower()
    matching_songs = [song for song in songs if search_text in song.track.lower() or search_text in song.artist.lower()]
    if not matching_songs or search_text.strip() == "":
        print("No se encontraron canciones que coincidan con tu búsqueda")
        time.sleep(1)
        research(search_songs, songs)
        return
    # Ordena las canciones de manera descendente por número de reproducciones
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
        research(top_songs_by_artist, songs)
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
    pattern = r'https://open\.spotify\.com/(track|artist)/[a-zA-Z0-9]{22}'
    return re.match(pattern, url) is not None

def is_valid_youtube_url(url):
    pattern = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+'
    return re.match(pattern, url) is not None

# Función para insertar un registro manualmente
def insert_manual_record():
    new_song = []

    # Obtener el último índice del archivo CSV
    try:
        with open('music.csv', 'r') as file:
            reader = csv.DictReader(file)
            last_index = max(int(row['Index']) for row in reader) + 1
    except (FileNotFoundError, KeyError):
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
            print("La URL de Spotify no es válida, vuelve a intentarlo (debe tener la forma https://open.spotify.com/artist o track/codigo aleatorio).")
            time.sleep(1)

    track = input("Nombre de la canción: ")
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
            print("La URI de Spotify no es válida, vuelve a intentarlo (debe tener la forma spotify:track:numeros_aleatorios).")
            time.sleep(1)

    # Valores por defecto para las columnas que no utilizamos en nuestro programa
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

    # Validar que la duración este en milisegundos
    while True:
        try:
            duration_ms = int(input("Duración en milisegundos: "))
            new_song.append(duration_ms)
            break
        except ValueError:
            print("La duración debe ser un número entero. Inténtalo de nuevo.")
            time.sleep(1)

    # Validar URL de YouTube
    while True:
        url_youtube = input("URL de YouTube: ")
        if is_valid_youtube_url(url_youtube):
            new_song.append(url_youtube)
            break
        else:
            print("La URL de YouTube no es válida. Inténtalo de nuevo.")
            time.sleep(1)

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
            print("Los likes deben ser un número entero, vuelve a intentarlo.")
    

    # Comentarios
    new_song.append(0)

    # Licence
    new_song.append(True)

    # Official video
    new_song.append(True)

    # Stream
    new_song.append(0)

    # Inserta la canciοn en el archivo CSV
    with open('music.csv', 'a', newline='', encoding='utf-8') as musics:
        music_csv = csv.writer(musics)
        if last_index == 0:
            headers = ["Index", "Artist", "Url_spotify", "Track", "Album", "Album_type", "Uri", "Danceability", "Energy", "Key", "Loudness", "Speechiness", "Acousticness", "Instrumentalness", "Liveness", "Valence", "Tempo", "Duration_ms", "Url_youtube", "Title", "Channel", "Views", "Likes", "Comments", "Licensed", "official_video", "Stream"]
            music_csv.writerow(headers)
        music_csv.writerow(new_song)
    print("Canción añadida con éxito.")
    print("Volviendo al menú...")
    time.sleep(2)
    menu()
    
# Función para mostrar la cantidad de álbumes de un artista y detalles por álbum
def artist_albums_info(songs):
    artist = input("Introduce el nombre del artista: ").lower()
    artist_songs = [song for song in songs if song.artist.lower() == artist.lower()]
    if not artist_songs:
        print("No se encontraron canciones de ese artista.")
        research(artist_albums_info, songs)
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
    
    research(artist_albums_info, songs)

# Función para procesar un archivo CSV con canciones
def process_music_csv():
    
    uploaded_file_path = input("Escribe el nombre del archivo (csv): ")
    # Verificar que el archivo subido sea un archivo CSV
    if not uploaded_file_path.endswith('.csv'):
        print("Error, el archivo debe tener la extensión .csv, vuelve a intentarlo.")
        return
    # Definir las columnas requeridas
    required_columns = ['Artist', 'Track', 'Album', 'Album_type', 'Uri_spotify', 'duration_ms', 
                        'Url_spotify', 'Url_youtube', 'Likes', 'Views']
    
    # Leer el archivo CSV subido
    with open(uploaded_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        
        # Verificar que las columnas requeridas están presentes en el archivo subido
        for column in required_columns:
            if column not in fieldnames:
                print(f"Falta la columna requerida: {column}, verifica el archivo nuevamente y vuelve a intentarlo.")
                print("Volviendo al menú...")
                time.sleep(2)
                menu()
                return
            
        # Contadores de canciones exitosas y fallidas
        success = 0
        failure = 0
        # Validar y procesar los datos
        for row in reader:
            new_song = []
            # Obtener el último índice del archivo CSV
            try:
                with open('music.csv', 'r') as file:
                    reader = csv.DictReader(file)
                    last_index = max(int(row['Index']) for row in reader) + 1
            except (FileNotFoundError, KeyError):
                last_index = 0
    
            new_song.append(last_index)

            artist = row['Artist']
            new_song.append(artist)

            # Validar URL de Spotify
            url_spotify = row['Url_spotify']
            if not is_valid_spotify_url(url_spotify):
                failure += 1
                continue
            new_song.append(url_spotify)

            track = row['Track']
            new_song.append(track)
        
            album = row['Album']
            new_song.append(album)
    
            album_type = row['Album_type']
            new_song.append(album_type)
            
            # Validar URI de Spotify    
            uri_spotify = row['Uri_spotify']
            if not is_valid_spotify_uri(uri_spotify):
                failure += 1
                continue
            new_song.append(uri_spotify)
            
            # Valores por defecto para las columnas que no utilizamos en nuestro programa
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
            
            duration_ms = int(row['duration_ms'])
            new_song.append(duration_ms)
            
            # Validar URL de YouTube
            url_youtube = row['Url_youtube']
            if not is_valid_youtube_url(url_youtube):
                failure += 1
                continue
            new_song.append(url_youtube)

            # Title
            new_song.append(track)
            
            # Channel
            new_song.append(artist)
        
            # Validar vistas y likes
            views = int(row['Views'])
            new_song.append(views)
            
            # Validar likes
            def is_valid_likes(likes, views):
                try:
                    likes = int(likes)
                    return likes <= views
                except ValueError:
                    return False
            
            # Validar que los likes no sean mayores que las vistas
            while True:
                likes = row['Likes']
                if not is_valid_likes(likes, views):
                    failure += 1
                    continue
                new_song.append(likes)
                break

            # Comentarios
            new_song.append(0)
        
            # Licence
            new_song.append(True)
        
            # Official video
            new_song.append(True)
        
            # Stream
            new_song.append(0)
    
            #Inserta la canciοn en el archivo CSV
            with open('music.csv', 'a', newline='', encoding='utf-8') as musics:
                music_csv = csv.writer(musics)
                if last_index == 0:
                    headers = ["Index", "Artist", "Url_spotify", "Track", "Album", "Album_type", "Uri", "Danceability", "Energy", "Key", "Loudness", "Speechiness", "Acousticness", "Instrumentalness", "Liveness", "Valence", "Tempo", "Duration_ms", "Url_youtube", "Title", "Channel", "Views", "Likes", "Comments", "Licensed", "official_video", "Stream"]
                    music_csv.writerow(headers)
                music_csv.writerow(new_song)
            success += 1
            new_song = []
        
        print(f"Procesamiento completado. {success} canción/es insertadas con éxito, {failure} canción/es fallidas.")
        print("Volviendo al menú...")
        time.sleep(2)
        menu()
    
# Función para mostrar la cantidad de álbumes de un artista y detalles por álbum
def artist_albums_info(songs):
    artist = input("Introduce el nombre del artista: ").lower()
    artist_songs = [song for song in songs if song.artist.lower() == artist.lower()]
    if not artist_songs:
        print("No se encontraron canciones de ese artista.")
        research(artist_albums_info, songs)
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
    
    research(artist_albums_info, songs)

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
        print("Como deseas insertar la canción?")
        print("1. Insertar canción manualmente")
        print("2. Insertar por archivo csv")
        print("3. Volver")
        option = input("Introduce el número de la opción que deseas: ")
        if option == "1":
            insert_manual_record()
        elif option == "2":
            print('''
Consideraciones:
A continuacion se te pedira el nombre del archivo csv que deseas importar, el mismo debe ser escrito con la extension .csv e incluirse en la carpeta del programa.
                  
Asegurate de que el archivo csv tenga las siguientes columnas:
Artist, Track, Album, Album_type, Uri_spotify, duration_ms, Url_spotify, Url_youtube, Likes, Views

En caso de que no tenga alguna de estas columnas, el archivo no podrá ser procesado.
En caso de que algun dato no pueda ser validado, la canción no será insertada.
                  
Al finalizar la importación, se mostrará la cantidad de canciones insertadas con éxito y las fallidas.
                  ''')
            time.sleep(5)
            try:
                process_music_csv()
            except FileNotFoundError:
                print("El archivo no se encuentra en la carpeta del programa.")
                time.sleep(1)
                process_music_csv()
            
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
    songs = parse_csv()
    menu()