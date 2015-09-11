import jautils

from unidecode import unidecode
from google.appengine.api import memcache

import re
import logging


JAPANESE_NAME_DICTIONARY = {}
for line in open('japanese_name_dict.txt', 'r'):
    kanji, hiragana = line[:-1].split('\t')
    JAPANESE_NAME_DICTIONARY[kanji.decode('utf-8')] = hiragana.decode('utf-8')


def romanize(word):
    """
    This method romanize all languages by unidecode.
    If word is hiragana or katakana, it is romanized by jautils.
    Args:
        word: should be script varianted
    Returns:
        script varianted word
    """
    if not word:
        return word

    if jautils.should_normalize(word):
        hiragana_word = jautils.normalize(word)
        return jautils.hiragana_to_romaji(hiragana_word)
    romanized_word = unidecode(word)
    return romanized_word


def romanize_japanese_name_by_name_dict(word):
    """
    This method romanize japanese name by using name dictionary.
    If word isn't found in dictionary, this method doesn't
    apply romanize.
    """
    if not word:
        return word

    if word in JAPANESE_NAME_DICTIONARY:
        yomigana = (JAPANESE_NAME_DICTIONARY[word])
        return jautils.hiragana_to_romaji(yomigana)

    return word


def apply_script_variant(query_txt):
    """
    Applies to script variant to each query_txt.
    This method uses unidecode and jautils for script variant.
    This method is called by search method in app/result.py.
    Args:
        query_txt: Search query
    Returns:
        script varianted query_txt (except kanji)
    """
    query_words = query_txt.split(' ')
    return ' '.join([romanize(word)
                     for word in query_words])
