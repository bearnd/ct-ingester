# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ct_ingester.utils import EnumBase


class ActualType(EnumBase):
    """Enumeration of the actual types."""

    ACTUAL = "Actual"
    ANTICIPATED = "Anticipated"
    ESTIMATE = "Estimated"


class YesNoType(EnumBase):
    """Enumeration of the yes/no types."""

    YES = "Yes"
    NO = "No"


class RecruitmentStatusType(EnumBase):
    """Enumeration of the recruitment-status types."""

    ACTIVE_NOT = "Active, not recruiting"
    COMPLETED = "Completed"
    INVITATION = "Enrolling by invitation"
    NOT_YET = "Not yet recruiting"
    RECRUITING = "Recruiting"
    SUSPENDED = "Suspended"
    TERMINATED = "Terminated"
    WITHDRAWN = "Withdrawn"


class AgencyClassType(EnumBase):
    """Enumeration of the agency-class types."""

    NIH = "NIH"
    US = "U.S. Fed"
    INDUSTRY = "Industry"
    OTHER = "Other"


class InterventionType(EnumBase):
    """Enumeration of the intervention types."""

    BEHAVIORAL = "Behavioral"
    BIOLOGICAL = "Biological"
    COMBINATION = "Combination Product"
    DEVICE = "Device"
    DIAGNOSTIC = "Diagnostic Test"
    DIETARY = "Dietary Supplement"
    DRUG = "Drug"
    GENETIC = "Genetic"
    PROCEDURE = "Procedure"
    RADIATION = "Radiation"
    OTHER = "Other"


class SamplingMethodType(EnumBase):
    """Enumeration of the sampling-method types."""

    PROBABILITY = "Probability Sample"
    NON_PROBABILITY = "Non-Probability Sample"


class GenderType(EnumBase):
    """Enumeration of the gender types."""

    FEMALE = "Female"
    MALE = "Male"
    ALL = "All"


class RoleType(EnumBase):
    """Enumeration of the role types."""

    PRINCIPAL = "Principal Investigator"
    SUB = "Sub-Investigator"
    CHAIR = "Study Chair"
    DIRECTOR = "Study Director"


class ResponsiblePartyType(EnumBase):
    """Enumeration of the responsible-party types."""

    SPONSOR = "Sponsor"
    PRINCIPAL = "Principal Investigator"
    SPONSOR_INVESTIGATOR = "Sponsor-Investigator"


class MeasureParameterType(EnumBase):
    """Enumeration of the measure-parameter types."""

    GEOMETRIC = "Geometric Mean"
    GLS_MEAN = "Geometric Least Squares Mean"
    LS_MEAN = "Least Squares Mean"
    LOG_MEAN = "Log Mean"
    MEAN = "Mean"
    MEDIAN = "Median"
    NUMBER = "Number"
    PARTICIPANTS = "Count of Participants"
    UNITS = "Count of Units"


class MeasureDispersionType(EnumBase):
    """Enumeration of the measure-dispersion types."""

    CI_80 = "80% Confidence Interval"
    CI_90 = "90% Confidence Interval"
    CI_95 = "95% Confidence Interval"
    CI_97 = "97.5% Confidence Interval"
    CI_99 = "99% Confidence Interval"
    FULL_RANGE = "Full Range"
    GCV = "Geometric Coefficient of Variation"
    IQR = "Inter-Quartile Range"
    SD = "Standard Deviation"
    SE = "Standard Error"


class NonInferiorityType(EnumBase):
    """Enumeration of the non-inferiority types."""

    SUPERIORITY = "Superiority"
    NON_INFERIORITY = "Non-Inferiority"
    EQUIVALENCE = "Equivalence"
    OTHER = "Other"


class NumSidesType(EnumBase):
    """Enumeration of the number of sides."""

    ONE = "1-Sided"
    TWO = "2-Sided"


class AnalysisDispersionType(EnumBase):
    """Enumeration of the analysis-dispersion types."""

    SD = "Standard Deviation"
    SEM = "Standard Error of the Mean"


class OutcomeType(EnumBase):
    """Enumeration of the outcome types."""

    PRIMARY = "Primary"
    SECONDARY = "Secondary"
    POST_HOC = "Post-Hoc"
    OTHER = "Other Pre-specified"


class EventAssessmentType(EnumBase):
    """Enumeration of the event-assessment types."""

    SYSTEMATIC = "Systematic Assessment"
    NON_SYSTEMATIC = "Non-systematic Assessment"


class PiEmployeeType(EnumBase):
    """Enumeration of the pi-employee types."""

    ARE_EMPLOYED = ("All Principal Investigators ARE employed by the "
                    "organization sponsoring the study.")
    NOT_EMPLOYED = ("Principal Investigators are NOT employed by the "
                    "organization sponsoring the study.")


class ExpandedAccessStatusType(EnumBase):
    """Enumeration of the expanded-access-status types."""

    AVAILABLE = "Available"
    UNAVAILABLE = "No longer available"
    TEMP_UNAVAILABLE = "Temporarily not available"
    APPROVED = "Approved for marketing"


class RedactedRecordStatusType(EnumBase):
    """Enumeration of the redacted-record-status types."""

    WITHHELD = "Withheld"


class UnknownStatusType(EnumBase):
    """Enumeration of the unknown-status types."""

    UNKNOWN = "Unknown status"


class OverallStatusType(EnumBase):
    """Enumeration of the overall-status types."""

    ACTIVE_NOT = "Active, not recruiting"
    COMPLETED = "Completed"
    INVITATION = "Enrolling by invitation"
    NOT_YET = "Not yet recruiting"
    RECRUITING = "Recruiting"
    SUSPENDED = "Suspended"
    TERMINATED = "Terminated"
    WITHDRAWN = "Withdrawn"
    AVAILABLE = "Available"
    UNAVAILABLE = "No longer available"
    TEMP_UNAVAILABLE = "Temporarily not available"
    APPROVED = "Approved for marketing"
    WITHHELD = "Withheld"
    UNKNOWN = "Unknown status"


class StudyType(EnumBase):
    """Enumeration of the study types."""

    EXPANDED = "Expanded Access"
    INTERVENTIONAL = "Interventional"
    NA = "N/A"
    OBSERVATIONAL = "Observational"
    OBSERVATIONAL_PR = "Observational [Patient Registry]"


class PhaseType(EnumBase):
    """Enumeration of the phase types."""

    NA = "N/A"
    PHASE_1_EARLY = "Early Phase 1"
    PHASE_1 = "Phase 1"
    PHASE_1_2 = "Phase 1/Phase 2"
    PHASE_2 = "Phase 2"
    PHASE_2_3 = "Phase 2/Phase 3"
    PHASE_3 = "Phase 3"
    PHASE_4 = "Phase 4"


class BiospecRetentionType(EnumBase):
    """Enumeration of the biospec-retention types."""

    NONE = "None Retained"
    SAMPLES_W_DNA = "Samples With DNA"
    SAMPLES_WO_DNA = "Samples Without DNA"
