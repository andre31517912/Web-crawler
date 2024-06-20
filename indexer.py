from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import math
import os
import json
import sys
from bs4 import BeautifulSoup
import nltk
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
import heapq
from functools import reduce
import json
import operator

dir_path = '/Users/karthikkalyanasundaram/Downloads/ANALYSTcopy'
documents_dict = {}
important_dict = {}
sentence_dict = {}
total_sentences = []
porter = PorterStemmer()
lancaster = LancasterStemmer()
c = 0


 

def write_traversed_dictionary(data):
    filename = '/Users/karthikkalyanasundaram/Downloads/traverse_dictionary1.txt'
    try:
        with open(filename, 'r') as f:
            inverted_index = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        inverted_index = {}

    for doc, words in data.items():
        for word in words:
            if word not in inverted_index:
                inverted_index[word] = {doc: 1}
            elif doc not in inverted_index[word]:
                inverted_index[word][doc] = 1
            else:
                inverted_index[word][doc] += 1

    with open(filename, 'w') as f:
        json.dump(data, f)


def traverse_directory(dir_path):
    for dir_name, subdirs, files in os.walk(dir_path):
        print(f'Entering directory {dir_name}')
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(dir_name, file)
                if file_path in documents_dict.keys():
                    break
                

                with open(file_path, 'r') as f:
                    try:
                        data = json.load(f)
                        soup = BeautifulSoup(data["content"], 'html.parser')
                    except (json.JSONDecodeError, KeyError):
                        # Skip broken or empty HTML files
                        continue
                with open(file_path, 'r') as f:
                    data = json.load(f)


                
                soup = BeautifulSoup(data["content"], 'html.parser')
                strong_tags = [tag.text for tag in soup.find_all('strong')]


                heading_tags = [tag.text for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]

                # Find the <title> tag and extract its text content

                #print(strong_tags,heading_tags)
                                                    

                answer = []
                word_list = []
                if strong_tags != []:
                    for tag in strong_tags:
                        if tag != None:
                            words = tag.split()
                            
                            for z in words:
                                word_list.append(z)
                                answer.append(z)

                

                if heading_tags != []:
                    for tag in heading_tags:
                        if tag != None:
                            words = tag.split()
                            for z in words:
                                word_list.append(z)
                                answer.append(z)

                for z in soup.get_text().split():
                    if str.isalnum(z):
                        answer.append(z)
                alphanumeric_content = filter(str.isalnum, soup.get_text())

                for z in soup.get_text().replace("\n", "").replace("\t","").replace("\xa0","").split("."):
                    total_sentences.append(z)
                
                documents_dict[file_path] = answer
                
                if len(documents_dict.keys())%15==0:
                    print("hello")
                    write_traversed_dictionary(documents_dict)

                important_dict[file_path] = word_list
                sentence_dict[file_path] = [soup.get_text().replace("\n", " ").replace("\t"," ").replace("\xa0"," ").split(".")]
            

        for subdir in subdirs:
            subdir_path = os.path.join(dir_name, subdir)
            traverse_directory(subdir_path)

    

traverse_directory(dir_path)




def stemmer_func(all_words):

    print("{0:20}{1:20}{2:20}".format("Word","Porter Stemmer","lancaster Stemmer"))
    for word in all_words:
        print("{0:20}{1:20}{2:20}".format(word,porter.stem(word),lancaster.stem(word)))

ranked_words,inverted_index,all_words = rank_words(documents_dict)



sorted_words = sorted(ranked_words.items(), key=lambda x: sum(x[1].values()), reverse=True)
stemmer_dict = {}

def stemmer_func_onsentences(total_sentences):
    for key,value in sentence_dict.items():
        for k in value:
            cur = []
            for z in k:

                r = [z, sentence_helper(z)]

                cur.append(r)
                    
            stemmer_dict[key] = cur
                

            


def sentence_helper(sentence):
    
    tokens = word_tokenize(sentence)
    answer = ""
    for z in tokens:
         answer += porter.stem(z) + " "
    return answer














        







