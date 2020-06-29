writer_tokens = ['ලියපු', 'ලිව්ව', 'හදපු', 'හැදුව', 'රචනා කරපු', 'රචකයා', 'ලිවූ', 'පද රචනය','හැදූ']
artist_tokens = ['ගායනය', 'ගායනා', 'ගායනා කරන', 'ගායනා කල', 'ගායකයා', 'කියන', 'කියනා', 'කිව්ව']
music_director_tokens = ['අධ්‍යක්ෂණය', 'සංගීතමය', 'සංගීතවත්' ]
rating_tokens = ['ඉහල', 'ඉහළම', 'හොඳ', 'හොඳම', 'වැඩිපුර', 'වැඩිපුරම', 'ජනප්‍රිය', 'ජනප්‍රියම', 'සුපිරි', 'සුපිරිම', 'ප්‍රකට', 'ප්‍රසිද්ධ']
song_tokens = ['ගීතය', 'ගීත', 'සිංදු', 'සින්දු']


def classify(token_list):

    writer_query = False
    artist_query = False
    md_query = False
    rate_query = False
    song_token = False
    other_tokens_str = ''
    
    for token in token_list:
        if token in writer_tokens:
            writer_query = True
        elif token in artist_tokens:
            artist_query = True
        elif token in music_director_tokens:
            md_query = True
        elif token in rating_tokens:
            rate_query = True
        elif token in song_tokens:
            song_token = True
        else:
            other_tokens_str += token + ' '

    if song_token:
        return (writer_query, artist_query, md_query, rate_query, other_tokens_str[:-1])
    return False


def is_rating_query(token_list):

    rate_query = False
    song_token = False
    other_tokens_str = ''

    for token in token_list:
        if token in rating_tokens:
            rate_query = True
        elif token in song_tokens:
            song_token = True
        else:
            other_tokens_str += token + ' '
    
    if song_token:
        return rate_query, other_tokens_str[:-1]
    return False, False
