import urllib.request, urllib.parse, urllib.error
import json
import sqlite3


def menu():
    ans = True
    while ans:
        print("""
         Welcome to the App Movie Service!
         Please choose one of the available actions below:
         1. Find and save information about the films you are interested in.
         2. Display a list of titles of saved movies.
         3. Display the best rated IMDB movie.
         4. Display the highest-grossing movie.
         5. Display the average rating of saved videos.
         6. Quit
         """)

        ans = input('Make your choice: ')
        if ans == '1':
            title = input('Enter the name of a movie: ')
            search_movie(title)
        elif ans == '2':
            database = input('Please enter a name for the database without extension: ')
            # example: movies
            print_database(database)
        elif ans == '3':
            best_rated_imdb()
        elif ans == '4':
            highest_grossing_movie()
        elif ans == '5':
            average_rating()
        elif ans == '6':
            ans = None
        else:
            print('\n Not Valid Choice Try again')


with open('APIkey.json') as f:  # My personal API
    keys_dict = json.load(f)
    omdbapi = keys_dict['OMDBapi']
    serviceurl = 'http://www.omdbapi.com/?'
    apikey = '&apikey=' + omdbapi


def search_movie(title):
    if len(title) < 1 or title == 'quit':
        print('Invalid title.')
        return None

    try:
        url = serviceurl + urllib.parse.urlencode({'t': title}) + apikey
        print(f'Retrieving the data of "{title}" now... ')
        uh = urllib.request.urlopen(url)
        data = uh.read()
        json_data = json.loads(data)

        if json_data['Response'] == 'True':
            print_json(json_data)

            # Asks user whether to save the movie information in a local database
            save_database_yes_no = input(
                'Save the movie info in a local database? Enter "yes" or "no": ').lower()
            if save_database_yes_no == 'yes':
                save_in_database(json_data)
            else:
                print('Error encountered: ', json_data['Error'])

    except urllib.error.URLError as e:
        print(f'ERROR: {e.reason}')


def print_json(json_data):  # Function for printing a JSON dataset
    list_keys = [
        'Title', 'Year', 'Rated', 'Released', 'Runtime', 'Genre', 'Director', 'Writer',
        'Actors', 'Plot', 'Language', 'Country', 'Awards', 'Ratings', 'BoxOffice',
        'imdbRating', 'imdbVotes', 'imdbID'
    ]
    print('=' * 100)
    for key in list_keys:
        if key in list(json_data.keys()):
            print(f'{key}: {json_data[key]}')
    print('=' * 100)


def save_in_database(json_data):
    filename = input('Please enter a name for the database without extension: ')
    filename = filename + '.sqlite'
    con = sqlite3.connect(str(filename))  # Create a Connection object
    cur = con.cursor()

    title = json_data['Title']
    # Goes through the json dataset and extracts information if it is available
    if json_data['Year'] != 'N/A':
        year = int(json_data['Year'])
    if json_data['Runtime'] != 'N/A':
        runtime = int(json_data['Runtime'].split()[0])
    if json_data['Country'] != 'N/A':
        country = json_data['Country']
    if json_data['BoxOffice'] != 'N/A':
        boxoffice = float(json_data['BoxOffice'])
    if json_data['imdbRating'] != 'N/A':
        imdb_rating = float(json_data['imdbRating'])
    else:
        imdb_rating = -1

    # Create SQL table MovieInfo (movieinfo.sqlite.)
    cur.execute('''CREATE TABLE IF NOT EXISTS MovieInfo 
    (Title TEXT, Year INTEGER, Runtime INTEGER, Country TEXT, BoxOffice REAL, IMDBRating REAL)''')

    cur.execute('SELECT Title FROM MovieInfo WHERE Title = ? ', (title,))
    row = cur.fetchone()

    if row is None:
        cur.execute('''INSERT INTO MovieInfo (Title, Year, Runtime, Country, BoxOffice, IMDBRating)
                VALUES (?,?,?,?,?,?)''', (title, year, runtime, country, boxoffice, imdb_rating))
    else:
        print('Record already found. No update made.')

    # Commits the change and close the connection to the database
    con.commit()
    con.close()


def print_database(database):  # Function to print all contents of the local database
    conn = sqlite3.connect(str(database))
    cur = conn.cursor()
    for row in cur.execute('SELECT * FROM MovieInfo'):
        print(row)
    conn.close()


def best_rated_imdb(database):
    conn = sqlite3.connect(str(database))
    cur = conn.cursor()
    for row in cur.execute(
            'SELECT * FROM MovieInfo '
            'ORDER BY IMDBRating DESC'
            'LIMIT 5'):
        print(row)
    conn.close()


def highest_grossing_movie(database):
    conn = sqlite3.connect(str(database))
    cur = conn.cursor()
    for row in cur.execute('SELECT MAX(BoxOffice) FROM MovieInfo'):
        print(row)
    conn.close()


def average_rating(database):
    conn = sqlite3.connect(str(database))
    cur = conn.cursor()
    for row in cur.execute('SELECT AVG(IMDBRating) FROM MovieInfo'):
        print(row)
    conn.close()


if __name__ == '__main__':
    menu()
