# SLR Snowballing Automation (Selenium)
This repository provides artifacts for automating the snowballing search.

# Before starting 

### Download the correct Selenium Chrome Driver and install the requirements.
```sh
$ ./download-driver.sh
$ pip install -r requirements.txt
```

# Provide a list of primary studies link.
```
./primary_studies.txt
```
# Set up Zotero stuff.

Follow [this](https://pypi.org/project/pyzotero/) to get you IDs and Keys. Everything must be set in the *configuration.cfg* file.
Note that you need to create a group only for Snowballing.

# Run the crawler.
```
python3 snowballing_crawler.py
```
