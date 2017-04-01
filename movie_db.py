import logging

import tmdbsimple as tmdb

from kalliope import Utils
from kalliope.core.NeuronModule import NeuronModule, MissingParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")

Slack_Actions = (
    "MOVIE",
    "PEOPLE",
    "POPULAR",
    "TOP_RATED",
    "UPCOMING",
    "NOW_PLAYING"
)

class Movie_db(NeuronModule):
    def __init__(self, **kwargs):

        super(Movie_db, self).__init__(**kwargs)

        # parameters
        self.api_key = kwargs.get('api_key', None)
        self.language = kwargs.get('language', 'en-us')
        self.action = kwargs.get('action', None)

        self.movie = kwargs.get('movie', None)
        self.region = kwargs.get('region', None)

        self.people = kwargs.get('people', None)

        logger.debug("Movie Db launch for action %s", self.action)
        
        # check parameters
        if self._is_parameters_ok():
            
            tmdb.API_KEY = self.api_key

            if self.action == Slack_Actions[0]:  # MOVIE
                if self._is_movie_parameters_ok():
                    logger.debug("Searching for movies %s for language %s", self.movie, self.language)

                    result = dict()
                    result["query"] = self.movie
                    search = tmdb.Search()
                    searchResponse = search.movie(query= self.movie, language= self.language)

                    firstMovie = next(iter(searchResponse["results"]), None)
                    if firstMovie is None:
                        logger.debug("No movie matches the query")

                    else:
                        logger.debug("Movie db first result : %s with id %s", firstMovie['title'], firstMovie['id'])
                    
                        movie = tmdb.Movies(firstMovie['id'])
                        result['movie'] = movie.info(language= self.language, append_to_response='credits')
                    
                    self.say(result)
                    
            if self.action == Slack_Actions[1]:  # PEOPLE
                if self.is_people_parameters_ok():   
                    logger.debug("Searching for people with query %s" % self.people)

                    search = tmdb.Search()
                    response = search.person(query= self.people)
                    firstPeople = search.results[0]
                    logger.debug("Movie db first result for people : %s" % firstPeople )
                    self.say(firstPeople)
                    
                    ##people = tmdb.People(firstPeople['id'])
                    ##peopleResponse = people.info()
                    ##self.say(peopleResponse)

            if self.action == Slack_Actions[2]:  # POPULAR
                logger.debug("Searching for popular movies for language %s" % self.language)
                movies = tmdb.Movies()
                popularResponse = movies.popular(language= self.language)
                self.say(popularResponse)

            if self.action == Slack_Actions[3]:  # TOP_RATED
                logger.debug("Searching for top rated movies for language %s" % self.language)
                movies = tmdb.Movies()
                popularResponse = movies.top_rated(language= self.language)
                self.say(popularResponse)

            if self.action == Slack_Actions[4]:  # UPCOMING
                logger.debug("Searching for upcoming movies for language %s" % self.language)
                movies = tmdb.Movies()
                popularResponse = movies.upcoming(language= self.language, region=self.region)
                self.say(popularResponse)

            if self.action == Slack_Actions[5]:  # NOW_PLAYING
                logger.debug("Searching for now playing movies for language %s" % self.language)
                movies = tmdb.Movies()
                popularResponse = movies.now_playing(language= self.language, region=self.region)
                self.say(popularResponse)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron.
        :return: True if parameters are ok, raise an exception otherwise.

        .. raises:: MissingParameterException
        """
        if self.api_key is None:
            raise MissingParameterException("MovieDb needs an api key")
        if self.action is None:
            raise MissingParameterException("MovieDb needs an action parameter")
        return True

    def _is_movie_parameters_ok(self):
        """
        Check if parameters required to action MOVIE are present.
        :return: True, if parameters are OK, raise exception otherwise.

        .. raises:: MissingParameterException
        """
        if self.movie is None:
            raise MissingParameterException("MovieDB MOVIE action needs a movie")
        
        return True

    def is_people_parameters_ok(self):
        """
        Check if parameters required to action PEOPLE are present.
        :return: True, if parameters are OK, raise exception otherwise.

        .. raises:: MissingParameterException
        """
        if self.people is None:
            raise MissingParameterException("MovieDb PEOPLE action needs a people to search")

        return True

    
