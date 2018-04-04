# -*- coding: utf-8 -*-

import datetime

import sqlalchemy.orm
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.engine.result import ResultProxy

from ct_ingester.loggers import create_logger
from ct_ingester.dal_base import DalBase
from ct_ingester.dal_base import with_session_scope
from ct_ingester.orm import Sponsor
from ct_ingester.orm import Keyword
from ct_ingester.orm import Condition
from ct_ingester.orm import Facility
from ct_ingester.orm import Person
from ct_ingester.orm import Contact
from ct_ingester.orm import Investigator
from ct_ingester.orm import Location
from ct_ingester.orm import LocationInvestigator
from ct_ingester.orm import OversightInfo
from ct_ingester.orm import ExpandedAccessInfo
from ct_ingester.orm import StudyDesignInfo
from ct_ingester.orm import ProtocolOutcome
from ct_ingester.orm import Group
from ct_ingester.orm import Analysis
from ct_ingester.orm import AnalysisGroup
from ct_ingester.orm import MeasureCount
from ct_ingester.orm import MeasureAnalyzed
from ct_ingester.orm import MeasureAnalyzedCount
from ct_ingester.orm import Measurement
from ct_ingester.orm import ResultOutcome
from ct_ingester.orm import ResultOutcomeGroup
from ct_ingester.orm import Enrollment
from ct_ingester.orm import ArmGroup
from ct_ingester.orm import Intervention
from ct_ingester.orm import Alias
from ct_ingester.orm import InterventionAlias
from ct_ingester.orm import InterventionArmGroup
from ct_ingester.orm import Eligibility
from ct_ingester.orm import Reference
from ct_ingester.orm import ResponsibleParty
from ct_ingester.orm import MeshTerm
from ct_ingester.orm import PatientData
from ct_ingester.orm import StudyDoc
from ct_ingester.orm import Study
from ct_ingester.orm import StudyAlias
from ct_ingester.orm import StudySponsor
from ct_ingester.orm import StudyOutcome
from ct_ingester.orm import StudyCondition
from ct_ingester.orm import StudyArmGroup
from ct_ingester.orm import StudyIntervention
from ct_ingester.orm import StudyInvestigator
from ct_ingester.orm import StudyLocation
from ct_ingester.orm import StudyReference
from ct_ingester.orm import StudyKeyword
from ct_ingester.orm import StudyMeshTerm
from ct_ingester.orm import StudyStudyDoc
from ct_ingester.orm import StudyDates
from ct_ingester.orm_enums import AgencyClassType
from ct_ingester.orm_enums import SponsorType
from ct_ingester.orm_enums import RoleType
from ct_ingester.orm_enums import RecruitmentStatusType
from ct_ingester.orm_enums import NonInferiorityType
from ct_ingester.orm_enums import AnalysisDispersionType
from ct_ingester.orm_enums import NumSidesType
from ct_ingester.orm_enums import OutcomeType
from ct_ingester.orm_enums import ActualType
from ct_ingester.orm_enums import InterventionType
from ct_ingester.orm_enums import SamplingMethodType
from ct_ingester.orm_enums import GenderType
from ct_ingester.orm_enums import ResponsiblePartyType
from ct_ingester.orm_enums import OverallStatusType
from ct_ingester.orm_enums import PhaseType
from ct_ingester.orm_enums import StudyType
from ct_ingester.orm_enums import BiospecRetentionType
from ct_ingester.orm_enums import MeshTermType
from ct_ingester.orm_enums import ReferenceType
from ct_ingester.utils import return_first_item


