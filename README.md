# Qualys VM ETL

Qualys HostAsset and VM API parser
Parse the Detection and Hostasset API output

## Requirments

1. python 3.8+
2. [pip package manager](https://pip.pypa.io/en/stable/installation/)

### Install packages with pip: -r requirements.txt
pip install -r requirements.txt
### Edit config
Rename the file config.xml.sample to config.xml
Change the **BASE_URL** to the correct platfrom. See [platform-identification](https://www.qualys.com/platform-identification/)
Change the **USERNAME** and **PASSWORD** information

SQL Will work but the driver needs to be detected by the user.
In most cases please just keep the flag **USE_SQL** set to ***false***

## Release Notes
1.0.0 - Innitial release;

1.0.1 - support for port & protocol data,installed software information;

1.1.1 - Host component support multiple requests;

1.1.2 - Support to filter host based on tags;

1.1.3 - use DAYS_OF_STATS to spacify the stats durnation;

1.1.3.1 - bug fix;

1.2.0 - PC, downloading the latest CSV report
#### For more information please see
<https://www.qualys.com/docs/qualys-api-vmpc-user-guide.pdf>
