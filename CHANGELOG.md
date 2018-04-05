## Changelog

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
