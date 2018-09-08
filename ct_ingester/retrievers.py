# coding=utf-8

from typing import Optional, List, Dict

import requests
from fform.orm_ct import Facility

from ct_ingester.loggers import create_logger
from ct_ingester.excs import GooglePlacesApiQueryLimitError


logger = create_logger(logger_name=__name__)


class RetrieverGoogleMaps(object):

    api_url_default_place_search = ("https://maps.googleapis.com/maps/api/"
                                    "place/findplacefromtext/json")

    api_url_default_place_details = ("https://maps.googleapis.com/maps/api/"
                                     "place/details/json")

    fields_defaults_place_search = [
        "place_id",
    ]

    fields_defaults_place_details = [
        "geometry/location",
        "formatted_address",
        "address_component",
        "name",
        "url",
        "formatted_phone_number",
        "international_phone_number",
        "website",
    ]

    def __init__(
        self,
        api_key: str,
        **kwargs
    ):
        """Constructor and initialization.

        Args:
            api_key (str): The Google Places API key.
        """

        # Internalize arguments.
        self.api_key = api_key

        self.logger = create_logger(
            logger_name=type(self).__name__,
            logger_level=kwargs.get("logger_level", "DEBUG")
        )

    def search_place(
        self,
        query: str,
        base_url: Optional[str] = None,
        fields: Optional[List[str]] = None,
    ) -> Dict:

        # Fallback to the default URL if none is defined.
        base_url = base_url if base_url else self.api_url_default_place_search

        # Fallback to the default fields if none are defined.
        fields = fields if fields else self.fields_defaults_place_search

        # Perform the request.
        response = requests.get(
            url=base_url,
            params={
                "key": self.api_key,
                "inputtype": "textquery",
                "input": query,
                "language": "en",
                "fields": ",".join(fields),
            }
        )

        result = None
        if response.ok:
            result = response.json()

        return result

    def get_place_details(
        self,
        google_place_id: str,
        base_url: Optional[str] = None,
        fields: Optional[List[str]] = None,
    ):

        # Fallback to the default URL if none is defined.
        base_url = base_url if base_url else self.api_url_default_place_details

        # Fallback to the default fields if none are defined.
        fields = fields if fields else self.fields_defaults_place_details

        # Perform the request.
        response = requests.get(
            url=base_url,
            params={
                "key": self.api_key,
                "place_id": google_place_id,
                "language": "en",
                "fields": ",".join(fields),
            }
        )

        result = None
        if response.ok:
            result = response.json()

        return result


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
        msg_fmt = msg.format(facility, query)
        logger.debug(msg_fmt)

        # Perform the request against the Google Places API.
        response = retriever.search_place(query=query)

        if not response:
            return None

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

