#!/bin/bash

echo "Which is the chromedriver version you want to install?"
echo "Check the first 7 numbers of your Chrome browser, then visit https://chromedriver.chromium.org/downloads."
read VERSION
echo "You selected the version "$VERSION
echo "Downloading the correct version..."
rm driver
mkdir driver
cd driver
PLATFORM=linux64 # Change this line if You're using other platform
#VERSION=$(curl http://chromedriver.storage.googleapis.com/LATEST_RELEASE)
curl http://chromedriver.storage.googleapis.com/$VERSION/chromedriver_$PLATFORM.zip -LOk
unzip chromedriver_*
rm chromedriver_*
cd ..
