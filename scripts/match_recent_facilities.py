import argparse
import datetime

import sqlalchemy.orm
from fform.dals_ct import DalClinicalTrials
from fform.orm_ct import Facility
from fform.orm_ct import FacilityCanonical
from fform.orm_ct import Study
from fform.orm_ct import StudyDates

from ct_ingester.config import import_config
from ct_ingester.loggers import create_logger
from ct_ingester.retrievers import RetrieverGoogleMaps
from ct_ingester.retrievers import find_facility_google_place
from ct_ingester.retrievers import get_place_details

from scripts.utils import iodu_canonical_facility_from_google

logger = create_logger(logger_name=__name__)


def find_recent_unmatched_facilities(dal: DalClinicalTrials):

    with dal.session_scope() as session:  # type: sqlalchemy.orm.Session
        query = session.query(Facility)
        query = query.join(Facility.studies)
        query = query.join(Study.study_dates)

        # Filter down to facilities not matched with a canonical facility.
        query = query.filter(Facility.facility_canonical_id.is_(None))

        # Filter down to studies updated in the last 2 days.
        query = query.filter(
            StudyDates.last_update_posted
            > (datetime.date.today() - datetime.timedelta(days=2))
        )

        query = query.group_by(Facility.facility_id)

        facilities_unmatched = query.all()

    return facilities_unmatched


def match(dal: DalClinicalTrials, retriever: RetrieverGoogleMaps):

    logger.info(
        "Retrieving unmatched facilities linked to studies updated in the "
        "past 2 days."
    )

    facilities_unmatched = find_recent_unmatched_facilities(dal=dal)

    logger.info(
        f"Retrieved {len(facilities_unmatched)} unmatched facilities linked "
        f"to studies updated in the past 2 days."
    )

    for facility in facilities_unmatched:

        logger.info(f"Processing facility {facility}.")

        logger.info(f"Matching facility {facility} against a Google Place.")

        place_response = find_facility_google_place(
            retriever=retriever, facility=facility
        )

        # Skip empty responses.
        if not place_response or not place_response.get("candidates"):
            logger.warning(
                f"No Google Place match found for facility {facility}."
                f" Skipping."
            )
            continue

        # Retrieving Google Place ID from the first candidate.
        google_place_id = place_response["candidates"][0]["place_id"]

        logger.info(
            f"Google Place with ID '{google_place_id}' found matching "
            f" facility {facility}."
        )

        with dal.session_scope() as session:  # type: sqlalchemy.orm.Session
            # noinspection PyTypeChecker
            facility_canonical = dal.get_by_attr(
                orm_class=FacilityCanonical,
                attr_name="google_place_id",
                attr_value=google_place_id,
                session=session,
            )  # type: FacilityCanonical

            if facility_canonical:
                facility_canonical_id = facility_canonical.facility_canonical_id

                logger.info(
                    f"Google Place with ID '{google_place_id}' previously "
                    f"stored as canonical facility {facility_canonical}."
                )
            else:
                logger.info(
                    f"Google Place with ID '{google_place_id}' not previously "
                    f"stored as a canonical facility."
                )

                logger.info(
                    f"Retrieving Google Place details for Google Place with "
                    f"ID '{google_place_id}'."
                )

                details_response = get_place_details(
                    google_place_id=google_place_id, retriever=retriever
                )

                if not details_response:
                    logger.warning(
                        f"No Google Place details retrieved for Google Place "
                        f"with ID '{google_place_id}'. Skipping."
                    )
                    continue

                facility_canonical_id = iodu_canonical_facility_from_google(
                    dal=dal,
                    google_place_id=google_place_id,
                    google_response=details_response,
                )

            logger.info(
                f"Linking facility {facility} with canonical facility "
                f"{facility_canonical}."
            )

            dal.update_attr_value(
                orm_class=Facility,
                pk=facility.facility_id,
                attr_name="facility_canonical_id",
                attr_value=facility_canonical_id,
                session=session,
            )


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser(
        description=(
            "ct-ingester: ClinicalTrials.gov XML dump parser and SQL "
            "ingester."
        )
    )
    argument_parser.add_argument(
        "--config-file",
        dest="config_file",
        help="configuration file",
        required=False,
    )
    arguments = argument_parser.parse_args()

    cfg = import_config(arguments.config_file)

    # Create a new DAL.
    _dal = DalClinicalTrials(
        sql_username=cfg.sql_username,
        sql_password=cfg.sql_password,
        sql_host=cfg.sql_host,
        sql_port=cfg.sql_port,
        sql_db=cfg.sql_db,
    )

    # Create a new retriever.
    _retriever = RetrieverGoogleMaps(api_key=cfg.google_maps_api_key)

    match(dal=_dal, retriever=_retriever)
