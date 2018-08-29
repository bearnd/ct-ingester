# -*- coding: utf-8 -*-

from typing import Dict

from fform.orm_ct import Facility

from ct_ingester.retrievers import RetrieverGoogleMaps
from ct_ingester.loggers import create_logger
from ct_ingester.excs import GooglePlacesApiQueryLimitError


logger = create_logger(logger_name=__name__)


def log_ingestion_of_document(
    document_name: str
):

    # Define the actual decorator. This three-tier decorator functions are
    # necessary when defining decorator functions with arguments.
    def log_ingestion_of_document_decorator(func):
        # Define the wrapper function.
        def wrapper(self, *args, **kwargs):

            msg = "Ingesting '{}' document"
            msg_fmt = msg.format(document_name)
            self.logger.debug(msg_fmt)

            # Simply execute the decorated method with the provided arguments
            # and return the result.
            return func(self, *args, **kwargs)

        return wrapper

    return log_ingestion_of_document_decorator


def find_facility_google_place(
    retriever: RetrieverGoogleMaps,
    facility: Facility
):
    """Searches for the Google Maps place matching a `Facility` record in an
    iterative manner.

    Args:
        retriever (RetrieverGoogleMaps): The `RetrieverGoogleMaps` object that
            will be used to interact with the Google Places API.
        facility (Facility): The `Facility` record object for which the search
            is performed.

    Returns:
        Dict: The Google Place API response containing the results of a
            successful match.

    Raises:
        GooglePlacesApiQueryLimitError: Raised when the Google Places API
            reports that the maximum number of requests for the day has been
            reached.
    """

    msg_fmt = "Performing place-search for facility '{}'.".format(facility)
    logger.info(msg_fmt)

    # Define a list of facility location components that can be used to identify
    # it in the Google Places API in order of decreasing granularity.
    search_input_components = [
        facility.name,
        facility.city,
        facility.state,
        facility.country,
    ]

    response = None
    # Perform iterative requests against the Google Places API gradually
    # decreasing granularity until a place if found.
    for i in range(len(search_input_components)):
        # Assemble a search query string by joining components that aren't
        # `None`.
        query = " ".join(list(filter(
            lambda x: x is not None,
            search_input_components[i:],
        )))

        # If the remaining query components yield an empty string then we cant
        # perform a search so we're returning `None`.
        if not query:
            return None

        msg = "Performing place-search for facility '{}' with query '{}'."
        msg_fmt = msg.format(Facility, query)
        logger.debug(msg_fmt)

        # Perform the request against the Google Places API.
        response = retriever.search_place(query=query)

        # If the response has a `ZERO_RESULTS` status then repeat the request
        # gradually decreasing granularity.
        if response["status"] == "ZERO_RESULTS":
            msg_fmt = "No results found for query '{}'.".format(query)
            logger.debug(msg_fmt)
            continue
        # If the response has a `OVER_QUERY_LIMIT` status then throw the
        # corresponding exception.
        elif response["status"] == "OVER_QUERY_LIMIT":
            msg_fmt = "Query limit exceeded."
            raise GooglePlacesApiQueryLimitError(msg_fmt)
        # If the request succeeded and a place was found then return the
        # response.
        elif response["status"] == "OK":
            msg = "Results '{}' found for query '{}'."
            msg_fmt = msg.format(response, query)
            logger.info(msg_fmt)
            return response

    return response
