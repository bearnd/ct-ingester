# coding=utf-8

import unittest

from fform.dals_ct import DalClinicalTrials
from fform.orm_base import Base

from ct_ingester.ingesters import IngesterDocumentClinicalTrial
from ct_ingester.parsers import ParserXmlClinicaStudy
from ct_ingester.config import import_config


class TestBase(unittest.TestCase):
    """Unit-test base-class."""

    def setUp(self):
        """Instantiates the DAL and creates the schema."""

        # Load the configuration.
        self.cfg = import_config(
            fname_config_file="/etc/ct-ingester/ct-ingester-test.json",
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
