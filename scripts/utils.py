from typing import List, Tuple, Dict, Optional, Union

from fform.dals_ct import DalClinicalTrials


def get_address_component_name(
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


def iodu_canonical_facility_from_google(
    dal: DalClinicalTrials, google_place_id: str, google_response: Dict
):
    result = google_response["result"]

    components = result.get("address_components")

    if not components:
        return None

    # Fallback to the country defined in the facility if Google
    # returns no country.
    country = get_address_component_name(components, ("country",))

    facility_canonical_id = dal.iodu_facility_canonical(
        google_place_id=google_place_id,
        name=result["name"],
        google_url=result["url"],
        url=result.get("website"),
        address=result["formatted_address"],
        phone_number=result.get("international_phone_number"),
        coordinate_longitude=result["geometry"]["location"]["lng"],
        coordinate_latitude=result["geometry"]["location"]["lat"],
        country=country,
        administrative_area_level_1=get_address_component_name(
            components, ("administrative_area_level_1",)
        ),
        administrative_area_level_2=get_address_component_name(
            components, ("administrative_area_level_2",)
        ),
        administrative_area_level_3=get_address_component_name(
            components, ("administrative_area_level_3",)
        ),
        administrative_area_level_4=get_address_component_name(
            components, ("administrative_area_level_4",)
        ),
        administrative_area_level_5=get_address_component_name(
            components, ("administrative_area_level_5",)
        ),
        locality=get_address_component_name(components, ("locality",)),
        sublocality=get_address_component_name(
            components,
            ("sublocality",),
            (
                "sublocality_level_1",
                "sublocality_level_2",
                "sublocality_level_3",
                "sublocality_level_4",
                "sublocality_level_5",
            ),
        ),
        sublocality_level_1=get_address_component_name(
            components, ("sublocality_level_1",)
        ),
        sublocality_level_2=get_address_component_name(
            components, ("sublocality_level_2",)
        ),
        sublocality_level_3=get_address_component_name(
            components, ("sublocality_level_3",)
        ),
        sublocality_level_4=get_address_component_name(
            components, ("sublocality_level_4",)
        ),
        sublocality_level_5=get_address_component_name(
            components, ("sublocality_level_5",)
        ),
        colloquial_area=get_address_component_name(
            components, ("colloquial_area",)
        ),
        floor=get_address_component_name(components, ("floor",)),
        room=get_address_component_name(components, ("room",)),
        intersection=get_address_component_name(components, ("intersection",)),
        neighborhood=get_address_component_name(components, ("neighborhood",)),
        post_box=get_address_component_name(components, ("post_box",)),
        postal_code=get_address_component_name(components, ("postal_code",)),
        postal_code_prefix=get_address_component_name(
            components, ("postal_code_prefix",)
        ),
        postal_code_suffix=get_address_component_name(
            components, ("postal_code_suffix",)
        ),
        postal_town=get_address_component_name(components, ("postal_town",)),
        premise=get_address_component_name(components, ("premise",)),
        subpremise=get_address_component_name(components, ("subpremise",)),
        route=get_address_component_name(components, ("route",)),
        street_address=get_address_component_name(
            components, ("street_address",)
        ),
        street_number=get_address_component_name(
            components, ("street_number",)
        ),
    )

    return facility_canonical_id
