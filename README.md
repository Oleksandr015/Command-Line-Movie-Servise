## Command-Line-Movie-Servise

A python script that allows you to look up movies on IMDB from the command line. The service http://www.omdbapi.com was used as a source of films. For testing purposes, my personal ApiKey is placed in the repository. The limit on the number of requests is 1000 per day. Enjoy)

## Using The Program

To get started, please download the application. This can be done in the Git repository Clone> Download .zip. Then open a command line, go to the folder containing the main file cmd_imdb.py. Also, the file can be opened in any IDE that you are using.

python cmd_imdb.py

Next, you should be guided by the application menu.


The search is made for one movie title. If such a movie exists in the database, then detailed information on it will appear.
Then the movie can be saved in your database, or you can refuse it. I used sqlite3 in my code.

When there are several films in your local database, you can sort them by IMDB rating, print highest-grossing or view the average rating.
