import { Component } from '@angular/core';
import * as $ from 'jquery';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'SearchEngine';
  result_boundary = 50;
  search_pressed;
  error_present;
  no_result;
  
  lan_selected;
  lan_selected_dict;
  retrievedLyrics = [];
  filteredLyrics = [];

  aggs_artist = [];
  aggs_lyric_wrt = [];
  aggs_genre = [];

  lan_dictionary_en = {
    'page-header': 'Sinhala Songs Search',
    'basic-input-placeholder': 'Enter song name or related data',
    'button': 'Search',
    'error-message': 'Sorry. An Error Occured!',
    'no-result-message': 'No Lyrics Found'
  }

  lan_dictionary_sn = {
    'page-header': 'සිංහල ගීත පොත',
    'basic-input-placeholder': 'ගීතය හො ඒ පිළිබද දත්ත අතුලත් කරන්න',
    'button': 'සොයන්න',
    'error-message': 'සමාවන්න!',
    'no-result-message': 'ගීතය නැත'
  }


  ngOnInit() {
    this.lan_selected_dict = this.lan_dictionary_sn;
    this.lan_selected = 'sn';
    this.search_pressed = false;
    this.error_present = false;
    this.no_result = false;
  }


  toggleLanguage() {
    if(this.lan_selected == 'en') {
      this.lan_selected = 'sn';
      this.lan_selected_dict = this.lan_dictionary_sn;
      $('.toggle-lan').removeClass('btn btn-warning');
      $('.toggle-lan').addClass('btn-success');
      $('.toggle-lan').html('Try English');
    } else {
      this.lan_selected = 'en';
      this.lan_selected_dict = this.lan_dictionary_en;
      $('.toggle-lan').removeClass('btn-success');
      $('.toggle-lan').addClass('btn btn-warning');
      $('.toggle-lan').html('සිංහලෙන් උත්සහ කරන්න');
    }
  }


  lyricSearch() {
    this.search_pressed = true;
    this.error_present = false;
    this.no_result = false;
    this.retrievedLyrics = [];
    this.filteredLyrics = [];
    this.aggs_artist = [];
    this.aggs_lyric_wrt = [];
    this.aggs_genre = [];

    let query = $('#basic_search_query').val();

    $.ajax({
      type: "POST",
      url: "http://127.0.0.1:5002/basicsearch",
      data: {query: query, size: this.result_boundary, language: this.lan_selected},
      success: res => {
        console.log(res.hits.hits)
        console.log(res.aggregations)

        this.search_pressed = false;
        let count = 0;

        if(res.hits.hits.length == 0) {
          this.no_result = true;
        }

        res.hits.hits.forEach(element => {
          if(element._score > 100) {
            this.retrievedLyrics.push(element._source)
            count += 1
          }
        });

        if(this.retrievedLyrics.length == 0) {
          res.hits.hits.forEach(element => {
            if(element._score > 60) {
              this.retrievedLyrics.push(element._source)
              count += 1
            }
          });
        }
        if(this.retrievedLyrics.length == 0) {
          res.hits.hits.forEach(element => {
            if(element._score > 30) {
              this.retrievedLyrics.push(element._source)
              count += 1
            }
          });
        }
        if(this.retrievedLyrics.length == 0) {
          res.hits.hits.forEach(element => {
            if(element._score > 20) {
              this.retrievedLyrics.push(element._source)
              count += 1
            }
          });
        }
        if(this.retrievedLyrics.length == 0) {
          res.hits.hits.forEach(element => {
            if(element._score > 10) {
              this.retrievedLyrics.push(element._source)
              count += 1
            }
          });
        }
        if(this.retrievedLyrics.length == 0) {
          res.hits.hits.forEach(element => {
            if(element._score > 5) {
              this.retrievedLyrics.push(element._source)
              count += 1
            }
          });
        }
        if(this.retrievedLyrics.length == 0) {
          res.hits.hits.forEach(element => {
            if(count < this.result_boundary/2) {
              this.retrievedLyrics.push(element._source)
              count += 1
            }
          });
        }

        this.filteredLyrics = this.retrievedLyrics;

        // aggregations
        if(res.aggregations.artist_filter !== undefined) {
          res.aggregations.artist_filter.buckets.forEach(element => {
            this.aggs_artist.push([element.key, element.doc_count])
          });
        }
        if(res.aggregations.lyric_filter !== undefined) {
          res.aggregations.lyric_filter.buckets.forEach(element => {
            this.aggs_lyric_wrt.push([element.key, element.doc_count])
          });
        }
        if(res.aggregations.genre_filter !== undefined) {
          res.aggregations.genre_filter.buckets.forEach(element => {
            this.aggs_genre.push([element.key, element.doc_count])
          });
        }

      },
      error: err => {
        this.search_pressed = false;
        this.error_present = true;
        this.retrievedLyrics = [],
        this.filteredLyrics = [];
        console.log(err)
      }
    });

  }

}
