# coding=utf-8

from lxml import etree

from tests.bases import TestBase
from tests.assets.NCT00000102 import document as doc_nct00000102
from tests.assets.NCT00000112 import document as doc_nct00000112


class TestIntegrationParsingIngestion(TestBase):
    """Full integration tests including parsing and ingestion."""

    def _parse_sample(self, sample):
        """Parses a clinical-trial XML document and returns the parsed
        document."""

        # Perform an XML parsing of the document.
        element = etree.fromstring(text=sample)

        # Parse the clinical-trial XML element.
        clinical_study = self.parser.parse_clinical_study(element=element)

        return clinical_study

    def test_integration_ingest_nct00000102(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT00000102 clinical-trial XML document
        asserting that parsing and ingestion were successful."""

        clinical_study = self._parse_sample(sample=doc_nct00000102)

        # Ingest the parsed clinical-trial document.
        obj_id = self.ingester.ingest(doc=clinical_study)

        self.assertEqual(obj_id, 1)

    def test_integration_ingest_doc_nct00000112(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT00000112 clinical-trial XML document
        asserting that parsing and ingestion were successful."""

        clinical_study = self._parse_sample(sample=doc_nct00000112)

        # Ingest the parsed clinical-trial document.
        obj_id = self.ingester.ingest(doc=clinical_study)

        self.assertEqual(obj_id, 1)

    def test_integration_ingest_nct00000102_multiple(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT00000102 clinical-trial XML document
        multiple times."""

        clinical_study = self._parse_sample(sample=doc_nct00000102)

        # Ingest the parsed clinical-trial document 3 times.
        for _ in range(3):
            obj_id = self.ingester.ingest(doc=clinical_study)
            self.assertEqual(obj_id, 1)

    def test_integration_ingest_nct00000112_multiple(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT00000112 clinical-trial XML document
        multiple times."""

        clinical_study = self._parse_sample(sample=doc_nct00000112)

        # Ingest the parsed clinical-trial document 3 times.
        for _ in range(3):
            obj_id = self.ingester.ingest(doc=clinical_study)
            self.assertEqual(obj_id, 1)
