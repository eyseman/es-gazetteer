# es-gazetteer

### DISCLAIMER
This repository is a modified mirror copy of [es-geonames](https://github.com/openeventdata/es-geonames) by the [Open Event Data Alliance](https://github.com/openeventdata) under the MIT license.

*Major modifications*
- elevated elasticsearch to v7.6.1
- modified index mapping to provide compatibility with elasticsearch v7
- added multi-threading support to the import script to increase speed

### INSTALLATION AND REQUIREMENTS
*STEP 0) OPTIONAL - Setup Python "Virtual Environment"*
```
python3 -m venv es-gazetteer_env
source es-gazetteer_env/bin/activate
```
STEP 1) Download the source code from Github
```
git clone https://github.com/eyseman/es-gazetteer
cd es-gazetteer
```
STEP 2) Install required libraries
```
python install -r requirements.txt
```
STEP 3) Create directory for index data of elasticsearch to be placed
```
mkdir gdata
sudo chmod 777
```
STEP 4) Initialise docker container
```
docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" --name es-gazetteer -v gdata/:/usr/share/elasticsearch/data elasticsearch:7.6.1
```
STEP XX) Test if elasticsearch index can be queried
```
curl -X GET "http://localhost:9200/geonames/_search?q=name:PUT-LOCATION-NAME-HERE&pretty=true"
```

