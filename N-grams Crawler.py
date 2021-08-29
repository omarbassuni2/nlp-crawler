import nltk
import numpy as np
import random 
import string
import bs4 as bs
import urllib.request
import re
import requests
import statistics 
from collections import defaultdict
#########################################################################
#here we get multiple links that are contained in an aritcle in wikipedia
#########################################################################
def browse(url):
    response = requests.get(url)
    html = response.text
    soup = bs.BeautifulSoup(html, "html.parser")
    article_link = []
    for element in soup.find_all('p'):
        if element.find('a'):
            article_link.append(element.find("a").get('href'))
    if not article_link:
        return
    
    return article_link

######################################################################################################
#this snippet of code scrapes the paragraphs of a given link and processes it for get Trigrams, Corpus
######################################################################################################
def wikiCrawler(ngrams, words_tokens, url):
    raw_html = urllib.request.urlopen(url)
    raw_html = raw_html.read()

    article_html = bs.BeautifulSoup(raw_html, 'lxml')
    article_paragraphs = article_html.find_all('p')
    article_text = ''

    for para in article_paragraphs:
        article_text += para.text
    article_text = article_text.lower()
    
    #to clear the unwanted characters
    article_text = re.sub(r'[^A-Za-z. ]', '', article_text)

    words_tokens += nltk.word_tokenize(article_text)
    for i in range(len(words_tokens)-3):
        ngrams[(words_tokens[i], words_tokens[i+1])][words_tokens[i+2]] += 1
    for w1_w2 in ngrams:
        total_count = float(sum(ngrams[w1_w2].values()))
        for w3 in ngrams[w1_w2]:
            ngrams[w1_w2][w3] /= total_count
    return len(article_text)
    

def main():
    
    ngrams = defaultdict(lambda: defaultdict(lambda: 0))
    words_tokens = []
    corpus_len = 0
    url = 'https://en.wikipedia.org/wiki/Political'
    #returns a list of links to be used by the crawler
    article_link = browse(url)
    for i in article_link:
        if(corpus_len >= 200000):
            break
        corpus_len += wikiCrawler(ngrams, words_tokens, url)
        url = urllib.parse.urljoin('https://en.wikipedia.org/', i)
        print('Fetching corpus from', url, '\nCurrent Corpus length: ', corpus_len)
    print('For fast testing, use one of these:\n\tpolitics is\n\tthe government')
    #we initialize the curr_sequence variable with the first trigram in the corpus.
    while(True):
        curr_seq = input('Enter two words: ')
        try:
            words=curr_seq.split(' ')
            my_dict=dict(ngrams[words[0],words[1]])
            key_max = max(my_dict.keys(), key=(lambda k: my_dict[k]))
            print(words[0],words[1],key_max)
        except:
            print('this trigram doesn\'t exist')

if __name__ == '__main__':
    main()

