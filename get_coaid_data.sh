#!/bin/bash

# download CoAID
git clone https://github.com/cuilimeng/CoAID
# cd into directory
cd CoAID/
# move files to parent
mv 05-01-2020/* .
# delete folders
rm -rf 05-01-2020 07-01-2020 09-01-2020 11-01-2020
# return to directory
cd ..
