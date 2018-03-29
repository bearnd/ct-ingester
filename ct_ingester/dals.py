# -*- coding: utf-8 -*-

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
from ct_ingester.orm import Participant
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
    def iodi_sponsor(
        self,
        agency: str,
        agency_class: AgencyClassType,
        sponsor_type: SponsorType,
        session: sqlalchemy.orm.Session=None,
    ) -> int:
        """Creates a new `Sponsor` record in an IODI manner.

        Args:
            agency (str): The sponsor agency.
            agency_class (AgencyClassType): An enumeration member denoting the
                sponsor agency class.
            sponsor_type (SponsorType): An enumeration member denoting the
                sponsor type.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Sponsor` record.
        """

        statement = insert(
            Sponsor,
            values={
                "agency": agency,
                "class": agency_class,
                "type": sponsor_type,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

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

        statement = insert(
            Keyword,
            values={
                "keyword": keyword,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

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

        statement = insert(
            Condition,
            values={
                "condition": condition,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

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

        statement = insert(
            Facility,
            values={
                "name": name,
                "city": city,
                "state": state,
                "zip_code": zip_code,
                "country": country,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

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

        statement = insert(
            Person,
            values={
                "name_first": name_first,
                "name_middle": name_middle,
                "name_last": name_last,
                "degrees": degrees,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

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

        statement = insert(
            Contact,
            values={
                "person_id": person_id,
                "phone": phone,
                "phone_ext": phone_ext,
                "email": email,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

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

        statement = insert(
            Investigator,
            values={
                "person_id": person_id,
                "role": role,
                "affiliation": affiliation,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

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

        return result.inserted_primary_key

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

        return result.inserted_primary_key

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

        return result.inserted_primary_key

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

        statement = insert(
            Alias,
            values={
                "alias": alias,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

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

        return result.inserted_primary_key

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
            InterventionAlias,
            values={
                "intervention_id": intervention_id,
                "arm_group_id": arm_group_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

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

        return result.inserted_primary_key

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

        statement = insert(
            MeshTerm,
            values={
                "term": term,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key

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

    @with_session_scope()
    def iodi_participant(
        self,
        group_id: int,
        count: int,
        doc_url: str,
        doc_comment: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `Participant` record in an IODI manner.

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
            int: The primary key ID of the `Participant` record.
        """

        statement = insert(
            Participant,
            values={
                "doc_id": doc_id,
                "doc_type": doc_type,
                "doc_url": doc_url,
                "doc_comment": doc_comment,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        return result.inserted_primary_key
