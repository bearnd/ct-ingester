## Changelog

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
