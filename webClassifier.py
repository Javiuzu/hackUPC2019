#!/usr/bin/env python
# -*- coding: utf-8 -*-

#pip install stemming  # <= Uncomment this if you do not have this library installed yet

# Llibreries necessàries.
from googletrans import Translator
import unicodedata
import pandas as pd
import numpy as np
import string
import urllib2
import re
import operator
from stemming.porter2 import stem
from math import log10
import json

# print "                                            "
# print "##############################################"
# print "### Authors : Ixent Gallego & Eric Santino ###"
# print "### Version : 1.0                          ###"
# print "### Date    : 27/11/16                     ###"
# print "### Website & Text Classifier              ###"
# print "##############################################"
# print "                                            "

dic_id_topic = {1:'Macroeconomics',2:'Civil Rights, Minority Issues, and Civil Liberties',3:'Health',4:'Agriculture',
                5:'Labor, Employment, and Immigration',6:'Education',7:'Environment',8:'Energy',10:'Transportation',
                12:'Law, Crime, and Family Issues',13:'Social Welfare',14:'Community Development and Housing Issues',
                15:'Banking, Finance, and Domestic Commerce',16:'Defense',17:'Space, Science, Technology and Communications',
                18:'Foreign Trade',19:'International Affairs and Foreign Aid',20:'Government Operations',
                21:'Public Lands and Water Management',24:'State and Local Government Administration',
                26:'Weather and Natural Disasters',27:'Fires',28:'Arts and Entertainment',29:'Sports and Recreation',
                30:'Death Notices',31:'Churches and Religion',99:'Other, Miscellaneous, and Human Interest'}

common_english_words = ('about', 'above', 'across', 'after', 'against', 'along', 'amidst', 'amid', 'among', 'anti', 'around',
                        'as', 'at', 'before', 'behind', 'below', 'beneath', 'beside', 'besides', 'between', 'beyond', 'but',
                        'by', 'concerning', 'considering', 'despite', 'down', 'during', 'except', 'excepting', 'excluding',
                        'following', 'for', 'from', 'hence', 'in', 'inside', 'into', 'like', 'minus', 'near', 'of', 'off',
                        'on', 'onto', 'opposite', 'outside', 'over', 'past', 'per', 'plus', 'regarding', 'round', 'save',
                        'since', 'such', 'therefore', 'therein', 'through', 'to', 'toward', 'towards', 'under', 'underneath',
                        'unlike', 'until', 'up', 'upon', 'versus', 'via', 'wherein', 'with', 'within', 'be', 'is', 'are', 'am',
                        'were', 'was', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'done', 'will', 'then', 'than',
                        'although', 'though', 'and', 'yet', 'rather', 'that', 'those', 'these', 'whose', 'who', 'what', 'when',
                        'where', 'why', 'how', 'much', 'many', 'all', 'none', 'no', 'more', 'most', 'less', 'least', 'lot',
                        'lots', 'a', 'an', 'the', 'new', 'I', 'you', 'he', 'she', 'it', 'we', 'they', 'mine', 'yours', 'his',
                        'hers', 'its', 'ours', 'theirs')

def fix_topics(size_topics):
    idx = [key for key in dic_id_topic]
    return pd.Series(size_topics,index=idx)

# Loadging all the data needed.

np_load_old = np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)
words_topics = np.load('words_topics.npy').item()
best_words = np.load('best_words.npy').item()
size_topics = fix_topics(np.load('size_topics.npy'))
topics = np.load('topics.npy')
np.load = np_load_old
df_shape = 31034

exclude = set(string.punctuation)
table = string.maketrans("","")

def count_news(df):
    """Retorna el número total de notícies que hi ha a la base de dades."""
    return len(df.index)

def count_topic_news(df):
    """Retorna el número total de notícies que hi ha de cada categoria (tòpic) a la base de dades."""
    grouped = df.groupby('Topic_2digit')
    return grouped.size()

#Netejem els 'Tags' del html
"""def cleanHtml(html):
    clean_r = re.compile('<.*?>')
    cleanText = re.sub(clean_r, '', html)
    return cleanText
"""
def count_words_web(content):
    word_dicc = dict()
    content = [stem(s.lower()) for s in content.translate(table, string.punctuation).split()
               if len(s)<13 and len(s)>2
               and (s not in common_english_words)]
    e_cont = enumerate(content)
    for idx,word in e_cont:
        if word not in word_dicc: word_dicc[word] = 1
        else: word_dicc[word] += 1
    return word_dicc

