# SLR Snowballing Automation (Selenium+Zotero)
This repository provides artifacts for automating the snowballing search.

# Before Starting 

### Download the Correct Selenium Chrome Driver and Install the Requirements.
```sh
$ ./download-driver.sh
$ pip install -r requirements.txt
```

# Provide a List of Primary Studies
```
./primary_studies.txt
```
# Set up Zotero stuff.

Follow [this](https://pypi.org/project/pyzotero/) to get you IDs and Keys. Everything must be set in the *configuration.cfg* file.
Note that you need to create a group only for Snowballing.

# Run the Crawler
```
python3 snowballing_crawler.py
```
