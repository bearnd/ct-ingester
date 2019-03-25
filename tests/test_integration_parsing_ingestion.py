# coding=utf-8

from lxml import etree

from tests.bases import TestBase
from tests.assets.NCT00000102 import document as doc_nct00000102
from tests.assets.NCT00000112 import document as doc_nct00000112
from tests.assets.NCT00000113 import document as doc_nct00000113
from tests.assets.NCT00000264 import document as doc_nct00000264
from tests.assets.NCT00005057 import document as doc_nct00005057
from tests.assets.NCT01782859 import document as doc_nct01782859
from tests.assets.NCT01533532 import document as doc_nct01533532
from tests.assets.NCT03825406 import document as doc_nct03825406
from tests.assets.NCT03829579 import document as doc_nct03829579
from tests.assets.NCT03830281 import document as doc_nct03830281
from tests.assets.NCT03832621 import document as doc_nct03832621
from tests.assets.NCT03834376 import document as doc_nct03834376
from tests.assets.NCT03835312 import document as doc_nct03835312
from tests.assets.NCT03835533 import document as doc_nct03835533
from tests.assets.NCT03835676 import document as doc_nct03835676
from tests.assets.NCT03835702 import document as doc_nct03835702


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

    def test_integration_ingest_doc_nct00000113(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT00000113 clinical-trial XML document
        asserting that parsing and ingestion were successful."""

        clinical_study = self._parse_sample(sample=doc_nct00000113)

        # Ingest the parsed clinical-trial document.
        obj_id = self.ingester.ingest(doc=clinical_study)

        self.assertEqual(obj_id, 1)

    def test_integration_ingest_doc_nct00000264(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT00000264 clinical-trial XML document
        asserting that parsing and ingestion were successful."""

        clinical_study = self._parse_sample(sample=doc_nct00000264)

        # Ingest the parsed clinical-trial document.
        obj_id = self.ingester.ingest(doc=clinical_study)

        self.assertEqual(obj_id, 1)

    def test_integration_ingest_doc_nct00005057(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT00005057 clinical-trial XML document
        asserting that parsing and ingestion were successful."""

        clinical_study = self._parse_sample(sample=doc_nct00005057)

        # Ingest the parsed clinical-trial document.
        obj_id = self.ingester.ingest(doc=clinical_study)

        self.assertEqual(obj_id, 1)

    def test_integration_ingest_doc_nct01782859(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT01782859 clinical-trial XML document
        asserting that parsing and ingestion were successful."""

        clinical_study = self._parse_sample(sample=doc_nct01782859)

        # Ingest the parsed clinical-trial document.
        obj_id = self.ingester.ingest(doc=clinical_study)

        self.assertEqual(obj_id, 1)

    def test_integration_ingest_doc_nct01533532(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT01533532 clinical-trial XML document
        asserting that parsing and ingestion were successful."""

        clinical_study = self._parse_sample(sample=doc_nct01533532)

        # Ingest the parsed clinical-trial document.
        obj_id = self.ingester.ingest(doc=clinical_study)

        self.assertEqual(obj_id, 1)

    def test_integration_ingest_doc_nct03825406(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT03825406 clinical-trial XML document
        asserting that parsing and ingestion were successful."""

        clinical_study = self._parse_sample(sample=doc_nct03825406)

        # Ingest the parsed clinical-trial document.
        obj_id = self.ingester.ingest(doc=clinical_study)

        self.assertEqual(obj_id, 1)

    def test_integration_ingest_doc_nct03829579(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT03829579 clinical-trial XML document
        asserting that parsing and ingestion were successful."""

        clinical_study = self._parse_sample(sample=doc_nct03829579)

        # Ingest the parsed clinical-trial document.
        obj_id = self.ingester.ingest(doc=clinical_study)

        self.assertEqual(obj_id, 1)

    def test_integration_ingest_doc_nct03830281(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT03830281 clinical-trial XML document
        asserting that parsing and ingestion were successful."""

        clinical_study = self._parse_sample(sample=doc_nct03830281)

        # Ingest the parsed clinical-trial document.
        obj_id = self.ingester.ingest(doc=clinical_study)

        self.assertEqual(obj_id, 1)

    def test_integration_ingest_doc_nct03832621(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT03832621 clinical-trial XML document
        asserting that parsing and ingestion were successful."""

        clinical_study = self._parse_sample(sample=doc_nct03832621)

        # Ingest the parsed clinical-trial document.
        obj_id = self.ingester.ingest(doc=clinical_study)

        self.assertEqual(obj_id, 1)

    def test_integration_ingest_doc_nct03834376(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT03834376 clinical-trial XML document
        asserting that parsing and ingestion were successful."""

        clinical_study = self._parse_sample(sample=doc_nct03834376)

        # Ingest the parsed clinical-trial document.
        obj_id = self.ingester.ingest(doc=clinical_study)

        self.assertEqual(obj_id, 1)

    def test_integration_ingest_doc_nct03835312(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT03835312 clinical-trial XML document
        asserting that parsing and ingestion were successful."""

        clinical_study = self._parse_sample(sample=doc_nct03835312)

        # Ingest the parsed clinical-trial document.
        obj_id = self.ingester.ingest(doc=clinical_study)

        self.assertEqual(obj_id, 1)

    def test_integration_ingest_doc_nct03835533(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT03835533 clinical-trial XML document
        asserting that parsing and ingestion were successful."""

        clinical_study = self._parse_sample(sample=doc_nct03835533)

        # Ingest the parsed clinical-trial document.
        obj_id = self.ingester.ingest(doc=clinical_study)

        self.assertEqual(obj_id, 1)

    def test_integration_ingest_doc_nct03835676(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT03835676 clinical-trial XML document
        asserting that parsing and ingestion were successful."""

        clinical_study = self._parse_sample(sample=doc_nct03835676)

        # Ingest the parsed clinical-trial document.
        obj_id = self.ingester.ingest(doc=clinical_study)

        self.assertEqual(obj_id, 1)

    def test_integration_ingest_doc_nct03835702(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT03835702 clinical-trial XML document
        asserting that parsing and ingestion were successful."""

        clinical_study = self._parse_sample(sample=doc_nct03835702)

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

    def test_integration_ingest_nct00000113_multiple(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT00000113 clinical-trial XML document
        multiple times."""

        clinical_study = self._parse_sample(sample=doc_nct00000113)

        # Ingest the parsed clinical-trial document 3 times.
        for _ in range(3):
            obj_id = self.ingester.ingest(doc=clinical_study)
            self.assertEqual(obj_id, 1)

    def test_integration_ingest_nct00000264_multiple(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT00000264 clinical-trial XML document
        multiple times."""

        clinical_study = self._parse_sample(sample=doc_nct00000264)

        # Ingest the parsed clinical-trial document 3 times.
        for _ in range(3):
            obj_id = self.ingester.ingest(doc=clinical_study)
            self.assertEqual(obj_id, 1)

    def test_integration_ingest_nct00005057_multiple(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT00005057 clinical-trial XML document
        multiple times."""

        clinical_study = self._parse_sample(sample=doc_nct00005057)

        # Ingest the parsed clinical-trial document 3 times.
        for _ in range(3):
            obj_id = self.ingester.ingest(doc=clinical_study)
            self.assertEqual(obj_id, 1)

    def test_integration_ingest_nct01782859_multiple(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT01782859 clinical-trial XML document
        multiple times."""

        clinical_study = self._parse_sample(sample=doc_nct01782859)

        # Ingest the parsed clinical-trial document 3 times.
        for _ in range(3):
            obj_id = self.ingester.ingest(doc=clinical_study)
            self.assertEqual(obj_id, 1)

    def test_integration_ingest_nct01533532_multiple(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT01533532 clinical-trial XML document
        multiple times."""

        clinical_study = self._parse_sample(sample=doc_nct01533532)

        # Ingest the parsed clinical-trial document 3 times.
        for _ in range(3):
            obj_id = self.ingester.ingest(doc=clinical_study)
            self.assertEqual(obj_id, 1)

    def test_integration_ingest_nct03825406_multiple(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT03825406 clinical-trial XML document
        multiple times."""

        clinical_study = self._parse_sample(sample=doc_nct03825406)

        # Ingest the parsed clinical-trial document 3 times.
        for _ in range(3):
            obj_id = self.ingester.ingest(doc=clinical_study)
            self.assertEqual(obj_id, 1)

    def test_integration_ingest_nct03829579_multiple(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT03829579 clinical-trial XML document
        multiple times."""

        clinical_study = self._parse_sample(sample=doc_nct03829579)

        # Ingest the parsed clinical-trial document 3 times.
        for _ in range(3):
            obj_id = self.ingester.ingest(doc=clinical_study)
            self.assertEqual(obj_id, 1)

    def test_integration_ingest_nct03832621_multiple(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT03832621 clinical-trial XML document
        multiple times."""

        clinical_study = self._parse_sample(sample=doc_nct03832621)

        # Ingest the parsed clinical-trial document 3 times.
        for _ in range(3):
            obj_id = self.ingester.ingest(doc=clinical_study)
            self.assertEqual(obj_id, 1)

    def test_integration_ingest_nct03834376_multiple(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT03834376 clinical-trial XML document
        multiple times."""

        clinical_study = self._parse_sample(sample=doc_nct03834376)

        # Ingest the parsed clinical-trial document 3 times.
        for _ in range(3):
            obj_id = self.ingester.ingest(doc=clinical_study)
            self.assertEqual(obj_id, 1)

    def test_integration_ingest_nct03835312_multiple(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT03835312 clinical-trial XML document
        multiple times."""

        clinical_study = self._parse_sample(sample=doc_nct03835312)

        # Ingest the parsed clinical-trial document 3 times.
        for _ in range(3):
            obj_id = self.ingester.ingest(doc=clinical_study)
            self.assertEqual(obj_id, 1)

    def test_integration_ingest_nct03835533_multiple(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT03835533 clinical-trial XML document
        multiple times."""

        clinical_study = self._parse_sample(sample=doc_nct03835533)

        # Ingest the parsed clinical-trial document 3 times.
        for _ in range(3):
            obj_id = self.ingester.ingest(doc=clinical_study)
            self.assertEqual(obj_id, 1)

    def test_integration_ingest_nct03835676_multiple(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT03835676 clinical-trial XML document
        multiple times."""

        clinical_study = self._parse_sample(sample=doc_nct03835676)

        # Ingest the parsed clinical-trial document 3 times.
        for _ in range(3):
            obj_id = self.ingester.ingest(doc=clinical_study)
            self.assertEqual(obj_id, 1)

    def test_integration_ingest_nct03835702_multiple(self):
        """Tests the `ingest` method of the `IngesterDocumentClinicalTrial`
        class by ingesting the NCT03835702 clinical-trial XML document
        multiple times."""

        clinical_study = self._parse_sample(sample=doc_nct03835702)

        # Ingest the parsed clinical-trial document 3 times.
        for _ in range(3):
            obj_id = self.ingester.ingest(doc=clinical_study)
            self.assertEqual(obj_id, 1)
