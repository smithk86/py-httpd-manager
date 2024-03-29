#!/bin/bash

# set httpd versions to test
declare -a HTTPD_VERSIONS=("2.4.20" "2.4.33" "2.4.37" "2.4.39" "2.4.41" "2.4.48" "2.4.53")

for VERSION in "${HTTPD_VERSIONS[@]}"; do
    echo "------------------------------------"
    echo "      testing httpd v${VERSION}"
    echo "------------------------------------"
    poetry run pytest --httpd-version="${VERSION}"
done
