# -*- coding: utf-8 -*-

import datetime
from typing import Union

import dateparser

from ct_ingester.loggers import create_logger


logger = create_logger(logger_name=__name__)


def parse_date_pattern(
    str_date: str,
    do_cast_to_date: bool=False,
) -> Union[datetime.datetime, None]:
    """Parses a possibly-partial date-string and converts it to an absolute
    date."""

    if ("N/A" in str_date) or (not str_date):
        return None

    #
    dt = dateparser.parse(
        date_string=str_date,
        settings={
            "PREFER_DAY_OF_MONTH": "first",
            "PREFER_DATES_FROM": "future",
        },
    )

    # If `dt` is defined and `do_cast_to_date` is set to `True` then cast the
    # `datetime.datetime` to `datetime.date`.
    if dt and do_cast_to_date:
        dt = dt.date()

    return dt
