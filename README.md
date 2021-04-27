# Tableau Backup Script

This script is intended to download all workbooks, datasources and flows from a Tableau Site to your computer. I built it to easily backup assets from my Tableau Online sandbox instance.

The code has been built from the login sample provided by Tableau's TSC samples: <https://github.com/tableau/server-client-python/tree/master/samples>

For more information on installing and using TSC, see the documentation:
<https://tableau.github.io/server-client-python/docs/>

## Usage
`usage: backup.py [-h] --server SERVER
                --target TARGET
                (--username USERNAME | --token-name TOKEN_NAME)
                [--sitename SITENAME]`