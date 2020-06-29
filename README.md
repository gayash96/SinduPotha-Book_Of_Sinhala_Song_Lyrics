# Sindu Potha v1.0

Sindu Potha is a Sinhala song lyrics retreival system which can handle both sinhala and english language related queries. This project has been developed using python, elasticsearch, angular and scrapy.  

## Getting Started with Sindu Potha

### First, create ElasticSearch Index

1. Download and run [Elasticsearch](https://www.elastic.co/downloads/elasticsearch).
  > Elasticsearch version 7.7.1. 
2. Install [ICU Analysis](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-icu.html).
3. Create the  index  `sinhalalyrics` in the Elasticsearch.

### Then, populate the ElasticSearch Index

1. Downlad [Scrapy](https://scrapy.org/download/).
2. Run the Elasticsearch instance.
3. Open the`/lyrics/` directory in the terminal and run  `$ scrapy crawl sinhalalyrics -o sinhala_songs.json`

### After that set up the Python Server

1. Install python flask and flask_cora.
2. Download [SinLing](https://github.com/nlpc-uom/Sinling). 


### Then the Angular Front end

1. Run `npm install` in the `/SearchEngine/` directory.

## Running the Sindu Potha

1. Run the Elasticsearch instance.
2. Run the Python backend server by running the  `main.py`  script in the `/BackEnd/` directory.
3. Then open the  `/SearchEngine/` directory in the terminal and type `ng serve --open` .


## Additional Details

The project has been developed using Python 3.6, and after implementing the Sindu Potha successfully in your local machine, you will be abel to search sinhala songs by the song name or the artist name, also Sindu Potha will answer some general queries like popular songs, songs based on genre,etc. Search can be performed using both Englsih and Sinhala language. 

Hope you will enjoy the Sindu Potha, and stay tuned for more amazing furure releases. 
