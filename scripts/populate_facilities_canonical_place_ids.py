# coding=utf-8

import multiprocessing

import sqlalchemy.orm
from fform.dals_ct import DalClinicalTrials
from fform.orm_ct import Facility

from ct_ingester.config import import_config
from ct_ingester.loggers import create_logger
from ct_ingester.retrievers import RetrieverGoogleMaps
from ct_ingester.retrievers import find_facility_google_place
from ct_ingester.utils import chunk_generator


logger = create_logger(logger_name=__name__)


def find_place(facility: Facility):
    global retriever
    return find_facility_google_place(retriever, facility)


def populate():

    with dal.session_scope() as session:
        # Query out `Facility` records without a canonical facility ID.
        query = session.query(Facility)  # type: sqlalchemy.orm.Query
        query = query.filter(Facility.facility_canonical_id.is_(None))

        # Chunk the query results.
        facilities_chunks = chunk_generator(
            generator=iter(query.yield_per(50)),
            chunk_size=50,
        )
        # Create a process pool.
        pool = multiprocessing.Pool(processes=50)

        for facilities_chunk in facilities_chunks:
            # Consume the generator creating a list of all facilities in the
            # chunk.
            facilities = list(facilities_chunk)
            # Retrieve the Google Place IDs for all facilities in the chunk in
            # parallel.
            responses = pool.map(find_place, facilities)

            # Iterate over the facilities in the chunk and the responses of the
            # Google place ID retrieval and persist the IDs in the DB.
            for facility, response in zip(facilities, responses):

                # Skip empty responses.
                if not response or not response.get("candidates"):
                    continue

                # Retrieving Google Place ID from the first candidate.
                place_id = response["candidates"][0]["place_id"]

                facility_canonical_id = dal.iodu_facility_canonical(
                    google_place_id=place_id,
                    name=None,
                    google_url=None,
                    url=None,
                    address=None,
                    phone_number=None,
                    coordinate_longitude=None,
                    coordinate_latitude=None,
                    country=None,
                    administrative_area_level_1=None,
                    administrative_area_level_2=None,
                    administrative_area_level_3=None,
                    administrative_area_level_4=None,
                    administrative_area_level_5=None,
                    locality=None,
                    sublocality=None,
                    sublocality_level_1=None,
                    sublocality_level_2=None,
                    sublocality_level_3=None,
                    sublocality_level_4=None,
                    sublocality_level_5=None,
                    colloquial_area=None,
                    floor=None,
                    room=None,
                    intersection=None,
                    neighborhood=None,
                    post_box=None,
                    postal_code=None,
                    postal_code_prefix=None,
                    postal_code_suffix=None,
                    postal_town=None,
                    premise=None,
                    subpremise=None,
                    route=None,
                    street_address=None,
                    street_number=None,
                )

                dal.update_attr_value(
                    orm_class=Facility,
                    pk=facility.facility_id,
                    attr_name="facility_canonical_id",
                    attr_value=facility_canonical_id,
                )


if __name__ == '__main__':
    cfg = import_config("/etc/ct-ingester/ct-ingester-dev.json")

    # Create a new DAL.
    dal = DalClinicalTrials(
        sql_username=cfg.sql_username,
        sql_password=cfg.sql_password,
        sql_host="192.168.0.168",
        sql_port=cfg.sql_port,
        sql_db=cfg.sql_db,
    )

    # Create a new retriever.
    retriever = RetrieverGoogleMaps(api_key=cfg.google_maps_api_key)

    populate()
