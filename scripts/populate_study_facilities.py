# coding=utf-8

"""
Script to populate the `study_facilities` table (optionally) limited to
recently updated studies.
"""

import argparse
import datetime
from typing import Iterable, Optional, List

from ct_ingester.config import import_config
from ct_ingester.loggers import create_logger

import sqlalchemy.orm
from fform.dals_ct import DalClinicalTrials
from fform.orm_ct import Study
from fform.orm_ct import StudyFacility
from fform.orm_ct import StudyDates

from ct_ingester.utils import chunk_generator

logger = create_logger(logger_name=__name__)


def find_recent_studies(
    session: sqlalchemy.orm.Session,
    num_days: Optional[int] = None,
    chunk_size: Optional[int] = 10,
    skip_populated: Optional[bool] = False,
) -> Iterable[Iterable[Study]]:
    """ Retrieves recently updated studies."""

    query = session.query(Study)  # type: sqlalchemy.orm.Query
    query = query.join(Study.study_dates)

    # Filter down to studies updated in the last `num_days` days.
    if num_days:
        query = query.filter(
            StudyDates.last_update_posted
            > (datetime.date.today() - datetime.timedelta(days=num_days))
        )

    if skip_populated:
        query = query.outerjoin(Study.study_facilities)
        query = query.filter(StudyFacility.study_id == None)

    studies_chunks = chunk_generator(
        generator=query.yield_per(chunk_size), chunk_size=chunk_size
    )

    return studies_chunks


def populate(
    dal: DalClinicalTrials,
    num_days: Optional[int] = None,
    chunk_size: Optional[int] = 10,
    skip_populated: Optional[bool] = False,
    dry_run: Optional[bool] = False,
):

    with dal.session_scope() as session:  # type: sqlalchemy.orm.Session

        studies_chunks = find_recent_studies(
            session=session,
            num_days=num_days,
            chunk_size=chunk_size,
            skip_populated=skip_populated,
        )
        for studies_chunk in studies_chunks:
            studies = list(studies_chunk)  # type: List[Study]
            logger.warning(len(studies))
            for study in studies:
                logger.info(f"Processing study with ID {study.study_id}")

                for location in study.locations:
                    logger.info(
                        f"Processing location with ID {location.location_id}"
                    )

                    facility_id = location.facility_id
                    facility_canonical_id = (
                        location.facility.facility_canonical_id
                    )

                    _prefix = "[DRY RUN] " if dry_run else ""

                    logger.info(
                        f"{_prefix}IODUing `StudyFacility` with a `study_id`"
                        f" of '{study.study_id}', `facility_id` of "
                        f"{facility_id}, and `facility_canonical_id` of "
                        f"'{facility_canonical_id}'."
                    )

                    if not dry_run:
                        dal.iodu_study_facility(
                            study_id=study.study_id,
                            facility_id=facility_id,
                            facility_canonical_id=facility_canonical_id,
                        )


if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser(
        description=(
            "ct-ingester: ClinicalTrials.gov XML dump parser and SQL "
            "ingester."
        )
    )
    argument_parser.add_argument(
        "--num-days",
        dest="num_days",
        help="number of days",
        required=False,
        default=None,
    )
    argument_parser.add_argument(
        "--dry-run",
        dest="dry_run",
        help="dry run",
        required=False,
        default=False,
        action="store_true",
    )
    argument_parser.add_argument(
        "--skip-populated",
        dest="skip_populated",
        help="skip previously populated studies",
        required=False,
        default=False,
        action="store_true",
    )
    argument_parser.add_argument(
        "--config-file",
        dest="config_file",
        help="configuration file",
        required=True,
    )
    arguments = argument_parser.parse_args()

    if arguments.dry_run:
        logger.info("Performing a dry-run.")

    cfg = import_config(arguments.config_file)

    # Create a new DAL.
    _dal = DalClinicalTrials(
        sql_username=cfg.sql_username,
        sql_password=cfg.sql_password,
        sql_host=cfg.sql_host,
        sql_port=cfg.sql_port,
        sql_db=cfg.sql_db,
    )

    populate(
        dal=_dal,
        num_days=int(arguments.num_days) if arguments.num_days else None,
        skip_populated=arguments.skip_populated,
        dry_run=arguments.dry_run,
    )
