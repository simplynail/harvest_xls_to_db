# harvest_xls_to_db
*Set of scripts to harvest data from multiple MS Excel files from filesystem that match the criteria.  
Then contents of the spreadsheets are harvested into the database (SQLite).  
After db is filled, the data can be used to aggregate and visualise data as interactive charts*

Developed in Python (with Threading)

MS Excel access lib: openpyxl  
ORM lib: pony  
Charting lib: bokeh  
Reports generation lib: jinja2 + HTML