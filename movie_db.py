import logging

import tmdbsimple as tmdb

from kalliope.core.NeuronModule import (NeuronModule,
                                        MissingParameterException,
                                        InvalidParameterException)

logging.basicConfig()
logger = logging.getLogger("kalliope")

MOVIEDB_ACTIONS = (
    "MOVIE",
    "PEOPLE",
    "POPULAR",
    "TOP_RATED",
    "UPCOMING",
    "NOW_PLAYING",
    "TV",
    "TV_POPULAR",
    "TV_TOP_RATED",
    "TV_LATEST",
    "TV_SEASON",
    "TV_EPISODE"
)

class Movie_db(NeuronModule):
    """
    Class used to search through The Movie Db API
    """
    def __init__(self, **kwargs):

        super(Movie_db, self).__init__(**kwargs)

        # parameters
        self.api_key = kwargs.get('api_key', None)
        self.language = kwargs.get('language', 'en-us')
        self.action = kwargs.get('action', None)
        self.region = kwargs.get('region', None)

        self.movie = kwargs.get('movie', None)
        self.movie_extra = kwargs.get('movie_extra', None)

        self.tv = kwargs.get('tv', None)
        self.tv_extra = kwargs.get('tv_extra', None)

        self.tv_season = kwargs.get('tv_season', None)
        self.tv_episode = kwargs.get('tv_episode', None)

        self.people = kwargs.get('people', None)

        logger.debug("Movie Db launch for action %s", self.action)

        # check parameters
        if self._is_parameters_ok():

            tmdb.API_KEY = self.api_key

            if self.action == MOVIEDB_ACTIONS[0]:  # MOVIE
                if self._is_movie_parameters_ok():
                    logger.debug("Searching for movies %s for language %s",
                                 self.movie,
                                 self.language)

                    result = dict()
                    result["query"] = self.movie
                    search = tmdb.Search()
                    search_response = search.movie(query=self.movie, language=self.language)

                    first_movie = next(iter(search_response["results"]), None)
                    if first_movie is None:
                        logger.debug("No movie matches the query")

                    else:
                        logger.debug("Movie db first result : %s with id %s",
                                     first_movie['title'],
                                     first_movie['id'])

                        movie = tmdb.Movies(first_movie['id'])
                        result['movie'] = movie.info(language=self.language,
                                                     append_to_response=self.movie_extra)

                    self.say(result)

            if self.action == MOVIEDB_ACTIONS[1]:  # PEOPLE
                if self.is_people_parameters_ok():
                    logger.debug("Searching for people with query %s", self.people)

                    search = tmdb.Search()
                    response = search.person(query=self.people)
                    first_people = search.results[0]
                    logger.debug("Movie db first result for people : %s", first_people)
                    self.say(first_people)

                    ##people = tmdb.People(firstPeople['id'])
                    ##peopleResponse = people.info()
                    ##self.say(peopleResponse)

            if self.action == MOVIEDB_ACTIONS[2]:  # POPULAR
                logger.debug("Searching for popular movies for language %s", self.language)
                movies = tmdb.Movies()
                popular_response = movies.popular(language=self.language)
                self.say(popular_response)

            if self.action == MOVIEDB_ACTIONS[3]:  # TOP_RATED
                logger.debug("Searching for top rated movies for language %s", self.language)
                movies = tmdb.Movies()
                top_rated_response = movies.top_rated(language=self.language)
                self.say(top_rated_response)

            if self.action == MOVIEDB_ACTIONS[4]:  # UPCOMING
                logger.debug("Searching for upcoming movies for language %s", self.language)
                movies = tmdb.Movies()
                upcoming = movies.upcoming(language=self.language, region=self.region)
                self.say(upcoming)

            if self.action == MOVIEDB_ACTIONS[5]:  # NOW_PLAYING
                logger.debug("Searching for now playing movies for language %s", self.language)
                movies = tmdb.Movies()
                now_playing_response = movies.now_playing(language=self.language,
                                                          region=self.region)
                self.say(now_playing_response)

            if self.action == MOVIEDB_ACTIONS[6]:  # TV
                if self._is_tv_parameters_ok():
                    logger.debug("Searching for tv show %s for language %s",
                                 self.tv,
                                 self.language)

                    result = dict()
                    result["query"] = self.tv
                    search = tmdb.Search()
                    search_response = search.tv(query=self.tv, language=self.language)

                    first_tv = next(iter(search_response["results"]), None)
                    if first_tv is None:
                        logger.debug("No tv matches the query")

                    else:
                        logger.debug("Movie db first result : %s with id %s",
                                     first_tv['name'],
                                     first_tv['id'])

                        tv = tmdb.TV(first_tv['id'])
                        result['tv'] = tv.info(language=self.language,
                                               append_to_response=self.tv_extra)

                    self.say(result)

            if self.action == MOVIEDB_ACTIONS[7]:  # TV_POPULAR
                logger.debug("Searching for popular TV Shows for language %s", self.language)
                tv = tmdb.TV()
                popular_response = tv.popular(language=self.language)
                self.say(popular_response)

            if self.action == MOVIEDB_ACTIONS[8]:  # TV_TOP_RATED
                logger.debug("Searching for top rated TV Shows for language %s", self.language)
                tv = tmdb.TV()
                top_rated_response = tv.top_rated(language=self.language)
                self.say(top_rated_response)

            if self.action == MOVIEDB_ACTIONS[9]:  # TV_LATEST
                logger.debug("Searching for latest TV Shows for language %s", self.language)
                tv = tmdb.TV()
                latest = tv.latest(language=self.language)
                self.say(latest)

            if self.action == MOVIEDB_ACTIONS[10]:  # TV_SEASON
                if self._is_tv_season_parameters_ok():
                    logger.debug("Searching for Season %s of TV Show %s for language %s",
                                 self.tv_season, self.tv, self.language)

                    search = tmdb.Search()
                    search_response = search.tv(query=self.tv, language=self.language)

                    result = dict()
                    result["query"] = dict()
                    result["query"]["tv"] = self.tv
                    result["query"]["season"] = self.tv_season

                    first_tv = next(iter(search_response["results"]), None)
                    result["tv"] = first_tv
                    if first_tv is None:
                        logger.debug("No tv matches the query")

                    else:
                        logger.debug("Movie db first result : %s with id %s",
                                     first_tv['name'],
                                     first_tv['id'])
                        season = tmdb.TV_Seasons(first_tv['id'], self.tv_season)
                        result["season"] = season.info(language=self.language,
                                                       append_to_response=self.tv_extra)

                    self.say(result)

            if self.action == MOVIEDB_ACTIONS[11]:  # TV_EPISODE
                if self._is_tv_episode_parameters_ok():
                    logger.debug("Searching for Episode %s of season %s of TV Show %s for language %s",
                                 self.tv_episode, self.tv_season, self.tv, self.language)

                    search = tmdb.Search()
                    search_response = search.tv(query=self.tv, language=self.language)

                    result = dict()
                    result["query"] = dict()
                    result["query"]["tv"] = self.tv
                    result["query"]["season"] = self.tv_season
                    result["query"]["episode"] = self.tv_episode

                    first_tv = next(iter(search_response["results"]), None)
                    result["tv"] = first_tv
                    if first_tv is None:
                        logger.debug("No tv matches the query")

                    else:
                        logger.debug("Movie db first result : %s with id %s",
                                     first_tv['name'],
                                     first_tv['id'])
                        episode = tmdb.TV_Episodes(first_tv['id'], self.tv_season, self.tv_episode)
                        result["episode"] = episode.info(language=self.language,
                                                         append_to_response=self.tv_extra)

                    self.say(result)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron.
        :return: True if parameters are ok, raise an exception otherwise.

        .. raises:: MissingParameterException, InvalidParameterException
        """
        if self.api_key is None:
            raise MissingParameterException("MovieDb needs an api key")
        if self.action is None:
            raise MissingParameterException("MovieDb needs an action parameter")
        if self.action not in MOVIEDB_ACTIONS:
            raise InvalidParameterException("MovieDb: invalid actions")
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

    def _is_tv_parameters_ok(self):
        """
        Check if parameters required to action TV are present.
        :return: True, if parameters are OK, raise exception otherwise.

        .. raises:: MissingParameterException
        """
        if self.tv is None:
            raise MissingParameterException("MovieDB TV action needs a tv")

        return True

    def _is_tv_season_parameters_ok(self):
        """
        Check if parameters required to action TV_SEASON are present.
        :return: True, if parameters are OK, raise exception otherwise.

        .. raises:: MissingParameterException
        """
        if self.tv is None:
            raise MissingParameterException("MovieDB TV_SEASON action needs a tv")
        if self.tv_season is None:
            raise MissingParameterException("MovieDB TV_SEASON action needs a tv season")

        return True

    def _is_tv_episode_parameters_ok(self):
        """
        Check if parameters required to action TV_EPISODE are present.
        :return: True, if parameters are OK, raise exception otherwise.

        .. raises:: MissingParameterException
        """
        if self.tv is None:
            raise MissingParameterException("MovieDB TV_EPISODE action needs a tv")
        if self.tv_season is None:
            raise MissingParameterException("MovieDB TV_EPISODE action needs a tv season")
        if self.tv_episode is None:
            raise MissingParameterException("MovieDB TV_EPISODE action needs a tv episode")

        return True
