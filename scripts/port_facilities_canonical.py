# coding=utf-8

import argparse
import binascii
import csv
from typing import List

from shapely import wkb
import sqlalchemy.orm
from fform.dals_ct import DalClinicalTrials
from fform.orm_ct import Facility
from fform.orm_ct import FacilityCanonical

from ct_ingester.config import import_config
from ct_ingester.loggers import create_logger
from ct_ingester.utils import chunk_generator


logger = create_logger(logger_name=__name__)


def read_facilities(filename_facilities_csv):

    msg = "Reading `facilities` CSV file '{}'"
    msg_fmt = msg.format(filename_facilities_csv)
    logger.info(msg_fmt)

    facilities = {}
    with open(filename_facilities_csv) as finp:
        reader = csv.DictReader(
            finp,
            fieldnames=[
                "facility_id",
                "name",
                "city",
                "state",
                "zip_code",
                "country",
                "md5",
                "facility_canonical_id",
            ],
            delimiter="|",
        )
        for entry in reader:
            md5 = entry["md5"].replace("\\x", "")
            facilities[md5] = entry

    return facilities


def read_facilities_canonical(filename_facilities_canonical_csv):

    msg = "Reading `facilities_canonical` CSV file '{}'"
    msg_fmt = msg.format(filename_facilities_canonical_csv)
    logger.info(msg_fmt)

    facilities_canonical = {}
    with open(filename_facilities_canonical_csv) as finp:
        reader = csv.DictReader(
            finp,
            fieldnames=[
                "facility_canonical_id",
                "google_place_id",
                "name",
                "google_url",
                "url",
                "address",
                "phone_number",
                "coordinates",
                "country",
                "administrative_area_level_1",
                "administrative_area_level_2",
                "administrative_area_level_3",
                "administrative_area_level_4",
                "administrative_area_level_5",
                "locality",
                "sublocality",
                "sublocality_level_1",
                "sublocality_level_2",
                "sublocality_level_3",
                "sublocality_level_4",
                "sublocality_level_5",
                "colloquial_area",
                "floor",
                "room",
                "intersection",
                "neighborhood",
                "post_box",
                "postal_code",
                "postal_code_prefix",
                "postal_code_suffix",
                "postal_town",
                "premise",
                "subpremise",
                "route",
                "street_address",
                "street_number",
            ],
            delimiter="|",
        )
        for entry in reader:
            facilities_canonical[entry["facility_canonical_id"]] = entry

    return facilities_canonical


def ingest_facility_canonical_old(facility_canonical_old):

    msg = "Ingesting canonical facility with Google Place ID '{}'"
    msg_fmt = msg.format(facility_canonical_old["google_place_id"])
    logger.info(msg_fmt)

    coordinates_str_hex = facility_canonical_old["coordinates"]
    if coordinates_str_hex:
        coordinates_str_bin = binascii.unhexlify(coordinates_str_hex)
        point = wkb.loads(coordinates_str_bin)
        coordinate_longitude = point.x
        coordinate_latitude = point.y
    else:
        coordinate_longitude = None
        coordinate_latitude = None

    facility_canonical_id = dal.iodu_facility_canonical(
        google_place_id=facility_canonical_old["google_place_id"],
        name=facility_canonical_old["name"],
        google_url=facility_canonical_old["google_url"],
        url=facility_canonical_old["url"],
        address=facility_canonical_old["address"],
        phone_number=facility_canonical_old["phone_number"],
        coordinate_longitude=coordinate_longitude,
        coordinate_latitude=coordinate_latitude,
        country=facility_canonical_old["country"],
        administrative_area_level_1=
        facility_canonical_old["administrative_area_level_1"],
        administrative_area_level_2=
        facility_canonical_old["administrative_area_level_2"],
        administrative_area_level_3=
        facility_canonical_old["administrative_area_level_3"],
        administrative_area_level_4=
        facility_canonical_old["administrative_area_level_4"],
        administrative_area_level_5=
        facility_canonical_old["administrative_area_level_5"],
        locality=facility_canonical_old["locality"],
        sublocality=facility_canonical_old["sublocality"],
        sublocality_level_1=facility_canonical_old["sublocality_level_1"],
        sublocality_level_2=facility_canonical_old["sublocality_level_2"],
        sublocality_level_3=facility_canonical_old["sublocality_level_3"],
        sublocality_level_4=facility_canonical_old["sublocality_level_4"],
        sublocality_level_5=facility_canonical_old["sublocality_level_5"],
        colloquial_area=facility_canonical_old["colloquial_area"],
        floor=facility_canonical_old["floor"],
        room=facility_canonical_old["room"],
        intersection=facility_canonical_old["intersection"],
        neighborhood=facility_canonical_old["neighborhood"],
        post_box=facility_canonical_old["post_box"],
        postal_code=facility_canonical_old["postal_code"],
        postal_code_prefix=facility_canonical_old["postal_code_prefix"],
        postal_code_suffix=facility_canonical_old["postal_code_suffix"],
        postal_town=facility_canonical_old["postal_town"],
        premise=facility_canonical_old["premise"],
        subpremise=facility_canonical_old["subpremise"],
        route=facility_canonical_old["route"],
        street_address=facility_canonical_old["street_address"],
        street_number=facility_canonical_old["street_number"],
    )

    return facility_canonical_id


