# coding=utf-8

import os

path = "/mnt/Downloads/_DUMP/download_station/AllPublicXML/"
fname_config = "/etc/ct-ingester/ct-ingester.json"
fname_script = "ingest_ct.sh"

# Collect subdirectories skipping files alongside them.
subdirs = [os.path.join(path, d) for d in os.listdir(path) if "." not in d]

# Collect all XML files from the various subdirectories.
fnames = []
for subdir in subdirs:
    for fname in os.listdir(subdir):
        if fname.endswith(".xml"):
            fnames.append(os.path.join(subdir, fname))

tmpl = ("python -m ct_ingester.ct_ingester {fname_xml} "
        "--config-file='{fname_config}'")

# Write out the ingestion template file.
with open(fname_script, "w") as fout:
    for fname in fnames:
        line = tmpl.format(fname_xml=fname, fname_config=fname_config)
        fout.write(line)
        fout.write("\n")
        fout.flush()
