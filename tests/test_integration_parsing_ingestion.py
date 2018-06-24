# coding=utf-8

import unittest

from lxml import etree
from fform.dals_ct import DalClinicalTrials
from fform.orm_base import Base

from ct_ingester.ingesters import IngesterDocumentClinicalTrial
from ct_ingester.parsers import ParserXmlClinicaStudy
from ct_ingester.config import import_config

from tests.assets.NCT00000102 import document as doc_nct00000102
from tests.assets.NCT00000112 import document as doc_nct00000112


class DalTestBase(unittest.TestCase):

    def setUp(self):
        """Instantiates the DAL and creates the schema."""

        # Load the configuration.
        self.cfg = import_config(
            fname_config_file="/etc/ct-ingester/ct-ingester.json",
        )

        self.dal = DalClinicalTrials(
            sql_username=self.cfg.sql_username,
            sql_password=self.cfg.sql_password,
            sql_host=self.cfg.sql_host,
            sql_port=self.cfg.sql_port,
            sql_db=self.cfg.sql_db
        )

        self.ingester = IngesterDocumentClinicalTrial(dal=self.dal)

        self.parser = ParserXmlClinicaStudy()

        # Drop any schema remnants and recreate it.
        Base.metadata.drop_all(self.dal.engine)
        Base.metadata.create_all(self.dal.engine)

    def tearDown(self):
        """Drops the DB schema created during setup."""

        Base.metadata.drop_all(self.dal.engine)

    def test_integration_ingest_nct00000102(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting a the NCT00000102 clinical-trial XML document
        asserting that parsing and ingestion were successful."""

        # Perform an XML parsing of the document.
        element = etree.fromstring(text=doc_nct00000102)

        # Parse the clinical-trial XML element.
        clinical_study = self.parser.parse_clinical_study(element=element)

        # Ingest the parsed clinical-trial document.
        obj_id = self.ingester.ingest(doc=clinical_study)

        self.assertEqual(obj_id, 1)

    def test_integration_ingest_doc_nct00000112(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting a the NCT00000112 clinical-trial XML document
        asserting that parsing and ingestion were successful."""

        # Perform an XML parsing of the document.
        element = etree.fromstring(text=doc_nct00000112)

        # Parse the clinical-trial XML element.
        clinical_study = self.parser.parse_clinical_study(element=element)

        # Ingest the parsed clinical-trial document.
        obj_id = self.ingester.ingest(doc=clinical_study)

        self.assertEqual(obj_id, 1)