def populate(
    filename_facilities_csv: str,
    filename_facilities_canonical_csv: str
):
    # Read the previous `facilities` table dump CSV.
    facilities_old = read_facilities(
        filename_facilities_csv=filename_facilities_csv,
    )
    # Read the previous `facilities_canonical` table dump CSV.
    facilities_canonical_old = read_facilities_canonical(
        filename_facilities_canonical_csv=filename_facilities_canonical_csv,
    )

    with dal.session_scope() as session:
        # Query out `Facility` records without a canonical facility ID.
        query = session.query(Facility)  # type: sqlalchemy.orm.Query
        query = query.filter(Facility.facility_canonical_id.is_(None))

        # Chunk the query results.
        facilities_chunks = chunk_generator(
            generator=iter(query.yield_per(50)),
            chunk_size=50,
        )

        # Iterate over the new facilities in a chunked-fashion.
        for facilities_chunk in facilities_chunks:
            facilities_new = list(facilities_chunk)  # type: List[Facility]

            # Iterate over the new facilities chunk.
            for facility_new in facilities_new:

                msg = "Processing facility with ID '{}'"
                msg_fmt = msg.format(facility_new.facility_id)
                logger.info(msg_fmt)

                # Get the hexadecimal MD5 of the new facility.
                md5_hex = facility_new.md5.hex()

                # Skip new facilities that aren't represented in
                # `facilities_old`.
                if md5_hex not in facilities_old:
                    continue

                facility_old = facilities_old[md5_hex]

                # Retrieve the ID of the old canonical facility this facility
                # should be associated with.
                facility_canonical_id_old = facility_old[
                    "facility_canonical_id"
                ]

                if facility_canonical_id_old not in facilities_canonical_old:
                    continue

                # Retrieve the data of the associated old canonical facility.
                facility_canonical_old = facilities_canonical_old[
                    facility_canonical_id_old
                ]

                # (Attempt to) retrieve the newly stored canonical facility
                # (possibly in a previous run of this script).
                facility_canonical_new = dal.get_by_attr(
                    orm_class=FacilityCanonical,
                    attr_name="google_place_id",
                    attr_value=facility_canonical_old["google_place_id"],
                )  # type: FacilityCanonical

                # If the canonical facility has not been stored anew (possibly
                # in a previous run) of this script then store it. Otherwise
                # retrieve the ID from the retrieved record.
                if not facility_canonical_new:
                    facility_canonical_id_new = ingest_facility_canonical_old(
                        facility_canonical_old=facility_canonical_old,
                    )
                else:
                    facility_canonical_id_new = \
                        facility_canonical_new.facility_canonical_id

                # Update the facility with the canonical facility ID.
                dal.update_attr_value(
                    orm_class=Facility,
                    pk=facility_new.facility_id,
                    attr_name="facility_canonical_id",
                    attr_value=facility_canonical_id_new,
                )


if __name__ == '__main__':

    argument_parser = argparse.ArgumentParser(
        description="Canonical facility porting utility.",
    )
    argument_parser.add_argument(
        "--facilities-dump",
        dest="filename_facilities_csv",
        help="Dumped CSV of the `facilities` table.",
        required=True,
    )
    argument_parser.add_argument(
        "--facilities-canonical-dump",
        dest="filename_facilities_canonical_csv",
        help="Dumped CSV of the `facilities_canonical` table.",
        required=True,
    )
    arguments = argument_parser.parse_args()

    cfg = import_config("/etc/ct-ingester/ct-ingester-dev.json")
    # Create a new DAL.
    dal = DalClinicalTrials(
        sql_username=cfg.sql_username,
        sql_password=cfg.sql_password,
        sql_host="localhost",
        sql_port=cfg.sql_port,
        sql_db=cfg.sql_db,
    )

    populate(
        filename_facilities_csv=arguments.filename_facilities_csv,
        filename_facilities_canonical_csv=
        arguments.filename_facilities_canonical_csv,
    )
