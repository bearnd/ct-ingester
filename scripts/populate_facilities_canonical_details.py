# coding=utf-8

import multiprocessing

import sqlalchemy.orm
from fform.dals_ct import DalClinicalTrials
from fform.orm_ct import FacilityCanonical

from ct_ingester.config import import_config
from ct_ingester.loggers import create_logger
from ct_ingester.retrievers import RetrieverGoogleMaps
from ct_ingester.retrievers import get_place_details
from ct_ingester.utils import chunk_generator

from scripts.utils import iodu_canonical_facility_from_google


logger = create_logger(logger_name=__name__)


api_keys = [
    "AIzaSyCJ65svcyTj2fEpBgjNhL7_Zk7yhfQxh6Y",
    "AIzaSyBBU2IJcRgMtYnCEgYwoVVTIZ_tR-kKg_g",
    "AIzaSyBhYcbF_PtLpA_BuckzQfd2A6XeWxF3s-Y",
    "AIzaSyDhG5rV9SNu0uQV88lq9QvjXRXI_Mzz3Lo",
]


def _get_place_details(google_place_id):
    global retriever
    return get_place_details(
        google_place_id=google_place_id,
        retriever=retriever
    )


def populate():

    with dal.session_scope() as session:

        # Query out `FacilityCanonical` records without a country, i.e.,
        # records that haven't had their details filled out.
        query = session.query(FacilityCanonical)  # type: sqlalchemy.orm.Query
        query = query.filter(FacilityCanonical.country.is_(None))

        # Chunk the query results.
        facilities_chunks = chunk_generator(
            generator=iter(query.yield_per(50)),
            chunk_size=50,
        )
        # Create a process pool.
        pool = multiprocessing.Pool(processes=50)

        for facilities_chunk in facilities_chunks:

            facilities = list(facilities_chunk)
            google_place_ids = [
                facility.google_place_id for facility in facilities
            ]
            responses = pool.map(_get_place_details, google_place_ids)

            for facility, response in zip(facilities, responses):

                if not response:
                    continue

                iodu_canonical_facility_from_google(
                    dal=dal,
                    google_place_id=facility.google_place_id,
                    google_response=response
                )


if __name__ == '__main__':
    cfg = import_config("/etc/ct-ingester/ct-ingester-dev.json")

    dal = DalClinicalTrials(
        sql_username=cfg.sql_username,
        sql_password=cfg.sql_password,
        sql_host="192.168.0.12",
        sql_port=cfg.sql_port,
        sql_db=cfg.sql_db,
    )

    retriever = RetrieverGoogleMaps(api_key=api_keys[0])

    populate()
