# coding=utf-8

import argparse
import os


def render_ingest_file(data_directory: str, config_file: str, output_file: str):

    # Collect subdirectories skipping files alongside them.
    subdirs = [
        os.path.join(data_directory, d)
        for d in os.listdir(data_directory)
        if "." not in d
    ]

    # Collect all XML files from the various subdirectories.
    fnames = []
    for subdir in subdirs:
        for fname in os.listdir(subdir):
            if fname.endswith(".xml"):
                fnames.append(os.path.join(subdir, fname))

    # Write out the ingestion template file.
    with open(output_file, "w") as fout:
        # Write `set -e` to stop at each error.
        fout.write("set -e\n")
        for fname in fnames:
            line = (
                f"python -m ct_ingester.ct_ingester {fname} "
                f"--config-file='{config_file}'"
            )
            fout.write(line)
            fout.write("\n")
            fout.flush()


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser(
        description=(
            "ct-ingester: ClinicalTrials.gov XML dump parser and SQL "
            "ingester."
        )
    )
    argument_parser.add_argument(
        "--data-directory",
        dest="data_directory",
        help="ClinicalTrials data directory",
        required=True,
    )
    argument_parser.add_argument(
        "--config-file",
        dest="config_file",
        help="configuration file",
        required=True,
    )
    argument_parser.add_argument(
        "--output-file", dest="output_file", help="Output file", required=True
    )
    arguments = argument_parser.parse_args()

    render_ingest_file(
        data_directory=arguments.data_directory,
        config_file=arguments.config_file,
        output_file=arguments.output_file,
    )
