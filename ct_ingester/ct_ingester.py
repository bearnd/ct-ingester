#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Main module."""

import os
import argparse

from ct_ingester.parsers import ParserXmlClinicaStudy
from fform.dals_ct import DalClinicalTrials
from ct_ingester.ingesters import IngesterDocumentClinicalTrial
from ct_ingester.retrievers import RetrieverCtRss
from ct_ingester.config import import_config
from ct_ingester.sentry import initialize_sentry


def load_config(args):
    if args.config_file:
        cfg = import_config(fname_config_file=args.config_file)
    elif "CT_INGESTER_CONFIG" in os.environ:
        fname_config_file = os.environ["CT_INGESTER_CONFIG"]
        cfg = import_config(fname_config_file=fname_config_file)
    else:
        msg_fmt = "Configuration file path not defined."
        raise ValueError(msg_fmt)

    return cfg


def main(args):
    cfg = load_config(args=args)

    # Initialize the Sentry agent.
    initialize_sentry(cfg=cfg)

    dal = DalClinicalTrials(
        sql_username=cfg.sql_username,
        sql_password=cfg.sql_password,
        sql_host=cfg.sql_host,
        sql_port=cfg.sql_port,
        sql_db=cfg.sql_db,
    )
    ingester = IngesterDocumentClinicalTrial(dal=dal)
    parser = ParserXmlClinicaStudy()

    if arguments.mode == "file":
        for filename in args.filenames:
            clinical_study = parser.parse(filename_xml=filename)
            ingester.ingest(doc=clinical_study)
    elif arguments.mode == "rss":
        retriever = RetrieverCtRss()
        for xml_string in retriever.get_new_studies():
            clinical_study = parser.parse_string(xml_string=xml_string)
            ingester.ingest(doc=clinical_study)


# main sentinel
if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser(
        description=("ct-ingester: ClinicalTrials.gov XML dump parser and SQL "
                     "ingester.")
    )
    argument_parser.add_argument(
        "filenames",
        nargs="*",
        help="ClinicalTrials.gov XML files to ingest.",
    )
    argument_parser.add_argument(
        "--mode",
        dest="mode",
        help="Ingestion mode",
        choices=[
            "rss",
            "file",
        ],
        required=False,
        default="file"
    )
    argument_parser.add_argument(
        "--config-file",
        dest="config_file",
        help="configuration file",
        required=False
    )
    arguments = argument_parser.parse_args()

    main(args=arguments)
