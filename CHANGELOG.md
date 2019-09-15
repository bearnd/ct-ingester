## Changelog

### v0.11.1

- Updated `render_ingest.py` script with CLI arguments.

### v0.11.0

- Story CH1138: Add Sentry to `ct-ingester`.

### v0.10.0

- Story CH1096: Switch `ct-ingester` Git deployment to GitLab.com.

### v0.9.2

Story No. 905: Implement an automatic facility canonicalisation through Google:

- Replaced the Google Maps API key with a new and encrypted key.

### v0.9.1

Story No. 905: Implement an automatic facility canonicalisation through Google:

- Updated Ansible role to cron the canonicalization of recent facilities.
- Updated query in `find_recent_unmatched_facilities` function.


### v0.9.0

Story No. 905: Implement an automatic facility canonicalisation through Google:

- Added TOML configuration file with `black` settings.
- Moved shared functionality into `utils.py`.
- Added new script to match recently updated yet unmatched facilities against a canonical facility.

### v0.8.0

Issue No. 311: psycopg2.IntegrityError: update or delete on table "arm_groups" violates foreign key constraint "fk_intervention_arm_groups_arm_group_id_arm_groups" on table "intervention_arm_groups":

- Updated the `delete_existing_arm_groups` method to delete arm-groups properly without violating referential integrity.

### v0.7.0

- Updated the Ansible role and added a task to create a cronjob that will trigger an hourly ingestion of new clinical-trials as they appear in the RSS feed.

### v0.6.0

Issue No. 206: Populate canonical facilities:

- Added script to read previously backed up canonical facility information and port it to a new DB.
- Updated Ansible role configuration variables.

Issue No. 7: Automatize the ingestion of clinicaltrials.gov data:

- Updated dependencies.
- Added a new `RetrieverCtRss` class that retrieves the latest clinical-trials through the RSS feed.
- Updated the `ParserXmlClinicalStudy` class and added a new` parse_string` method that parses an XML study directly from a string.
- Updated the main sentinel to run the ingester in RSS mode.

### v0.5.0

Issue No. 184:

- Updated the Ansible configuration so that the local PG database has all required schemata.
- Updated the makefile to properly run unit-tests and coverage
- Updated existing clinical-trial asset files and added new ones.
- Added new unit-tests.
- Added a new `parse_ipd_info_types` method to parse the 1-N IPD info types for patient-data records.
- Updated the `parse_patient_data` method to include the new fields introduced in the 2019 schema.
- Updated the various calls to renamed IODI methods.
- Added a new `delete_existing_study_secondary_ids` method to the `IngesterDocumentClinicalTrial` class and also updated the `ingest` method to store multiple secondary IDs per study after deleting any existing ones.
- Added a new `delete_existing_pata_data_ipd_info_types ` method to the `IngesterDocumentClinicalTrial` class and also updated the `ingest_patient_data` and `ingest` methods to store the newly introduced patient-data fields as well as the 1-N IPD info types.

Issue No. 200:

- Removed the `ingest_mesh_term ` method and updated the `ingest` method of the `IngesterDocumentClinicalTrial` class to retrieve the ID of a pre-stored MeSH descriptor and store it against the ingested study.

### v0.4.2

- Fixed bug that precluded `StudyDocs` records from being populated.

### v0.4.1

Issue No. 1: Improper textblock whitespace sanitization:

- Updated the `_etb` method of the `ParserXmlClinicaStudy` class and removed the whitespace sanitization operation as it was breaking the format of long text-blocks.

### v0.4.0

- Moved the `find_facility_google_place` function from `utils.py` to `retrievers.py`.
- Added a new `get_place_details` function to `retrievers.py` to retrieve the details for a google place through its ID.
- Renamed the script under `populate_facilities_canonical.py` and updated to only retrieve and store the Google Place ID for facilities without that info.
- Added a new script to retrieve and populate the details for canonical facilities that have a Google Place ID but no country and therefore no details.
- Added a new script to copy Google Place details from facilities to affiliations.
- Added a new script to populate the `study_facilities` table.

### v0.3.1

- Made fixes to the `find_facility_google_place` function.
- Added a new `chunk_generator` function to chunk a generator.
- Ansible role bug fixes.
- As this script will now be exclusively populating the Google Place ID for the different facilities I commented out the majority of the code and added multiprocessing to speed up the process.
- Updated the multiprocessing pool used in `populate` to use 50 processes instead of 10.

### v0.3.0

- Refactored and cleaned-up Ansible role adding the ability to provide the service user with access to the PostgreSQL schemata created for local-testing.
- Updated the unit-tests.
- Updated Python dependencies.
- Added a new `retrievers.py` module with a `RetrieverGoogleMaps` class that can be used to perform place-search and place-details queries against the Google Place API.
- Updated the Ansible configuration and added the Google Maps API key.
- Added a new `find_facility_google_place` function to find a matching Google Place for a `Facility` record object in an iterative manner.
- Added a new script to proccess existing facilities and find and store canonicalised facilities.

