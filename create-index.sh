echo "Starting Docker container and data volume..."
sudo docker run -d -p 127.0.0.1:9200:9200 -v $PWD/geonames_index/:/usr/share/elasticsearch/data --name es-gazetteer elasticsearch:7.6.1

echo "Downloading Geonames data..."
wget http://download.geonames.org/export/dump/allCountries.zip
echo "Unpacking Geonames data..."
unzip allCountries.zip

echo "Creating mappings for the fields in the Geonames index..."
curl -XPUT 'localhost:9200/geonames' -H 'Content-Type: application/json' -d @geonames_mapping.json

echo "Installing all required Python libraries..."
python install -r requirements.txt

echo "Loading gazetteer into Elasticsearch..."
python geonames_elasticsearch_loader.py

echo "Done"
