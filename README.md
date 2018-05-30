# 23andMe Neanderthal Variant Demo
Command-line program which retrieves genetic data from the 23andMe API and analyzes for Neanderthal variant matches in demo user.


## System requirements
- Python 3 (brew install python)
- Pip (python get-pip.py)


## Create virtual environment and run program
- python3 -m venv venv
- source venv/bin/activate
- make


## Performance
Demo currently downloads a limited amount of data from the 23andMe API to reduce run-time. Adjust LIMIT (currently 5000) in manage.py to control number of records retrieved.


## Future development
1) Download complete data for each accession_id by utilizing the "next" field to call data in batches to completion.

2) Improve run-time and client experience by asynchronously running data processing functions while API calls continue.

3) Improve database schema and eliminate data redundancies by creating relation between neanderthal_variants and neanderthal_accessions on accession_id.

4) Separate functions in manage.py into their own file.

5) Investigate filtering on API calls to retrieve only records which contain dosage > 0 (currently retrieving all data for accession_id, then inserting into database only those records with dosage > 0).

6) Create user interface for web app, with graphical status updates during processing.

7) Include option (with OAuth) for user to login to their own 23andMe account to obtain personalized data.


## Author
Christine Taylor
christine.e.taylor.sf@gmail.com