### v0.2.3

- Updated `.gitignore`.
- Updated the `parse_eligibility` method of the `ParseXmlClinicalStudy` class to replace `N/A` values under `minimum_age` and `maximum_age` with `None`.

### v0.2.2

- `ingesters.py`: Fixed bug in the `delete_existing_protocol_outcomes` method of the `IngesterDocumentClinicalTrial` class where the records were being deleted in the wrong order causing foreign-key constraints to fail.
- `ingesters.py`: Fixed bug in the `delete_existing_study_docs` method of the `IngesterDocumentClinicalTrial` class where the records were being deleted in the wrong order causing foreign-key constraints to fail.
- `ingesters.py`: Fixed bug in the `delete_existing_arm_groups` method of the `IngesterDocumentClinicalTrial` class where the records were being deleted in the wrong order in addition to having missed `InterventionArmGroup` records causing foreign-key constraints to fail.
- Added another clinical-trial document to the test assets and extended tests to include it.

### v0.2.1

- `ingesters.py`: Fixed import bug.

### v0.2.0

Port ORM and DAL to `fightfor-orm`:
- Ported all ORM and DAL modules and classes to the `fightfor-orm` project.
- Changed the `fform` imports to fit the updated package.
- Updated the `fightfor-orm` dependency entry to use a Gitlab token.
- Fixed bugs in the Ansible tasks.
- Renamed the database name to `fightfor`.
- `env.py`: Updated the `run_migrations_online` function to account for the schema name.
- Replaced the multiple Alembic migration files with a new one in order to account for the schema name.
- Ansible related configuration changes.

Issue No.3: Add ansible-vault secret-management to Ansible roles:
- Updated Python dependencies.
- Updated the Ansible variables with the encrypted versions of the SQL DB passwords instead of plain-text ones.
- `Vagrantfile`: Updated the Ansible provisioning settings to use the Ansible Vault password.
- Added an ignore for the `.ansible-vault-password` file.
- `Vagrantfile`: Fixed bug.
- `README.md`: Added instructions regarding Ansible Vault.
- Updated Python dependencies.

Issue No.16: Iterative XML element parsing skips first element:
- `parsers.py`: Fixed bug in the iterative XML element parsing in the `generate_xml_elements` method of the `ParserXmlBase` class where the first element was always skipped.
- Fixed issue with Ansible Vault variables.
- Removed the Alembic configuration and revisions as this functionality was ported to `fightfor-alembic`.

Issue No.2: Improper unique-ing and study-updates:
- Updated Python dependencies.
- Updated Ansible role to install the latest version of Python dependencies so that the latest version of `fform` will be installed. The rest of the dependencies will still behave the same as they’re pinned.
- `excs.py`: Removed unused exception classes.
- `parsers.py`: Fixed bugs in the imports.
- `ingesters.py`: Replaced IODI calls with IODU calls to relfect the latest version of `fightfor-orm`.
- `ingesters.py`: Updated the `IngesterDocumentClinicalTrial` class and added new methods to delete records linked to a `Study` record via association tables as well as the association records themselves when the linked records cannot be uniquely identified and would cause duplication if re-inserted. These methods are now called during the ingestion points of those records in the `ingest` method.
- `ingesters.py`: Updated the `IngesterDocumentClinicalTrial` class and added a `update_study_fk` which updates a foreign-key attribute in a `Study` record linked a record that cannot be uniquely identified. Once the FK is updated the old record is deleted. Calls to this method have been added in the `ingest` method.
- Removed unit-test placeholder module.
- Added a new `tests/bases.py` module with a unit-test base-class.
- Added unit-test asset modules.
- Added a new `tests/test_parsers.py` module with unit-tests for the `ParserXmlBase` class.
- Added basic integration tests testing the parsing and ingestion of entire clinical-study XML documents.

### v0.1.5

- `orm.py`: Updated the `Facility` class and set the `city` and `country` to nullable as the encompassing `<address>` element does not have to be defined under a `<facility>`.
- Added Alembic migration file.

### v0.1.4

- `orm.py`: Updated the `Investigator` class and set the `role` to nullable as it is not always defined.
- Added Alembic migration file.

### v0.1.3

- `orm.py`: Updated the `ResponsibleParty` class and set the `responsible_party_type` to nullable as it is not defined in older records.

### v0.1.2

- Added a new `scripts` package.
- Added a new script that simple iterates over the clinical-trials XML dump and creates ingestion commands.
- `orm.py`: Fixed the non-nullable field argument for `enrollment_id` under the `Study` class.
- Added Alembic migration file.

### v0.1.1

- `orm.py`:
    - Fixed the nullable state of several fields that were set incorrectly.
    - Added a couple more relationships.
- Added a new Alembic migration file.

### v0.1.0

- Initial release.
