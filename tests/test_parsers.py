# coding=utf-8

from lxml import etree

from tests.bases import TestBase


class ParserXmlBaseTest(TestBase):

    def test_et(self):
        """Tests the `_et` method of the `ParserXmlBase` class."""

        element = etree.Element("some_element")
        element.text = "some text"

        self.assertEqual(self.parser._et(element), "some text")

    def test_et_whitespace(self):
        """Tests the `_et` method of the `ParserXmlBase` class when the
        element text has whitespace around which should be stripped."""

        element = etree.Element("some_element")
        element.text = "   some text    "

        self.assertEqual(self.parser._et(element), "some text")

    def test_et_empty_string(self):
        """Tests the `_et` method of the `ParserXmlBase` class when the
        element text is an empty string."""

        element = etree.Element("some_element")
        element.text = ""

        self.assertIsNone(self.parser._et(element))

    def test_et_text_none(self):
        """Tests the `_et` method of the `ParserXmlBase` class when the
        element has no text."""

        element = etree.Element("some_element")

        self.assertIsNone(self.parser._et(element))

    def test_et_none(self):
        """Tests the `_et` method of the `ParserXmlBase` class when the
        element is undefined."""

        self.assertIsNone(self.parser._et(None))

    def test_eav(self):
        """Tests the `_eav` method of the `ParserXmlBase` class."""

        element = etree.Element(
            "some_element",
            attrib={
                "some_attribute": "some_value"
            }
        )

        result_eval = self.parser._eav(element, "some_attribute")

        self.assertEqual(result_eval, "some_value")

    def test_eav_empty_string(self):
        """Tests the `_eav` method of the `ParserXmlBase` class when the value
        of the attribute is an empty string."""

        element = etree.Element(
            "some_element",
            attrib={
                "some_attribute": ""
            }
        )

        result_eval = self.parser._eav(element, "some_attribute")

        self.assertIsNone(result_eval)

    def test_eav_none(self):
        """Tests the `_eav` method of the `ParserXmlBase` class when the
        element is undefined."""

        result_eval = self.parser._eav(None, "some_attribute")

        self.assertIsNone(result_eval)


class ParserXmlClinicalStudy(TestBase):

    def test_yn_to_bool_yes(self):
        """ Tests the `_yn_to_bool` method of the `ParserXmlClinicaStudy`
            class when the element value is `Υes`.
        """

        element = etree.Element("some_element")
        element.text = "Yes"

        self.assertEqual(self.parser._yn_to_bool(element), True)

    def test_yn_to_bool_no(self):
        """ Tests the `_yn_to_bool` method of the `ParserXmlClinicaStudy`
            class when the element value is `No`.
        """

        element = etree.Element("some_element")
        element.text = "No"

        self.assertEqual(self.parser._yn_to_bool(element), False)

    def test_yn_to_bool_none(self):
        """ Tests the `_yn_to_bool` method of the `ParserXmlClinicaStudy`
            class when the element is undefined.
        """

        self.assertEqual(self.parser._yn_to_bool(None), None)

    def test_etb(self):
        """ Tests the `_etb` method of the `ParserXmlClinicaStudy` class with a
            simple element with extra whitespace to test its sanitization.
        """

        element = etree.Element("some_element")
        element_tb = etree.Element("textblock")
        element_tb.text = "   test\ntest  test\n\ntest   "
        element.append(element_tb)

        self.assertEqual(self.parser._etb(element), "test\ntest  test\n\ntest")

    def test_etb_none(self):
        """ Tests the `_etb` method of the `ParserXmlClinicaStudy` class when
            the element is `None`.
        """

        self.assertEqual(self.parser._etb(None), None)

    def test_etb_textblock_none(self):
        """ Tests the `_etb` method of the `ParserXmlClinicaStudy` class when
            the element's textblock element is `None`.
        """

        element = etree.Element("some_element")

        self.assertEqual(self.parser._etb(element), None)

    def test_etb_textblock_empty(self):
        """ Tests the `_etb` method of the `ParserXmlClinicaStudy` class when
            the element's textblock element is an empty string.
        """

        element = etree.Element("some_element")
        element_tb = etree.Element("textblock")
        element_tb.text = ""
        element.append(element_tb)

        self.assertEqual(self.parser._etb(element), None)

    def test_etb_textblock_whitespace(self):
        """ Tests the `_etb` method of the `ParserXmlClinicaStudy` class when
            the element's textblock element only consists of whitespace.
        """

        element = etree.Element("some_element")
        element_tb = etree.Element("textblock")
        element_tb.text = " "
        element.append(element_tb)

        self.assertEqual(self.parser._etb(element), None)
