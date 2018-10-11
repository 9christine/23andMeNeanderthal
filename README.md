# 23andMe Neanderthal Variant Demo
Command-line app retrieves genetic data from the 23andMe API and analyzes for Neanderthal variant matches in demo user.
[Raw genetic data API is no longer supported.](https://api.23andme.com/)


## System requirements
- Python 3 (Run `brew install python` if needed)
- Pip (Run `python get-pip.py` if needed)


## Create virtual environment and run program
- python3 -m venv venv
- source venv/bin/activate
- make


## API reference
https://api.23andme.com


## Performance
App currently downloads a limited amount of data from the 23andMe API to reduce run-time. Adjust LIMIT (currently 5000) in manage.py to control number of records retrieved.


## Future development
- Download complete data for each accession_id by utilizing the "next" field to call data in batches to completion.
- Improve run-time and client experience by asynchronously running data processing functions while API calls continue.
- Improve database schema and eliminate data redundancies by creating relation between neanderthal_variants and neanderthal_accessions on accession_id.
- Separate functions in manage.py into their own file.
- Investigate filtering on API calls to retrieve only records which contain dosage > 0 (currently retrieving all data for accession_id, then inserting into database only those records with dosage > 0).
- Create user interface for web app, with graphical status updates during processing.
- Include option (with OAuth) for user to login to their own 23andMe account to obtain personalized data.


## Author
Christine Taylor
