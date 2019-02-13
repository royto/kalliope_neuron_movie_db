# Using Movie DB Extra Data

## Introduction

Movie DB allows you to get [additional data](https://developers.themoviedb.org/3/getting-started/append-to-response) when querying a Movie, a People, a TV Show, a TV episode or a TV Season. This feature is implemented in the neuron allowing you to get extra data related to your search.

Multiple additional data is supported, just comma separate the values.

## Example
Let's see an example where we will get [recommendations](https://developers.themoviedb.org/3/tv/get-tv-recommendations) based on a TV Show.

We use the neuron action *TV* with 'recommendations' as *tv_extra* parameter value.

### Synapse
``` yml
  - name: "recommendations-tv"
    signals:
      - order: "recommend me TV Show like  {{ tv }}"
    neurons:
      - movie_db:
          api_key: "YOUR API KEY"
          action: "TV"
          language: "fr"
          tv_extra: "recommendations"
          file_template: templates/tv_recommendations_db_movie.j2
          tv: {{ tv }}
```

Extra data will be available in a property named as the extra data name, tv["recommendations]" in our case.

The template defined in the templates/tv_recommendations_db_movie.j2 gets name of every recommendations.
```jinja2
{% if tv is defined %}
    Recommendations based on {{ tv["name"] }}

    {% if tv['recommendations'] is defined %}
        {% set recommendations = tv['recommendations']['results'] %}
         {{ recommendations|map(attribute='name')|join(', ') }}
    {% endif %}
{% else %}
    No TV Show found
{% endif %}
```