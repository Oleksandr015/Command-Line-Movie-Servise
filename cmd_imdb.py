import urllib.request, urllib.parse, urllib.error
import json
import sqlite3


with open('APIkey.json') as f:  # My personal API
    keys_dict = json.load(f)
    omdbapi = keys_dict['OMDBapi']
    serviceurl = 'http://
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



