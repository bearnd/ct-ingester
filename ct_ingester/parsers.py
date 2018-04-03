# -*- coding: utf-8 -*-

import abc
import re
import gzip
from typing import List, Union

from lxml import etree

from ct_ingester.loggers import create_logger
from ct_ingester.parser_utils import parse_date_pattern
from ct_ingester.orm_enums import SponsorType
from ct_ingester.orm_enums import YesNoType
from ct_ingester.orm_enums import OverallStatusType
from ct_ingester.orm_enums import ActualType
from ct_ingester.orm_enums import PhaseType
from ct_ingester.orm_enums import StudyType
from ct_ingester.orm_enums import OutcomeType
from ct_ingester.orm_enums import InterventionType
from ct_ingester.orm_enums import BiospecRetentionType
from ct_ingester.orm_enums import SamplingMethodType
from ct_ingester.orm_enums import GenderType
from ct_ingester.orm_enums import RoleType
from ct_ingester.orm_enums import RecruitmentStatusType
from ct_ingester.orm_enums import ReferenceType
from ct_ingester.orm_enums import ResponsiblePartyType
from ct_ingester.orm_enums import MeshTermType
from ct_ingester.orm_enums import AgencyClassType


class ParserXmlBase(object):
    def __init__(self, **kwargs):

        self.logger = create_logger(
            logger_name=type(self).__name__,
            logger_level=kwargs.get("logger_level", "DEBUG")
        )

    @staticmethod
    def _et(element):
        """Extracts the element text (ET)"""

        text = None
        if element is not None:
            text = element.text

        if not text:
            text = None

        return text

    @staticmethod
    def _eav(element, attribute):
        """Extracts the element attrbiute value (EAV)"""

        value = None
        if element is not None:
            value = element.get(attribute)

        if not value:
            value = None

        return value

    @staticmethod
    def generate_xml_elements(file_xml, element_tag=None):

        document = etree.iterparse(
            file_xml,
            events=("start", "end"),
            tag=element_tag
        )

        _, element_root = next(document)
        start_tag = None
        for event, element in document:
            if event == 'start' and start_tag is None:
                start_tag = element.tag
            if event == 'end' and element.tag == start_tag:
                yield element
                start_tag = None
                element_root.clear()

    def open_xml_file(self, filename_xml):

        msg_fmt = "Opening XML file '{0}'".format(filename_xml)
        self.logger.info(msg=msg_fmt)

        if filename_xml.endswith(".gz"):
            file_xml = gzip.GzipFile(filename=filename_xml, mode="rb")
        else:
            file_xml = open(filename_xml, "rb")

        return file_xml

    @abc.abstractmethod
    def parse(self, filename_xml):
        raise NotImplementedError


