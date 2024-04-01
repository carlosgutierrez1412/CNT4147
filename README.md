In this project I will be using the concepts and tools learned in CNT 4147, specifically Apache Hadoop and Apache Spark in order to collect, process, clean, analize and deploy two Netflix Movies and Shows open datasets; a titles dataset  that includes the following features :

Field                      | Description
---------------------------|---------------------------------------
id                         | The title ID on JustWatch.
title                      | The name of the title.
show_type                  | TV show or movie.
description                | A brief description.
release_year               | The release year.
age_certification          | The age certification.
runtime                    | The length of the episode (SHOW) or movie.
genres                     | A list of genres.
production_countries       | A list of countries that produced the title.
seasons                    | Number of seasons if it's a SHOW.
imdb_id                    | The title ID on IMDB.
imdb_score                 | Score on IMDB.
imdb_votes                 | Votes on IMDB.
tmdb_popularity            | Popularity on TMDB.
tmdb_score                 | Score on TMDB.


and a credits dataset with the following features:


Field            | Description
-----------------|--------------------------------
person_ID        | The person ID on JustWatch.
id               | The title ID on JustWatch.
name             | The actor or director's name.
character_name   | The character name.
role             | ACTOR or DIRECTOR.
production_countries       | A list of countries that produced the title.
seasons                    | Number of seasons if it's a SHOW.
imdb_id                    | The title ID on IMDB.

this, with the ultimate purpose, to create a GUI where the user can interact with two different systems: a filtering system which will take different parameters selected by the user and return all the different Netflix Movies or Shows that match those specific parameters, and a content recommendation system where the user will input the name of a Netflix Movie or Show and the model will return the top 3 most similar titles to the one the user selected as well as a similarity score provided by the use of a cosine similarity approach.
