# coding=utf-8

from ct_ingester.config import import_config
from ct_ingester.loggers import create_logger

import sqlalchemy.orm
from fform.dals_ct import DalClinicalTrials
from fform.orm_ct import Study
from fform.orm_ct import Location
from fform.orm_ct import Facility

logger = create_logger(logger_name=__name__)


def populate():

    with dal.session_scope() as session:

        query = session.query(Study)
        # query = query.options(
        #     sqlalchemy.orm.load_only(Study.study_id),
        #     sqlalchemy.orm.joinedload(
        #         Study.locations
        #     ).load_only(
        #         Location.location_id
        #     ).joinedload(Location.facility).load_only(
        #         Facility.facility_id,
        #         Facility.facility_canonical_id,
        #     ),
        # )

        for study in query.yield_per(10):
            msg_fmt = "Processing study {}".format(study)
            logger.info(msg_fmt)

            for location in study.locations:
                msg_fmt = "Processing location {}".format(location)
                logger.info(msg_fmt)

                facility_id = location.facility_id
                facility_canonical_id = location.facility.facility_canonical_id
                dal.iodu_study_facility(
                    study_id=study.study_id,
                    facility_id=facility_id,
                    facility_canonical_id=facility_canonical_id,
                )


if __name__ == '__main__':

    cfg = import_config("/etc/ct-ingester/ct-ingester-dev.json")

    # Create a new clinical-trials DAL.
    dal = DalClinicalTrials(
        sql_username="somada141",
        sql_password="BcOGAdy6kHnk0tIcLyYLRcfB8ZiqT6PiSn8mHjc6",
        sql_host="192.168.0.12",
        sql_port=cfg.sql_port,
        sql_db=cfg.sql_db,
    )

    populate()
