# -*- coding: utf-8 -*-

import abc
from typing import Union, List, Type

from fform.orm_base import OrmBase
from fform.orm_ct import Study
from fform.orm_ct import OversightInfo
from fform.orm_ct import ExpandedAccessInfo
from fform.orm_ct import StudyDesignInfo
from fform.orm_ct import Enrollment
from fform.orm_ct import Eligibility
from fform.orm_ct import StudyDates
from fform.orm_ct import ResponsibleParty
from fform.orm_ct import PatientDataIpdInfoType
from fform.orm_ct import PatientData
from fform.orm_ct import StudySecondaryId
from fform.orm_ct import ProtocolOutcome
from fform.orm_ct import StudyOutcome
from fform.orm_ct import ArmGroup
from fform.orm_ct import StudyArmGroup
from fform.orm_ct import StudyIntervention
from fform.orm_ct import InterventionArmGroup
from fform.orm_ct import StudyDoc
from fform.orm_ct import StudyStudyDoc
from fform.orm_mt import Descriptor
from fform.dals_ct import DalClinicalTrials

from ct_ingester.loggers import create_logger
from ct_ingester.utils import log_ingestion_of_document


class IngesterDocumentBase(object):
    def __init__(self, dal, **kwargs):

        self.dal = dal

        self.logger = create_logger(
            logger_name=type(self).__name__,
            logger_level=kwargs.get("logger_level", "DEBUG")
        )

    @abc.abstractmethod
    def ingest(
        self,
        document: dict
    ):
        raise NotImplementedError


