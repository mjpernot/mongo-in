# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [0.1.1] - 2025-05-09

### Fixed
- process_insert: Replaced json.load with ast.literal_eval call and also further checks on if data object is a dictionary.


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
