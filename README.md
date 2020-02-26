# The Movie Db

[![](https://img.shields.io/github/release/royto/kalliope_neuron_movie_db.svg?style=flat-square)](https://github.com/royto/kalliope_neuron_movie_db/releases/latest)

## Synopsis

This neuron allows you to query The Movie DB API to

- get info about a MOVIE.
- get info about a PEOPLE.
- get list of Popular Movies
- get list of Top rated Movies
- get list of upcoming movies
- get list of playing now movies
- get info about a TV Show
- get list of popular TV Shows
- get list of Top rated TV Shows
- get list of latest TV Shows
- get info about a TV Show Season
- get info about a TV Show Episode

## Installation

```bash
kalliope install --git-url https://github.com/royto/kalliope_neuron_movie_db.git
```

## Specification

The Movie Db Neuron has multiple available actions : `MOVIE, PEOPLE`, `POPULAR`, `TOP_RATED`, `UPCOMING` and `PLAYING NOW`, `TV`, `TV_POPULAR`, `TV_TOP_RATED`, `TV_LATEST`, `TV_SEASON`, `TV_EPISODE`.

Each of them requires specific options, return values and synapses

#### MOVIE

##### Options

| parameter   | required | type   | default | choices    | comment                              |
|-------------|----------|--------|---------|------------|--------------------------------------|
| action      | YES      | String | None    | MOVIE      | Defines the action type              |
| api_key     | YES      | String | None    |            | The API Key                          |
| movie       | YES      | String | None    |            | The movie to search for              |
| language    | NO       | String | en-US   |            | The language as ISO 639-1 code       |
| movie_extra | NO       | String | None    |            | [extra data about the movie](EXTRA_DATA.md) |

##### Return Values

| Name    | Description                                    | Type   | sample      |
|---------|------------------------------------------------|--------|-------------|
| movie   | Information about the 1st movie matching query | Object | see [get details schema](https://developers.themoviedb.org/3/movies/get-movie-details)        |

##### Synapses example

``` yml
  - name: "search-movie"
    signals:
      - order: "search for Movie {{ movie}}"
    neurons:
      - movie_db:
          api_key: "YOUR_API_KEY"
          action: "MOVIE"
          language: "fr"
          movie_extra: "credits"
          file_template: templates/movie_db_movie.j2
          movie: "{{ movie }}"

```

The template defined in the templates/movie_db_movie.j2

```jinja2
{% if movie is defined %}
  {{ movie["title"] }}, is a film released on {{ movie["release_date"][:4] }}.
  {{ movie["title"] }} is a movie of {{ movie["genres"]|map(attribute='name')|join(', ') }}

  Synopsis :
  {{ movie["overview"] }}

  {% if movie['credits'] is defined %}
    {% set actors = movie['credits']['cast'] %}
    Main actors are: {{ actors[:5]|map(attribute='name')|join(', ') }}
  {% endif %}
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
| language    | NO       | String | en-US   |            | The language as ISO 639-1 code       |
| people      | YES      | String | None    |            | The people to search for             |

##### Return Values

| Name    | Description                                     | Type   | sample      |
|---------|-------------------------------------------------|--------|-------------|
| people  | Information about the 1st people matching query | Object | see [get search person schema](https://developers.themoviedb.org/3/search/search-people)     |

##### Synapses example

``` yml
  - name: "movie-people"
    signals:
      - order: "get Info about actor {{ people }}"
      - order: "get Info about actress {{ people }}"
      - order: "get Info about director {{ people }}"
    neurons:
      - movie_db:
          api_key: "YOUR_API_KEY"
          action: "PEOPLE"
          language: "fr"
          say_template:
          - "{{ name }}, born {{ birthday }} at {{place_of_birth }}, {{ biography }}, known for {{ known_for[:5]|map(attribute='title')|join(', ') }} "
          people: "{{ people }}"
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
    - order: "what are popular movies"
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
| result  | List of top rated movies        | List   |             |

##### Synapses example

``` yml
- name: "top-rated-movie"
  signals:
    - order: "what are the top rated movies"
  neurons:
    - movie_db:
        api_key: "YOUR_API_KEY"
        action: "TOP_RATED"
        language: "en"
        file_template: templates/movie_db_top_rated.j2
```

The template defined in the templates/movie_db_top_rated.j2

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
| result  | List of upcoming movies         | List   |             |

##### Synapses example

``` yml
- name: "upcoming-movie"
  signals:
    - order: "what are upcoming movies"
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
| result  | List of now playing movies      | List   |             |

##### Synapses example

``` yml
- name: "now-playing-movie"
   signals:
     - order: "what are the movies played now"
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

#### TV

##### Options

| parameter   | required | type   | default | choices    | comment                              |
|-------------|----------|--------|---------|------------|--------------------------------------|
| action      | YES      | String | None    | TV         | Defines the action type              |
| api_key     | YES      | String | None    |            | The API Key                          |
| tv          | YES      | String | None    |            | The TV Show to search for            |
| language    | NO       | String | en-US   |            | The language as ISO 639-1 code       |
| tv_extra    | NO       | String | None    |            | [extra data about the tv](EXTRA_DATA.md) |

##### Return Values

| Name    | Description                                      | Type   | sample      |
|---------|--------------------------------------------------|--------|-------------|
| tv      | Information about the 1st TV Show matching query | Object | see [get details schema](https://developers.themoviedb.org/3/tv/get-tv-details)        |

##### Synapses example

``` yml
  - name: "search-tv"
    signals:
      - order: "search for TV Show {{ tv }}"
    neurons:
      - movie_db:
          api_key: "YOUR_API_KEY"
          action: "TV"
          language: "fr"
          tv_extra: "credits"
          file_template: templates/tv_db_movie.j2
          tv: "{{ tv }}"

```

The template defined in the templates/tv_db_movie.j2

```jinja2
{% if tv is defined %}

{{ tv["name"] }}, is a TV Show of {{ tv["number_of_episodes"] }} on {{ tv["number_of_seasons"] }} seasons.

{{ tv["name"] }} is a TV Show of {{ tv["genres"]|map(attribute='name')|join(', ') }}

Synopsis :
{{ tv["overview"] }}
    {% if tv['credits'] is defined %}
        {% set actors = tv['credits']['cast'] %}
        Main actors are: {{ actors[:5]|map(attribute='name')|join(', ') }}
    {% endif %}
{% else %}
    No TV Show found
{% endif %}
```

### TV_POPULAR

##### Options

| parameter   | required | type   | default | choices    | comment                              |
|-------------|----------|--------|---------|------------|--------------------------------------|
| action      | YES      | String | None    | TV_POPULAR | Defines the action type              |
| api_key     | YES      | String | None    |            | The API Key                          |
| language    | NO       | String | en-US   |            | The language as ISO 639-1 code       |

##### Return Values

see [get popular tv response schema](https://developers.themoviedb.org/3/tv/get-popular-tv)

| Name    | Description                     | Type   | sample      |
|---------|---------------------------------|--------|-------------|
| result  | List of popular TV Show         | List   |             |

##### Synapses example

```yml
  - name: "popular-tv"
    signals:
      - order: "What are popular tv shows"
    neurons:
      - movie_db:
          api_key: "YOUR_API_KEY"
          action: "TV_POPULAR"
          language: "en"
          file_template: templates/movie_db_tv_popular.j2
```

The template defined in the templates/movie_db_tv_popular.j2

```jinja2
List of popular TV Shows :
{% for tv in results %}
    {{ tv['name'] }}
{% endfor %}
```

### TV_TOP_RATED

##### Options

| parameter   | required | type   | default | choices      | comment                              |
|-------------|----------|--------|---------|--------------|--------------------------------------|
| action      | YES      | String | None    | TV_TOP_RATED | Defines the action type              |
| api_key     | YES      | String | None    |              | The API Key                          |
| language    | NO       | String | en-US   |              | The language as ISO 639-1 code       |

##### Return Values

see [get top rated tv response schema](https://developers.themoviedb.org/3/tv/get-top-rated-tv)

| Name    | Description                     | Type   | sample      |
|---------|---------------------------------|--------|-------------|
| result  | List of top rated TV Show       | List   |             |

##### Synapses example

```yml
  - name: "top-rated-tv"
    signals:
      - order: "What are top rated Tv shows"
    neurons:
      - movie_db:
          api_key: "YOUR_API_KEY"
          action: "TV_TOP_RATED"
          language: "fr"
          file_template: templates/movie_db_tv_top_rated.j2
```

The template defined in the templates/movie_db_tv_top_rated.j2

```jinja2
List of top rated TV Shows :
{% for tv in results %}
    {{ tv['name'] }}
{% endfor %}
```

### TV_LATEST

##### Options

| parameter   | required | type   | default | choices    | comment                              |
|-------------|----------|--------|---------|------------|--------------------------------------|
| action      | YES      | String | None    | TV_LATEST  | Defines the action type              |
| api_key     | YES      | String | None    |            | The API Key                          |
| language    | NO       | String | en-US   |            | The language as ISO 639-1 code       |

##### Return Values

see [get latest tv response schema](https://developers.themoviedb.org/3/tv/get-latest-tv)

| Name   | Description                        | Type   | sample      |
|--------|------------------------------------|--------|-------------|
| result | List of most newly created TV show | List   |             |

##### Synapses example

```yml
  - name: "latest-tv"
    signals:
      - order: "What are the most newly created TV show"
    neurons:
      - movie_db:
          api_key: "YOUR_API_KEY"
          action: "TV_LATEST"
          language: "fr"
          file_template: templates/movie_db_tv_latest.j2
```

The template defined in the templates/movie_db_tv_latest.j2

```jinja2
Latest TV Show: {{ name }}
```

### TV_SEASON

##### Options

| parameter   | required | type   | default | choices    | comment                              |
|-------------|----------|--------|---------|------------|--------------------------------------|
| action      | YES      | String | None    | TV         | Defines the action type              |
| api_key     | YES      | String | None    |            | The API Key                          |
| tv          | YES      | String | None    |            | The TV Show to search for            |
| tv_season   | YES      | Int    | None    |            | The TV Show season to search for     |
| language    | NO       | String | en-US   |            | The language as ISO 639-1 code       |
| tv_extra    | NO       | String | None    |            | [extra data about the tv](EXTRA_DATA.md) |

##### Return Values
see [get tv season details response schema](https://developers.themoviedb.org/3/tv-seasons)

| Name   | Description                        | Type   | sample      |
|--------|------------------------------------|--------|-------------|
| query  | List of parameters (Tv, season)    | Object |             |
| tv     | Info about TV Show                 | Object |             |
| season | Info about TV Show Season          | Object |             |

##### Synapses example

```yml
- name: "tv-season"
    signals:
      - order: "Info about season {{ tv_season }} of {{ tv }}"
    neurons:
      - movie_db:
          api_key: "YOUR_API_KEY"
          action: "TV_SEASON"
          language: "fr"
          file_template: templates/movie_db_tv_season.j2
          tv: "{{ tv }}"
          tv_season: "{{ tv_season }}"
```

The template defined in the templates/movie_db_tv_season.j2

```jinja2
{% if tv is defined %}
    {% if season is defined %}
        Season {{ query["season"] }} of {{ query["tv"] }} : {{ season["name"] }}.

        Overview : {{ season["overview"] }}

        Name of {{ season["episodes"] }} episodes:
        {% for episode in season["episodes"] %}
            Episode {{ episode["episode_number"] }}: {{ episode["name"] }}
        {% endfor %}
    {% else %}
        Season {{ query["season"] }} of {{ query["tv"] }} not found
    {% endif %}
{% else %}
    Tv Show {{ query["tv"] }} not found
{% endif %}
```

### TV_EPISODE

##### Options

| parameter   | required | type   | default | choices    | comment                              |
|-------------|----------|--------|---------|------------|--------------------------------------|
| action      | YES      | String | None    | TV         | Defines the action type              |
| api_key     | YES      | String | None    |            | The API Key                          |
| tv          | YES      | String | None    |            | The movie to search for              |
| tv_season   | YES      | Int    | None    |            | The TV Show season to search for     |
| tv_episode  | YES      | Int    | None    |            | The TV Show episode to search for    |
| language    | NO       | String | en-US   |            | The language as ISO 639-1 code       |
| tv_extra    | NO       | String | None    |            | [extra data about the tv](EXTRA_DATA.md) |

##### Return Values

see [get tv episode details response schema](https://developers.themoviedb.org/3/tv-episodes)

| Name    | Description                              | Type   | sample      |
|---------|------------------------------------------|--------|-------------|
| query   | List of parameters (Tv, season, episode) | Object |             |
| tv      | Info about TV Show                       | Object |             |
| episode | Info about TV Show Episode               | Object |             |

##### Synapses example

```yml
  - name: "tv-episode"
    signals:
      - order: "Info about episode {{ tv_episode }} of season {{ tv_season }} of {{ tv }}"
    neurons:
      - movie_db:
          api_key: "YOUR_API_KEY"
          action: "TV_SEASON"
          language: "fr"
          file_template: templates/movie_db_tv_episode.j2
          tv: "{{ tv }}"
          tv_season: "{{ tv_season }}"
          tv_episode: "{{ tv_episode }}"
```

The template defined in the templates/movie_db_tv_episode.j2

```jinja2
{% if tv is defined %}
    {% if episode is defined %}
        Episode {{ query["episode"] }} of season {{ query["season"] }} of {{ query["tv"] }} : {{ episode["name"] }}.

        Overview: {{ episode["overview"] }}
    {% else %}
        Episode {{ query["episode"] }} of season {{ query["season"] }} of {{ query["tv"] }} not found
    {% endif %}
{% else %}
    TV Show {{ query["tv"] }} not found
{% endif %}
```

## Notes

In order to be able to query The Movie Db API, you need to get a api Key.

### How to get your The Movie Db Api Key

1. Create a [Movie Db account](https://www.themoviedb.org/account/signup)
1. Connect to your account
1. Go to API in the menu
1. Create a request for developer api key
1. Accept licence agreement
1. Fill information about application

See [Getting Started](https://developers.themoviedb.org/3/getting-started) for more information.
