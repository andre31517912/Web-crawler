#!/usr/bin/env python3
import json
import os
import math
import time
import operator

FILE_DOC_IDS = "./docIds.txt"
FILE_INVERTED_INDEX = "/Users/karthikkalyanasundaram/Downloads/inverted_index.txt"
FILE_TERM_IDS = "/Users/karthikkalyanasundaram/Downloads/ranked_words.txt"
FILE_DUMP = "./FileDump/"
FILE_DOCUMENT_MAGNITUDES = "./documentMagnitudes.txt"
ranked_words,inverted_index,all_words = {},{},{}



    
    



def load_inverted_index():
    inverted_index = {}
    with open("inverted_index.txt", "r") as f:
        inverted_index = json.load(f)
    
    

def create_inverted_index(url_corpus_dict):
    inverted_index = {}
    all_words = set()
    print(url_corpus_dict.values())
    for url, corpus in url_corpus_dict.items():
        for word in corpus:
            
            word1 = word.lower()
            if word1 not in inverted_index:
                inverted_index[word1] = {}
            if url not in inverted_index[word1]:
                inverted_index[word1][url] = 0
            inverted_index[word1][url] += 1
            all_words.add(word1)
    return inverted_index, list(all_words)


def get_tf_idf_scores(word, inverted_index, num_docs):
    tf_idf_scores = {url: 0 for url in inverted_index[word]} if word in inverted_index else {}
    for url, freq in inverted_index[word].items():
        tf = freq / len(inverted_index[word])
        idf = math.log(num_docs / len(inverted_index[word]))
        tf_idf_scores[url] = tf * idf
    return tf_idf_scores

def rank_words(url_corpus_dict):
    inverted_index, all_words = create_inverted_index(url_corpus_dict)
    num_docs = len(url_corpus_dict)
    ranked_words = {}
    for word in all_words:
        tf_idf_scores = get_tf_idf_scores(word, inverted_index, num_docs)
        if len(tf_idf_scores) > 0:
            ranked_words[word.lower()] = {}
            for url, score in tf_idf_scores.items():
                ranked_words[word.lower()][url] = score
    
    return ranked_words, inverted_index, all_words

def load_dictionary():
    loaded_dictionary = {}
    with open("/Users/karthikkalyanasundaram/Downloads/traverse_dictionary1.txt","r") as f:
        loaded_dictionary = json.load(f)

    
    ranked_words, inverted_index, all_words = rank_words(loaded_dictionary)

    print(ranked_words.keys())
    return ranked_words, inverted_index, all_words




def query(dictionary):
    querier = input("What word/words would you like to search ")
    
    if " " not in querier:

        start_time = time.time()
        while querier not in dictionary.keys():
            querier = input(" Invalid key, What word/words would you like to search ")
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.2f} seconds")
        return top_20_urls(dictionary, querier,5 )
    else:
        start_time = time.time()
        new_q = querier.split(" ")
        new_l = []
        for z in new_q:
            new_l.append(set([t[0] for t in top_20_urls(dictionary,z,10)]))
        
    
        
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.2f} seconds")
        return set.intersection(*new_l)
    


def top_20_urls(dictionary, word,counter):
    cur_word = dictionary[word] 
    second_c = 0
    answer = {}
    if counter > len(cur_word):
        return sorted(cur_word.items(),key = operator.itemgetter(1),reverse = True)
    return sorted(cur_word.items(),key = operator.itemgetter(1),reverse = True)[0:counter]

ranked_words, inverted_index, all_words = load_dictionary()
x = True
c = 0


while c < 10:
    print(query(inverted_index))
    