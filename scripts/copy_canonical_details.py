# coding=utf-8

from ct_ingester.config import import_config
from ct_ingester.loggers import create_logger

from fform.dals_ct import DalClinicalTrials
from fform.dals_pubmed import DalPubmed
from fform.orm_ct import FacilityCanonical
from fform.orm_pubmed import AffiliationCanonical
from geoalchemy2.shape import to_shape

logger = create_logger(logger_name=__name__)


def populate():

    with dal_ct.session_scope() as session_ct:

        query = session_ct.query(
            FacilityCanonical,
            AffiliationCanonical,
        )
        query = query.join(
            AffiliationCanonical,
            FacilityCanonical.google_place_id ==
            AffiliationCanonical.google_place_id,
        )
        query = query.filter(FacilityCanonical.country.isnot(None))
        query = query.filter(AffiliationCanonical.country.is_(None))

        for fac, aff in query.yield_per(5):

            msg = "Copying place details from {} to {}."
            msg_fmt = msg.format(fac, aff)
            logger.info(msg_fmt)

            coords = None
            if fac.coordinates is not None:
                coords = to_shape(fac.coordinates).coords[0]

            dal_pm.iodu_affiliation_canonical(
                google_place_id=fac.google_place_id,
                name=fac.name,
                google_url=fac.google_url,
                url=fac.url,
                address=fac.address,
                phone_number=fac.phone_number,
                coordinate_longitude=coords[0] if coords else None,
                coordinate_latitude=coords[1] if coords else None,
                country=fac.country,
                administrative_area_level_1=fac.administrative_area_level_1,
                administrative_area_level_2=fac.administrative_area_level_2,
                administrative_area_level_3=fac.administrative_area_level_3,
                administrative_area_level_4=fac.administrative_area_level_4,
                administrative_area_level_5=fac.administrative_area_level_5,
                locality=fac.locality,
                sublocality=fac.sublocality,
                sublocality_level_1=fac.sublocality_level_1,
                sublocality_level_2=fac.sublocality_level_2,
                sublocality_level_3=fac.sublocality_level_3,
                sublocality_level_4=fac.sublocality_level_4,
                sublocality_level_5=fac.sublocality_level_5,
                colloquial_area=fac.colloquial_area,
                floor=fac.floor,
                room=fac.room,
                intersection=fac.intersection,
                neighborhood=fac.neighborhood,
                post_box=fac.post_box,
                postal_code=fac.postal_code,
                postal_code_prefix=fac.postal_code_prefix,
                postal_code_suffix=fac.postal_code_suffix,
                postal_town=fac.postal_town,
                premise=fac.premise,
                subpremise=fac.subpremise,
                route=fac.route,
                street_address=fac.street_address,
                street_number=fac.street_number,
            )


if __name__ == '__main__':

    cfg = import_config("/etc/ct-ingester/ct-ingester-dev.json")

    # Create a new clinical-trials DAL.
    dal_ct = DalClinicalTrials(
        sql_username="somada141",
        sql_password="BcOGAdy6kHnk0tIcLyYLRcfB8ZiqT6PiSn8mHjc6",
        sql_host="192.168.0.12",
        sql_port=cfg.sql_port,
        sql_db=cfg.sql_db,
    )

    dal_pm = DalPubmed(
        sql_username="somada141",
        sql_password="BcOGAdy6kHnk0tIcLyYLRcfB8ZiqT6PiSn8mHjc6",
        sql_host="192.168.0.12",
        sql_port=cfg.sql_port,
        sql_db=cfg.sql_db,
    )

    populate()
