# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import hashlib

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.types

from ct_ingester.orm_base import Base, OrmBase
from ct_ingester.orm_enums import AgencyClassType
from ct_ingester.orm_enums import SponsorType
from ct_ingester.orm_enums import RecruitmentStatusType
from ct_ingester.orm_enums import RoleType
from ct_ingester.orm_enums import NonInferiorityType
from ct_ingester.orm_enums import AnalysisDispersionType
from ct_ingester.orm_enums import NumSidesType
from ct_ingester.orm_enums import OutcomeType
from ct_ingester.orm_enums import MeasureParameterType
from ct_ingester.orm_enums import ActualType
from ct_ingester.orm_enums import InterventionType
from ct_ingester.orm_enums import SamplingMethodType
from ct_ingester.orm_enums import GenderType
from ct_ingester.orm_enums import ResponsiblePartyType
from ct_ingester.orm_enums import EventAssessmentType
from ct_ingester.orm_enums import OverallStatusType
from ct_ingester.orm_enums import PhaseType
from ct_ingester.orm_enums import StudyType
from ct_ingester.orm_enums import BiospecRetentionType
from ct_ingester.orm_enums import ReferenceType
from ct_ingester.orm_enums import MeshTermType


class Sponsor(Base, OrmBase):
    """Table of `<sponsor>` element record."""

    # set table name
    __tablename__ = "sponsors"

    # Autoincrementing primary key ID.
    sponsor_id = sqlalchemy.Column(
        name="sponsor_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Agency (value of the `<agency>` element).
    agency = sqlalchemy.Column(
        name="agency",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # Agency class (value of the `<agency_class>` element).
    agency_class = sqlalchemy.Column(
        name="class",
        type_=sqlalchemy.types.Enum(AgencyClassType),
        nullable=False,
        default=None,
        index=True
    )

    # MD5 hash of the keyword.
    md5 = sqlalchemy.Column(
        name="md5",
        type_=sqlalchemy.types.Binary(),
        unique=True,
        index=True,
        nullable=False,
    )

    # Relationship to a list of `Study` records.
    studies = sqlalchemy.orm.relationship(
        argument="Study",
        secondary="study_sponsors",
        back_populates="sponsors"
    )

    @sqlalchemy.orm.validates(
        "agency",
        "agency_class",
    )
    def update_md5(self, key, value):
        attrs = {
            "agency": self.agency,
            "agency_class": self.agency_class,
        }
        attrs[key] = value

        # Retrieve the full concatenated name.
        name = " ".join([str(value) for value in attrs.values()])

        # Encode the full concatenated name to UTF8 (in case it contains
        # unicode characters).
        name_encoded = name.encode("utf-8")

        # Calculate the MD5 hash of the encoded full concatenated name and store
        # it under the `md5` attribute.
        md5 = hashlib.md5(name_encoded).digest()
        self.md5 = md5

        return value


class Keyword(Base, OrmBase):
    """Table of `<keyword>` element records."""

    # set table name
    __tablename__ = "keywords"

    # Autoincrementing primary key ID.
    keyword_id = sqlalchemy.Column(
        name="keyword_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Keyword name (value of the `<keyword>` element).
    keyword = sqlalchemy.Column(
        name="keyword",
        type_=sqlalchemy.types.Unicode(),
        unique=True,
        nullable=False,
        index=True,
    )

    # MD5 hash of the keyword.
    md5 = sqlalchemy.Column(
        name="md5",
        type_=sqlalchemy.types.Binary(),
        unique=True,
        index=True,
        nullable=False,
    )

    # Relationship to a list of `Study` records.
    studies = sqlalchemy.orm.relationship(
        argument="Study",
        secondary="study_keywords",
        back_populates="keywords"
    )

    @sqlalchemy.orm.validates("keyword")
    def update_md5(self, key, value):
        # Dumb hack to make the linter shut up that the `key` isn't used.
        assert key

        # Encode the keyword to UTF8 (in case it contains unicode characters).
        keyword_encoded = str(value).encode("utf-8")

        # Calculate the MD5 hash of the encoded keyword and store under the
        # `md5` attribute.
        md5 = hashlib.md5(keyword_encoded).digest()
        self.md5 = md5

        return value


class Condition(Base, OrmBase):
    """Table of `<condition>` element records."""

    # set table name
    __tablename__ = "conditions"

    # Autoincrementing primary key ID.
    condition_id = sqlalchemy.Column(
        name="condition_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Condition name (value of the `<condition>` element).
    condition = sqlalchemy.Column(
        name="condition",
        type_=sqlalchemy.types.Unicode(),
        unique=True,
        nullable=False,
        index=True,
    )

    # MD5 hash of the keyword.
    md5 = sqlalchemy.Column(
        name="md5",
        type_=sqlalchemy.types.Binary(),
        unique=True,
        index=True,
        nullable=False,
    )

    # Relationship to a list of `Study` records.
    studies = sqlalchemy.orm.relationship(
        argument="Study",
        secondary="study_conditions",
        back_populates="conditions"
    )

    @sqlalchemy.orm.validates("condition")
    def update_md5(self, key, value):
        # Dumb hack to make the linter shut up that the `key` isn't used.
        assert key

        # Encode the condition to UTF8 (in case it contains unicode characters).
        condition_encoded = str(value).encode("utf-8")

        # Calculate the MD5 hash of the encoded condition and store under the
        # `md5` attribute.
        md5 = hashlib.md5(condition_encoded).digest()
        self.md5 = md5

        return value


class Facility(Base, OrmBase):
    """Table of `<facility>` elements and their underlying `<address>` element
    records."""

    # set table name
    __tablename__ = "facilities"

    # Autoincrementing primary key ID.
    facility_id = sqlalchemy.Column(
        name="facility_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Facility name (referring to the `<name>` element).
    name = sqlalchemy.Column(
        name="name",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Facility city (referring to the `<city>` element under the `<address>`
    # element).
    city = sqlalchemy.Column(
        name="city",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # Facility state (referring to the `<city>` element under the `<address>`
    # element).
    state = sqlalchemy.Column(
        name="state",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Facility zip-code (referring to the `<zip>` element under the `<address>`
    # element).
    zip_code = sqlalchemy.Column(
        name="zip_code",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Facility country (referring to the `<country>` element under the
    # `<address>` element).
    country = sqlalchemy.Column(
        name="country",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # MD5 hash of the author's full name.
    md5 = sqlalchemy.Column(
        name="md5",
        type_=sqlalchemy.types.Binary(),
        unique=True,
        index=True,
        nullable=False
    )

    @sqlalchemy.orm.validates(
        "name",
        "city",
        "state",
        "zip_code",
        "country",
    )
    def update_md5(self, key, value):
        attrs = {
            "name": self.name,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "country": self.country,
        }
        attrs[key] = value

        # Retrieve the full concatenated name.
        name = " ".join([str(value) for value in attrs.values()])

        # Encode the full concatenated name to UTF8 (in case it contains
        # unicode characters).
        name_encoded = name.encode("utf-8")

        # Calculate the MD5 hash of the encoded full concatenated name and store
        # it under the `md5` attribute.
        md5 = hashlib.md5(name_encoded).digest()
        self.md5 = md5

        return value


class Person(Base, OrmBase):
    """Table of person records normalized out of `<contact>` and
    `<investigator> element records."""

    # set table name
    __tablename__ = "persons"

    # Autoincrementing primary key ID.
    person_id = sqlalchemy.Column(
        name="person_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Person first name (referring to the `<first_name>` element).
    name_first = sqlalchemy.Column(
        name="name_first",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Person middle name (referring to the `<middle_name>` element).
    name_middle = sqlalchemy.Column(
        name="name_middle",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Person last name (referring to the `<last_name>` element).
    name_last = sqlalchemy.Column(
        name="name_last",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Contact degrees (referring to the `<degrees>` element).
    degrees = sqlalchemy.Column(
        name="degrees",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # MD5 hash of the contact's full name.
    md5 = sqlalchemy.Column(
        name="md5",
        type_=sqlalchemy.types.Binary(),
        unique=True,
        index=True,
        nullable=False
    )

    @sqlalchemy.orm.validates(
        "name_first",
        "name_middle",
        "name_last",
        "degrees",
    )
    def update_md5(self, key, value):
        attrs = {
            "name_first": self.name_first,
            "name_middle": self.name_middle,
            "name_last": self.name_last,
            "degrees": self.degrees,
        }
        attrs[key] = value

        # Retrieve the full concatenated name.
        name = " ".join([str(value) for value in attrs.values()])

        # Encode the full concatenated name to UTF8 (in case it contains
        # unicode characters).
        name_encoded = name.encode("utf-8")

        # Calculate the MD5 hash of the encoded full concatenated name and store
        # it under the `md5` attribute.
        md5 = hashlib.md5(name_encoded).digest()
        self.md5 = md5

        return value


class Contact(Base, OrmBase):
    """Table of `<contact>` elements records."""

    # set table name
    __tablename__ = "contacts"

    # Autoincrementing primary key ID.
    contact_id = sqlalchemy.Column(
        name="contact_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the person ID.
    person_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("persons.person_id"),
        name="person_id",
        nullable=False,
    )

    # Contact phone number (referring to the `<phone>` element).
    phone = sqlalchemy.Column(
        name="phone",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Contact phone number extension (referring to the `<phone_ext>` element).
    phone_ext = sqlalchemy.Column(
        name="phone_ext",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Contact email (referring to the `<email>` element).
    email = sqlalchemy.Column(
        name="email",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # MD5 hash of the contact's full name.
    md5 = sqlalchemy.Column(
        name="md5",
        type_=sqlalchemy.types.Binary(),
        unique=True,
        index=True,
        nullable=False
    )

    # Relationship to a `Person` record.
    person = sqlalchemy.orm.relationship(
        argument="Person",
    )

    @sqlalchemy.orm.validates(
        "person_id",
        "phone",
        "phone_ext",
        "email",
    )
    def update_md5(self, key, value):
        attrs = {
            "person_id": self.person_id,
            "phone": self.phone,
            "phone_ext": self.phone_ext,
            "email": self.email,
        }
        attrs[key] = value

        # Retrieve the full concatenated name.
        name = " ".join([str(value) for value in attrs.values()])

        # Encode the full concatenated name to UTF8 (in case it contains
        # unicode characters).
        name_encoded = name.encode("utf-8")

        # Calculate the MD5 hash of the encoded full concatenated name and store
        # it under the `md5` attribute.
        md5 = hashlib.md5(name_encoded).digest()
        self.md5 = md5

        return value


class Investigator(Base, OrmBase):
    """Table of `<investigator>` elements records."""

    # set table name
    __tablename__ = "investigators"

    # Autoincrementing primary key ID.
    investigator_id = sqlalchemy.Column(
        name="investigator_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the person ID.
    person_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("persons.person_id"),
        name="person_id",
        nullable=False,
    )

    # Investigator role (referring to the `<role>` element).
    role = sqlalchemy.Column(
        name="role",
        type_=sqlalchemy.types.Enum(RoleType),
        nullable=True,
        index=True
    )

    # Investigator affiliation (referring to the `<affiliation>` element).
    affiliation = sqlalchemy.Column(
        name="affiliation",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # MD5 hash of the contact's full name.
    md5 = sqlalchemy.Column(
        name="md5",
        type_=sqlalchemy.types.Binary(),
        unique=True,
        index=True,
        nullable=False
    )

    # Relationship to a `Person` record.
    person = sqlalchemy.orm.relationship(
        argument="Person",
    )

    # Relationship to a list of `Location` records.
    locations = sqlalchemy.orm.relationship(
        argument="Location",
        secondary="location_investigators",
    )

    @sqlalchemy.orm.validates(
        "person_id",
        "role",
        "affiliation",
    )
    def update_md5(self, key, value):
        attrs = {
            "person_id": self.person_id,
            "role": self.role,
            "affiliation": self.affiliation,
        }
        attrs[key] = value

        # Retrieve the full concatenated name.
        name = " ".join([str(value) for value in attrs.values()])

        # Encode the full concatenated name to UTF8 (in case it contains
        # unicode characters).
        name_encoded = name.encode("utf-8")

        # Calculate the MD5 hash of the encoded full concatenated name and store
        # it under the `md5` attribute.
        md5 = hashlib.md5(name_encoded).digest()
        self.md5 = md5

        return value


class Location(Base, OrmBase):
    """Table of `<location>` elements records."""

    # set table name
    __tablename__ = "locations"

    # Autoincrementing primary key ID.
    location_id = sqlalchemy.Column(
        name="location_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the facility ID.
    facility_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("facilities.facility_id"),
        name="facility_id",
        nullable=True,
    )

    # Recruitment status (defined by the name of the element of `<status>`
    # type).
    status = sqlalchemy.Column(
        name="status",
        type_=sqlalchemy.types.Enum(RecruitmentStatusType),
        nullable=True,
        index=True
    )

    # Foreign key to the primary contact ID.
    contact_primary_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("contacts.contact_id"),
        name="contact_primary_id",
        nullable=True,
    )

    # Foreign key to the backup contact ID.
    contact_backup_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("contacts.contact_id"),
        name="contact_backup_id",
        nullable=True,
    )

    # Relationship to a `Contact` record for the primary contact.
    contact_primary = sqlalchemy.orm.relationship(
        argument="Contact",
        foreign_keys=contact_primary_id
    )

    # Relationship to a `Contact` record for the backup contact.
    contact_backup = sqlalchemy.orm.relationship(
        argument="Contact",
        foreign_keys=contact_backup_id
    )

    # Relationship to a list of `Investigator` records.
    investigators = sqlalchemy.orm.relationship(
        argument="Investigator",
        secondary="location_investigators",
    )

    # Relationship to a list of `Studies` records.
    studies = sqlalchemy.orm.relationship(
        argument="Study",
        secondary="study_locations",
        back_populates="locations",
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint(
            "facility_id",
            "contact_primary_id",
            "contact_backup_id",
        ),
    )


class LocationInvestigator(Base, OrmBase):
    """Associative table between `Location` and `Investigator` records."""

    # set table name
    __tablename__ = "location_investigators"

    # Autoincrementing primary key ID.
    location_investigator_id = sqlalchemy.Column(
        name="location_investigator_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the location ID.
    location_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("locations.location_id"),
        name="location_id",
        nullable=False,
    )

    # Foreign key to the investigator ID.
    investigator_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("investigators.investigator_id"),
        name="investigator_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('location_id', 'investigator_id'),
    )


class OversightInfo(Base, OrmBase):
    """Table of `<oversight_info>` elements records."""

    # set table name
    __tablename__ = "oversight_infos"

    # Autoincrementing primary key ID.
    oversight_info_id = sqlalchemy.Column(
        name="oversight_info_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the `<has_dmc>` element.
    has_dmc = sqlalchemy.Column(
        name="has_dmc",
        type_=sqlalchemy.types.Boolean(),
        nullable=True
    )

    # Referring to the `<is_fda_regulated_drug>` element.
    is_fda_regulated_drug = sqlalchemy.Column(
        name="is_fda_regulated_drug",
        type_=sqlalchemy.types.Boolean(),
        nullable=True
    )

    # Referring to the `<is_fda_regulated_device>` element.
    is_fda_regulated_device = sqlalchemy.Column(
        name="is_fda_regulated_device",
        type_=sqlalchemy.types.Boolean(),
        nullable=True
    )

    # Referring to the `<is_unapproved_device>` element.
    is_unapproved_device = sqlalchemy.Column(
        name="is_unapproved_device",
        type_=sqlalchemy.types.Boolean(),
        nullable=True
    )

    # Referring to the `<is_ppsd>` element.
    is_ppsd = sqlalchemy.Column(
        name="is_ppsd",
        type_=sqlalchemy.types.Boolean(),
        nullable=True
    )

    # Referring to the `<is_us_export>` element.
    is_us_export = sqlalchemy.Column(
        name="is_us_export",
        type_=sqlalchemy.types.Boolean(),
        nullable=True
    )


class ExpandedAccessInfo(Base, OrmBase):
    """Table of `<expanded_access_info>` elements records."""

    # set table name
    __tablename__ = "expanded_access_infos"

    # Autoincrementing primary key ID.
    expanded_access_info_id = sqlalchemy.Column(
        name="expanded_access_info_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the `<expanded_access_type_individual>` element.
    expanded_access_type_individual = sqlalchemy.Column(
        name="individual",
        type_=sqlalchemy.types.Boolean(),
        nullable=True
    )

    # Referring to the `<expanded_access_type_intermediate>` element.
    expanded_access_type_intermediate = sqlalchemy.Column(
        name="intermediate",
        type_=sqlalchemy.types.Boolean(),
        nullable=True
    )

    # Referring to the `<expanded_access_type_treatment>` element.
    expanded_access_type_treatment = sqlalchemy.Column(
        name="treatment",
        type_=sqlalchemy.types.Boolean(),
        nullable=True
    )


class StudyDesignInfo(Base, OrmBase):
    """Table of `<study_design_info>` elements records."""

    # set table name
    __tablename__ = "study_design_infos"

    # Autoincrementing primary key ID.
    study_design_info_id = sqlalchemy.Column(
        name="study_design_info_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the `<allocation>` element.
    allocation = sqlalchemy.Column(
        name="allocation",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<intervention_model>` element.
    intervention_model = sqlalchemy.Column(
        name="intervention_model",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<intervention_model_description>` element.
    intervention_model_description = sqlalchemy.Column(
        name="intervention_model_description",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<primary_purpose>` element.
    primary_purpose = sqlalchemy.Column(
        name="primary_purpose",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<observational_model>` element.
    observational_model = sqlalchemy.Column(
        name="observational_model",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<time_perspective>` element.
    time_perspective = sqlalchemy.Column(
        name="time_perspective",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<masking>` element.
    masking = sqlalchemy.Column(
        name="masking",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<masking_description>` element.
    masking_description = sqlalchemy.Column(
        name="masking_description",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )


class ProtocolOutcome(Base, OrmBase):
    """Table of `<protocol_outcome>` elements records."""

    # set table name
    __tablename__ = "protocol_outcomes"

    # Autoincrementing primary key ID.
    protocol_outcome_id = sqlalchemy.Column(
        name="protocol_outcome_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the `<measure>` element.
    measure = sqlalchemy.Column(
        name="measure",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # Referring to the `<time_frame>` element.
    time_frame = sqlalchemy.Column(
        name="time_frame",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<description>` element.
    description = sqlalchemy.Column(
        name="description",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )


class Group(Base, OrmBase):
    """Table of `<group>` elements records."""

    # set table name
    __tablename__ = "groups"

    # Autoincrementing primary key ID.
    group_id = sqlalchemy.Column(
        name="group_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `group_id` attribute of the `<group>`
    # element.
    identifier = sqlalchemy.Column(
        name="identifier",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # Referring to the `<title>` element.
    title = sqlalchemy.Column(
        name="title",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<description>` element.
    description = sqlalchemy.Column(
        name="description",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )


class Analysis(Base, OrmBase):
    """Table of `<analysis>` element records."""

    # set table name
    __tablename__ = "analyses"

    # Autoincrementing primary key ID.
    analysis_id = sqlalchemy.Column(
        name="analysis_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the `<groups_desc>` element.
    groups_desc = sqlalchemy.Column(
        name="groups_desc",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<non_inferiority_type>` element.
    non_inferiority_type = sqlalchemy.Column(
        name="non_inferiority_type",
        type_=sqlalchemy.types.Enum(NonInferiorityType),
        nullable=True,
        default=None,
        index=True
    )

    # Referring to the `<non_inferiority_desc>` element.
    non_inferiority_desc = sqlalchemy.Column(
        name="non_inferiority_desc",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<p_value>` element.
    p_value = sqlalchemy.Column(
        name="p_value",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<p_value_desc>` element.
    p_value_desc = sqlalchemy.Column(
        name="p_value_desc",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<method>` element.
    method = sqlalchemy.Column(
        name="method",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<method_desc>` element.
    method_desc = sqlalchemy.Column(
        name="method_desc",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<param_type>` element.
    param_type = sqlalchemy.Column(
        name="param_type",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<param_value>` element.
    param_value = sqlalchemy.Column(
        name="param_value",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<dispersion_type>` element.
    dispersion_type = sqlalchemy.Column(
        name="dispersion_type",
        type_=sqlalchemy.types.Enum(AnalysisDispersionType),
        nullable=True,
        default=None,
        index=True
    )

    # Referring to the `<dispersion_value>` element.
    dispersion_value = sqlalchemy.Column(
        name="dispersion_value",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<ci_percent>` element.
    ci_percent = sqlalchemy.Column(
        name="ci_percent",
        type_=sqlalchemy.types.Float(),
        nullable=True,
    )

    # Referring to the `<ci_n_sides>` element.
    ci_n_sides = sqlalchemy.Column(
        name="ci_n_sides",
        type_=sqlalchemy.types.Enum(NumSidesType),
        nullable=True,
    )

    # Referring to the `<ci_lower_limit>` element.
    ci_lower_limit = sqlalchemy.Column(
        name="ci_lower_limit",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<ci_upper_limit>` element.
    ci_upper_limit = sqlalchemy.Column(
        name="ci_upper_limit",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<ci_upper_limit_na_comment>` element.
    ci_upper_limit_na_comment = sqlalchemy.Column(
        name="ci_upper_limit_na_comment",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<estimate_desc>` element.
    estimate_desc = sqlalchemy.Column(
        name="estimate_desc",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<other_analysis_desc>` element.
    other_analysis_desc = sqlalchemy.Column(
        name="other_analysis_desc",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )


class AnalysisGroup(Base, OrmBase):
    """Associative table between `Analysis` and `Group` records."""

    # set table name
    __tablename__ = "analysis_groups"

    # Autoincrementing primary key ID.
    analysis_group_id = sqlalchemy.Column(
        name="analysis_group_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the analysis ID.
    analysis_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("analyses.analysis_id"),
        name="analysis_id",
        nullable=False,
    )

    # Foreign key to the group ID.
    group_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("groups.group_id"),
        name="group_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('analysis_id', 'group_id'),
    )


class MeasureCount(Base, OrmBase):
    """Table of `<measure_count>` element records."""

    # set table name
    __tablename__ = "measure_counts"

    # Autoincrementing primary key ID.
    measure_count_id = sqlalchemy.Column(
        name="measure_count_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the group ID.
    group_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("groups.group_id"),
        name="group_id",
        nullable=False,
    )

    # Referring to the `<value>` element.
    value = sqlalchemy.Column(
        name="value",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )


class MeasureAnalyzed(Base, OrmBase):
    """Table of `<measure_analyzed>` element records."""

    # set table name
    __tablename__ = "measure_analyzeds"

    # Autoincrementing primary key ID.
    measure_analyzed_id = sqlalchemy.Column(
        name="measure_analyzed_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the `<units>` element.
    units = sqlalchemy.Column(
        name="units",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<scope>` element.
    scope = sqlalchemy.Column(
        name="scope",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )


class MeasureAnalyzedCount(Base, OrmBase):
    """Associative table between `MeasureAnalyzed` and `MeasureCount`
    records."""

    # set table name
    __tablename__ = "measure_analyzed_counts"

    # Autoincrementing primary key ID.
    measure_analyzed_count_id = sqlalchemy.Column(
        name="measure_analyzed_count_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the analysis ID.
    measure_analyzed_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("measure_analyzeds.measure_analyzed_id"),
        name="measure_analyzed_id",
        nullable=False,
    )

    # Foreign key to the measure-count ID.
    measure_count_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("measure_counts.measure_count_id"),
        name="measure_count_id",
        nullable=False,
    )


class Measurement(Base, OrmBase):
    """Table of `<measurement>` element records."""

    # set table name
    __tablename__ = "measurements"

    # Autoincrementing primary key ID.
    measurement_id = sqlalchemy.Column(
        name="measurement_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the group ID.
    group_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("groups.group_id"),
        name="group_id",
        nullable=False,
    )

    # Referring to the value of the `value` attribute.
    value = sqlalchemy.Column(
        name="value",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `spread` attribute.
    spread = sqlalchemy.Column(
        name="spread",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `lower_limit` attribute.
    lower_limit = sqlalchemy.Column(
        name="lower_limit",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `upper_limit` attribute.
    upper_limit = sqlalchemy.Column(
        name="upper_limit",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Relationship to a `MeasureCategory` record.
    measure_category = sqlalchemy.orm.relationship(
        argument="MeasureCategory",
        secondary="measure_category_measurements",
    )


class MeasureCategory(Base, OrmBase):
    """Table of `<measure_category>` element records."""

    # set table name
    __tablename__ = "measure_categories"

    # Autoincrementing primary key ID.
    measure_category_id = sqlalchemy.Column(
        name="measure_category_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the `<title>` element.
    title = sqlalchemy.Column(
        name="title",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Relationship to a list of `Measurement` records.
    measurements = sqlalchemy.orm.relationship(
        argument="Measurement",
        secondary="measure_category_measurements",
    )


class MeasureCategoryMeasurement(Base, OrmBase):
    """Associative table between `MeasureCategory` and `Measurement` records."""

    # set table name
    __tablename__ = "measure_category_measurements"

    # Autoincrementing primary key ID.
    measure_category_measurement_id = sqlalchemy.Column(
        name="measure_category_measurement_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the measure-category ID.
    measure_category_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("measure_categories.measure_category_id"),
        name="measure_category_id",
        nullable=False,
    )

    # Foreign key to the measurement ID.
    measurement_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("measurements.measurement_id"),
        name="measurement_id",
        nullable=False,
    )


class MeasureClass(Base, OrmBase):
    """Table of `<measure_class>` element records."""

    # set table name
    __tablename__ = "measure_classes"

    # Autoincrementing primary key ID.
    measure_class_id = sqlalchemy.Column(
        name="measure_class_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Relationship to a list of `MeasureAnalyzed` records.
    measure_analyzeds = sqlalchemy.orm.relationship(
        argument="MeasureAnalyzed",
        secondary="measure_class_analyzeds",
    )

    # Relationship to a list of `MeasureCategory` records.
    measure_categories = sqlalchemy.orm.relationship(
        argument="MeasureCategory",
        secondary="measure_class_categories",
    )


class MeasureClassAnalyzed(Base, OrmBase):
    """Associative table between `MeasureClass` and `MeasureAnalyzed`
    records."""

    # set table name
    __tablename__ = "measure_class_analyzeds"

    # Autoincrementing primary key ID.
    measure_class_analyzed_id = sqlalchemy.Column(
        name="measure_class_analyzed_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the measure-class ID.
    measure_class_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("measure_classes.measure_class_id"),
        name="measure_class_id",
        nullable=False,
    )

    # Foreign key to the measure-analyzed ID.
    measure_analyzed_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("measure_analyzeds.measure_analyzed_id"),
        name="measure_analyzed_id",
        nullable=False,
    )


class MeasureClassCategories(Base, OrmBase):
    """Associative table between `MeasureClass` and `MeasureCategory`
    records."""

    # set table name
    __tablename__ = "measure_class_categories"

    # Autoincrementing primary key ID.
    measure_class_category_id = sqlalchemy.Column(
        name="measure_class_category_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the measure-class ID.
    measure_class_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("measure_classes.measure_class_id"),
        name="measure_class_id",
        nullable=False,
    )

    # Foreign key to the measure-category ID.
    measure_category_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("measure_categories.measure_category_id"),
        name="measure_category_id",
        nullable=False,
    )


class Measure(Base, OrmBase):
    """Table of `<measure>` element records."""

    # set table name
    __tablename__ = "measures"

    # Autoincrementing primary key ID.
    measure_id = sqlalchemy.Column(
        name="measure_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the `<title>` element.
    title = sqlalchemy.Column(
        name="title",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # Referring to the `<description>` element.
    description = sqlalchemy.Column(
        name="description",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<population>` element.
    population = sqlalchemy.Column(
        name="population",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<units>` element.
    units = sqlalchemy.Column(
        name="units",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<param>` element.
    parameter = sqlalchemy.Column(
        name="parameter",
        type_=sqlalchemy.types.Enum(MeasureParameterType),
        nullable=False,
    )

    # Referring to the `<dispersion>` element.
    dispersion = sqlalchemy.Column(
        name="dispersion",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<units_analyzed>` element.
    units_analyzed = sqlalchemy.Column(
        name="units_analyzed",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Relationship to a list of `MeasureAnalyzed` records.
    measure_analyzeds = sqlalchemy.orm.relationship(
        argument="MeasureAnalyzed",
        secondary="measure_measure_analyzeds",
    )

    # Relationship to a list of `MeasureClass` records.
    measure_classes = sqlalchemy.orm.relationship(
        argument="MeasureClass",
        secondary="measure_measure_classes",
    )


class MeasureMeasureAnalyzed(Base, OrmBase):
    """Associative table between `Measure` and `MeasureAnalyzed` records."""

    # set table name
    __tablename__ = "measure_measure_analyzeds"

    # Autoincrementing primary key ID.
    measure_measure_analyzed_id = sqlalchemy.Column(
        name="measure_measure_analyzed_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the measure ID.
    measure_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("measures.measure_id"),
        name="measure_id",
        nullable=False,
    )

    # Foreign key to the measure-analyzed ID.
    measure_analyzed_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("measure_analyzeds.measure_analyzed_id"),
        name="measure_analyzed_id",
        nullable=False,
    )


class MeasureMeasureClass(Base, OrmBase):
    """Associative table between `Measure` and `MeasureClass` records."""

    # set table name
    __tablename__ = "measure_measure_classes"

    # Autoincrementing primary key ID.
    measure_measure_class_id = sqlalchemy.Column(
        name="measure_measure_class_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the measure ID.
    measure_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("measures.measure_id"),
        name="measure_id",
        nullable=False,
    )

    # Foreign key to the measure-class ID.
    measure_class_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("measure_classes.measure_class_id"),
        name="measure_class_id",
        nullable=False,
    )


class ResultOutcome(Base, OrmBase):
    """Table of `<results_outcome>` element records."""

    # set table name
    __tablename__ = "result_outcomes"

    # Autoincrementing primary key ID.
    result_outcome_id = sqlalchemy.Column(
        name="result_outcome_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the `<type>` element.
    outcome_type = sqlalchemy.Column(
        name="type",
        type_=sqlalchemy.types.Enum(OutcomeType),
        nullable=False,
    )

    # Referring to the `<title>` element.
    title = sqlalchemy.Column(
        name="title",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # Referring to the `<description>` element.
    description = sqlalchemy.Column(
        name="description",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<time_frame>` element.
    time_frame = sqlalchemy.Column(
        name="time_frame",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<safety_issue>` element.
    safety_issue = sqlalchemy.Column(
        name="safety_issue",
        type_=sqlalchemy.types.Boolean(),
        nullable=True
    )

    # TODO: posting_date_type

    # Referring to the `<population>` element.
    population = sqlalchemy.Column(
        name="population",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Foreign key to the measure ID.
    measure_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("measures.measure_id"),
        name="measure_id",
        nullable=False,
    )

    # Relationship to a list of `Group` records.
    groups = sqlalchemy.orm.relationship(
        argument="Group",
        secondary="result_outcome_groups",
    )

    # Relationship to a `Measure` record.
    measure = sqlalchemy.orm.relationship(
        argument="Measure",
    )


class ResultOutcomeGroup(Base, OrmBase):
    """Associative table between `ResultOutcome` and `Group` records."""

    # set table name
    __tablename__ = "result_outcome_groups"

    # Autoincrementing primary key ID.
    result_outcome_group_id = sqlalchemy.Column(
        name="result_outcome_group_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the resut-outcome ID.
    result_outcome_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("result_outcomes.result_outcome_id"),
        name="result_outcome_id",
        nullable=False,
    )

    # Foreign key to the group ID.
    group_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("groups.group_id"),
        name="group_id",
        nullable=False,
    )


class Enrollment(Base, OrmBase):
    """Table of `<enrollment>` element records."""

    # set table name
    __tablename__ = "enrollments"

    # Autoincrementing primary key ID.
    enrollment_id = sqlalchemy.Column(
        name="enrollment_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `<enrollment>` element.
    value = sqlalchemy.Column(
        name="value",
        type_=sqlalchemy.types.Integer(),
        nullable=False,
    )

    # Referring to the value of the `type` attribute.
    enrollment_type = sqlalchemy.Column(
        name="type",
        type_=sqlalchemy.types.Enum(ActualType),
        nullable=True,
    )


class ArmGroup(Base, OrmBase):
    """Table of `<arm_group>` element records."""

    # set table name
    __tablename__ = "arm_groups"

    # Autoincrementing primary key ID.
    arm_group_id = sqlalchemy.Column(
        name="arm_group_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `<arm_group_label>` element.
    label = sqlalchemy.Column(
        name="label",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # Referring to the value of the `<arm_group_type>` element.
    arm_group_type = sqlalchemy.Column(
        name="type",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `<description>` element.
    description = sqlalchemy.Column(
        name="description",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )


class Intervention(Base, OrmBase):
    """Table of `<intervention>` element records."""

    # set table name
    __tablename__ = "interventions"

    # Autoincrementing primary key ID.
    intervention_id = sqlalchemy.Column(
        name="intervention_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `<intervention_type>` attribute.
    intervention_type = sqlalchemy.Column(
        name="type",
        type_=sqlalchemy.types.Enum(InterventionType),
        nullable=False,
    )

    # Referring to the value of the `<intervention_name>` element.
    name = sqlalchemy.Column(
        name="name",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # Referring to the value of the `<description>` element.
    description = sqlalchemy.Column(
        name="description",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Relationship to a list of `ArmGroup` records.
    arm_groups = sqlalchemy.orm.relationship(
        argument="ArmGroup",
        secondary="intervention_arm_groups",
    )

    # Relationship to a list of `Alias` records.
    aliases = sqlalchemy.orm.relationship(
        argument="Alias",
        secondary="intervention_aliases",
    )


class Alias(Base, OrmBase):
    """Table of aliases."""

    # set table name
    __tablename__ = "aliases"

    # Autoincrementing primary key ID.
    alias_id = sqlalchemy.Column(
        name="alias_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Alias value.
    alias = sqlalchemy.Column(
        name="alias",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # MD5 hash of the keyword.
    md5 = sqlalchemy.Column(
        name="md5",
        type_=sqlalchemy.types.Binary(),
        unique=True,
        index=True,
        nullable=False,
    )

    @sqlalchemy.orm.validates("alias")
    def update_md5(self, key, value):
        # Dumb hack to make the linter shut up that the `key` isn't used.
        assert key

        # Encode the alias to UTF8 (in case it contains unicode characters).
        alias_encoded = str(value).encode("utf-8")

        # Calculate the MD5 hash of the encoded alias and store under the
        # `md5` attribute.
        md5 = hashlib.md5(alias_encoded).digest()
        self.md5 = md5

        return value


class InterventionAlias(Base, OrmBase):
    """Associative table between `Intervention` and `Alias` records."""

    # set table name
    __tablename__ = "intervention_aliases"

    # Autoincrementing primary key ID.
    intervention_alias_id = sqlalchemy.Column(
        name="intervention_alias_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the intervention ID.
    intervention_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("interventions.intervention_id"),
        name="intervention_id",
        nullable=False,
    )

    # Foreign key to the alias ID.
    alias_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("aliases.alias_id"),
        name="alias_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('intervention_id', 'alias_id'),
    )


class InterventionArmGroup(Base, OrmBase):
    """Associative table between `Intervention` and `ArmGroup` records."""

    # set table name
    __tablename__ = "intervention_arm_groups"

    # Autoincrementing primary key ID.
    intervention_arm_group_id = sqlalchemy.Column(
        name="intervention_arm_group_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the intervention ID.
    intervention_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("interventions.intervention_id"),
        name="intervention_id",
        nullable=False,
    )

    # Foreign key to the arm-group ID.
    arm_group_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("arm_groups.arm_group_id"),
        name="arm_group_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('intervention_id', 'arm_group_id'),
    )


class Eligibility(Base, OrmBase):
    """Table of `<eligibility>` element records."""

    # set table name
    __tablename__ = "eligibilities"

    # Autoincrementing primary key ID.
    eligibility_id = sqlalchemy.Column(
        name="eligibility_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `<study_pop>` element.
    study_pop = sqlalchemy.Column(
        name="study_pop",
        type_=sqlalchemy.types.UnicodeText(),
        nullable=True,
    )

    # Referring to the value of the `<sampling_method>` attribute.
    sampling_method = sqlalchemy.Column(
        name="sampling_method",
        type_=sqlalchemy.types.Enum(SamplingMethodType),
        nullable=True,
    )

    # Referring to the value of the `<criteria>` element.
    criteria = sqlalchemy.Column(
        name="criteria",
        type_=sqlalchemy.types.UnicodeText(),
        nullable=True,
    )

    # Referring to the value of the `<gender>` attribute.
    gender = sqlalchemy.Column(
        name="gender",
        type_=sqlalchemy.types.Enum(GenderType),
        nullable=True,
    )

    # Referring to the `<gender_based>` element.
    gender_based = sqlalchemy.Column(
        name="gender_based",
        type_=sqlalchemy.types.Boolean(),
        nullable=True,
    )

    # Referring to the value of the `<gender_description>` element.
    gender_description = sqlalchemy.Column(
        name="gender_description",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # TODO: convert ages to floats
    # Referring to the value of the `<minimum_age>` element.
    minimum_age = sqlalchemy.Column(
        name="minimum_age",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `<maximum_age>` element.
    maximum_age = sqlalchemy.Column(
        name="maximum_age",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `<healthy_volunteers>` element.
    healthy_volunteers = sqlalchemy.Column(
        name="healthy_volunteers",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )


class Reference(Base, OrmBase):
    """Table of `<reference>` element records."""

    # set table name
    __tablename__ = "references"

    # Autoincrementing primary key ID.
    reference_id = sqlalchemy.Column(
        name="reference_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `<citation>` element.
    citation = sqlalchemy.Column(
        name="citation",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `<PMID>` element.
    pmid = sqlalchemy.Column(
        name="pmid",
        type_=sqlalchemy.types.Integer(),
        nullable=True,
        unique=True,
    )


class ResponsibleParty(Base, OrmBase):
    """Table of `<responsible_party>` element records."""

    # set table name
    __tablename__ = "responsible_parties"

    # Autoincrementing primary key ID.
    responsible_party_id = sqlalchemy.Column(
        name="responsible_party_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `<name_title>` element.
    name_title = sqlalchemy.Column(
        name="name_title",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `<organization>` element.
    organization = sqlalchemy.Column(
        name="organization",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `<responsible_party_type>` attribute.
    responsible_party_type = sqlalchemy.Column(
        name="type",
        type_=sqlalchemy.types.Enum(ResponsiblePartyType),
        nullable=True,
    )

    # Referring to the value of the `<investigator_affiliation>` element.
    investigator_affiliation = sqlalchemy.Column(
        name="investigator_affiliation",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `<investigator_full_name>` element.
    investigator_full_name = sqlalchemy.Column(
        name="investigator_full_name",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `<investigator_title>` element.
    investigator_title = sqlalchemy.Column(
        name="investigator_title",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )


class MeshTerm(Base, OrmBase):
    """Table of `<mesh_term>` element records."""

    # set table name
    __tablename__ = "mesh_terms"

    # Autoincrementing primary key ID.
    mesh_term_id = sqlalchemy.Column(
        name="mesh_term_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `<mesh_term>` element.
    term = sqlalchemy.Column(
        name="term",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # MD5 hash of the term.
    md5 = sqlalchemy.Column(
        name="md5",
        type_=sqlalchemy.types.Binary(),
        unique=True,
        index=True,
        nullable=False,
    )

    # Relationship to a list of `Study` records.
    studies = sqlalchemy.orm.relationship(
        argument="Study",
        secondary="study_mesh_terms",
        back_populates="mesh_terms"
    )

    @sqlalchemy.orm.validates("term")
    def update_md5(self, key, value):
        # Dumb hack to make the linter shut up that the `key` isn't used.
        assert key

        # Encode the term to UTF8 (in case it contains unicode characters).
        term_encoded = str(value).encode("utf-8")

        # Calculate the MD5 hash of the encoded term and store under the
        # `md5` attribute.
        md5 = hashlib.md5(term_encoded).digest()
        self.md5 = md5

        return value


class PatientData(Base, OrmBase):
    """Table of `<patient_data>` element records."""

    # set table name
    __tablename__ = "patient_datas"

    # Autoincrementing primary key ID.
    patient_data_id = sqlalchemy.Column(
        name="patient_data_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `<sharing_ipd>` element.
    sharing_ipd = sqlalchemy.Column(
        name="sharing_ipd",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # Referring to the value of the `<ipd_description>` element.
    ipd_description = sqlalchemy.Column(
        name="ipd_description",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )


class StudyDoc(Base, OrmBase):
    """Table of `<study_doc>` element records."""

    # set table name
    __tablename__ = "study_docs"

    # Autoincrementing primary key ID.
    study_doc_id = sqlalchemy.Column(
        name="study_doc_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `<doc_id>` element.
    doc_id = sqlalchemy.Column(
        name="doc_id",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `<doc_type>` element.
    doc_type = sqlalchemy.Column(
        name="doc_type",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `<doc_url>` element.
    doc_url = sqlalchemy.Column(
        name="doc_url",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `<doc_comment>` element.
    doc_comment = sqlalchemy.Column(
        name="doc_comment",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )


class Participant(Base, OrmBase):
    """Table of `<participants>` element records."""

    # set table name
    __tablename__ = "participants"

    # Autoincrementing primary key ID.
    participant_id = sqlalchemy.Column(
        name="participant_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the group ID.
    group_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("groups.group_id"),
        name="group_id",
        nullable=False,
    )

    # Referring to the value of the `<count>` element.
    count = sqlalchemy.Column(
        name="count",
        type_=sqlalchemy.types.Integer(),
        nullable=True,
    )

    # Relationship to a `Milestone` record.
    milestones = sqlalchemy.orm.relationship(
        argument="Milestone",
        secondary="milestone_participants",
    )


class Milestone(Base, OrmBase):
    """Table of `<milestone>` element records."""

    # set table name
    __tablename__ = "milestones"

    # Autoincrementing primary key ID.
    milestone_id = sqlalchemy.Column(
        name="milestone_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `<title>` element.
    title = sqlalchemy.Column(
        name="title",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Relationship to a list of `Participant` records.
    participants = sqlalchemy.orm.relationship(
        argument="Participant",
        secondary="milestone_participants",
    )


class DropWithdrawReason(Base, OrmBase):
    """Table of `<drop_withdraw_reason>` element records."""

    # set table name
    __tablename__ = "drop_withdraw_reasons"

    # Autoincrementing primary key ID.
    drop_withdraw_reason_id = sqlalchemy.Column(
        name="drop_withdraw_reason_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `<title>` element.
    title = sqlalchemy.Column(
        name="title",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )


class MilestoneParticipant(Base, OrmBase):
    """Associative table between `Milestone` and `Participant` records."""

    # set table name
    __tablename__ = "milestone_participants"

    # Autoincrementing primary key ID.
    milestone_participant_id = sqlalchemy.Column(
        name="milestone_participant_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the milestone ID.
    milestone_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("milestones.milestone_id"),
        name="milestone_id",
        nullable=False,
    )

    # Foreign key to the participant ID.
    participant_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("participants.participant_id"),
        name="participant_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('milestone_id', 'participant_id'),
    )


class Period(Base, OrmBase):
    """Table of `<period>` element records."""

    # set table name
    __tablename__ = "periods"

    # Autoincrementing primary key ID.
    period_id = sqlalchemy.Column(
        name="period_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `<title>` element.
    title = sqlalchemy.Column(
        name="title",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # Relationship to a list of `Milestone` records.
    milestones = sqlalchemy.orm.relationship(
        argument="Milestone",
        secondary="period_milestones",
    )

    # Relationship to a list of `DropWithdrawReason` records.
    drop_withdraw_reasons = sqlalchemy.orm.relationship(
        argument="DropWithdrawReason",
        secondary="period_drop_withdraw_reasons",
    )


class PeriodMilestone(Base, OrmBase):
    """Associative table between `Period` and `Milestone` records."""

    # set table name
    __tablename__ = "period_milestones"

    # Autoincrementing primary key ID.
    period_milestone_id = sqlalchemy.Column(
        name="period_milestone_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the period ID.
    period_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("periods.period_id"),
        name="period_id",
        nullable=False,
    )

    # Foreign key to the milestone ID.
    milestone_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("milestones.milestone_id"),
        name="milestone_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('period_id', 'milestone_id'),
    )


class PeriodDropWithdrawReason(Base, OrmBase):
    """Associative table between `Period` and `DropWithdrawReason` records."""

    # set table name
    __tablename__ = "period_drop_withdraw_reasons"

    # Autoincrementing primary key ID.
    period_drop_withdraw_reason_id = sqlalchemy.Column(
        name="period_drop_withdraw_reason_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the period ID.
    period_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("periods.period_id"),
        name="period_id",
        nullable=False,
    )

    # Foreign key to the milestone ID.
    drop_withdraw_reason_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey(
            "drop_withdraw_reasons.drop_withdraw_reason_id"
        ),
        name="drop_withdraw_reason_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('period_id', 'drop_withdraw_reason_id'),
    )


class ParticipantFlow(Base, OrmBase):
    """Table of `<participant_flow>` element records."""

    # set table name
    __tablename__ = "participant_flows"

    # Autoincrementing primary key ID.
    participant_flow_id = sqlalchemy.Column(
        name="participant_flow_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `<recruitment_details>` element.
    recruitment_details = sqlalchemy.Column(
        name="recruitment_details",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `<pre_assignment_details>` element.
    pre_assignment_details = sqlalchemy.Column(
        name="pre_assignment_details",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Relationship to a list of `Group` records.
    groups = sqlalchemy.orm.relationship(
        argument="Group",
        secondary="participant_flow_groups",
    )

    # Relationship to a list of `Period` records.
    periods = sqlalchemy.orm.relationship(
        argument="Period",
        secondary="participant_flow_periods",
    )


class ParticipantFlowGroup(Base, OrmBase):
    """Associative table between `ParticipantFlow` and `Group` records."""

    # set table name
    __tablename__ = "participant_flow_groups"

    # Autoincrementing primary key ID.
    participant_flow_group_id = sqlalchemy.Column(
        name="participant_flow_group_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the participant-flow ID.
    participant_flow_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("participant_flows.participant_flow_id"),
        name="participant_flow_id",
        nullable=False,
    )

    # Foreign key to the group ID.
    group_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("groups.group_id"),
        name="group_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('participant_flow_id', 'group_id'),
    )


class ParticipantFlowPeriod(Base, OrmBase):
    """Associative table between `ParticipantFlow` and `Period` records."""

    # set table name
    __tablename__ = "participant_flow_periods"

    # Autoincrementing primary key ID.
    participant_flow_period_id = sqlalchemy.Column(
        name="participant_flow_period_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the participant-flow ID.
    participant_flow_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("participant_flows.participant_flow_id"),
        name="participant_flow_id",
        nullable=False,
    )

    # Foreign key to the period ID.
    period_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("periods.period_id"),
        name="period_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('participant_flow_id', 'period_id'),
    )


class Baseline(Base, OrmBase):
    """Table of `<baseline>` element records."""

    # set table name
    __tablename__ = "baselines"

    # Autoincrementing primary key ID.
    baseline_id = sqlalchemy.Column(
        name="baseline_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `<population>` element.
    population = sqlalchemy.Column(
        name="population",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Relationship to a list of `Group` records.
    groups = sqlalchemy.orm.relationship(
        argument="Group",
        secondary="baseline_groups",
    )

    # Relationship to a list of `MeasureAnalyzed` records.
    measure_analyzeds = sqlalchemy.orm.relationship(
        argument="MeasureAnalyzed",
        secondary="baseline_measure_analyzeds",
    )

    # Relationship to a list of `Measures` records.
    measures = sqlalchemy.orm.relationship(
        argument="Measure",
        secondary="baseline_measures",
    )


class BaselineGroup(Base, OrmBase):
    """Associative table between `Baseline` and `Group` records."""

    # set table name
    __tablename__ = "baseline_groups"

    # Autoincrementing primary key ID.
    baseline_group_id = sqlalchemy.Column(
        name="baseline_group_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the baseline ID.
    baseline_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("baselines.baseline_id"),
        name="baseline_id",
        nullable=False,
    )

    # Foreign key to the group ID.
    group_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("groups.group_id"),
        name="group_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('baseline_id', 'group_id'),
    )


class BaselineMeasureAnalyzed(Base, OrmBase):
    """Associative table between `Baseline` and `MeasureAnalyzed` records."""

    # set table name
    __tablename__ = "baseline_measure_analyzeds"

    # Autoincrementing primary key ID.
    baseline_measure_analyzed_id = sqlalchemy.Column(
        name="baseline_measure_analyzed_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the baseline ID.
    baseline_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("baselines.baseline_id"),
        name="baseline_id",
        nullable=False,
    )

    # Foreign key to the measure-analyzed ID.
    measure_analyzed_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("measure_analyzeds.measure_analyzed_id"),
        name="measure_analyzed_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('baseline_id', 'measure_analyzed_id'),
    )


class BaselineMeasure(Base, OrmBase):
    """Associative table between `Baseline` and `Measure` records."""

    # set table name
    __tablename__ = "baseline_measures"

    # Autoincrementing primary key ID.
    baseline_measure_id = sqlalchemy.Column(
        name="baseline_measure_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the baseline ID.
    baseline_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("baselines.baseline_id"),
        name="baseline_id",
        nullable=False,
    )

    # Foreign key to the measure ID.
    measure_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("measures.measure_id"),
        name="measure_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('baseline_id', 'measure_id'),
    )


class EventCount(Base, OrmBase):
    """Table of `<event_count>` element records."""

    # set table name
    __tablename__ = "event_counts"

    # Autoincrementing primary key ID.
    event_count_id = sqlalchemy.Column(
        name="event_count_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the group ID.
    group_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("groups.group_id"),
        name="group_id",
        nullable=False,
    )

    # Referring to the value of the `<subjects_affected>` element.
    subjects_affected = sqlalchemy.Column(
        name="subjects_affected",
        type_=sqlalchemy.types.Integer(),
        nullable=True,
    )

    # Referring to the value of the `<subjects_at_risk>` element.
    subjects_at_risk = sqlalchemy.Column(
        name="subjects_at_risk",
        type_=sqlalchemy.types.Integer(),
        nullable=True,
    )

    # Referring to the value of the `<events>` element.
    events = sqlalchemy.Column(
        name="events",
        type_=sqlalchemy.types.Integer(),
        nullable=True,
    )


class Event(Base, OrmBase):
    """Table of `<event>` element records."""

    # set table name
    __tablename__ = "events"

    # Autoincrementing primary key ID.
    event_id = sqlalchemy.Column(
        name="event_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `<sub_title>` element.
    sub_title = sqlalchemy.Column(
        name="sub_title",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `<assessment>` element.
    assessment = sqlalchemy.Column(
        name="assessment",
        type_=sqlalchemy.types.Enum(EventAssessmentType),
        nullable=True,
        default=None,
        index=True
    )

    # Referring to the value of the `<description>` element.
    description = sqlalchemy.Column(
        name="description",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Relationship to a list of `EventCount` records.
    counts = sqlalchemy.orm.relationship(
        argument="EventCount",
        secondary="event_event_counts",
    )


class EventEventCount(Base, OrmBase):
    """Associative table between `Event` and `EventCount` records."""

    # set table name
    __tablename__ = "event_event_counts"

    # Autoincrementing primary key ID.
    event_event_count_id = sqlalchemy.Column(
        name="event_event_count_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the event ID.
    event_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("events.event_id"),
        name="event_id",
        nullable=False,
    )

    # Foreign key to the event-count ID.
    event_count_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("event_counts.event_count_id"),
        name="event_count_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('event_id', 'event_count_id'),
    )


class EventCategory(Base, OrmBase):
    """Table of `<event_category>` element records."""

    # set table name
    __tablename__ = "event_categories"

    # Autoincrementing primary key ID.
    event_category_id = sqlalchemy.Column(
        name="event_category_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `<title>` element.
    title = sqlalchemy.Column(
        name="title",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Relationship to a list of `Event` records.
    events = sqlalchemy.orm.relationship(
        argument="Event",
        secondary="event_category_events",
    )


class EventCategoryEvent(Base, OrmBase):
    """Associative table between `EventCategory` and `Event` records."""

    # set table name
    __tablename__ = "event_category_events"

    # Autoincrementing primary key ID.
    event_category_event_id = sqlalchemy.Column(
        name="event_category_event_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the event-category ID.
    event_category_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("event_categories.event_category_id"),
        name="event_category_id",
        nullable=False,
    )

    # Foreign key to the event ID.
    event_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("events.event_id"),
        name="event_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('event_category_id', 'event_id'),
    )


class EventList(Base, OrmBase):
    """Table of `<events>` element records."""

    # set table name
    __tablename__ = "event_lists"

    # Autoincrementing primary key ID.
    event_list_id = sqlalchemy.Column(
        name="event_list_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `<frequency_threshold>` element.
    frequency_threshold = sqlalchemy.Column(
        name="frequency_threshold",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `<default_vocab>` element.
    default_vocab = sqlalchemy.Column(
        name="default_vocab",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `<default_assessment>` element.
    default_assessment = sqlalchemy.Column(
        name="default_assessment",
        type_=sqlalchemy.types.Enum(EventAssessmentType),
        nullable=True,
        default=None,
        index=True
    )

    # Relationship to a list of `EventCategory` records.
    event_categories = sqlalchemy.orm.relationship(
        argument="EventCategory",
        secondary="event_list_categories",
    )


class EventListCategories(Base, OrmBase):
    """Associative table between `EventList` and `EventCategory` records."""

    # set table name
    __tablename__ = "event_list_categories"

    # Autoincrementing primary key ID.
    event_list_category_id = sqlalchemy.Column(
        name="event_list_category_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the event-list ID.
    event_list_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("event_lists.event_list_id"),
        name="event_list_id",
        nullable=False,
    )

    # Foreign key to the event-category ID.
    event_category_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("event_categories.event_category_id"),
        name="event_category_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('event_list_id', 'event_category_id'),
    )


class ReportedEvent(Base, OrmBase):
    """Table of `<reported_events>` element records."""

    # set table name
    __tablename__ = "reported_events"

    # Autoincrementing primary key ID.
    reported_event_id = sqlalchemy.Column(
        name="reported_event_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `<time_frame>` element.
    time_frame = sqlalchemy.Column(
        name="time_frame",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `<desc>` element.
    desc = sqlalchemy.Column(
        name="desc",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Relationship to a list of `Group` records.
    groups = sqlalchemy.orm.relationship(
        argument="Group",
        secondary="reported_event_groups",
    )

    # Foreign key to an event-list ID.
    serious_event_list_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("event_lists.event_list_id"),
        name="serious_event_list_id",
        nullable=False,
    )

    # Foreign key to an event-list ID.
    other_event_list_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("event_lists.event_list_id"),
        name="other_event_list_id",
        nullable=False,
    )

    # Relationship to a `EventList` record for the 'serious events'.
    serious_event_list = sqlalchemy.orm.relationship(
        argument="EventList",
        foreign_keys=serious_event_list_id
    )

    # Relationship to a `EventList` record for the 'other events'.
    other_event_list = sqlalchemy.orm.relationship(
        argument="EventList",
        foreign_keys=other_event_list_id
    )


class ReportedEventGroup(Base, OrmBase):
    """Associative table between `ReportedEvent` and `Group` records."""

    # set table name
    __tablename__ = "reported_event_groups"

    # Autoincrementing primary key ID.
    reported_event_group_id = sqlalchemy.Column(
        name="reported_event_group_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the reported-event ID.
    reported_event_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("reported_events.reported_event_id"),
        name="reported_event_id",
        nullable=False,
    )

    # Foreign key to the group ID.
    group_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("groups.group_id"),
        name="group_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('reported_event_id', 'group_id'),
    )


class StudyDates(Base, OrmBase):
    """Table of secondary dates pertaining to a `<clinical_study>` element
    record."""

    # set table name
    __tablename__ = "study_dates"

    # Autoincrementing primary key ID.
    study_dates_id = sqlalchemy.Column(
        name="study_dates_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `<study_first_submitted>` element.
    study_first_submitted = sqlalchemy.Column(
        name="study_first_submitted",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Referring to the value of the `<study_first_submitted_qc>` element.
    study_first_submitted_qc = sqlalchemy.Column(
        name="study_first_submitted_qc",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Referring to the value of the `<study_first_posted>` element.
    study_first_posted = sqlalchemy.Column(
        name="study_first_posted",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Referring to the value of the `<results_first_submitted>` element.
    results_first_submitted = sqlalchemy.Column(
        name="results_first_submitted",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Referring to the value of the `<results_first_submitted_qc>` element.
    results_first_submitted_qc = sqlalchemy.Column(
        name="results_first_submitted_qc",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Referring to the value of the `<results_first_posted>` element.
    results_first_posted = sqlalchemy.Column(
        name="results_first_posted",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Referring to the value of the `<disposition_first_submitted>` element.
    disposition_first_submitted = sqlalchemy.Column(
        name="disposition_first_submitted",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Referring to the value of the `<disposition_first_submitted_qc>` element.
    disposition_first_submitted_qc = sqlalchemy.Column(
        name="disposition_first_submitted_qc",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Referring to the value of the `<disposition_first_posted>` element.
    disposition_first_posted = sqlalchemy.Column(
        name="disposition_first_posted",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Referring to the value of the `<last_update_submitted>` element.
    last_update_submitted = sqlalchemy.Column(
        name="last_update_submitted",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Referring to the value of the `<last_update_submitted_qc>` element.
    last_update_submitted_qc = sqlalchemy.Column(
        name="last_update_submitted_qc",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Referring to the value of the `<last_update_posted>` element.
    last_update_posted = sqlalchemy.Column(
        name="last_update_posted",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )


class Study(Base, OrmBase):
    """Table of `<clinical_study>` element records."""

    # set table name
    __tablename__ = "studies"

    # Autoincrementing primary key ID.
    study_id = sqlalchemy.Column(
        name="study_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `<org_study_id>` element.
    org_study_id = sqlalchemy.Column(
        name="org_study_id",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `<secondary_id>` element.
    secondary_id = sqlalchemy.Column(
        name="secondary_id",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `<nct_id>` element.
    nct_id = sqlalchemy.Column(
        name="nct_id",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
        unique=True,
    )

    # Relationship to a list of `Alias` records.
    aliases = sqlalchemy.orm.relationship(
        argument="Alias",
        secondary="study_aliases",
    )

    # Referring to the value of the `<brief_title>` element.
    brief_title = sqlalchemy.Column(
        name="brief_title",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # Referring to the value of the `<acronym>` element.
    acronym = sqlalchemy.Column(
        name="acronym",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `<official_title>` element.
    official_title = sqlalchemy.Column(
        name="official_title",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Relationship to a list of `Sponsor` records.
    sponsors = sqlalchemy.orm.relationship(
        argument="Sponsor",
        secondary="study_sponsors",
        back_populates="studies",
    )

    # Referring to the value of the `<source>` element.
    source = sqlalchemy.Column(
        name="source",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # Foreign key to the oversight-info ID.
    oversight_info_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("oversight_infos.oversight_info_id"),
        name="oversight_info_id",
        nullable=True,
    )

    # Relationship to a list of `OversightInfo` records.
    oversight_info = sqlalchemy.orm.relationship(
        argument="OversightInfo",
    )

    # Referring to the value of the `<brief_summary>` element.
    brief_summary = sqlalchemy.Column(
        name="brief_summary",
        type_=sqlalchemy.types.UnicodeText(),
        nullable=True,
    )

    # Referring to the value of the `<detailed_description>` element.
    detailed_description = sqlalchemy.Column(
        name="detailed_description",
        type_=sqlalchemy.types.UnicodeText(),
        nullable=True,
    )

    # Referring to the value of the `<overall_status>` element.
    overall_status = sqlalchemy.Column(
        name="overall_status",
        type_=sqlalchemy.types.Enum(OverallStatusType),
        nullable=False,
        index=True
    )

    # Referring to the value of the `<last_known_status>` element.
    last_known_status = sqlalchemy.Column(
        name="last_known_status",
        type_=sqlalchemy.types.Enum(OverallStatusType),
        nullable=True,
        index=True
    )

    # Referring to the value of the `<why_stopped>` element.
    why_stopped = sqlalchemy.Column(
        name="why_stopped",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the value of the `<start_date>` element.
    start_date = sqlalchemy.Column(
        name="start_date",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Referring to the value of the `<completion_date>` element.
    completion_date = sqlalchemy.Column(
        name="completion_date",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Referring to the value of the `<primary_completion_date>` element.
    primary_completion_date = sqlalchemy.Column(
        name="primary_completion_date",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Referring to the value of the `<verification_date>` element.
    verification_date = sqlalchemy.Column(
        name="verification_date",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Referring to the value of the `<phase>` element.
    phase = sqlalchemy.Column(
        name="phase",
        type_=sqlalchemy.types.Enum(PhaseType),
        nullable=False,
        index=True
    )

    # Referring to the value of the `<study_type>` element.
    study_type = sqlalchemy.Column(
        name="study_type",
        type_=sqlalchemy.types.Enum(StudyType),
        nullable=False,
        index=True
    )

    # Foreign key to the expanded-access-info ID.
    expanded_access_info_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey(
            "expanded_access_infos.expanded_access_info_id"
        ),
        name="expanded_access_info_id",
        nullable=True,
    )

    # Relationship to a list of `ExpandedAccessInfo` records.
    expanded_info = sqlalchemy.orm.relationship(
        argument="ExpandedAccessInfo",
    )

    # Foreign key to the study-design-info ID.
    study_design_info_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("study_design_infos.study_design_info_id"),
        name="study_design_info_id",
        nullable=True,
    )

    # Relationship to a list of `StudyDesignInfo` records.
    study_design_info = sqlalchemy.orm.relationship(
        argument="StudyDesignInfo",
    )

    # Referring to the value of the `<target_duration>` element.
    target_duration = sqlalchemy.Column(
        name="target_duration",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Relationship to a list of `ProtocolOutcome` records.
    outcomes = sqlalchemy.orm.relationship(
        argument="ProtocolOutcome",
        secondary="study_outcomes",
    )

    # Foreign key to the enrollment ID.
    enrollment_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("enrollments.enrollment_id"),
        name="enrollment_id",
        nullable=True,
    )

    # Relationship to a list of `Enrollment` records.
    enrollment = sqlalchemy.orm.relationship(
        argument="Enrollment",
    )

    # Relationship to a list of `Condition` records.
    conditions = sqlalchemy.orm.relationship(
        argument="Condition",
        secondary="study_conditions",
        back_populates="studies",
    )

    # Relationship to a list of `ArmGroup` records.
    arm_groups = sqlalchemy.orm.relationship(
        argument="ArmGroup",
        secondary="study_arm_groups",
    )

    # Relationship to a list of `Intervention` records.
    interventions = sqlalchemy.orm.relationship(
        argument="Intervention",
        secondary="study_interventions",
    )

    # Referring to the value of the `<biospec_retention>` element.
    biospec_retention = sqlalchemy.Column(
        name="biospec_retention",
        type_=sqlalchemy.types.Enum(BiospecRetentionType),
        nullable=True,
        index=True
    )

    # Referring to the value of the `<biospec_desc>` element.
    biospec_description = sqlalchemy.Column(
        name="biospec_description",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Foreign key to the elligibility ID.
    eligibility_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("eligibilities.eligibility_id"),
        name="eligibility_id",
        nullable=True,
    )

    # Relationship to an `Elligibility` record.
    elligibility = sqlalchemy.orm.relationship(
        argument="Eligibility",
    )

    # Relationship to a list of `Investigator` records.
    investigators = sqlalchemy.orm.relationship(
        argument="Investigator",
        secondary="study_investigators",
    )

    # Foreign key to a contact ID of 'primary' type.
    contact_primary_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("contacts.contact_id"),
        name="contact_primary_id",
        nullable=True,
    )

    # Relationship to a `Contact` record of 'primary' type.
    contact_primary = sqlalchemy.orm.relationship(
        argument="Contact",
        foreign_keys=contact_primary_id
    )

    # Foreign key to a contact ID of 'backup' type.
    contact_backup_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("contacts.contact_id"),
        name="contact_backup_id",
        nullable=True,
    )

    # Relationship to a `Contact` record of 'backup' type.
    contact_backup = sqlalchemy.orm.relationship(
        argument="Contact",
        foreign_keys=contact_backup_id
    )

    # Relationship to a list of `Location` records.
    locations = sqlalchemy.orm.relationship(
        argument="Location",
        secondary="study_locations",
        back_populates="studies"
    )

    # TODO: location_countries
    # TODO: removed_countries
    # Skipping link`

    # Relationship to a list of `Reference` records.
    references = sqlalchemy.orm.relationship(
        argument="Reference",
        secondary="study_references",
    )

    # Foreign key to the study-dates ID.
    study_dates_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("study_dates.study_dates_id"),
        name="study_dates_id",
        nullable=False,
    )

    # Relationship to a list of `StudyDates` records.
    study_dates = sqlalchemy.orm.relationship(
        argument="StudyDates",
    )

    # Foreign key to a responsible-party ID.
    responsible_party_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("responsible_parties.responsible_party_id"),
        name="responsible_party_id",
        nullable=True,
    )

    # Relationship to a `ResponsibleParty` record.
    responsible_party = sqlalchemy.orm.relationship(
        argument="ResponsibleParty",
    )

    # Relationship to a list of `Keyword` records.
    keywords = sqlalchemy.orm.relationship(
        argument="Keyword",
        secondary="study_keywords",
        back_populates="studies",
    )

    # Relationship to a list of `MeshTerm` records.
    mesh_terms = sqlalchemy.orm.relationship(
        argument="MeshTerm",
        secondary="study_mesh_terms",
        back_populates="studies",
    )

    # Foreign key to a patient-data ID.
    patient_data_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("patient_datas.patient_data_id"),
        name="patient_data_id",
        nullable=True,
    )

    # Relationship to a `PatientData` record.
    patient_data = sqlalchemy.orm.relationship(
        argument="PatientData",
    )

    # Relationship to a list of `StudyDoc` records.
    study_docs = sqlalchemy.orm.relationship(
        argument="StudyDoc",
        secondary="study_study_docs",
    )

    # TODO: clinical_results


class StudyAlias(Base, OrmBase):
    """Associative table between `Study` and `Alias` records."""

    # set table name
    __tablename__ = "study_aliases"

    # Autoincrementing primary key ID.
    study_alias_id = sqlalchemy.Column(
        name="study_alias_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the study ID.
    study_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("studies.study_id"),
        name="study_id",
        nullable=False,
    )

    # Foreign key to the alias ID.
    alias_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("aliases.alias_id"),
        name="alias_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('study_id', 'alias_id'),
    )


class StudySponsor(Base, OrmBase):
    """Associative table between `Study` and `Sponsor` records."""

    # set table name
    __tablename__ = "study_sponsors"

    # Autoincrementing primary key ID.
    study_sponsor_id = sqlalchemy.Column(
        name="study_sponsor_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the study ID.
    study_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("studies.study_id"),
        name="study_id",
        nullable=False,
    )

    # Foreign key to the sponsor ID.
    sponsor_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("sponsors.sponsor_id"),
        name="sponsor_id",
        nullable=False,
    )

    # Sponsor type (defined by the name of the element of `<sponsor>` type.
    sponsor_type = sqlalchemy.Column(
        name="type",
        type_=sqlalchemy.types.Enum(SponsorType),
        nullable=False,
        index=True
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('study_id', 'sponsor_id'),
    )


class StudyOutcome(Base, OrmBase):
    """Associative table between `Study` and `ProtocolOutcome` records."""

    # set table name
    __tablename__ = "study_outcomes"

    # Autoincrementing primary key ID.
    study_primary_outcome_id = sqlalchemy.Column(
        name="study_primary_outcome_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the study ID.
    study_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("studies.study_id"),
        name="study_id",
        nullable=False,
    )

    # Foreign key to the protocol-outcome ID.
    protocol_outcome_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("protocol_outcomes.protocol_outcome_id"),
        name="protocol_outcome_id",
        nullable=False,
    )

    # Referring to the type of outcome.
    outcome_type = sqlalchemy.Column(
        name="type",
        type_=sqlalchemy.types.Enum(OutcomeType),
        nullable=False,
        index=True
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('study_id', 'protocol_outcome_id'),
    )


class StudyCondition(Base, OrmBase):
    """Associative table between `Study` and `Condition` records."""

    # set table name
    __tablename__ = "study_conditions"

    # Autoincrementing primary key ID.
    study_condition_id = sqlalchemy.Column(
        name="study_condition_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the study ID.
    study_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("studies.study_id"),
        name="study_id",
        nullable=False,
    )

    # Foreign key to the condition ID.
    condition_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("conditions.condition_id"),
        name="condition_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('study_id', 'condition_id'),
    )


class StudyArmGroup(Base, OrmBase):
    """Associative table between `Study` and `ArmGroup` records."""

    # set table name
    __tablename__ = "study_arm_groups"

    # Autoincrementing primary key ID.
    study_arm_group_id = sqlalchemy.Column(
        name="study_arm_group_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the study ID.
    study_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("studies.study_id"),
        name="study_id",
        nullable=False,
    )

    # Foreign key to the arm-group ID.
    arm_group_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("arm_groups.arm_group_id"),
        name="arm_group_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('study_id', 'arm_group_id'),
    )


class StudyIntervention(Base, OrmBase):
    """Associative table between `Study` and `Intervention` records."""

    # set table name
    __tablename__ = "study_interventions"

    # Autoincrementing primary key ID.
    study_intervention_id = sqlalchemy.Column(
        name="study_intervention_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the study ID.
    study_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("studies.study_id"),
        name="study_id",
        nullable=False,
    )

    # Foreign key to the intervention ID.
    intervention_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("interventions.intervention_id"),
        name="intervention_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('study_id', 'intervention_id'),
    )


class StudyInvestigator(Base, OrmBase):
    """Associative table between `Study` and `Investigator` records."""

    # set table name
    __tablename__ = "study_investigators"

    # Autoincrementing primary key ID.
    study_investigator_id = sqlalchemy.Column(
        name="study_investigator_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the study ID.
    study_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("studies.study_id"),
        name="study_id",
        nullable=False,
    )

    # Foreign key to the investigator ID.
    investigator_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("investigators.investigator_id"),
        name="investigator_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('study_id', 'investigator_id'),
    )


class StudyLocation(Base, OrmBase):
    """Associative table between `Study` and `Location` records."""

    # set table name
    __tablename__ = "study_locations"

    # Autoincrementing primary key ID.
    study_location_id = sqlalchemy.Column(
        name="study_location_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the study ID.
    study_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("studies.study_id"),
        name="study_id",
        nullable=False,
    )

    # Foreign key to the location ID.
    location_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("locations.location_id"),
        name="location_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('study_id', 'location_id'),
    )


class StudyReference(Base, OrmBase):
    """Associative table between `Study` and `Reference` records."""

    # set table name
    __tablename__ = "study_references"

    # Autoincrementing primary key ID.
    study_reference_id = sqlalchemy.Column(
        name="study_reference_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the study ID.
    study_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("studies.study_id"),
        name="study_id",
        nullable=False,
    )

    # Foreign key to the reference ID.
    reference_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("references.reference_id"),
        name="reference_id",
        nullable=False,
    )

    # Referring to the type of reference.
    reference_type = sqlalchemy.Column(
        name="type",
        type_=sqlalchemy.types.Enum(ReferenceType),
        nullable=False,
        index=True
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('study_id', 'reference_id'),
    )


class StudyKeyword(Base, OrmBase):
    """Associative table between `Study` and `Keyword` records."""

    # set table name
    __tablename__ = "study_keywords"

    # Autoincrementing primary key ID.
    study_keyword_id = sqlalchemy.Column(
        name="study_keyword_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the study ID.
    study_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("studies.study_id"),
        name="study_id",
        nullable=False,
    )

    # Foreign key to the keyword ID.
    keyword_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("keywords.keyword_id"),
        name="keyword_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('study_id', 'keyword_id'),
    )


class StudyMeshTerm(Base, OrmBase):
    """Associative table between `Study` and `MeshTerm` records."""

    # set table name
    __tablename__ = "study_mesh_terms"

    # Autoincrementing primary key ID.
    study_mesh_term_id = sqlalchemy.Column(
        name="study_mesh_term_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the study ID.
    study_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("studies.study_id"),
        name="study_id",
        nullable=False,
    )

    # Foreign key to the mesh-term ID.
    mesh_term_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh_terms.mesh_term_id"),
        name="mesh_term_id",
        nullable=False,
    )

    # Referring to the type of mesh-term.
    mesh_term_type = sqlalchemy.Column(
        name="type",
        type_=sqlalchemy.types.Enum(MeshTermType),
        nullable=False,
        index=True
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('study_id', 'mesh_term_id'),
    )


class StudyStudyDoc(Base, OrmBase):
    """Associative table between `Study` and `StudyDoc` records."""

    # set table name
    __tablename__ = "study_study_docs"

    # Autoincrementing primary key ID.
    study_study_doc_id = sqlalchemy.Column(
        name="study_study_doc_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the study ID.
    study_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("studies.study_id"),
        name="study_id",
        nullable=False,
    )

    # Foreign key to the study-doc ID.
    study_doc_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("study_docs.study_doc_id"),
        name="study_doc_id",
        nullable=False,
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('study_id', 'study_doc_id'),
    )
