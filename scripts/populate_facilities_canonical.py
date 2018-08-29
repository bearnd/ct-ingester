# coding=utf-8

import multiprocessing
from typing import List, Dict, Optional, Tuple, Union

import sqlalchemy.orm
from fform.dals_ct import DalClinicalTrials
from fform.orm_ct import Facility

from ct_ingester.config import import_config
from ct_ingester.loggers import create_logger
from ct_ingester.retrievers import RetrieverGoogleMaps
from ct_ingester.utils import find_facility_google_place
from ct_ingester.utils import chunk_generator


logger = create_logger(logger_name=__name__)


def _get_address_component_name(
    address_components: List[Dict],
    include_types: Tuple[str],
    exclude_types: Optional[Tuple[str, ...]] = (),
) -> Union[str, None]:

    component = None
    for _component in address_components:
        s01 = set(_component["types"])
        s02 = set(include_types)
        s03 = set(exclude_types)

        # If the component `types` don't contain all `include_types` then
        # skip the component.
        if not s01.issuperset(s02):
            continue

        # If the componment `types` include any of the `exclude_types` then
        # skip the component.
        if s01.intersection(s03):
            continue

        component = _component
        break

    if component:
        return component["long_name"]

    return None


def find_place(facility: Facility):
    global retriever
    return find_facility_google_place(retriever, facility)


def populate():

    with dal.session_scope() as session:
        query = session.query(Facility)  # type: sqlalchemy.orm.Query
        query = query.filter(Facility.facility_canonical_id.is_(None))

        facilities_chunks = chunk_generator(
            generator=iter(query.yield_per(50)),
            chunk_size=50,
        )
        pool = multiprocessing.Pool(processes=50)
        for facilities_chunk in facilities_chunks:

            facilities = list(facilities_chunk)
            responses = pool.map(find_place, facilities)

            for facility, response in zip(facilities, responses):
                if not response:
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

            # # Retrieving Google Place details for the first candidate's ID.
            # response = retriever.get_place_details(google_place_id=place_id)
            #
            # if not response:
            #     continue
            #
            # print(response)
            #
            # if not response["status"] == "OK":
            #     continue
            #
            # result = response["result"]
            #
            # components = result["address_components"]

            # Fallback to the country defined in the facility if Google returns
            # no country.
            # country = _get_address_component_name(
            #     components, ("country",)
            # )
            # country = country if country else facility.country


            # facility_canonical_id = dal.iodu_facility_canonical(
            #     google_place_id=place_id,
            #     name=result["name"],
            #     google_url=result["url"],
            #     url=result.get("website"),
            #     address=result["formatted_address"],
            #     phone_number=result.get("international_phone_number"),
            #     coordinate_longitude=result["geometry"]["location"]["lng"],
            #     coordinate_latitude=result["geometry"]["location"]["lat"],
            #     country=country,
            #     administrative_area_level_1=_get_address_component_name(
            #         components,
            #         ("administrative_area_level_1",)
            #     ),
            #     administrative_area_level_2=_get_address_component_name(
            #         components,
            #         ("administrative_area_level_2",)
            #     ),
            #     administrative_area_level_3=_get_address_component_name(
            #         components,
            #         ("administrative_area_level_3",)
            #     ),
            #     administrative_area_level_4=_get_address_component_name(
            #         components,
            #         ("administrative_area_level_4",)
            #     ),
            #     administrative_area_level_5=_get_address_component_name(
            #         components,
            #         ("administrative_area_level_5",)
            #     ),
            #     locality=_get_address_component_name(
            #         components, ("locality",)
            #     ),
            #     sublocality=_get_address_component_name(
            #         components,
            #         ("sublocality",),
            #         (
            #             "sublocality_level_1",
            #             "sublocality_level_2",
            #             "sublocality_level_3",
            #             "sublocality_level_4",
            #             "sublocality_level_5",
            #         )
            #     ),
            #     sublocality_level_1=_get_address_component_name(
            #         components,
            #         ("sublocality_level_1",)
            #     ),
            #     sublocality_level_2=_get_address_component_name(
            #         components,
            #         ("sublocality_level_2",)
            #     ),
            #     sublocality_level_3=_get_address_component_name(
            #         components,
            #         ("sublocality_level_3",)
            #     ),
            #     sublocality_level_4=_get_address_component_name(
            #         components,
            #         ("sublocality_level_4",)
            #     ),
            #     sublocality_level_5=_get_address_component_name(
            #         components,
            #         ("sublocality_level_5",)
            #     ),
            #     colloquial_area=_get_address_component_name(
            #         components,
            #         ("colloquial_area",)
            #     ),
            #     floor=_get_address_component_name(
            #         components,
            #         ("floor",)
            #     ),
            #     room=_get_address_component_name(
            #         components,
            #         ("room",)
            #     ),
            #     intersection=_get_address_component_name(
            #         components,
            #         ("intersection",)
            #     ),
            #     neighborhood=_get_address_component_name(
            #         components,
            #         ("neighborhood",)
            #     ),
            #     post_box=_get_address_component_name(
            #         components,
            #         ("post_box",)
            #     ),
            #     postal_code=_get_address_component_name(
            #         components,
            #         ("postal_code",)
            #     ),
            #     postal_code_prefix=_get_address_component_name(
            #         components,
            #         ("postal_code_prefix",)
            #     ),
            #     postal_code_suffix=_get_address_component_name(
            #         components,
            #         ("postal_code_suffix",)
            #     ),
            #     postal_town=_get_address_component_name(
            #         components,
            #         ("postal_town",)
            #     ),
            #     premise=_get_address_component_name(
            #         components,
            #         ("premise",)
            #     ),
            #     subpremise=_get_address_component_name(
            #         components,
            #         ("subpremise",)
            #     ),
            #     route=_get_address_component_name(
            #         components,
            #         ("route",)
            #     ),
            #     street_address=_get_address_component_name(
            #         components,
            #         ("street_address",)
            #     ),
            #     street_number=_get_address_component_name(
            #         components,
            #         ("street_number",)
            #     ),
            # )


if __name__ == '__main__':
    cfg = import_config("/etc/ct-ingester/ct-ingester-dev.json")

    dal = DalClinicalTrials(
        sql_username=cfg.sql_username,
        sql_password=cfg.sql_password,
        sql_host="192.168.0.12",
        sql_port=cfg.sql_port,
        sql_db=cfg.sql_db,
    )

    retriever = RetrieverGoogleMaps(api_key=cfg.google_maps_api_key)

    populate()