class ParserXmlClinicaStudy(ParserXmlBase):
    def __init__(self, **kwargs):

        super(ParserXmlClinicaStudy, self).__init__(kwargs=kwargs)

    def _yn_to_bool(
        self,
        element: etree.Element
    ) -> Union[bool, None]:
        """Casts an element of `yes_no_enum` type to a boolean.

        Args:
            element (etree.Element): Element of `yes_no_enum` type to be casted
                to a boolean.

        Returns:
            bool: The casted value or `None` if undefined.
        """

        text = self._et(element)

        if text == YesNoType.YES.value:
            return True
        elif text == YesNoType.NO.value:
            return False

        return None

    def _etb(
        self,
        element: etree.Element,
    ) -> Union[str, None]:
        """Extracted and sanitizes the text out of an element containing an
        element of `<textblock_struct>` type.

        Note:
            Sanitization is limited to removing new-line characters and
            compressing multi-character whitespace to single-character
            whitespace.

        Args:
            element (etree.Element): Element containing an element of
                `<textblock_struct>` type.

        Returns:
            str: A sanitized version of the contained text or `None` if
                undefined.
        """

        if element is None:
            return None

        element_textblock = element.find("textblock")

        if element_textblock is None:
            return None

        textblock = self._et(element_textblock)

        if not textblock:
            return None

        # Replace instances of 1 or more whitespace character with a single
        # space. This will include new-lines, tab-characters, and spaces.
        textblock = re.sub("\s+", " ", textblock)
        # Strip and leading and trailing whitespace.
        textblock = textblock.strip()

        if not textblock:
            return None

        return textblock

    def parse_vdt(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `variable_date_type` and returns the values
        of the contained elements.

        Args:
            element (etree.Element): The element of type `variable_date_type`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        variable_date = {
            "type": ActualType.get_member(
                self._eav(element, "type")
            ),
            "date": parse_date_pattern(
                str_date=self._et(element),
                do_cast_to_date=True,
            )
        }

        return variable_date

    def parse_id_info(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `id_info_struct` and returns the values of
        the contained elements.

        Args:
            element (etree.Element): The element of type `id_info_struct`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        id_info = {
            "org_study_id": self._et(element.find("org_study_id")),
            "secondary_ids": [
                {
                    "secondary_id": self._et(_element)
                } for _element in element.findall("secondary_id")
            ],
            "nct_id": self._et(element.find("nct_id")),
            "nct_aliases": [
                {
                    "nct_alias": self._et(_element)
                } for _element in element.findall("nct_alias")
            ],
        }

        return id_info

    def parse_sponsor(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `sponsor_struct` and returns the values of
        the contained elements.

        Args:
            element (etree.Element): The element of type `sponsor_struct`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        sponsor = {
            "agency": self._et(element.find("agency")),
            "agency_class": AgencyClassType.get_member(
                self._et(element.find("agency_class"))
            ),
            "type": None
        }

        # Assign the appropriate sponsor-type enumeration value based on the
        # element tag.
        if element.tag == "lead_sponsor":
            sponsor["type"] = SponsorType.LEAD
        elif element.tag == "collaborator":
            sponsor["type"] = SponsorType.COLLABORATOR

        return sponsor

    def parse_sponsors(
        self,
        element: etree.Element,
    ) -> list:
        """Parses an element of type `sponsors_struct` and returns the values of
        the contained elements.

        Args:
            element (etree.Element): The element of type `sponsors_struct`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        sponsors = []

        if element is None:
            return sponsors

        for _element in element.getchildren():
            sponsors.append(self.parse_sponsor(_element))

        return sponsors

    def parse_oversight_info(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `oversight_info_struct` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type
                `oversight_info_struct`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        oversight_info = {
            "has_dmc": self._yn_to_bool(element.find("has_dmc")),
            "is_fda_regulated_drug": self._yn_to_bool(
                element.find("is_fda_regulated_drug")
            ),
            "is_fda_regulated_device": self._yn_to_bool(
                element.find("is_fda_regulated_device")
            ),
            "is_unapproved_device": self._yn_to_bool(
                element.find("is_unapproved_device")
            ),
            "is_ppsd": self._yn_to_bool(element.find("is_ppsd")),
            "is_us_export": self._yn_to_bool(element.find("is_us_export")),
        }

        return oversight_info

    def parse_expanded_access_info(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `expanded_access_info_struct` and returns
        the values of the contained elements.

        Args:
            element (etree.Element): The element of type
                `expanded_access_info_struct`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        expanded_access_info = {
            "expanded_access_type_individual": self._yn_to_bool(
                element.find("expanded_access_type_individual")
            ),
            "expanded_access_type_intermediate": self._yn_to_bool(
                element.find("expanded_access_type_intermediate")
            ),
            "expanded_access_type_treatment": self._yn_to_bool(
                element.find("expanded_access_type_treatment")
            ),
        }

        return expanded_access_info

    def parse_study_design_info(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `study_design_info_struct` and returns
        the values of the contained elements.

        Args:
            element (etree.Element): The element of type
                `study_design_info_struct`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        study_design_info = {
            "allocation": self._et(element.find("allocation")),
            "intervention_model": self._et(element.find("intervention_model")),
            "intervention_model_description": self._et(
                element.find("intervention_model_description")
            ),
            "primary_purpose": self._et(element.find("primary_purpose")),
            "observational_model": self._et(
                element.find("observational_model")
            ),
            "time_perspective": self._et(element.find("time_perspective")),
            "masking": self._et(element.find("masking")),
            "masking_description": self._et(
                element.find("masking_description")
            ),
        }

        return study_design_info

    def parse_protocol_outcome(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `protocol_outcome_struct` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type
                `protocol_outcome_struct`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        protocol_outcome = {
            "measure": self._et(element.find("measure")),
            "time_frame": self._et(element.find("time_frame")),
            "description": self._et(element.find("description")),
        }

        # Assign the appropriate protocol-outcome-type enumeration value based
        # on the element tag.
        if element.tag == "primary_outcome":
            protocol_outcome["type"] = OutcomeType.PRIMARY
        elif element.tag == "secondary_outcome":
            protocol_outcome["type"] = OutcomeType.SECONDARY
        elif element.tag == "other_outcome":
            protocol_outcome["type"] = OutcomeType.OTHER

        return protocol_outcome

    def parse_protocol_outcomes(
        self,
        element_clinical_study: etree.Element,
    ) -> list:
        """Extracts and parses elements of type `<protocol_outcome_struct>` from
        a `<clinical_study>` element and returns the values of the contained
        elements.

        Args:
            element_clinical_study (etree.Element): The `<clinical_study>`
                element.

        Returns:
            dict: The parsed values of the contained elements.
        """

        protocol_outcomes = []

        if element_clinical_study is None:
            return protocol_outcomes

        for _element in element_clinical_study.findall("primary_outcome"):
            protocol_outcomes.append(self.parse_protocol_outcome(_element))

        for _element in element_clinical_study.findall("secondary_outcome"):
            protocol_outcomes.append(self.parse_protocol_outcome(_element))

        for _element in element_clinical_study.findall("other_outcome"):
            protocol_outcomes.append(self.parse_protocol_outcome(_element))

        return protocol_outcomes

    def parse_enrollment(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `enrollment_struct` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type
                `enrollment_struct`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        enrollment = {
            "value": self._et(element),
            "type": self._eav(element, "type"),
        }

        return enrollment

    def parse_conditions(
        self,
        element_clinical_study: etree.Element,
    ) -> list:
        """Extracts and parses `<condition>` elements from a `<clinical_study>`
        element and returns the values of the contained elements.

        Args:
            element_clinical_study (etree.Element): The `<clinical_study>`
                element.

        Returns:
            dict: The parsed values of the contained elements.
        """

        conditions = []

        if element_clinical_study is None:
            return conditions

        for _element in element_clinical_study.findall("condition"):
            conditions.append({
                "condition": self._et(_element)
            })

        return conditions

    def parse_arm_group(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `arm_group_struct` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type
                `arm_group_struct`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        arm_group = {
            "arm_group_label": self._et(element.find("arm_group_label")),
            "arm_group_type": self._et(element.find("arm_group_type")),
            "description": self._et(element.find("description")),
        }

        return arm_group

    def parse_arm_groups(
        self,
        element_clinical_study: etree.Element,
    ) -> list:
        """Extracts and parses elements of type `<arm_group_struct>` from
        a `<clinical_study>` element and returns the values of the contained
        elements.

        Args:
            element_clinical_study (etree.Element): The `<clinical_study>`
                element.

        Returns:
            dict: The parsed values of the contained elements.
        """

        arm_groups = []

        if element_clinical_study is None:
            return arm_groups

        for _element in element_clinical_study.findall("arm_group"):
            arm_groups.append(self.parse_arm_group(_element))

        return arm_groups

    def parse_intervention(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `intervention_struct` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type
                `intervention_struct`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        intervention = {
            "intervention_type": InterventionType.get_member(
                self._et(element.find("intervention_type"))
            ),
            "intervention_name": self._et(element.find("intervention_name")),
            "description": self._et(element.find("description")),
            "arm_group_labels": [{
                "arm_group_label": self._et(_element)
            } for _element in element.findall("arm_group_label")],
            "other_names": [{
                "other_name": self._et(_element)
            } for _element in element.findall("other_name")],
        }

        return intervention

    def parse_interventions(
        self,
        element_clinical_study: etree.Element,
    ) -> list:
        """Extracts and parses elements of type `<intervention_struct>` from
        a `<clinical_study>` element and returns the values of the contained
        elements.

        Args:
            element_clinical_study (etree.Element): The `<clinical_study>`
                element.

        Returns:
            dict: The parsed values of the contained elements.
        """

        interventions = []

        if element_clinical_study is None:
            return interventions

        for _element in element_clinical_study.findall("intervention"):
            interventions.append(self.parse_intervention(_element))

        return interventions

    def parse_eligibility(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `eligibility_struct` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type
                `eligibility_struct`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        eligibility = {
            "study_pop": self._etb(element.find("study_pop")),
            "sampling_method": SamplingMethodType.get_member(
                self._et(element.find("sampling_method"))
            ),
            "criteria": self._etb(element.find("criteria")),
            "gender": GenderType.get_member(self._et(element.find("gender"))),
            "gender_based": self._yn_to_bool(element.find("gender_based")),
            "gender_description": self._et(element.find("gender_description")),
            "minimum_age": self._et(element.find("minimum_age")),
            "maximum_age": self._et(element.find("maximum_age")),
            "healthy_volunteers": self._et(element.find("healthy_volunteers")),
        }

        return eligibility

    def parse_investigator(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `investigator_struct` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type
                `investigator_struct`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        investigator = {
            "first_name": self._et(element.find("intervention_name")),
            "middle_name": self._et(element.find("middle_name")),
            "last_name": self._et(element.find("last_name")),
            "degrees": self._et(element.find("degrees")),
            "role": RoleType.get_member(
                self._et(element.find("role"))
            ),
            "affiliation": self._et(element.find("affiliation")),
        }

        return investigator

    def parse_investigators(
        self,
        elements_investigators: List[etree.Element],
    ) -> list:
        """Parses elements of `investigator_struct` type and returns the values
        of the contained elements.

        Args:
            elements_investigators (list[etree.Element]): A list of elements of
                `investigator_struct` type.

        Returns:
            dict: The parsed values of the contained elements.
        """

        investigators = []

        if not elements_investigators:
            return investigators

        for _element in elements_investigators:
            investigators.append(self.parse_investigator(_element))

        return investigators

    def parse_contact(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `contact_struct` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type `contact_struct`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        contact = {
            "first_name": self._et(element.find("intervention_name")),
            "middle_name": self._et(element.find("middle_name")),
            "last_name": self._et(element.find("last_name")),
            "degrees": self._et(element.find("degrees")),
            "phone": self._et(element.find("phone")),
            "phone_ext": self._et(element.find("phone_ext")),
            "email": self._et(element.find("email")),
        }

        return contact

    def parse_address(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `address_struct` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type `address_struct`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        address = {
            "city": self._et(element.find("city")),
            "state": self._et(element.find("state")),
            "zip": self._et(element.find("zip")),
            "country": self._et(element.find("country")),
        }

        return address

    def parse_facility(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `facility_struct` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type `facility_struct`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        facility = {
            "name": self._et(element.find("name")),
            "address": self.parse_address(element.find("address"))
        }

        return facility

    def parse_location(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `location_struct` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type `location_struct`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        location = {
            "facility": self.parse_facility(element.find("facility")),
            "status": RecruitmentStatusType.get_member(
                self._et(element.find("status"))
            ),
            "contact": self.parse_contact(element.find("contact")),
            "contact_backup": self.parse_contact(
                element.find("contact_backup")
            ),
            "investigators": self.parse_investigators(
                element.findall("investigator")
            ),
        }

        return location

    def parse_locations(
        self,
        element_clinical_study: etree.Element,
    ) -> list:
        """Extracts and parses elements of type `location_struct` from
        a `<clinical_study>` element and returns the values of the contained
        elements.

        Args:
            element_clinical_study (etree.Element): The `<clinical_study>`
                element.

        Returns:
            dict: The parsed values of the contained elements.
        """

        locations = []

        if element_clinical_study is None:
            return locations

        for _element in element_clinical_study.findall("location"):
            locations.append(self.parse_location(_element))

        return locations

    def parse_reference(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `reference_struct` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type `reference_struct`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        pmid = self._et(element.find("PMID"))

        reference = {
            "citation": self._et(element.find("citation")),
            # Convert the PMID to an integer if defined.
            "pmid": int(pmid) if pmid else None,
            "type": None,
        }

        if element.tag == "reference":
            reference["type"] = ReferenceType.STANDARD
        elif element.tag == "results_reference":
            reference["type"] = ReferenceType.RESULTS

        return reference

    def parse_references(
        self,
        element_clinical_study: etree.Element,
    ) -> list:
        """Extracts and parses elements of type `<reference_struct>` from
        a `<clinical_study>` element and returns the values of the contained
        elements.

        Args:
            element_clinical_study (etree.Element): The `<clinical_study>`
                element.

        Returns:
            dict: The parsed values of the contained elements.
        """

        references = []

        if element_clinical_study is None:
            return references

        for _element in element_clinical_study.findall("reference"):
            references.append(self.parse_reference(_element))

        for _element in element_clinical_study.findall("results_reference"):
            references.append(self.parse_reference(_element))

        return references

    def parse_study_dates(
        self,
        element_clinical_study: etree.Element,
    ) -> dict:
        """Extracts and parses the 'new dates' from a `<clinical_study>`
        element and returns the values of the contained elements.

        Args:
            element_clinical_study (etree.Element): The `<clinical_study>`
                element.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element_clinical_study is None:
            return {}

        study_dates = {
            "study_first_submitted": self.parse_vdt(
                element_clinical_study.find("study_first_submitted")
            ),
            "study_first_submitted_qc": self.parse_vdt(
                element_clinical_study.find("study_first_submitted_qc")
            ),
            "study_first_posted": self.parse_vdt(
                element_clinical_study.find("study_first_posted")
            ),
            "results_first_submitted": self.parse_vdt(
                element_clinical_study.find("results_first_submitted")
            ),
            "results_first_submitted_qc": self.parse_vdt(
                element_clinical_study.find("results_first_submitted_qc")
            ),
            "results_first_posted": self.parse_vdt(
                element_clinical_study.find("results_first_posted")
            ),
            "disposition_first_submitted": self.parse_vdt(
                element_clinical_study.find("disposition_first_submitted")
            ),
            "disposition_first_submitted_qc": self.parse_vdt(
                element_clinical_study.find("disposition_first_submitted_qc")
            ),
            "disposition_first_posted": self.parse_vdt(
                element_clinical_study.find("disposition_first_posted")
            ),
            "last_update_submitted": self.parse_vdt(
                element_clinical_study.find("last_update_submitted")
            ),
            "last_update_submitted_qc": self.parse_vdt(
                element_clinical_study.find("last_update_submitted_qc")
            ),
            "last_update_posted": self.parse_vdt(
                element_clinical_study.find("last_update_posted")
            ),
        }

        return study_dates

    def parse_responsible_party(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `responsible_party_struct` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type
                `responsible_party_struct`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        responsible_party = {
            "name_title": self._et(element.find("name_title")),
            "organization": self._et(element.find("organization")),
            "responsible_party_type": ResponsiblePartyType.get_member(
                self._et(element.find("responsible_party_type"))
            ),
            "investigator_affiliation": self._et(
                element.find("investigator_affiliation")
            ),
            "investigator_full_name": self._et(
                element.find("investigator_full_name")
            ),
            "investigator_title": self._et(
                element.find("investigator_title")
            ),
        }

        return responsible_party

    def parse_keywords(
        self,
        element_clinical_study: etree.Element,
    ) -> list:
        """Extracts and parses `<keyword>` elements from a `<clinical_study>`
        element and returns the values of the contained elements.

        Args:
            element_clinical_study (etree.Element): The `<clinical_study>`
                element.

        Returns:
            dict: The parsed values of the contained elements.
        """

        keywords = []

        if element_clinical_study is None:
            return keywords

        for _element in element_clinical_study.findall("keyword"):
            keywords.append({"keyword": self._et(_element)})

        return keywords

    def parse_mesh_terms(
        self,
        element_clinical_study: etree.Element,
    ) -> list:
        """Extracts and parses elements of type `<browse_struct>` from
        a `<clinical_study>` element and returns the values of the contained
        elements.

        Args:
            element_clinical_study (etree.Element): The `<clinical_study>`
                element.

        Returns:
            dict: The parsed values of the contained elements.
        """

        mesh_terms = []

        if element_clinical_study is None:
            return mesh_terms

        _element_condition_browse = element_clinical_study.find(
            "condition_browse"
        )
        if _element_condition_browse is not None:
            for _element in _element_condition_browse.findall("mesh_term"):
                mesh_term = {
                    "type": MeshTermType.CONDITION,
                    "mesh_term": self._et(_element),
                }
                mesh_terms.append(mesh_term)

        _element_intervention_browse = element_clinical_study.find(
            "intervention_browse"
        )
        if _element_intervention_browse is not None:
            for _element in _element_intervention_browse.findall("mesh_term"):
                mesh_term = {
                    "type": MeshTermType.CONDITION,
                    "mesh_term": self._et(_element),
                }
                mesh_terms.append(mesh_term)

        return mesh_terms

    def parse_patient_data(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `patient_data_struct` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type
                `patient_data_struct`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        patient_data = {
            "sharing_ipd": self._et(element.find("sharing_ipd")),
            "ipd_description": self._et(element.find("ipd_description")),
        }

        return patient_data

    def parse_study_doc(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `study_doc_struct` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type `study_doc_struct`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        study_doc = {
            "doc_id": self._et(element.find("doc_id")),
            "doc_type": self._et(element.find("doc_type")),
            "doc_url": self._et(element.find("doc_url")),
            "doc_comment": self._et(element.find("doc_comment")),
        }

        return study_doc

    def parse_study_docs(
        self,
        element: etree.Element,
    ) -> list:
        """Extracts and parses elements of type `<study_docs_struct>` from
        a `<clinical_study>` element and returns the values of the contained
        elements.

        Args:
            element (etree.Element): The element of type `study_docs_struct`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        study_docs = []

        if element is None:
            return study_docs

        for _element in element.findall("study_doc"):
            study_docs.append(self.parse_study_doc(_element))

        return study_docs

    def parse_clinical_study(self, element):

        if element is None:
            return {}

        clinical_study = {
            "id_info": self.parse_id_info(element.find("id_info")),
            "brief_title": self._et(element.find("brief_title")),
            "acronym": self._et(element.find("acronym")),
            "official_title": self._et(element.find("official_title")),
            "sponsors": self.parse_sponsors(element.find("sponsors")),
            "source": self._et(element.find("source")),
            "oversight_info": self.parse_oversight_info(
                element.find("oversight_info")
            ),
            "brief_summary": self._etb(element.find("brief_summary")),
            "detailed_description": self._etb(
                element.find("detailed_description")
            ),
            "overall_status": OverallStatusType.get_member(
                self._et(element.find("overall_status"))
            ),
            "last_known_status": OverallStatusType.get_member(
                self._et(element.find("last_known_status"))
            ),
            "why_stopped": self._et(element.find("why_stopped")),
            "start_date": self.parse_vdt(element.find("start_date")),
            "completion_date": self.parse_vdt(element.find("completion_date")),
            "primary_completion_date": self.parse_vdt(
                element.find("primary_completion_date")
            ),
            "phase": PhaseType.get_member(self._et(element.find("phase"))),
            "study_type": StudyType.get_member(
                self._et(element.find("study_type"))
            ),
            "expanded_access_info": self.parse_expanded_access_info(
                element.find("expanded_access_info")
            ),
            "study_design_info": self.parse_study_design_info(
                element.find("study_design_info")
            ),
            "target_duration": self._et(element.find("target_duration")),
            "protocol_outcomes": self.parse_protocol_outcomes(element),
            "enrollment": self.parse_enrollment(element.find("enrollment")),
            "conditions": self.parse_conditions(element),
            "arm_groups": self.parse_arm_groups(element),
            "interventions": self.parse_interventions(element),
            "biospec_retention": BiospecRetentionType.get_member(
                self._et(element.find("biospec_retention"))
            ),
            "biospec_descr": self._etb(
                element.find("biospec_descr")
            ),
            "eligibility": self.parse_eligibility(element.find("eligibility")),
            "overall_officials": self.parse_investigators(
                element.findall("overall_official")
            ),
            "overall_contact": self.parse_contact(
                element.find("overall_contact")
            ),
            "overall_contact_backup": self.parse_contact(
                element.find("overall_contact_backup")
            ),
            "locations": self.parse_locations(element),
            "references": self.parse_references(element),
            "verification_date": self.parse_vdt(
                element.find("verification_date")
            ),
            "study_dates": self.parse_study_dates(element),
            "responsible_party": self.parse_responsible_party(
                element.find("responsible_party")
            ),
            "keywords": self.parse_keywords(element),
            "mesh_terms": self.parse_mesh_terms(element),
            "patient_data": self.parse_patient_data(
                element.find("patient_data")
            ),
            "study_docs": self.parse_study_docs(
                element.find("study_docs_struct")
            ),
        }

        return clinical_study

    def parse(self, filename_xml):

        msg_fmt = "Parsing Pubmed XML file '{0}'".format(filename_xml)
        self.logger.info(msg=msg_fmt)

        file_xml = self.open_xml_file(filename_xml=filename_xml)

        element = etree.parse(file_xml)

        clinical_study = self.parse_clinical_study(element)

        return clinical_study