class IngesterDocumentClinicalTrial(IngesterDocumentBase):
    def __init__(
        self,
        dal: DalClinicalTrials,
        **kwargs
    ):

        super(IngesterDocumentClinicalTrial, self).__init__(
            dal=dal,
            kwargs=kwargs,
        )

    @staticmethod
    def _edt(dt):
        """Extracts the value of the `date` key from a parsed date
        dictionary.

        Args:
            dt (dict): A parsed `date` dictionary which (may) contain a `date`
                and `type` keys.

        Returns:
            datetime.date: The value of the `date` key or `None` if not defined.
        """
        if dt and isinstance(dt, dict) and ("date" in dt):
            return dt["date"]

        return None

    @log_ingestion_of_document(document_name="sponsor")
    def ingest_sponsor(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<sponsor_struct>` and creates a
        `Sponsor` record.

        Args:
            doc (dict): The element of type `<sponsor_struct>` parsed into a
                dictionary.

        Returns:
             int: The primary-key ID of the `Sponsor` record.
        """

        if not doc:
            return None

        obj_id = self.dal.iodi_sponsor(
            agency=doc.get("agency"),
            agency_class=doc.get("agency_class"),
        )

        return obj_id

    @log_ingestion_of_document(document_name="keyword")
    def ingest_keyword(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<keyword>` and creates a `Keyword`
         record.

        Args:
            doc (dict): The element of type `<keyword>` parsed into a
                dictionary.

        Returns:
             int: The primary-key ID of the `Keyword` record.
        """

        if not doc:
            return None

        obj_id = self.dal.iodi_keyword(
            keyword=doc.get("keyword"),
        )

        return obj_id

    @log_ingestion_of_document(document_name="condition")
    def ingest_condition(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<condition>` and creates a
        `Condition` record.

        Args:
            doc (dict): The element of type `<condition>` parsed into a
                dictionary.

        Returns:
             int: The primary-key ID of the `Condition` record.
        """

        if not doc:
            return None

        obj_id = self.dal.iodi_condition(
            condition=doc.get("condition"),
        )

        return obj_id

    @log_ingestion_of_document(document_name="facility")
    def ingest_facility(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<facility_struct>` and creates a
        `Facility` record.

        Args:
            doc (dict): The element of type `<facility_struct>` parsed into a
                dictionary.

        Returns:
             int: The primary-key ID of the `Facility` record.
        """

        if not doc:
            return None

        address = doc.get("address", {})

        obj_id = self.dal.iodi_facility(
            name=doc.get("name"),
            city=address.get("city"),
            state=address.get("state"),
            zip_code=address.get("zip"),
            country=address.get("country"),
        )

        return obj_id

    @log_ingestion_of_document(document_name="investigator")
    def ingest_investigator(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<investigator_struct>` and creates
        a `Investigator` record.

        Args:
            doc (dict): The element of type `<investigator_struct>` parsed into
                a dictionary.

        Returns:
             int: The primary-key ID of the `Investigator` record.
        """

        if not doc:
            return None

        person_obj_id = self.dal.iodi_person(
            name_first=doc.get("first_name"),
            name_middle=doc.get("middle_name"),
            name_last=doc.get("last_name"),
            degrees=doc.get("degrees"),
        )

        obj_id = self.dal.iodi_investigator(
            person_id=person_obj_id,
            role=doc.get("role"),
            affiliation=doc.get("affiliation"),
        )

        return obj_id

    @log_ingestion_of_document(document_name="contact")
    def ingest_contact(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<contact_struct>` and creates
        a `Contact` record.

        Args:
            doc (dict): The element of type `<contact_struct>` parsed into
                a dictionary.

        Returns:
             int: The primary-key ID of the `Contact` record.
        """

        if not doc:
            return None

        person_obj_id = self.dal.iodi_person(
            name_first=doc.get("first_name"),
            name_middle=doc.get("middle_name"),
            name_last=doc.get("last_name"),
            degrees=doc.get("degrees"),
        )

        obj_id = self.dal.iodi_contact(
            person_id=person_obj_id,
            phone=doc.get("phone"),
            phone_ext=doc.get("phone_ext"),
            email=doc.get("email"),
        )

        return obj_id

    @log_ingestion_of_document(document_name="location")
    def ingest_location(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<location_struct>` and creates
        a `Location` record.

        Args:
            doc (dict): The element of type `<location_struct>` parsed into
                a dictionary.

        Returns:
             int: The primary-key ID of the `Location` record.
        """

        if not doc:
            return None

        facility_id = self.ingest_facility(doc.get("facility"))

        contact_primary_id = self.ingest_contact(doc.get("contact"))

        contact_backup_id = self.ingest_contact(doc.get("contact_backup"))

        obj_id = self.dal.iodu_location(
            facility_id=facility_id,
            status=doc.get("status"),
            contact_primary_id=contact_primary_id,
            contact_backup_id=contact_backup_id,
        )

        # Ingest all investigators under the location.
        investigators = doc.get("investigators", [])
        investigator_ids = []
        for investigator in investigators:
            investigator_id = self.ingest_investigator(investigator)
            if investigator_id:
                investigator_ids.append(investigator_id)

        # Add `LocationInvestigator` records for each `Investigator`.
        for investigator_id in investigator_ids:
            self.dal.iodi_location_investigator(
                location_id=obj_id,
                investigator_id=investigator_id
            )

        return obj_id

    @log_ingestion_of_document(document_name="oversight_info")
    def ingest_oversight_info(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<oversight_info_struct>` and
        creates a `OversightInto` record.

        Args:
            doc (dict): The element of type `<oversight_info_struct>` parsed
                into a dictionary.

        Returns:
             int: The primary-key ID of the `OversightInto` record.
        """

        if not doc:
            return None

        obj_id = self.dal.insert_oversight_info(
            has_dmc=doc.get("has_dmc"),
            is_fda_regulated_drug=doc.get("is_fda_regulated_drug"),
            is_fda_regulated_device=doc.get("is_fda_regulated_device"),
            is_unapproved_device=doc.get("is_unapproved_device"),
            is_ppsd=doc.get("is_ppsd"),
            is_us_export=doc.get("is_us_export"),
        )

        return obj_id

    def update_study_fk(
        self,
        study: Study,
        fk_name: str,
        orm_class: Type[OrmBase],
        id_old: int,
        id_new: int,
    ):
        """Updates the value of a foreign-key attribute of a `Study` record
        and deletes the record of `orm_class` type the `Study` used to link
        to."""

        if study and getattr(study, fk_name):
            msg = ("Updating foreign-key `{}` of `Study` record with ID '{}' "
                   "from value '{}' to '{}' and deleting old record of type "
                   "'{}'.")
            msg_fmt = msg.format(
                fk_name,
                study.study_id,
                id_old,
                id_new,
                orm_class.__name__,
            )
            self.logger.debug(msg_fmt)

            # Update the foreign-key value.
            self.dal.update_attr_value(
                orm_class=Study,
                pk=study.study_id,
                attr_name=fk_name,
                attr_value=id_new,
            )
            # Update the old linked record.
            self.dal.delete(
                orm_class=orm_class,
                pk=id_old,
            )

    @log_ingestion_of_document(document_name="expanded_access_info")
    def ingest_expanded_access_info(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<expanded_access_info_struct>` and
        creates a `ExpandedAccessInfo` record.

        Args:
            doc (dict): The element of type `<expanded_access_info_struct>`
                parsed into a dictionary.

        Returns:
             int: The primary-key ID of the `ExpandedAccessInfo` record.
        """

        if not doc:
            return None

        obj_id = self.dal.insert_expanded_access_info(
            expanded_access_type_individual=doc.get(
                "expanded_access_type_individual"
            ),
            expanded_access_type_intermediate=doc.get(
                "expanded_access_type_intermediate"
            ),
            expanded_access_type_treatment=doc.get(
                "expanded_access_type_treatment"
            ),
        )

        return obj_id

    @log_ingestion_of_document(document_name="study_design_info")
    def ingest_study_design_info(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<study_design_info_struct>` and
        creates a `StudyDesignInfo` record.

        Args:
            doc (dict): The element of type `<study_design_info>` parsed into a
                dictionary.

        Returns:
             int: The primary-key ID of the `StudyDesignInfo` record.
        """

        if not doc:
            return None

        obj_id = self.dal.insert_study_design_info(
            allocation=doc.get("allocation"),
            intervention_model=doc.get("intervention_model"),
            intervention_model_description=doc.get(
                "intervention_model_description"
            ),
            primary_purpose=doc.get("primary_purpose"),
            observational_model=doc.get("observational_model"),
            time_perspective=doc.get("time_perspective"),
            masking=doc.get("masking"),
            masking_description=doc.get("masking_description"),
        )

        return obj_id

    def delete_existing_study_secondary_ids(
        self,
        study: Study,
    ) -> None:
        """ Deletes the existing `StudySecondaryId` records associated with the
            currently ingested study.

        Args:
            study (Study): The existing `Study` record object for which the
                `StudySecondaryId` records will be deleted.
        """

        if not study:
            return None

        # Collect all `StudySecondaryId` objects linked to the given `Study`
        # record.
        study_secondary_ids = self.dal.bget_by_attr(
            orm_class=StudySecondaryId,
            attr_name="study_id",
            attr_values=[study.study_id],
            do_sort=False,
        )  # type: List[StudySecondaryId]

        # Collect all `StudySecondaryId` IDs.
        study_secondary_ids_ids = [
            study_secondary_id.study_secondary_id_id
            for study_secondary_id in study_secondary_ids
        ]

        # Delete all related `StudySecondaryId` records.
        for study_secondary_ids_id in study_secondary_ids_ids:
            self.dal.delete(
                orm_class=StudySecondaryId,
                pk=study_secondary_ids_id
            )

    def delete_existing_protocol_outcomes(
        self,
        study: Study,
    ) -> None:
        """Deletes the existing `ProtocolOutcome` and `StudyOutcome` records
        associated with the currently ingested study.

        Args:
            study (Study): The existing `Study` record object for which the
                `ProtocolOutcome` and `StudyOutcome` records will be deleted.
        """

        if not study:
            return None

        # Collect all `StudyOutcome` objects linked to the given `Study` record.
        study_outcomes = self.dal.bget_by_attr(
            orm_class=StudyOutcome,
            attr_name="study_id",
            attr_values=[study.study_id],
            do_sort=False,
        )  # type: List[StudyOutcome]

        # Collect all `ProtocolOutcome` IDs.
        protocol_outcome_ids = [
            study_outcome.protocol_outcome_id
            for study_outcome in study_outcomes
        ]

        # Collect all `StudyOutcome` IDs.
        study_outcome_ids = [
            study_outcome.study_outcome_id
            for study_outcome in study_outcomes
        ]

        # Delete all related `StudyOutcome` records.
        for study_outcome_id in study_outcome_ids:
            self.dal.delete(
                orm_class=StudyOutcome,
                pk=study_outcome_id
            )

        # Delete all related `ProtocolOutcome` records.
        for protocol_outcome_id in protocol_outcome_ids:
            self.dal.delete(
                orm_class=ProtocolOutcome,
                pk=protocol_outcome_id
            )

    @log_ingestion_of_document(document_name="protocol_outcome")
    def ingest_protocol_outcome(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<protocol_outcome_struct>` and
        creates a `ProtocolOutcome` record.

        Args:
            doc (dict): The element of type `<protocol_outcome_struct>` parsed
                into a dictionary.

        Returns:
             int: The primary-key ID of the `ProtocolOutcome` record.
        """

        if not doc:
            return None

        obj_id = self.dal.insert_protocol_outcome(
            measure=doc.get("measure"),
            time_frame=doc.get("time_frame"),
            description=doc.get("description"),
        )

        return obj_id

    @log_ingestion_of_document(document_name="enrollment")
    def ingest_enrollment(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<enrollment_struct>` and creates
        an `Enrollment` record.

        Args:
            doc (dict): The element of type `<enrollment_struct>` parsed into a
                dictionary.

        Returns:
             int: The primary-key ID of the `Enrollment` record.
        """

        if not doc:
            return None

        obj_id = self.dal.insert_enrollment(
            value=doc.get("value"),
            enrollment_type=doc.get("type"),
        )

        return obj_id

    def delete_existing_arm_groups(
        self,
        study: Study,
    ) -> None:
        """Deletes the existing `ArmGroup` and `StudyArmGroup` records
        associated with the currently ingested study.

        Args:
            study (Study): The existing `Study` record object for which the
                `ArmGroup` and `StudyArmGroup` records will be deleted.
        """

        if not study:
            return None

        # Collect all `StudyArmGroup` objects linked to the given `Study`
        # record.
        study_arm_groups = self.dal.bget_by_attr(
            orm_class=StudyArmGroup,
            attr_name="study_id",
            attr_values=[study.study_id],
            do_sort=False,
        )  # type: List[StudyArmGroup]

        # Collect all `StudyIntervention` objects linked to the given `Study`
        # record.
        study_interventions = self.dal.bget_by_attr(
            orm_class=StudyIntervention,
            attr_name="study_id",
            attr_values=[study.study_id],
            do_sort=False,
        )  # type: List[StudyIntervention]

        # Collect all `InterventionArmGroup` objects linked to the given `Study`
        # record through the collected `StudyIntervention` records.
        intervention_arm_groups = []
        for study_intervention in study_interventions:
            intervention_arm_groups += self.dal.bget_by_attr(
                orm_class=InterventionArmGroup,
                attr_name="intervention_id",
                attr_values=[study_intervention.intervention_id],
                do_sort=False,
            )  # type: List[InterventionArmGroup]

        # Collect all `StudyArmGroup` IDs.
        study_arm_group_ids = [
            study_arm_group.study_arm_group_id
            for study_arm_group in study_arm_groups
        ]

        # Collect all `InterventionArmGroup` IDs.
        interventions_arm_group_ids = [
            intervention_arm_group.intervention_arm_group_id
            for intervention_arm_group in intervention_arm_groups
        ]

        # Collect all `ArmGroup` IDs.
        arm_group_ids = [
            study_arm_group.arm_group_id
            for study_arm_group in study_arm_groups
        ] + [
            intervention_arm_group.arm_group_id
            for intervention_arm_group in intervention_arm_groups
        ]
        arm_group_ids = list(set(arm_group_ids))

        # Delete all related `StudyArmGroup` records.
        for study_arm_group_id in study_arm_group_ids:
            self.dal.delete(
                orm_class=StudyArmGroup,
                pk=study_arm_group_id
            )

        # Delete all related `InterventionArmGroup` records.
        for interventions_arm_group_id in interventions_arm_group_ids:
            self.dal.delete(
                orm_class=InterventionArmGroup,
                pk=interventions_arm_group_id
            )

        # Delete all related `ArmGroup` records.
        for arm_group_id in arm_group_ids:
            self.dal.delete(
                orm_class=ArmGroup,
                pk=arm_group_id,
            )

    @log_ingestion_of_document(document_name="arm_group")
    def ingest_arm_group(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<arm_group_struct>` and creates
        an `ArmGroup` record.

        Args:
            doc (dict): The element of type `<arm_group_struct>` parsed into a
                dictionary.

        Returns:
             int: The primary-key ID of the `ArmGroup` record.
        """

        if not doc:
            return None

        obj_id = self.dal.insert_arm_group(
            label=doc.get("arm_group_label"),
            arm_group_type=doc.get("arm_group_type"),
            description=doc.get("description"),
        )

        return obj_id

    @log_ingestion_of_document(document_name="intervention")
    def ingest_intervention(
        self,
        doc: dict,
        arm_group_labels_ids: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<intervention_struct>` and creates
        an `Intervention` record.

        Args:
            doc (dict): The element of type `<intervention_struct>` parsed into
                a dictionary.
            arm_group_labels_ids (dict): A dictionary of `label:ID` pairs
                pertaining to the previously added `ArmGroup` records.

        Returns:
             int: The primary-key ID of the `Intervention` record.
        """

        if not doc:
            return None

        obj_id = self.dal.iodi_intervention(
            intervention_type=doc.get("intervention_type"),
            name=doc.get("intervention_name"),
            description=doc.get("description"),
        )

        # Add `Alias` and `InterventionAlias` records.
        for alias_data in doc.get("other_names", []):
            alias = alias_data.get("other_name")
            alias_id = self.dal.iodi_alias(alias=alias)
            self.dal.iodi_intervention_alias(
                intervention_id=obj_id,
                alias_id=alias_id,
            )

        for arm_group_label_data in doc.get("arm_group_labels", []):
            arm_group_label = arm_group_label_data.get("arm_group_label")
            if arm_group_label not in arm_group_labels_ids:
                continue
            self.dal.iodi_intervention_arm_group(
                intervention_id=obj_id,
                arm_group_id=arm_group_labels_ids[arm_group_label],
            )

        return obj_id

    @log_ingestion_of_document(document_name="reference")
    def ingest_reference(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<reference_struct>` and creates a
        `Reference` record.

        Args:
            doc (dict): The element of type `<reference_struct>` parsed into a
                dictionary.

        Returns:
             int: The primary-key ID of the `Reference` record.
        """

        if not doc:
            return None

        obj_id = self.dal.iodu_reference(
            citation=doc.get("citation"),
            pmid=doc.get("pmid"),
        )

        return obj_id

    @log_ingestion_of_document(document_name="study_dates")
    def ingest_study_dates(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests the parsed 'new dates' out of a parsed `<clinical_study>`
        element and creates a `StudyDates` record.

        Args:
            doc (dict): The element of type `<clinical_study>` parsed into a
                dictionary.

        Returns:
             int: The primary-key ID of the `StudyDates` record.
        """

        if not doc:
            return None

        obj_id = self.dal.insert_study_dates(
            study_first_submitted=self._edt(doc.get("study_first_submitted")),
            study_first_submitted_qc=self._edt(
                doc.get("study_first_submitted_qc")
            ),
            study_first_posted=self._edt(doc.get("study_first_posted")),
            results_first_submitted=self._edt(
                doc.get("results_first_submitted")
            ),
            results_first_submitted_qc=self._edt(
                doc.get("results_first_submitted_qc")
            ),
            results_first_posted=self._edt(doc.get("results_first_posted")),
            disposition_first_submitted=self._edt(
                doc.get("disposition_first_submitted")
            ),
            disposition_first_submitted_qc=self._edt(
                doc.get("disposition_first_submitted_qc")
            ),
            disposition_first_posted=self._edt(
                doc.get("disposition_first_posted")
            ),
            last_update_submitted=self._edt(doc.get("last_update_submitted")),
            last_update_submitted_qc=self._edt(
                doc.get("last_update_submitted_qc")
            ),
            last_update_posted=self._edt(doc.get("last_update_posted")),
        )

        return obj_id

    @log_ingestion_of_document(document_name="responsible_party")
    def ingest_responsible_party(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<responsible_party_struct>` and
        creates a `ResponsibleParty` record.

        Args:
            doc (dict): The element of type `<responsible_party_struct>` parsed
                into a dictionary.

        Returns:
             int: The primary-key ID of the `ResponsibleParty` record.
        """

        if not doc:
            return None

        obj_id = self.dal.insert_responsible_party(
            name_title=doc.get("name_title"),
            organization=doc.get("organization"),
            responsible_party_type=doc.get("responsible_party_type"),
            investigator_affiliation=doc.get("investigator_affiliation"),
            investigator_full_name=doc.get("investigator_full_name"),
            investigator_title=doc.get("investigator_title"),
        )

        return obj_id

    def delete_existing_pata_data_ipd_info_types(
        self,
        patient_data_id: int,
    ) -> None:
        """ Deletes the existing `PatientDataIpdInfoType` records associated
            with the currently ingested `PatientData` record.

        Args:
            patient_data_id (int): The ID of the `PatientData` record for which
                the `PatientDataIpdInfoType` records will be deleted.
        """

        if not patient_data_id:
            return None

        # Collect all `PatientDataIpdInfoType` objects linked to the given
        # `PatientData` record.
        ipd_info_types = self.dal.bget_by_attr(
            orm_class=PatientDataIpdInfoType,
            attr_name="patient_data_id",
            attr_values=[patient_data_id],
            do_sort=False,
        )  # type: List[PatientDataIpdInfoType]

        # Collect all `PatientDataIpdInfoType` IDs.
        patient_data_ipd_info_type_ids = [
            ipd_info_type.patient_data_ipd_info_type_id
            for ipd_info_type in ipd_info_types
        ]

        # Delete all related `StudySecondaryId` records.
        for patient_data_ipd_info_type_id in patient_data_ipd_info_type_ids:
            self.dal.delete(
                orm_class=PatientDataIpdInfoType,
                pk=patient_data_ipd_info_type_id,
            )

    @log_ingestion_of_document(document_name="patient_data")
    def ingest_patient_data(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<patient_data_struct>` and creates
        a `PatientData` record.

        Args:
            doc (dict): The element of type `<patient_data_struct>` parsed into
                a dictionary.

        Returns:
             int: The primary-key ID of the `PatientData` record.
        """

        if not doc:
            return None

        obj_id = self.dal.insert_patient_data(
            sharing_ipd=doc.get("sharing_ipd"),
            ipd_description=doc.get("ipd_description"),
            ipd_time_frame=doc.get("ipd_time_frame"),
            ipd_access_criteria=doc.get("ipd_access_criteria"),
            ipd_url=doc.get("ipd_url"),
        )

        return obj_id

    def delete_existing_study_docs(
        self,
        study: Study,
    ) -> None:
        """Deletes the existing `StudyDoc` and `StudyStudyDoc` records
        associated with the currently ingested study.

        Args:
            study (Study): The existing `Study` record object for which the
                `StudyDoc` and `StudyStudyDoc` records will be deleted.
        """

        if not study:
            return None

        # Collect all `StudyStudyDoc` objects linked to the given `Study`
        # record.
        study_study_docs = self.dal.bget_by_attr(
            orm_class=StudyStudyDoc,
            attr_name="study_id",
            attr_values=[study.study_id],
            do_sort=False,
        )  # type: List[StudyStudyDoc]

        # Collect all `StudyDoc` IDs.
        study_doc_ids = [
            study_study_doc.study_doc_id
            for study_study_doc in study_study_docs
        ]

        # Collect all `StudyStudyDoc` IDs.
        study_study_doc_ids = [
            study_study_doc.study_study_doc_id
            for study_study_doc in study_study_docs
        ]

        # Delete all related `StudyStudyDoc` records.
        for study_study_doc_id in study_study_doc_ids:
            self.dal.delete(
                orm_class=StudyStudyDoc,
                pk=study_study_doc_id
            )

        # Delete all related `StudyDoc` records.
        for study_doc_id in study_doc_ids:
            self.dal.delete(
                orm_class=StudyDoc,
                pk=study_doc_id,
            )

    @log_ingestion_of_document(document_name="study_doc")
    def ingest_study_doc(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<study_doc_struct>` and creates
        a `StudyDoc` record.

        Args:
            doc (dict): The element of type `<study_doc_struct>` parsed into
                a dictionary.

        Returns:
             int: The primary-key ID of the `StudyDoc` record.
        """

        if not doc:
            return None

        obj_id = self.dal.insert_study_doc(
            doc_id=doc.get("doc_id"),
            doc_type=doc.get("doc_type"),
            doc_url=doc.get("doc_url"),
            doc_comment=doc.get("doc_comment"),
        )

        return obj_id

    @log_ingestion_of_document(document_name="eligibility")
    def ingest_eligibility(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<eligibility_struct>` and creates
        a `Eligibility` record.

        Args:
            doc (dict): The element of type `<eligibility_struct>` parsed into
                a dictionary.

        Returns:
             int: The primary-key ID of the `Eligibility` record.
        """

        if not doc:
            return None

        obj_id = self.dal.insert_eligibility(
            study_pop=doc.get("study_pop"),
            sampling_method=doc.get("sampling_method"),
            criteria=doc.get("criteria"),
            gender=doc.get("gender"),
            gender_based=doc.get("gender_based"),
            gender_description=doc.get("gender_description"),
            minimum_age=doc.get("minimum_age"),
            maximum_age=doc.get("maximum_age"),
            healthy_volunteers=doc.get("healthy_volunteers"),
        )

        return obj_id

    @log_ingestion_of_document(document_name="clinical_study")
    def ingest(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<clinical_study>` and creates a
        `Study` record.

        Args:
            doc (dict): The element of type `<clinical_study`> parsed into a
                dictionary.

        Returns:
             int: The primary-key ID of the `Study` record.
        """

        if not doc:
            return None

        # Retrieve the `id_info` object.
        id_info = doc.get("id_info", {})

        # Retrieve the NCT ID of the study.
        nct_id = id_info.get("nct_id")

        # Check for the existence of a study with the same NCT ID and retrieve
        # it if it does exist.
        study = self.dal.get_by_attr(
            orm_class=Study,
            attr_name="nct_id",
            attr_value=nct_id,
        )

        # Create the `OversightInfo` record and hold on to its primary-key ID.
        oversight_info_id = self.ingest_oversight_info(
            doc.get("oversight_info"),
        )
        # Update the `oversight_info_id` of the existing `Study` record
        # (if defined) and delete the old `OversightInfo` record.
        if study and study.oversight_info_id:
            self.update_study_fk(
                study=study,
                fk_name="oversight_info_id",
                orm_class=OversightInfo,
                id_old=study.oversight_info_id,
                id_new=oversight_info_id,
            )

        # Create the `ExpandedAccessInfo` record and hold on to its primary-key
        # ID.
        expanded_access_info_id = self.ingest_expanded_access_info(
            doc.get("expanded_access_info"),
        )
        # Update the `expanded_access_info_id` of the existing `Study` record
        # (if defined) and delete the old `ExpandedAccessInfo` record.
        if study and study.expanded_access_info_id:
            self.update_study_fk(
                study=study,
                fk_name="expanded_access_info_id",
                orm_class=ExpandedAccessInfo,
                id_old=study.expanded_access_info_id,
                id_new=expanded_access_info_id,
            )

        # Create the `StudyDesignInfo` record and hold on to its primary-key
        # ID.
        study_design_info_id = self.ingest_study_design_info(
            doc.get("study_design_info"),
        )
        # Update the `study_design_info_id` of the existing `Study` record (if
        # defined) and delete the old `StudyDesignInfo` record.
        if study and study.study_design_info_id:
            self.update_study_fk(
                study=study,
                fk_name="study_design_info_id",
                orm_class=StudyDesignInfo,
                id_old=study.study_design_info_id,
                id_new=study_design_info_id,
            )

        # Create the `Enrollment` record and hold on to its primary-key ID.
        enrollment_id = self.ingest_enrollment(doc.get("enrollment"))
        # Update the `enrollment_id` of the existing `Study` record (if defined)
        # and delete the old `StudyDesignInfo` record.
        if study and study.enrollment_id:
            self.update_study_fk(
                study=study,
                fk_name="enrollment_id",
                orm_class=Enrollment,
                id_old=study.enrollment_id,
                id_new=enrollment_id,
            )

        # Create the `Eligibility` record and hold on to its primary-key ID.
        eligibility_id = self.ingest_eligibility(doc.get("eligibility"))
        # Update the `eligibility_id` of the existing `Study` record (if
        # defined) and delete the old `Eligibility` record.
        if study and study.eligibility_id:
            self.update_study_fk(
                study=study,
                fk_name="eligibility_id",
                orm_class=Eligibility,
                id_old=study.eligibility_id,
                id_new=eligibility_id,
            )

        # Create the primary `Contact` record and hold on to its primary-key ID.
        contact_primary_id = self.ingest_contact(doc.get("overall_contact"))

        # Create the backup `Contact` record and hold on to its primary-key ID.
        contact_backup_id = self.ingest_contact(
            doc.get("overall_contact_backup")
        )

        # Create the `StudyDates` record and hold on to its primary-key ID.
        study_dates_id = self.ingest_study_dates(doc.get("study_dates"))
        # Update the `study_dates_id` of the existing `Study` record (if
        # defined) and delete the old `StudyDates` record.
        if study and study.study_dates_id:
            self.update_study_fk(
                study=study,
                fk_name="study_dates_id",
                orm_class=StudyDates,
                id_old=study.study_dates_id,
                id_new=study_dates_id,
            )

        # Create the `ResponsibleParty` record and hold on to its primary-key
        # ID.
        responsible_party_id = self.ingest_responsible_party(
            doc.get("responsible_party")
        )
        # Update the `responsible_party_id` of the existing `Study` record (if
        # defined) and delete the old `ResponsibleParty` record.
        if study and study.responsible_party_id:
            self.update_study_fk(
                study=study,
                fk_name="responsible_party_id",
                orm_class=ResponsibleParty,
                id_old=study.responsible_party_id,
                id_new=responsible_party_id,
            )

        # Create the `PatientData` record and hold on to its primary-key ID.
        patient_data_id = self.ingest_patient_data(doc.get("patient_data"))
        # Update the `patient_data_id` of the existing `Study` record (if
        # defined) and delete the old `PatientData` record.
        if study and study.patient_data_id:
            self.delete_existing_pata_data_ipd_info_types(
                patient_data_id=patient_data_id,
            )
            self.update_study_fk(
                study=study,
                fk_name="patient_data_id",
                orm_class=PatientData,
                id_old=study.patient_data_id,
                id_new=patient_data_id,
            )

        obj_id = self.dal.iodu_study(
            org_study_id=id_info.get("org_study_id"),
            nct_id=id_info.get("nct_id"),
            brief_title=doc.get("brief_title"),
            acronym=doc.get("acronym"),
            official_title=doc.get("official_title"),
            source=doc.get("source"),
            oversight_info_id=oversight_info_id,
            brief_summary=doc.get("brief_summary"),
            detailed_description=doc.get("detailed_description"),
            overall_status=doc.get("overall_status"),
            last_known_status=doc.get("last_known_status"),
            why_stopped=doc.get("why_stopped"),
            start_date=self._edt(doc.get("start_date")),
            completion_date=self._edt(doc.get("completion_date")),
            primary_completion_date=self._edt(
                doc.get("primary_completion_date")
            ),
            verification_date=self._edt(doc.get("verification_date")),
            phase=doc.get("phase"),
            study_type=doc.get("study_type"),
            expanded_access_info_id=expanded_access_info_id,
            study_design_info_id=study_design_info_id,
            target_duration=doc.get("target_duration"),
            enrollment_id=enrollment_id,
            biospec_retention=doc.get("biospec_retention"),
            biospec_description=doc.get("biospec_description"),
            eligibility_id=eligibility_id,
            contact_primary_id=contact_primary_id,
            contact_backup_id=contact_backup_id,
            study_dates_id=study_dates_id,
            responsible_party_id=responsible_party_id,
            patient_data_id=patient_data_id,
        )

        # Create `Alias` and `StudyAlias` records.
        for alias_data in id_info.get("nct_aliases", []):
            alias = alias_data["nct_alias"]
            alias_id = self.dal.iodi_alias(alias=alias)
            self.dal.iodi_study_alias(study_id=obj_id, alias_id=alias_id)

        # Create `Sponsor` and `StudySponsor` records.
        for sponsor in doc.get("sponsors", []):
            sponsor_id = self.ingest_sponsor(sponsor)
            self.dal.iodu_study_sponsor(
                study_id=obj_id,
                sponsor_id=sponsor_id,
                sponsor_type=sponsor.get("type"),
            )

        # Delete the existing `StudySecondaryId` records (if they exist).
        self.delete_existing_study_secondary_ids(study=study)
        # Create `StudySecondaryId` records.
        for secondary_id in id_info.get("secondary_ids", []):
            self.dal.insert_study_secondary_id(
                study_id=obj_id,
                secondary_id=secondary_id.get("secondary_id"),
            )

        # Delete the existing `ProtocolOutcome` and `StudyOutcome` records (if
        # they exist).
        self.delete_existing_protocol_outcomes(study=study)
        # Create `ProtocolOutcome` and `StudyOutcome` records.
        for protocol_outcome in doc.get("protocol_outcomes", []):
            protocol_outcome_id = self.ingest_protocol_outcome(protocol_outcome)
            self.dal.iodu_study_outcome(
                study_id=obj_id,
                protocol_outcome_id=protocol_outcome_id,
                outcome_type=protocol_outcome.get("type"),
            )

        # Create `Condition` and `StudyCondition` records.
        for condition in doc.get("conditions", []):
            condition_id = self.ingest_condition(condition)
            self.dal.iodi_study_condition(
                study_id=obj_id,
                condition_id=condition_id,
            )

        # Delete the existing `ArmGroup` and `StudyArmGroup` records (if they
        # exist).
        self.delete_existing_arm_groups(study=study)
        # Create `ArmGroup` and `StudyArmGroup` records.
        arm_group_labels_ids = {}
        for arm_group in doc.get("arm_groups", []):
            arm_group_id = self.ingest_arm_group(arm_group)
            arm_group_label = arm_group.get("arm_group_label")
            arm_group_labels_ids[arm_group_label] = arm_group_id
            self.dal.iodi_study_arm_group(
                study_id=obj_id,
                arm_group_id=arm_group_id
            )

        # Create `Intevention` and `StudyIntervention` records.
        for intervention in doc.get("interventions", []):
            intervention_id = self.ingest_intervention(
                intervention,
                arm_group_labels_ids=arm_group_labels_ids,
            )
            self.dal.iodi_study_intervention(
                study_id=obj_id,
                intervention_id=intervention_id,
            )

        # Create `Investigator` and `StudyInvestigator` records.
        for investigator in doc.get("overall_officials", []):
            investigator_id = self.ingest_investigator(investigator)
            self.dal.iodi_study_investigator(
                study_id=obj_id,
                investigator_id=investigator_id,
            )

        # Create `Location` and `StudyLocation` records.
        for location in doc.get("locations", []):
            location_id = self.ingest_location(location)
            self.dal.iodi_study_location(
                study_id=obj_id,
                location_id=location_id,
            )

        # Create `Reference` and `StudyReference` records.
        for reference in doc.get("references", []):
            reference_id = self.ingest_reference(reference)
            self.dal.iodu_study_reference(
                study_id=obj_id,
                reference_id=reference_id,
                reference_type=reference.get("type"),
            )

        # Create `Keyword` and `StudyKeyword` records.
        for keyword in doc.get("keywords", []):
            keyword_id = self.ingest_keyword(keyword)
            self.dal.iodi_study_keyword(
                study_id=obj_id,
                keyword_id=keyword_id,
            )

        # Create `StudyDescriptor` records.
        for mesh_term in doc.get("mesh_terms", []):
            descriptor = self.dal.get_by_attr(
                orm_class=Descriptor,
                attr_name="name",
                attr_value=mesh_term.get("mesh_term"),
            )  # type: Descriptor
            if descriptor:
                self.dal.iodu_study_descriptor(
                    study_id=obj_id,
                    descriptor_id=descriptor.descriptor_id,
                    study_descriptor_type=mesh_term.get("type")
                )

        # Delete the existing `StudyDoc` and `StudyStudyDoc` records (if they
        # exist).
        self.delete_existing_study_docs(study=study)
        # Create `StudyDoc` and `StudyStudyDoc` records.
        for study_doc in doc.get("study_docs", []):
            study_doc_id = self.ingest_study_doc(study_doc)
            self.dal.iodi_study_study_doc(
                study_id=obj_id,
                study_doc_id=study_doc_id,
            )

        return obj_id
