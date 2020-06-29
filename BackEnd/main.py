import flask
from flask_cors import CORS, cross_origin
import json
from elasticsearch import Elasticsearch
from mtranslate import translate
import re
import process_sinhala
from rule_classifier import classify, is_rating_query


index_name = 'sinhalalyrics'
es = Elasticsearch('localhost', port=9200)
tokenizer = None
stemmer = None
beat_pattern = re.compile('\d*\/\d*')


def search(search_term, limit):
    
    num_list = [int(s) for s in search_term.split() if s.isdigit()]
    if len(num_list) != 0 and not beat_pattern.search(search_term):
        limit = num_list[0]
    
    res = es.search(
        index = index_name,
        size = limit,
        body = {
            'query': {
                'multi_match': {
                    'query': search_term,
                    'fields': [
                        "lyric^4",
                        "songName^4",
                        "artist^4",
                        "genre^2",
                        "lyricWriter^2",
                        "musicDirector^2",
                    ]
                }
            },
            "aggs": {
                "artist_filter": {
                    "terms": {
                        "field": "artist.keyword",
                        "size": 5
                    }
                },
                "lyric_filter": {
                    "terms": {
                        "field": "lyricWriter.keyword",
                        "size": 5
                    }
                },
                "genre_filter": {
                    "terms": {
                        "field": "genre.keyword",
                        "size": 5
                    }
                }
            }
        }
    )

    return res



def boosted_search(limit, classify_out):
    
    search_term = classify_out[4]
    should_list = []
    aggs_dict = {}

    num_list = [int(s) for s in search_term.split() if s.isdigit()]
    if len(num_list) != 0 and not beat_pattern.search(search_term):
        limit = num_list[0]
        if search_term == str(limit):
            search_term = ''

    if classify_out[0]:      
        should_list.append({'match': {'lyricWriter': search_term}})
    elif classify_out[1]:      
        should_list.append({'match': {'artist': search_term}})
    elif classify_out[2]:       
        should_list.append({'match': {'musicDirector': search_term}})
    elif search_term != '':
        should_list.append({'match': {'songName': search_term}})
        should_list.append({'match': {'lyric': search_term}})
        should_list.append({'match': {'artist': search_term}})
    
    if classify_out[0] and not classify_out[1]:     
        aggs_dict['artist_filter'] = {'terms': {'field': 'artist.keyword', 'size': 5}}
    if classify_out[1] and not classify_out[0]:     
        aggs_dict['lyric_filter'] = {'terms': {'field': 'lyricWriter.keyword', 'size': 5}}
    aggs_dict['genre_filter'] = {'terms': {'field': 'genre.keyword', 'size': 5}}

    if classify_out[3]:         
        res = es.search(
            index = index_name,
            size = limit,
            body = {
                'query': {
                    'bool': {
                        'should': should_list
                    }
                },
                'sort': [
                    {
                        'views': {
                            'order': 'desc'
                        }
                    }
                ],
                'aggs': aggs_dict
            }
        )
    
    else:
        res = es.search(
            index = index_name,
            size = limit,
            body = {
                'query': {
                    'bool': {
                        'should': should_list
                    }
                },
                'aggs': aggs_dict
            }
        )

    return res


def basicSearch(obj):
   

    language = obj['language']
    limit = obj['size']
    query = obj['query']

    if language == 'en':
        query = translate(query, 'si', 'en')

    query = query.replace('.', ' ')

  
    token_list, query = process_sinhala.token_stem(query, tokenizer, stemmer)
    rules = classify(token_list)

    if not rules:           
        return search(query, limit)
    else:
        return boosted_search(limit, rules)



app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'sindupotha'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

@app.route('/basicsearch', methods=['POST'])
def serve():
    return flask.jsonify(basicSearch(flask.request.form))


if __name__ == '__main__':
    tokenizer, stemmer = process_sinhala.get_sn_process_setup()

    app.run(host='127.0.0.1', port='5002')