def word_count_web(dic,word):
    if stem(word) not in dic:
        return "The word '"+word+"' does not apear in the website "+web
    else:
        return dic[stem(word)]

def top_words_web(dic,N):
    sorted_dic = sorted(dic.items(), key=operator.itemgetter(1))
    millors = sorted_dic[::-1][:N]
    millors = [w[0] for w in millors]
    return millors

def top_words_list(selected_words):
    """Retorna la llista de paraules més comunes entre tots els temes."""
    # El problema és que 'best_words' és un diccionari, i per tant no té un ordre definit. Però necessitem un ordre fixe
    # per a poder definir els vectors de característiques! SOLUCIÓ: Fixem un ordre qualssevol.
    x = []
    for topic in topics:
        x += selected_words[topic]
    # També necessitem filtrar aquelles paraules que estiguin repetides entre diferents tòpics.
    return list(set(x))

def create_features_web(best_words_web, selected_words):
    dict_feat_vector = dict()

    # Cridem a la funció 'top_words_list' per a crear una llista de totes les paraules més populars.
    list_best_words = top_words_list(selected_words)
    length = len(list_best_words)

    # Ara, per a cada notícia a la base de dades 'train_data', mirem si cada una de les paraules a 'list_best_words'
    # apareix a la notícia o no.
    arr = np.zeros(length)

    for k in xrange(length):
        if list_best_words[k] in best_words_web: arr[k] = 1.0

    # Assignem el vector de característiques resultant a la notícia, on la clau és l'ID de la notícia.
    dict_feat_vector = arr.copy()
    # Finalment, retornem el diccionari resultant.
    return dict_feat_vector

def bayes_web_classify(dicc_topics, llista_millors, vectors_noticies):
    M = size_topics.shape[0]
    probabilitats = [0.]*M

    e_topics = list(enumerate(topics))
    e_millors = list(enumerate(llista_millors))

    for i, topic in e_topics:
        B = 1. * size_topics[topic]

        for j, paraula in e_millors:
            # Recordem que el número de notícies on apareix una paraula està guardat com 2on element a 'dicc_topics'.
            A = dicc_topics[topic][paraula][1] if (paraula in dicc_topics[topic]) else 0
            if vectors_noticies[j] == 0.:
                A = B - A
            # Càlcul de la probabilitat condicionada p(x|Y). Per evitar problemes d'underflow, usem logaritmes.
            if A != 0:
                probabilitats[i] += log10(A / B)
            else:
                probabilitats[i] += log10(1 / ((B + M) * len(paraula)))
        # Tenim en compte també la probabilitat P(Y) de cada tòpic, per tal d'aconseguir més precisió.
        probabilitats[i] += log10(B / df_shape)
    # Finalment, escollim com a tòpic més probable aquell amb probabilitat total més gran.
    return topics[probabilitats.index(max(probabilitats))]

"""def read_webs():
    arr = []
    with open("web_list.txt") as inputfile:
            for line in inputfile:
                if line[0] is not "#":
                    arr.append(line)
    return arr
"""
# Funcio que es pot fer servir un cop executades les caselles anteriors, què engloba tot el seu funcionament.
def main_classify_webs():
    #webs = read_webs()
    #for web in webs:
        #c = urllib2.urlopen(web)
        #content = c.read()
        #content = cleanHtml(content)
        
        #file_read
        ads_file = open("./tmp/words/ad.txt", 'r')
        content = ads_file.read()
        
        classified_ads = []
        

        translator = Translator()
        if translator.detect(content).lang != "en":
            new_word = (translator.translate(content).text).encode('ascii','ignore')
            print type(new_word)
            content = new_word
        
        dic = count_words_web(content)
        llista_millors_web = top_words_web(dic,50)
        dict_feat_vector_web = create_features_web(llista_millors_web,best_words)
        clsf = bayes_web_classify(words_topics,top_words_list(best_words),dict_feat_vector_web)
        #print "ha estat classificada com a:",dic_id_topic[clsf],"\n"
        #print "---------------------------------------------------------------------------------------"
        #classified_ad = dic_id_topic[clsf]
        classified_ad = dic_id_topic
        classified_file = open("./tmp/words/class_words.txt", "w+")
        classified_file.write(str(classified_ad))
main_classify_webs()
