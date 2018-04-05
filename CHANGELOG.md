## Changelog

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