class DalClinicalTrials(DalBase):
    def __init__(
        self,
        sql_username,
        sql_password,
        sql_host,
        sql_port,
        sql_db,
        *args,
        **kwargs
    ):

        self.logger = create_logger(
            logger_name=type(self).__name__,
            logger_level=kwargs.get("logger_level", "DEBUG")
        )

        super(DalClinicalTrials, self).__init__(
            sql_username=sql_username,
            sql_password=sql_password,
            sql_host=sql_host,
            sql_port=sql_port,
            sql_db=sql_db,
            *args,
            **kwargs
        )

    @with_session_scope()
    def get_by_md5(
        self,
        orm_class,
        md5: bytes,
        session: sqlalchemy.orm.Session = None,
    ):
        """Retrieves an object of a class derived off `OrmBase` through its MD5.

        Args:
            md5 (bytes): The MD5 has of the `OrmBase` record to be retrieved.
            orm_class: An object of a class derived off `OrmBase` implementing
                an `md5` attribute.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            The matching `OrmBase` record object or `None` if no such record
                exists.
        """

        query = session.query(orm_class)
        query = query.filter(orm_class.md5 == md5)

        obj = query.one_or_none()

        return obj

    @with_session_scope()
    def get_by_attrs(
        self,
        orm_class,
        attrs_names_values: dict,
        session: sqlalchemy.orm.Session = None,
    ):
        """Retrieves the record object of `orm_class` type through attribute
        name-value pairs.

        Note:
            This method should only be used through unique attributes/fields as
            it uses the `one_or_none` retrieval method and will raise an
            exception should multiple records with a given attribute value be
            found.

        Args:
            orm_class: An object of a class derived off `OrmBase` implementing
                an `md5` attribute.
            attrs_names_values (dict): A dictionary of attribute name-value
                pairs to be used in filtering out a single record.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            orm_class: The record object of type `orm_class` matching the
                attribute name-value pairs and `None` if no record exists.

        Raises:
            sqlalchemy.orm.exc.MultipleResultsFound: Raised when multiple
                records were found with the given attribute(s).
        """

        query = session.query(orm_class)
        for attr_name, attr_value in attrs_names_values.items():
            query = query.filter(
                getattr(orm_class, attr_name) == attr_value
            )

        obj = query.one_or_none()

        return obj

    @return_first_item
    @with_session_scope()
    def iodi_sponsor(
        self,
        agency: str,
        agency_class: AgencyClassType,
        session: sqlalchemy.orm.Session=None,
    ) -> int:
        """Creates a new `Sponsor` record in an IODI manner.

        Args:
            agency (str): The sponsor agency.
            agency_class (AgencyClassType): An enumeration member denoting the
                sponsor agency class.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Sponsor` record.
        """

        # Create and populate a `Sponsor` object so that we can retrieve the
        # MD5 hash.
        sponsor_obj = Sponsor()
        sponsor_obj.agency = agency
        sponsor_obj.agency_class = agency_class

        statement = insert(
            Sponsor,
            values={
                "agency": agency,
                "class": agency_class,
                "md5": sponsor_obj.md5,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            sponsor_obj = self.get_by_md5(
                orm_class=Sponsor,
                md5=sponsor_obj.md5,
                session=session,
            )  # type: Sponsor
            return sponsor_obj.sponsor_id

    @return_first_item
    @with_session_scope()
    def iodi_keyword(
        self,
        keyword: str,
        session: sqlalchemy.orm.Session=None,
    ) -> int:
        """Creates a new `Keyword` record in an IODI manner.

        Args:
            keyword (str): The keyword.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Keyword` record.
        """

        # Create and populate a `Person` object so that we can retrieve the
        # MD5 hash.
        keyword_obj = Keyword()
        keyword_obj.keyword = keyword

        statement = insert(
            Keyword,
            values={
                "keyword": keyword,
                "md5": keyword_obj.md5
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            keyword_obj = self.get_by_md5(
                orm_class=Keyword,
                md5=keyword_obj.md5,
                session=session,
            )  # type: Keyword
            return keyword_obj.keyword_id

    @return_first_item
    @with_session_scope()
    def iodi_condition(
        self,
        condition: str,
        session: sqlalchemy.orm.Session=None,
    ) -> int:
        """Creates a new `Condition` record in an IODI manner.

        Args:
            condition (str): The condition.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Condition` record.
        """

        # Create and populate a `Condition` object so that we can retrieve the
        # MD5 hash.
        condition_obj = Condition()
        condition_obj.condition = condition

        statement = insert(
            Condition,
            values={
                "condition": condition,
                "md5": condition_obj.md5,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            condition_obj = self.get_by_md5(
                orm_class=Condition,
                md5=condition_obj.md5,
                session=session,
            )  # type: Condition
            return condition_obj.condition_id

    @return_first_item
    @with_session_scope()
    def iodi_facility(
        self,
        name: str,
        city: str,
        state: str,
        zip_code: str,
        country: str,
        session: sqlalchemy.orm.Session=None,
    ) -> int:
        """Creates a new `Facility` record in an IODI manner.

        Args:
            name (str): The facility name.
            city (str): The facility city.
            state (str): The facility state.
            zip_code (str): The facility zip-code.
            country (str): The facility country.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Condition` record.
        """

        # Create and populate a `Facility` object so that we can retrieve the
        # MD5 hash.
        facility_obj = Facility()
        facility_obj.name = name,
        facility_obj.city = city
        facility_obj.state = state
        facility_obj.zip_code = zip_code
        facility_obj.country = country

        statement = insert(
            Facility,
            values={
                "name": name,
                "city": city,
                "state": state,
                "zip_code": zip_code,
                "country": country,
                "md5": facility_obj.md5,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            facility_obj = self.get_by_md5(
                orm_class=Facility,
                md5=facility_obj.md5,
                session=session,
            )  # type: Facility
            return facility_obj.facility_id

    @return_first_item
    @with_session_scope()
    def iodi_person(
        self,
        name_first: str,
        name_middle: str,
        name_last: str,
        degrees: str,
        session: sqlalchemy.orm.Session=None,
    ) -> int:
        """Creates a new `Person` record in an IODI manner.

        Args:
            name_first (str): The person first name.
            name_middle (str): The person middle name.
            name_last (str): The person last name.
            degrees (str): The person degrees.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Person` record.
        """

        # Create and populate a `Person` object so that we can retrieve the
        # MD5 hash.
        person_obj = Person()
        person_obj.name_first = name_first
        person_obj.name_middle = name_middle
        person_obj.name_last = name_last
        person_obj.degrees = degrees

        statement = insert(
            Person,
            values={
                "name_first": name_first,
                "name_middle": name_middle,
                "name_last": name_last,
                "degrees": degrees,
                "md5": person_obj.md5,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            person_obj = self.get_by_md5(
                orm_class=Person,
                md5=person_obj.md5,
                session=session,
            )  # type: Person
            return person_obj.person_id

    @return_first_item
    @with_session_scope()
    def iodi_contact(
        self,
        person_id: int,
        phone: str,
        phone_ext: str,
        email: str,
        session: sqlalchemy.orm.Session=None,
    ) -> int:
        """Creates a new `Contact` record in an IODI manner.

        Args:
            person_id (int): The linked `Person` record primary-key ID.
            phone (str): The contact phone.
            phone_ext (str): The contact phone extension.
            email (str): The contact email.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Contact` record.
        """

        # Create and populate a `Contact` object so that we can retrieve the
        # MD5 hash.
        contact_obj = Contact()
        contact_obj.person_id = person_id
        contact_obj.phone = phone
        contact_obj.phone_ext = phone_ext
        contact_obj.email = email

        statement = insert(
            Contact,
            values={
                "person_id": person_id,
                "phone": phone,
                "phone_ext": phone_ext,
                "email": email,
                "md5": contact_obj.md5,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            contact_obj = self.get_by_md5(
                orm_class=Contact,
                md5=contact_obj.md5,
                session=session,
            )  # type: Contact
            return contact_obj.contact_id

    @return_first_item
    @with_session_scope()
    def iodi_investigator(
        self,
        person_id: int,
        role: RoleType,
        affiliation: str,
        session: sqlalchemy.orm.Session=None,
    ) -> int:
        """Creates a new `Contact` record in an IODI manner.

        Args:
            person_id (int): The linked `Person` record primary-key ID.
            role (RoleType): The investigator role-type.
            affiliation (str): The investigator affiliation.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Investigator` record.
        """

        # Create and populate a `Investigator` object so that we can retrieve
        # the MD5 hash.
        investigator_obj = Investigator()
        investigator_obj.person_id = person_id
        investigator_obj.role = role
        investigator_obj.affiliation = affiliation

        statement = insert(
            Investigator,
            values={
                "person_id": person_id,
                "role": role,
                "affiliation": affiliation,
                "md5": investigator_obj.md5,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            investigator_obj = self.get_by_md5(
                orm_class=Investigator,
                md5=investigator_obj.md5,
                session=session,
            )  # type: Investigator
            return investigator_obj.investigator_id

    @return_first_item
    @with_session_scope()
    def iodi_location(
        self,
        facility_id: int,
        status: RecruitmentStatusType,
        contact_primary_id: int,
        contact_backup_id: int,
        session: sqlalchemy.orm.Session=None,
    ) -> int:
        """Creates a new `Location` record in an IODI manner.

        Args:
            facility_id (int): The linked `Facility` record primary-key ID.
            status (RoleType): The location recruitment-status-type.
            contact_primary_id (str): The linked primary `Contact` record.
            contact_backup_id (str): The linked backup `Contact` record.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Location` record.
        """

        statement = insert(
            Location,
            values={
                "facility_id": facility_id,
                "status": status,
                "contact_primary_id": contact_primary_id,
                "contact_backup_id": contact_backup_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            location_obj = self.get_by_attrs(
                orm_class=Location,
                attrs_names_values={
                    "facility_id": facility_id,
                    "contact_primary_id": contact_primary_id,
                    "contact_backup_id": contact_backup_id,
                },
                session=session,
            )  # type: Location
            return location_obj.location_id

    @return_first_item
    @with_session_scope()
    def iodi_location_investigator(
        self,
        location_id: int,
        investigator_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `LocationInvestigator` record in an IODI manner.

        Args:
            location_id (int): The linked `Location` record primary-key ID.
            investigator_id (int): The linked `Investigator` record primary-key
                ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `LocationInvestigator` record.
        """

        statement = insert(
            LocationInvestigator,
            values={
                "location_id": location_id,
                "investigator_id": investigator_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=LocationInvestigator,
                attrs_names_values={
                    "location_id": location_id,
                    "investigator_id": investigator_id,
                },
                session=session,
            )  # type: LocationInvestigator
            return obj.location_investigator_id

    @return_first_item
    @with_session_scope()
    def iodi_oversight_info(
        self,
        has_dmc: bool,
        is_fda_regulated_drug: bool,
        is_fda_regulated_device: bool,
        is_unapproved_device: bool,
        is_ppsd: bool,
        is_us_export: bool,
        session: sqlalchemy.orm.Session=None,
    ) -> int:
        """Creates a new `OversightInfo` record in an IODI manner.

        Args:
            has_dmc (bool): Whether the study has DMC.
            is_fda_regulated_drug (bool): Whether the study involves an FDA
                regulated drug.
            is_fda_regulated_device (bool): Whether the study involves an FDA
                regulated device.
            is_unapproved_device (bool): Whether the study involves an
                unapproved device.
            is_ppsd (bool): Whether the study is PPSD.
            is_us_export (bool): Whether the study involves a US export.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `OversightInfo` record.
        """

        statement = insert(
            OversightInfo,
            values={
                "has_dmc": has_dmc,
                "is_fda_regulated_drug": is_fda_regulated_drug,
                "is_fda_regulated_device": is_fda_regulated_device,
                "is_unapproved_device": is_unapproved_device,
                "is_ppsd": is_ppsd,
                "is_us_export": is_us_export,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

    @return_first_item
    @with_session_scope()
    def iodi_expanded_access_info(
        self,
        expanded_access_type_individual: bool,
        expanded_access_type_intermediate: bool,
        expanded_access_type_treatment: bool,
        session: sqlalchemy.orm.Session=None,
    ) -> int:
        """Creates a new `ExpandedAccessInfo` record in an IODI manner.

        Args:
            expanded_access_type_individual (bool): Whether the study has
                individual expanded access.
            expanded_access_type_intermediate (bool): Whether the study has
                intermediate expanded access.
            expanded_access_type_treatment (bool): Whether the study has
                treatment expanded access.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `ExpandedAccessInfo` record.
        """

        statement = insert(
            ExpandedAccessInfo,
            values={
                "individual": expanded_access_type_individual,
                "intermediate": expanded_access_type_intermediate,
                "treatment": expanded_access_type_treatment,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

    @return_first_item
    @with_session_scope()
    def iodi_study_design_info(
        self,
        allocation: str,
        intervention_model: str,
        intervention_model_description: str,
        primary_purpose: str,
        observational_model: str,
        time_perspective: str,
        masking: str,
        masking_description: str,
        session: sqlalchemy.orm.Session=None,
    ) -> int:
        """Creates a new `StudyDesignInfo` record in an IODI manner.

        Args:
            allocation (str): Study allocation.
            intervention_model (str): Study intervention model.
            intervention_model_description (str): Study intervention model
                description.
            primary_purpose (str): Study primary purpose.
            observational_model (str): Study observational model.
            time_perspective (str): Study time perspective.
            masking (str): Study masking.
            masking_description (str): Study masking description.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `StudyDesignInfo` record.
        """

        _dummy = intervention_model_description

        statement = insert(
            StudyDesignInfo,
            values={
                "allocation": allocation,
                "intervention_model": intervention_model,
                "intervention_model_description": _dummy,
                "primary_purpose": primary_purpose,
                "observational_model": observational_model,
                "time_perspective": time_perspective,
                "masking": masking,
                "masking_description": masking_description,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

    @return_first_item
    @with_session_scope()
    def iodi_protocol_outcome(
        self,
        measure: str,
        time_frame: str,
        description: str,
        session: sqlalchemy.orm.Session=None,
    ) -> int:
        """Creates a new `ProtocolOutcome` record in an IODI manner.

        Args:
            measure (str): Protocol outcome measure.
            time_frame (str): Protocol outcome time-frame.
            description (str): Protocol description.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `ProtocolOutcome` record.
        """

        statement = insert(
            ProtocolOutcome,
            values={
                "measure": measure,
                "time_frame": time_frame,
                "description": description,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

    @return_first_item
    @with_session_scope()
    def iodi_group(
        self,
        identifier: str,
        title: str,
        description: str,
        session: sqlalchemy.orm.Session=None,
    ) -> int:
        """Creates a new `Group` record in an IODI manner.

        Args:
            identifier (str): Group identifier.
            title (str): Group title.
            description (str): Protocol description.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Group` record.
        """

        statement = insert(
            Group,
            values={
                "identifier": identifier,
                "title": title,
                "description": description,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

    @return_first_item
    @with_session_scope()
    def iodi_analysis(
        self,
        groups_desc: str,
        non_inferiority_type: NonInferiorityType,
        non_inferiority_desc: str,
        p_value: str,
        p_value_desc: str,
        method: str,
        method_desc: str,
        param_type: str,
        param_value: str,
        dispersion_type: AnalysisDispersionType,
        dispersion_value: str,
        ci_percent: float,
        ci_n_sides: NumSidesType,
        ci_lower_limit: str,
        ci_upper_limit: str,
        ci_upper_limit_na_comment: str,
        estimate_desc: str,
        other_analysis_desc: str,
        session: sqlalchemy.orm.Session=None,
    ) -> int:
        """Creates a new `Analysis` record in an IODI manner.

        Args:
            groups_desc (str): Analysis groups description.
            non_inferiority_type (NonInferiorityType): Analysis non-inferiority
                type.
            non_inferiority_desc (str): Analysis non-inferiority description.
            p_value (str): Analysis p-value.
            p_value_desc (str): Analysis p-value description.
            method (str): Analysis method.
            method_desc (str): Analysis method description.
            param_type (str): Analysis parameter-type.
            param_value (str): Analysis parameter-value.
            dispersion_type (AnalysisDispersionType): Analysis dispersion type.
            dispersion_value (str): Analysis dispersion value.
            ci_percent (float): Analysis confidence-interval percentage.
            ci_n_sides (NumSidesType): Analysis confidence-interval side-number.
            ci_lower_limit (str): Analysis confidence-interval lower limit.
            ci_upper_limit (str): Analysis confidence-interval upper limit.
            ci_upper_limit_na_comment (str): Analysis confidence-interval limit
                non-applicable comment.
            estimate_desc (str): Analysis estimate description.
            other_analysis_desc (str): Analysis other description.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Analysis` record.
        """

        statement = insert(
            Analysis,
            values={
                "groups_desc": groups_desc,
                "non_inferiority_type": non_inferiority_type,
                "non_inferiority_desc": non_inferiority_desc,
                "p_value": p_value,
                "p_value_desc": p_value_desc,
                "method": method,
                "method_desc": method_desc,
                "param_type": param_type,
                "param_value": param_value,
                "dispersion_type": dispersion_type,
                "dispersion_value": dispersion_value,
                "ci_percent": ci_percent,
                "ci_n_sides": ci_n_sides,
                "ci_lower_limit": ci_lower_limit,
                "ci_upper_limit": ci_upper_limit,
                "ci_upper_limit_na_comment": ci_upper_limit_na_comment,
                "estimate_desc": estimate_desc,
                "other_analysis_desc": other_analysis_desc,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

    @return_first_item
    @with_session_scope()
    def iodi_analysis_group(
        self,
        analysis_id: int,
        group_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `AnalysisGroup` record in an IODI manner.

        Args:
            analysis_id (int): The linked `Analysis` record primary-key ID.
            group_id (int): The linked `Group` record primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `AnalysisGroup` record.
        """

        statement = insert(
            AnalysisGroup,
            values={
                "analysis_id": analysis_id,
                "group_id": group_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=AnalysisGroup,
                attrs_names_values={
                    "analysis_id": analysis_id,
                    "group_id": group_id,
                },
                session=session,
            )  # type: AnalysisGroup
            return obj.analysis_group_id

    @return_first_item
    @with_session_scope()
    def iodi_measure_count(
        self,
        group_id: int,
        value: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `MeasureCount` record in an IODI manner.

        Args:
            group_id (int): The linked `Group` record primary-key ID.
            value (str): The measure-count value.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `MeasureCount` record.
        """

        statement = insert(
            MeasureCount,
            values={
                "group_id": group_id,
                "value": value,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

    @return_first_item
    @with_session_scope()
    def iodi_measure_analyzed(
        self,
        units: str,
        scope: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `MeasureAnalyzed` record in an IODI manner.

        Args:
            units (int): The measure-analyzed units.
            scope (str): The measure-analyzed scope.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `MeasureAnalyzed` record.
        """

        statement = insert(
            MeasureAnalyzed,
            values={
                "units": units,
                "scope": scope,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

    @return_first_item
    @with_session_scope()
    def iodi_measure_analyzed_count(
        self,
        measure_analyzed_id: int,
        measure_count_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `MeasureAnalyzedCount` record in an IODI manner.

        Args:
            measure_analyzed_id (int): The linked `MeasureAnalyzed` record
                primary-key ID.
            measure_count_id (int): The linked `MeasureCount` record
                primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `MeasureAnalyzedCount` record.
        """

        statement = insert(
            MeasureAnalyzedCount,
            values={
                "measure_analyzed_id": measure_analyzed_id,
                "measure_count_id": measure_count_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

    @return_first_item
    @with_session_scope()
    def iodi_measurement(
        self,
        group_id: int,
        value: str,
        spread: str,
        lower_limit: str,
        upper_limit: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `Measurement` record in an IODI manner.

        Args:
            group_id (int): The linked `Group` record primary-key ID.
            value (str): The measurement value.
            spread (str): The measurement spread.
            lower_limit (str): The measurement lower-limit.
            upper_limit (str): The measurement upper-limit.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Measurement` record.
        """

        statement = insert(
            Measurement,
            values={
                "group_id": group_id,
                "value": value,
                "spread": spread,
                "lower_limit": lower_limit,
                "upper_limit": upper_limit,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

    @return_first_item
    @with_session_scope()
    def iodi_result_outcome(
        self,
        outcome_type: OutcomeType,
        title: str,
        description: str,
        time_frame: str,
        safety_issue: bool,
        population: str,
        measure_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `ResultOutcome` record in an IODI manner.

        Args:
            outcome_type (int): The result-outcome type.
            title (str): The result-outcome title.
            description (str): The result-outcome description.
            time_frame (str): The result-outcome time-frame.
            safety_issue (str): The result-outcome safety-issue.
            population (str): The result-outcome population.
            measure_id (int): The linked `Measure` record primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `ResultOutcome` record.
        """

        statement = insert(
            ResultOutcome,
            values={
                "outcome_type": outcome_type,
                "title": title,
                "description": description,
                "time_frame": time_frame,
                "safety_issue": safety_issue,
                "population": population,
                "measure_id": measure_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

    @return_first_item
    @with_session_scope()
    def iodi_result_outcome_group(
        self,
        result_outcome_id: int,
        group_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `ResultOutcomeGroup` record in an IODI manner.

        Args:
            result_outcome_id (int): The linked `ResultOutcome` record
                primary-key ID.
            group_id (int): The linked `Group` record primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `ResultOutcomeGroup` record.
        """

        statement = insert(
            ResultOutcomeGroup,
            values={
                "result_outcome_id": result_outcome_id,
                "group_id": group_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

    @return_first_item
    @with_session_scope()
    def iodi_enrollment(
        self,
        value: str,
        enrollment_type: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `Enrollment` record in an IODI manner.

        Args:
            value (str): The enrollment value.
            enrollment_type (ActualType): The enrollment type.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Enrollment` record.
        """

        statement = insert(
            Enrollment,
            values={
                "value": value,
                "type": enrollment_type,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

    @return_first_item
    @with_session_scope()
    def iodi_arm_group(
        self,
        label: str,
        arm_group_type: str,
        description: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `ArmGroup` record in an IODI manner.

        Args:
            label (str): The arm-group label.
            arm_group_type (str): The arm-group type.
            description (str): The arm-group description.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `ArmGroup` record.
        """

        statement = insert(
            ArmGroup,
            values={
                "label": label,
                "type": arm_group_type,
                "description": description,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

    @return_first_item
    @with_session_scope()
    def iodi_intervention(
        self,
        intervention_type: InterventionType,
        name: str,
        description: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `Intervention` record in an IODI manner.

        Args:
            intervention_type (InterventionType): The intervention type.
            name (str): The intervention name.
            description (str): The intervention description.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Intervention` record.
        """

        statement = insert(
            Intervention,
            values={
                "type": intervention_type,
                "name": name,
                "description": description,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

    @return_first_item
    @with_session_scope()
    def iodi_alias(
        self,
        alias: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `Alias` record in an IODI manner.

        Args:
            alias (str): The alias.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Alias` record.
        """

        # Create and populate a `Alias` object so that we can retrieve
        # the MD5 hash.
        alias_obj = Alias()
        alias_obj.alias = alias

        statement = insert(
            Alias,
            values={
                "alias": alias,
                "md5": alias_obj.md5,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_md5(
                orm_class=Alias,
                md5=alias_obj.md5,
                session=session,
            )  # type: Alias
            return obj.alias_id

    @return_first_item
    @with_session_scope()
    def iodi_intervention_alias(
        self,
        intervention_id: int,
        alias_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `InterventionAlias` record in an IODI manner.

        Args:
            intervention_id (int): The linked `Intervention` record
                primary-key ID.
            alias_id (int): The linked `Alias` record primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `InterventionAlias` record.
        """

        statement = insert(
            InterventionAlias,
            values={
                "intervention_id": intervention_id,
                "alias_id": alias_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=InterventionAlias,
                attrs_names_values={
                    "intervention_id": intervention_id,
                    "alias_id": alias_id,
                },
                session=session,
            )  # type: InterventionAlias
            return obj.intervention_alias_id

    @return_first_item
    @with_session_scope()
    def iodi_intervention_arm_group(
        self,
        intervention_id: int,
        arm_group_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `InterventionArmGroup` record in an IODI manner.

        Args:
            intervention_id (int): The linked `Intervention` record
                primary-key ID.
            arm_group_id (int): The linked `ArmGroup` record primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `InterventionArmGroup` record.
        """

        statement = insert(
            InterventionArmGroup,
            values={
                "intervention_id": intervention_id,
                "arm_group_id": arm_group_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=InterventionArmGroup,
                attrs_names_values={
                    "intervention_id": intervention_id,
                    "arm_group_id": arm_group_id,
                },
                session=session,
            )  # type: InterventionArmGroup
            return obj.intervention_arm_group_id

    @return_first_item
    @with_session_scope()
    def iodi_eligibility(
        self,
        study_pop: str,
        sampling_method: SamplingMethodType,
        criteria: str,
        gender: GenderType,
        gender_based: bool,
        gender_description: str,
        minimum_age: str,
        maximum_age: str,
        healthy_volunteers: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `Eligibility` record in an IODI manner.

        Args:
            study_pop (str): The eligibility study population.
            sampling_method (SamplingMethodType): The eligibility sampling
                method type.
            criteria (str): The eligibility study population.
            gender (GenderType): The eligibility gender-type.
            gender_based (bool): Whether the study is gender-based.
            gender_description (str): The eligibility gender description.
            minimum_age (str): The eligibility minimum-age.
            maximum_age (str): The eligibility maximum-age.
            healthy_volunteers (str): The description of healthy volunteers in
                the study.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Eligibility` record.
        """

        statement = insert(
            Eligibility,
            values={
                "study_pop": study_pop,
                "sampling_method": sampling_method,
                "criteria": criteria,
                "gender": gender,
                "gender_based": gender_based,
                "gender_description": gender_description,
                "minimum_age": minimum_age,
                "maximum_age": maximum_age,
                "healthy_volunteers": healthy_volunteers,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

    @return_first_item
    @with_session_scope()
    def iodi_reference(
        self,
        citation: str,
        pmid: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `Reference` record in an IODI manner.

        Args:
            citation (str): The citation.
            pmid (int): The reference PMID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Reference` record.
        """

        statement = insert(
            Reference,
            values={
                "citation": citation,
                "pmid": pmid,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=Reference,
                attrs_names_values={
                    "pmid": pmid,
                },
                session=session,
            )  # type: Reference
            return obj.reference_id

    @return_first_item
    @with_session_scope()
    def iodi_responsible_party(
        self,
        name_title: str,
        organization: str,
        responsible_party_type: ResponsiblePartyType,
        investigator_affiliation: str,
        investigator_full_name: str,
        investigator_title: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `ResponsibleParty` record in an IODI manner.

        Args:
            name_title (str): The name/title of the responsible party.
            organization (str): The organization of the responsible party.
            responsible_party_type (ResponsiblePartyType): The type of the
                responsible party.
            investigator_affiliation (str): The investigator affiliation of the
                responsible party.
            investigator_full_name (str): The investigator full name of the
                responsible party.
            investigator_title (str): The investigator title of the
                responsible party.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `ResponsibleParty` record.
        """

        statement = insert(
            ResponsibleParty,
            values={
                "name_title": name_title,
                "organization": organization,
                "type": responsible_party_type,
                "investigator_affiliation": investigator_affiliation,
                "investigator_full_name": investigator_full_name,
                "investigator_title": investigator_title,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

    @return_first_item
    @with_session_scope()
    def iodi_mesh_term(
        self,
        term: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `MeshTerm` record in an IODI manner.

        Args:
            term (str): The MeSH term.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `MeshTerm` record.
        """

        # Create and populate a `MeshTerm` object so that we can retrieve the
        # MD5 hash.
        mesh_term_obj = MeshTerm()
        mesh_term_obj.term = term

        statement = insert(
            MeshTerm,
            values={
                "term": term,
                "md5": mesh_term_obj.md5,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_md5(
                orm_class=MeshTerm,
                md5=mesh_term_obj.md5,
                session=session,
            )  # type: MeshTerm
            return obj.mesh_term_id

    @return_first_item
    @with_session_scope()
    def iodi_patient_data(
        self,
        sharing_ipd: str,
        ipd_description: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `PatientData` record in an IODI manner.

        Args:
            sharing_ipd (str): The sharing IPD.
            ipd_description (str): The IPD description.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `PatientData` record.
        """

        statement = insert(
            PatientData,
            values={
                "sharing_ipd": sharing_ipd,
                "ipd_description": ipd_description,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

    @return_first_item
    @with_session_scope()
    def iodi_study_doc(
        self,
        doc_id: str,
        doc_type: str,
        doc_url: str,
        doc_comment: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `StudyDoc` record in an IODI manner.

        Args:
            doc_id (str): The study-doc ID.
            doc_type (str): The study-doc type.
            doc_url (str): The study-doc URL.
            doc_comment (str): The study-doc comment.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `StudyDoc` record.
        """

        statement = insert(
            StudyDoc,
            values={
                "doc_id": doc_id,
                "doc_type": doc_type,
                "doc_url": doc_url,
                "doc_comment": doc_comment,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

    @return_first_item
    @with_session_scope()
    def iodi_study_dates(
        self,
        study_first_submitted: datetime.date,
        study_first_submitted_qc: datetime.date,
        study_first_posted: datetime.date,
        results_first_submitted: datetime.date,
        results_first_submitted_qc: datetime.date,
        results_first_posted: datetime.date,
        disposition_first_submitted: datetime.date,
        disposition_first_submitted_qc: datetime.date,
        disposition_first_posted: datetime.date,
        last_update_submitted: datetime.date,
        last_update_submitted_qc: datetime.date,
        last_update_posted: datetime.date,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `StudyDates` record in an IODI manner.

        Args:
            study_first_submitted (datetime.date): The date the study was
                submitted.
            study_first_submitted_qc (datetime.date): The date the study was
                submitted for quality-control.
            study_first_posted (datetime.date): The date the study was
                first-posted.
            results_first_submitted (datetime.date): The date the results were
                first-submitted.
            results_first_submitted_qc (datetime.date): The date the results
                were submitted for quality-control.
            results_first_posted (datetime.date): The date the results were
                first-posted.
            disposition_first_submitted (datetime.date): The date the
                disposition was first-submitted.
            disposition_first_submitted_qc (datetime.date): The date the
                disposition was first-submitted for quality-control.
            disposition_first_posted (datetime.date): The date the
                disposition was first-posted.
            last_update_submitted (datetime.date): The date the latest update
                was submitted.
            last_update_submitted_qc (datetime.date): The date the latest update
                was submitted for quality-control.
            last_update_posted (datetime.date): The date the latest update
                was posted.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `StudyDates` record.
        """

        _dummy = disposition_first_submitted_qc

        statement = insert(
            StudyDates,
            values={
                "study_first_submitted": study_first_submitted,
                "study_first_submitted_qc": study_first_submitted_qc,
                "study_first_posted": study_first_posted,
                "results_first_submitted": results_first_submitted,
                "results_first_submitted_qc": results_first_submitted_qc,
                "results_first_posted": results_first_posted,
                "disposition_first_submitted": disposition_first_submitted,
                "disposition_first_submitted_qc": _dummy,
                "disposition_first_posted": disposition_first_posted,
                "last_update_submitted": last_update_submitted,
                "last_update_submitted_qc": last_update_submitted_qc,
                "last_update_posted": last_update_posted,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

    @return_first_item
    @with_session_scope()
    def iodi_study(
        self,
        org_study_id: str,
        secondary_id: str,
        nct_id: str,
        brief_title: str,
        acronym: str,
        official_title: str,
        source: str,
        oversight_info_id: int,
        brief_summary: str,
        detailed_description: str,
        overall_status:  OverallStatusType,
        last_known_status: OverallStatusType,
        why_stopped: str,
        start_date: datetime.date,
        completion_date: datetime.date,
        primary_completion_date: datetime.date,
        verification_date: datetime.date,
        phase: PhaseType,
        study_type: StudyType,
        expanded_access_info_id: int,
        study_design_info_id: int,
        target_duration: str,
        enrollment_id: int,
        biospec_retention: BiospecRetentionType,
        biospec_description: str,
        eligibility_id: int,
        contact_primary_id: int,
        contact_backup_id: int,
        study_dates_id: int,
        responsible_party_id: int,
        patient_data_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `Study` record in an IODI manner.

        Args:
            org_study_id (str): The organizational study ID.
            secondary_id (str): A secondary study ID.
            nct_id (str): The NCT study ID.
            brief_title (str): A brief study title.
            acronym (str): The study acronym.
            official_title (str): The official study title.
            source (str): The study source.
            oversight_info_id (int): The linked `OversightInfo` record
                primary-key ID.
            brief_summary (str): The brief study summary.
            detailed_description (str): The detailed summary description.
            overall_status: (OverallStatusType): The study overall status.
            last_known_status (OverallStatusType): THe study last-known status.
            why_stopped (str): Why the study was stopped (if applicable).
            start_date: (datetime.date): The date the study will start.
            completion_date: (datetime.date): The date the study will be
                completed.
            primary_completion_date: (datetime.date): The date of the study
                primary-completion.
            verification_date: (datetime.date): The date the study will be
                verified.
            phase (PhaseType): The study phase.
            study_type (StudyType): The study type.
            expanded_access_info_id (int): The linked `ExpandedAccessInfo`
                record primary-key ID.
            study_design_info_id (int): The linked `StudyDesignInfo` record
                primary-key ID.
            target_duration (str): The study target duration.
            enrollment_id (int): The linked `Enrollment` record primary-key ID.
            biospec_retention (BiospecRetentionType): The study
                biospec-retention type.
            biospec_description (str): The study biospec description.
            eligibility_id (int): The linked `Eligibility` record
                primary-key ID.
            contact_primary_id (int): The linked `Contact` record
                primary-key ID for the study's primary contact.
            contact_backup_id (int): The linked `Contact` record
                primary-key ID for the study's backup contact.
            study_dates_id (int): The linked `StudyDates` record
                primary-key ID.
            responsible_party_id (int): The linked `ResponsibleParty` record
                primary-key ID.
            patient_data_id (int): The linked `Patientdata` record
                primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Study` record.
        """

        statement = insert(
            Study,
            values={
                "org_study_id": org_study_id,
                "secondary_id": secondary_id,
                "nct_id": nct_id,
                "brief_title": brief_title,
                "acronym": acronym,
                "official_title": official_title,
                "source": source,
                "oversight_info_id": oversight_info_id,
                "brief_summary": brief_summary,
                "detailed_description": detailed_description,
                "overall_status": overall_status,
                "last_known_status": last_known_status,
                "why_stopped": why_stopped,
                "start_date": start_date,
                "completion_date": completion_date,
                "primary_completion_date": primary_completion_date,
                "verification_date": verification_date,
                "phase": phase,
                "study_type": study_type,
                "expanded_access_info_id": expanded_access_info_id,
                "study_design_info_id": study_design_info_id,
                "target_duration": target_duration,
                "enrollment_id": enrollment_id,
                "biospec_retention": biospec_retention,
                "biospec_description": biospec_description,
                "eligibility_id": eligibility_id,
                "contact_primary_id": contact_primary_id,
                "contact_backup_id": contact_backup_id,
                "study_dates_id": study_dates_id,
                "responsible_party_id": responsible_party_id,
                "patient_data_id": patient_data_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=Study,
                attrs_names_values={
                    "nct_id": nct_id,
                },
                session=session,
            )  # type: Study
            return obj.study_id

    @return_first_item
    @with_session_scope()
    def iodi_study_alias(
        self,
        study_id: int,
        alias_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `StudyAlias` record in an IODI manner.

        Args:
            study_id (int): The linked `Study` record primary-key ID.
            alias_id (int): The linked `Alias` record primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `StudyAlias` record.
        """

        statement = insert(
            StudyAlias,
            values={
                "study_id": study_id,
                "alias_id": alias_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=StudyAlias,
                attrs_names_values={
                    "study_id": study_id,
                    "alias_id": alias_id,
                },
                session=session,
            )  # type: StudyAlias
            return obj.study_alias_id

    @return_first_item
    @with_session_scope()
    def iodi_study_sponsor(
        self,
        study_id: int,
        sponsor_id: int,
        sponsor_type: SponsorType,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `StudySponsor` record in an IODI manner.

        Args:
            study_id (int): The linked `Study` record primary-key ID.
            sponsor_id (int): The linked `Sponsor` record primary-key ID.
            sponsor_type (SponsorType): An enumeration member denoting the
                sponsor type.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `StudySponsor` record.
        """

        statement = insert(
            StudySponsor,
            values={
                "study_id": study_id,
                "sponsor_id": sponsor_id,
                "type": sponsor_type,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=StudySponsor,
                attrs_names_values={
                    "study_id": study_id,
                    "sponsor_id": sponsor_id,
                },
                session=session,
            )  # type: StudySponsor
            return obj.study_sponsor_id

    @return_first_item
    @with_session_scope()
    def iodi_study_outcome(
        self,
        study_id: int,
        protocol_outcome_id: int,
        outcome_type: OutcomeType,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `StudyOutcome` record in an IODI manner.

        Args:
            study_id (int): The linked `Study` record primary-key ID.
            protocol_outcome_id (int): The linked `Outcome` record primary-key
                ID.
            outcome_type (OutcomeType): The linked `Outcome` type.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `StudyOutcome` record.
        """

        statement = insert(
            StudyOutcome,
            values={
                "study_id": study_id,
                "protocol_outcome_id": protocol_outcome_id,
                "type": outcome_type,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=StudyOutcome,
                attrs_names_values={
                    "study_id": study_id,
                    "protocol_outcome_id": protocol_outcome_id,
                },
                session=session,
            )  # type: StudyOutcome
            return obj.study_primary_outcome_id

    @return_first_item
    @with_session_scope()
    def iodi_study_condition(
        self,
        study_id: int,
        condition_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `StudyCondition` record in an IODI manner.

        Args:
            study_id (int): The linked `Study` record primary-key ID.
            condition_id (int): The linked `Condition` record primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `StudyCondition` record.
        """

        statement = insert(
            StudyCondition,
            values={
                "study_id": study_id,
                "condition_id": condition_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=StudyCondition,
                attrs_names_values={
                    "study_id": study_id,
                    "condition_id": condition_id,
                },
                session=session,
            )  # type: StudyCondition
            return obj.study_condition_id

    @return_first_item
    @with_session_scope()
    def iodi_study_arm_group(
        self,
        study_id: int,
        arm_group_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `StudyArmGroup` record in an IODI manner.

        Args:
            study_id (int): The linked `Study` record primary-key ID.
            arm_group_id (int): The linked `ArmGroup` record primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `StudyArmGroup` record.
        """

        statement = insert(
            StudyArmGroup,
            values={
                "study_id": study_id,
                "arm_group_id": arm_group_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=StudyArmGroup,
                attrs_names_values={
                    "study_id": study_id,
                    "arm_group_id": arm_group_id,
                },
                session=session,
            )  # type: StudyArmGroup
            return obj.study_arm_group_id

    @return_first_item
    @with_session_scope()
    def iodi_study_intervention(
        self,
        study_id: int,
        intervention_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `StudyIntervention` record in an IODI manner.

        Args:
            study_id (int): The linked `Study` record primary-key ID.
            intervention_id (int): The linked `Intervention` record primary-key
                ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `StudyIntervention` record.
        """

        statement = insert(
            StudyIntervention,
            values={
                "study_id": study_id,
                "intervention_id": intervention_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=StudyIntervention,
                attrs_names_values={
                    "study_id": study_id,
                    "intervention_id": intervention_id,
                },
                session=session,
            )  # type: StudyIntervention
            return obj.study_intervention_id

    @return_first_item
    @with_session_scope()
    def iodi_study_investigator(
        self,
        study_id: int,
        investigator_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `StudyInvestigator` record in an IODI manner.

        Args:
            study_id (int): The linked `Study` record primary-key ID.
            investigator_id (int): The linked `Investigator` record primary-key
                ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `StudyInvestigator` record.
        """

        statement = insert(
            StudyInvestigator,
            values={
                "study_id": study_id,
                "investigator_id": investigator_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=StudyInvestigator,
                attrs_names_values={
                    "study_id": study_id,
                    "investigator_id": investigator_id,
                },
                session=session,
            )  # type: StudyInvestigator
            return obj.study_investigator_id

    @return_first_item
    @with_session_scope()
    def iodi_study_location(
        self,
        study_id: int,
        location_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `StudyLocation` record in an IODI manner.

        Args:
            study_id (int): The linked `Study` record primary-key ID.
            location_id (int): The linked `Location` record primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `StudyLocation` record.
        """

        statement = insert(
            StudyLocation,
            values={
                "study_id": study_id,
                "location_id": location_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=StudyLocation,
                attrs_names_values={
                    "study_id": study_id,
                    "location_id": location_id,
                },
                session=session,
            )  # type: StudyLocation
            return obj.study_location_id

    @return_first_item
    @with_session_scope()
    def iodi_study_reference(
        self,
        study_id: int,
        reference_id: int,
        reference_type: ReferenceType,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `StudyReference` record in an IODI manner.

        Args:
            study_id (int): The linked `Study` record primary-key ID.
            reference_id (int): The linked `Reference` record primary-key ID.
            reference_type (ReferenceType): The reference type.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `StudyReference` record.
        """

        statement = insert(
            StudyReference,
            values={
                "study_id": study_id,
                "reference_id": reference_id,
                "type": reference_type,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=StudyReference,
                attrs_names_values={
                    "study_id": study_id,
                    "reference_id": reference_id,
                },
                session=session,
            )  # type: StudyReference
            return obj.study_reference_id

    @return_first_item
    @with_session_scope()
    def iodi_study_keyword(
        self,
        study_id: int,
        keyword_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `StudyKeyword` record in an IODI manner.

        Args:
            study_id (int): The linked `Study` record primary-key ID.
            keyword_id (int): The linked `Keyword` record primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `StudyKeyword` record.
        """

        statement = insert(
            StudyKeyword,
            values={
                "study_id": study_id,
                "keyword_id": keyword_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=StudyKeyword,
                attrs_names_values={
                    "study_id": study_id,
                    "keyword_id": keyword_id,
                },
                session=session,
            )  # type: StudyKeyword
            return obj.study_keyword_id

    @return_first_item
    @with_session_scope()
    def iodi_study_mesh_term(
        self,
        study_id: int,
        mesh_term_id: int,
        mesh_term_type: MeshTermType,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `StudyMeshTerm` record in an IODI manner.

        Args:
            study_id (int): The linked `Study` record primary-key ID.
            mesh_term_id (int): The linked `MeshTerm` record primary-key ID.
            mesh_term_type (MeshTermType): The mesh-term type.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `StudyMeshTerm` record.
        """

        statement = insert(
            StudyMeshTerm,
            values={
                "study_id": study_id,
                "mesh_term_id": mesh_term_id,
                "type": mesh_term_type,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=StudyMeshTerm,
                attrs_names_values={
                    "study_id": study_id,
                    "mesh_term_id": mesh_term_id,
                },
                session=session,
            )  # type: StudyMeshTerm
            return obj.study_mesh_term_id

    @return_first_item
    @with_session_scope()
    def iodi_study_study_doc(
        self,
        study_id: int,
        study_doc_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `StudyStudyDoc` record in an IODI manner.

        Args:
            study_id (int): The linked `Study` record primary-key ID.
            study_doc_id (int): The linked `StudyDoc` record primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `StudyStudyDoc` record.
        """

        statement = insert(
            StudyStudyDoc,
            values={
                "study_id": study_id,
                "study_doc_id": study_doc_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=StudyStudyDoc,
                attrs_names_values={
                    "study_id": study_id,
                    "study_doc_id": study_doc_id,
                },
                session=session,
            )  # type: StudyStudyDoc
            return obj.study_study_doc_id
