import pathlib
import datetime
import time
import csv
from dataclasses import dataclass

@dataclass
class MovieDto:
    title: str
    year: str
    age: str
    rating: float
    available_in_netflix: bool
    available_in_hulu: bool
    available_in_prime_video: bool
    available_in_disney_plus: bool

    def rating_as_float(self) -> float:
        score = int(self.rating.split('/')[0])
        return score / 100

def parse_csv() -> list:
    movies = []
    try:
        with open(f"{pathlib.Path(__file__).parent.absolute()}/movies.csv", 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=',')
            for row in csv_reader:
                movie = MovieDto(
                    row['Title'],
                    row['Year'],
                    row['Age'],
                    row['Rating'],
                    row['Netflix'] == '1',
                    row['Hulu'] == '1',
                    row['Prime Video'] == '1',
                    row['Disney+'] == '1',
                )
                movies.append(movie)
        return movies
    except (FileNotFoundError):
        print("File not found")
        exit(1)

def searchMovie_name():
    name = input("Introduce el nombre de la plataforma o inicial de la misma: ")
    movies = parse_csv()
    name = name.lower()
    count = 1
    
    def research():
        search = input("Quieres realizar una nueva busqueda (si/no): ").lower()
        if search == "si":
            searchMovie_name()
        elif search == "no":
            print("Volviendo al menu...")
            time.sleep(1)
            menu()
        else:
            print("Opción no válida, intenta nuevamente")
            time.sleep(1)
            research()
            
    for movie in movies:
        if movie.title.lower().startswith(name):
            print(f"{count}. {movie.title}")
            count += 1
    research()
    
def searchmovie_by_platform(movies):
    platform = input("Introduce la plataforma a buscar (Netflix, Hulu, Prime Video, Disney Plus): ").lower()
    matching_movies = []
    for movie in movies:
        if platform == "netflix" and movie.available_in_netflix:
            matching_movies.append(movie)
        elif platform == "hulu" and movie.available_in_hulu:
            matching_movies.append(movie)
        elif platform == "prime video" and movie.available_in_prime_video:
            matching_movies.append(movie)
        elif platform == "disney plus" and movie.available_in_disney_plus:
            matching_movies.append(movie)
    if not any([platform in ["netflix", "hulu", "prime video", "disney plus"]]):
        print("Platarforma no encontrada, intenta nuevamente con una de las opciones válidas (Netflix, Hulu, Prime Video, Disney Plus)")
        time.sleep(1)
        searchmovie_by_platform(movies)
        return
    
    def get_movie_rating(movie):
        if '/' in movie.rating:
            rating = movie.rating.split('/')[0]
            return int(rating)
        else:
            return 0


    matching_movies.sort(key=get_movie_rating, reverse=True)
    for movie in matching_movies[:10]:
        print(f"{movie.title} está disponible en {platform.capitalize()} con una puntuación de {movie.rating}")
    
    def research():
        search = input("Quieres realizar una nueva busqueda (si/no): ").lower()
        if search == "si":
            searchmovie_by_platform(movies)
        elif search == "no":
            print("Volviendo al menu...")
            time.sleep(1)
            menu()
            return
        else:
            print("Opción no válida, intenta nuevamente")
            time.sleep(1)
            research()
    
    research()
    
def searchmovie_by_age(movies):
    age = input("Introduce la edad que quieres buscar (+7, +13, +16, +18, all): ").lower()
    matching_movies = []
    for movie in movies:
        if age == "all" and movie.age == "all":
            matching_movies.append(movie)
        elif age in ["+7", "7+", "7"] and movie.age in ["+7", "7+"]:
            matching_movies.append(movie)
        elif age in ["+13", "13+", "13"] and movie.age in ["+13", "13+"]:
            matching_movies.append(movie)
        elif age in ["+16", "16+", "16"] and movie.age in ["+16", "16+"]:
            matching_movies.append(movie)
        elif age in ["+18", "18+", "18"] and movie.age in ["+18", "18+"]:
            matching_movies.append(movie)
    if not any([age in ["+7", "7+", "7", "+13", "13+", "13", "+16", "16+", "16", "+18", "18+", "18", "all"]]):
        print("Edad no encontrada, intenta nuevamente con una de las opciones válidas (+7, +13, +16, +18, all)")
        time.sleep(1)
        searchmovie_by_age(movies)
        return
    def get_movie_rating(movie):
        return movie.rating
    
    matching_movies.sort(key=get_movie_rating, reverse=True)
    for movie in matching_movies[:10]:
        print(f"{movie.title} está disponible con una puntuación de {movie.rating}")
    
    def research():
        search = input("Quieres realizar una nueva busqueda (si/no): ").lower()
        if search == "si":
            searchmovie_by_age(movies)
        elif search == "no":
            print("Volviendo al menu...")
            time.sleep(1)
            menu()
            return
        else:
            print("Opción no válida, intenta nuevamente")
            time.sleep(1)
            research()
    
    research()

