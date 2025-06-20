# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [0.1.2] - 2025-06-03
- Updated to work with pymongo v4.X
- Updated mongo-lib to v4.5.2

### Fixed
- insert_mongo: Replaced get_hack with get_time and changed timeformat to include time and include database and table name as part of the failed insert file name.

### Changed
- main: Added flavor_id for the program lock.
- run_program: Replaced create_hack with create_time and get_hack with get_time.
- Documentation changes.


## [0.1.1] - 2025-05-09

### Fixed
- process_insert: Replaced data_conversion call and also added additional checks on the data type of the object being converted.

### Added
- data_conversion: Convert data.


## [0.1.0] - 2025-04-22
Alpha Release
- Updated python-lib v4.0.1
- Added option to remove file after insert is completed.

### Changed
- insert_data: Refactored function to handle archiving and removing files and move failed inserts into error directory.

### Removed
- Removed support for Mongo 4.2


## [0.0.2] - 2025-03-11
- Added support for Mongo 7.0
- Updated mongo-libs to v4.5.1

### Fixed
- Fixed pre-header where to determine which python version to use.


## [0.0.1] - 2025-01-31
- Initial program.
