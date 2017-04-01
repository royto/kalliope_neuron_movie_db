# The Movie Db

## Synopsis

This neuron allows you to query The Movie DB API to
- get info about a MOVIE.
- get info about a PEOPLE.
- get list of Popular Movies
- get list of Top rated Movies
- get list of upcoming movies
- get list of playing now movies 

## Installation
```bash
kalliope install --git-url https://github.com/royto/kalliope_neuron_movie_db.git
```

## Specification

The Movie Db Neuron has multiple available actions : MOVIE, PEOPLE, POPULAR, TOP_RATED, UPCOMING and PLAYING NOW.

Each of them requires specific options, return values and synapses example : 

#### MOVIE 
##### Options

| parameter   | required | type   | default | choices    | comment                              |
|-------------|----------|--------|---------|------------|--------------------------------------|
| action      | YES      | String | None    | MOVIE      | Defines the action type              |
| api_key     | YES      | String | None    |            | The API Key                          |
| movie       | YES      | String | None    |            | The movie to search for              |
| language    | NO       | String | en-US   |            | The language as ISO 639-1 code       |


##### Return Values

| Name    | Description                                    | Type   | sample      |
|---------|------------------------------------------------|--------|-------------|
| movie   | Information about the 1st movie matching query | Object | see [get details schema](https://developers.themoviedb.org/3/movies/get-movie-details)        |

##### Synapses example

``` yml
  - name: "search-movie"
    signals:
      - order: "Search for Movie {{ movie}}"
    neurons:
      - movie_db:
          api_key: "YOUR_API_KEY"
          action: "MOVIE"
          language: "fr"
          file_template: templates/movie_db_movie.j2
          args:
            - movie

```

The template defined in the templates/movie_db_movie.j2
```jinja2
{% if movie is defined %}
  {{ movie["title"] }}, is a film released on {{ movie["release_date"][:4] }}.
  {{ movie["title"] }} is a movie of {{ movie["genres"]|map(attribute='name')|join(', ') }}

  Synopsis :
  {{ movie["overview"] }}

  {% set actors = movie['credits']['cast'] %}
  Main actors are: {{ actors[:5]|map(attribute='name')|join(', ') }}

{% else %}
    No movie found
{% endif %}
```

#### PEOPLE
##### Options

| parameter   | required | type   | default | choices    | comment                              |
|-------------|----------|--------|---------|------------|--------------------------------------|
| action      | YES      | String | None    | PEOPLE     | Defines the action type              |
| api_key     | YES      | String | None    |            | The API Key                          |
| people      | YES      | String | None    |            | The people to search for             |


##### Return Values


| Name    | Description                                     | Type   | sample      |
|---------|-------------------------------------------------|--------|-------------|
| people  | Information about the 1st people matching query | Object | see [get person details schema](https://developers.themoviedb.org/3/people/get-person-details)     |

##### Synapses example

``` yml
  - name: "movie-people"
    signals:
      - order: "Get Info about Movie {{ people }}"
    neurons:
      - movie_db:
          api_key: "YOUR_API_KEY"
          action: "PEOPLE"
          say_template:
          - "{{ name }}, born {{ birthday }} at {{place_of_birth }}, {{ biography }}, known for [:5]|map(attribute='title')|join(', ')  "
          args:
            - people
```

#### POPULAR
##### Options

| parameter   | required | type   | default | choices    | comment                              |
|-------------|----------|--------|---------|------------|--------------------------------------|
| action      | YES      | String | None    | POPULAR    | Defines the action type              |
| api_key     | YES      | String | None    |            | The API Key                          |
| language    | NO       | String | en-US   |            | The language as ISO 639-1 code       |


##### Return Values
see [get popular movies response schema](https://developers.themoviedb.org/3/movies/get-popular-movies) 

| Name    | Description                     | Type   | sample      |
|---------|---------------------------------|--------|-------------|
| result  | List of popular movies          | List   |             |

##### Synapses example

``` yml
- name: "popular-movie"
  signals:
    - order: "What are popular movies"
  neurons:
    - movie_db:
        api_key: "YOUR_API_KEY"
        action: "POPULAR"
        language: "en"
        file_template: templates/movie_db_popular.j2
```

The template defined in the templates/movie_db_popular.j2
``` jinja2
List of popular movies :
{% for movie in results %}
    {{ movie['title'] }}
{% endfor %}
```


#### TOP_RATED
##### Options

| parameter   | required | type   | default | choices    | comment                              |
|-------------|----------|--------|---------|------------|--------------------------------------|
| action      | YES      | String | None    | TOP_RATED  | Defines the action type              |
| api_key     | YES      | String | None    |            | The API Key                          |
| language    | NO       | String | en-US   |            | The language as ISO 639-1 code       |


##### Return Values
see [get top rated movies response schema](https://developers.themoviedb.org/3/movies/get-top-rated-movies) 

| Name    | Description                     | Type   | sample      |
|---------|---------------------------------|--------|-------------|
| result  | List of popular movies          | List   |             |

##### Synapses example

``` yml
- name: "top-rated-movie"
  signals:
    - order: "What are the top rated movies"
  neurons:
    - movie_db:
        api_key: "YOUR_API_KEY"
        action: "TOP_RATED"
        language: "en"
        file_template: templates/movie_db_top_rated.j2
```

The template defined in the tamplates/movie_db_top_rated.j2
``` jinja2
List of top rated movies :
{% for movie in results %}
    {{ movie['title'] }}
{% endfor %}
```

#### UPCOMING
##### Options

| parameter   | required | type   | default | choices    | comment                              |
|-------------|----------|--------|---------|------------|--------------------------------------|
| action      | YES      | String | None    | UPCOMING   | Defines the action type              |
| api_key     | YES      | String | None    |            | The API Key                          |
| language    | NO       | String | en-US   |            | The language as ISO 639-1 code       |
| region      | NO       | String | None    |            | The region as ISO 3166-1 code to filter release dates. |


##### Return Values
see [get upcoming movies response schema](https://developers.themoviedb.org/3/movies/get-upcoming) 

| Name    | Description                     | Type   | sample      |
|---------|---------------------------------|--------|-------------|
| result  | List of popular movies          | List   |             |

##### Synapses example

``` yml
- name: "upcoming-movie"
  signals:
    - order: "What are upcoming movies"
  neurons:
    - movie_db:
        api_key: "YOUR_API_KEY"
        action: "UPCOMING"
        language: "fr"
        region: "FR"
        file_template: templates/movie_db_upcoming.j2
```

The template defined in the templates/movie_db_upcoming.j2
``` jinja2
List of upcoming movies :
{% for movie in results %}
    {{ movie['title'] }}
{% endfor %}
```

#### NOW_PLAYING
##### Options

| parameter   | required | type   | default | choices     | comment                              |
|-------------|----------|--------|---------|-------------|--------------------------------------|
| action      | YES      | String | None    | NOW_PLAYING | Defines the action type              |
| api_key     | YES      | String | None    |             | The API Key                          |
| language    | NO       | String | en-US   |             | The language as ISO 639-1 code       |
| region      | NO       | String | None    |             | The region as ISO 3166-1 code to filter release dates. |


##### Return Values
see [get now playing movies response schema](https://developers.themoviedb.org/3/movies/get-now-playing) 

| Name    | Description                     | Type   | sample      |
|---------|---------------------------------|--------|-------------|
| result  | List of popular movies          | List   |             |

##### Synapses example

``` yml
- name: "now-playing-movie"
   signals:
     - order: "What are the movies played now"
   neurons:
     - movie_db:
         api_key: "YOUR_API_KEY"
         action: "NOW_PLAYING"
         language: "fr"
         region: "FR"
         file_template: templates/movie_db_now_playing.j2
```

The template defined in the templates/movie_db_now_playing.j2
``` jinja2
List of movies played now:
{% for movie in results %}
    {{ movie['title'] }}
{% endfor %}
```


##### 

## Notes

In order to be able to query The Movie Db API, you need to get a api Key. 

### How to get your The Movie Db Api Key

1. Create a [Movie Db account](https://slack.com/signin)
2. Connect to your account
3. Go to API in the menu
4. Create a request for developper api key  
5. Accept licence agreement
6. Fill informations about application