def add_movie(movies):
    new_movie = []
    new_movie.append(input("Ingrese el título de la película: "))

    def add_year():
        year = input("Ingrese el año de la pelicula: ")
        if not year.isdigit() or len(year) != 4:
            print("Error: El año debe ser un número de cuatro dígitos..")
            time.sleep(1)
            add_year()
        current_year = datetime.datetime.now().year
        if not 1900 <= int(year) <= current_year:
            print("Error: Año no válido. Por favor ingrese un año entre 1900 y el año actual.")
            time.sleep(1)
            add_year()
        new_movie.append(year)
    
    add_year()
    
    def add_age_rating():
        age_rating = input("Ingrese la clasificación por edad (+7, +13, +16, +18, or all): ")
        if age_rating not in ['+7', '+13', '+16', '+18', '7+', '13+', '16+', '18+', 'all']:
            print("Error: Clasificación de edad no válida. Ingrese +7, +13, +16, +18 o all")
            time.sleep(1)
            add_age_rating()
        new_movie.append(age_rating)

    add_age_rating()

    def add_rating():
        rating = input("Ingrese el rating de la película (de 1 a 100): ")
        if rating.isdigit() and 1 <= int(rating) <= 100:
            new_movie.append(f"{rating}/100")
        else:
            print("Error: El rating debe ser un número entero entre 1 y 100.")
            time.sleep(1)
            add_rating()

    add_rating()
            
    def add_netflix():
        netflix = input("¿Disponible en Netflix? (si/no): ")
        if netflix.lower() == "si":
            new_movie.append("1")
        elif netflix.lower() == "no":
            new_movie.append("0")
        else:
            print("Opción no válida, intenta nuevamente")
            time.sleep(1)
            add_netflix()
    
    add_netflix()
            
    def add_hulu():
        hulu = input("¿Disponible en Hulu? (si/no): ")
        if hulu.lower() == "si":
            new_movie.append("1")
        elif hulu.lower() == "no":
            new_movie.append("0")
        else:
            print("Opción no válida, intenta nuevamente")
            time.sleep(1)
            add_hulu()
    
    add_hulu()
            
    def add_prime_video():
        prime_video = input("¿Disponible en Prime Video? (si/no): ")
        if prime_video.lower() == "si":
            new_movie.append("1")
        elif prime_video.lower() == "no":
            new_movie.append("0")
        else:
            print("Opción no válida, intenta nuevamente")
            time.sleep(1)
            add_prime_video()
    
    add_prime_video()
            
    def add_disney():
        disney = input("¿Disponible en Disney+? (si/no): ")
        if disney.lower() == "si":
            new_movie.append("1")
        elif disney.lower() == "no":
            new_movie.append("0")
        else:
            print("Opción no válida, intenta nuevamente")
            time.sleep(1)
            add_disney()
    
    add_disney()

    new_movie[1] = int(new_movie[1])

    with open('movies.csv', 'a', newline='', encoding='utf-8') as movies:
        movies_csv = csv.writer(movies)
        movies_csv.writerow(new_movie)

    print("La película se ha insertado correctamente.")
    time.sleep(1)
    
    def research():
        search = input("¿Quieres agregar otra pelicula? (si/no): ").lower()
        if search == "si":
            searchmovie_by_age(movies)
        elif search == "no":
            print("Volviendo al menu...")
            time.sleep(1)
            menu()
            return
        else:
            print("Opción no válida, intenta nuevamente")
            time.sleep(1)
            research()

    research()

def menu():
    movies = parse_csv()
    print("Bienvenido al buscador de películas")
    print("1. Buscar película por nombre")
    print("2. Buscar película por plataforma")
    print("3. Buscar película por audiencia")
    print("4. Insertar pelicula")
    print("5. Salir")
    option = input("Introduce el número de la opción que deseas: ")
    if option == "1":
        searchMovie_name()
    elif option == "2":
        searchmovie_by_platform(movies)
    elif option == "3":
        searchmovie_by_age(movies)  
    elif option == "4":
        add_movie(movies)
    elif option == "5":
        print("Saliendo...")
        time.sleep(1)
        return
    else:
        print("Opción no válida, intenta nuevamente")
        time.sleep(1)
        menu()

if __name__ == '__main__':
    movies = parse_csv()
    menu()