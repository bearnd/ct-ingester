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
