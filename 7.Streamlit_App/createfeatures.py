"""
Create the features given text input.
For details, see the notebook Data Cleaning and text preparation.
"""

import re
import string
import spacy
import pickle

#we load TfidfVectorizer object
with open('7.Streamlit_App/tfidf.pickle', 'rb') as input_file:
    tfidf=pickle.load(input_file)

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    #some special entities, see https://www.htmlhelp.com/reference/html40/entities/special.html
    # to know what is included: df_news[df_news['Texto'].str.contains('quot')]['Texto']
    pattern = re.compile("|".join(['&amp','ndash','mdash','lsquo','rsquo','ldquo','rdquo']))
    text = pattern.sub('', text)
    return re.sub(clean, '', text)


#We create a dictionary to replace these symbols into accent marks readables.
tildes={"&#225;":'á',"&#233;":'e',"&#237;":'í',"&#243;":'ó',"&#250;":'ú'}


def clean_text(text):
    """Clean the text from punctuation"""
    #remove htlm tags
    text=remove_html_tags(text)
    #make text lowercase
    text = text.lower()
    #correct accent marks
    for key in tildes.keys():
        text = text.replace(key, tildes[key])
    #remove punctuation
    text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
    #remove some non-ASCII characters, see https://www.codetable.net/asciikeycodes
    text=re.sub(r'[\x7f-\x9f]','',text)
    #this is a white space
    text=re.sub(r'[\xa0]',' ', text)
    text=re.sub(r'[\xa1-\xbf]','',text)
    #remove words containing numbers
    text = re.sub('\w*\d\w*', '', text)
    #remove some additional punctuation that was missed the first time around.
    text = re.sub('[‘’“”…«»–]', '', text)
    #remove linespaces
    text = re.sub('\n', ' ', text)
    #removes leading and trailing whitespaces
    text = re.sub('\s+', ' ',text).strip()
    return text

#Stopwords from https://countwordsfree.com/stopwords/spanish + modified by stopwords.py
my_file = open("7.Streamlit_App/stopwords_spanish.txt", "r")
stopwords = my_file.read()
stopwords  = stopwords.split("\n")
my_file.close()

#We use spacy for lemmatization
nlp = spacy.load('es_core_news_sm')

#Previously we check that the lemmatization is bad for some words. 
#Manually and by inspection we add them into this list.
words_with_bad_lemmatization=['lucas','coronavirus','efemérides','argentina','wanda','drive','core','sosa','matías']
words_with_bad_lemmatization_2={'argentino':'argentina','argentinos':'argentina','ruso':'rusia',
                                'rusa':'rusia','rusos':'rusia','rusas':'rusia','ucraniano':'ucrania','ucraniana':
                               'ucrania','ucranianas':'ucrania','ucranianos':'ucrania','francés':'francia','actriz':'actor',
                               'actrices':'actor'}


def create_features(my_input):
    """lemmatization and transform using TfidfVectorizer"""
    lemmatized_words = []
    text=clean_text(my_input)
    text=nlp(text)
    for palabra in text:
        lemma=palabra.lemma_
        for word in lemma.split():
            if word not in stopwords and palabra.text not in words_with_bad_lemmatization and palabra.text not in words_with_bad_lemmatization_2.keys():
                lemmatized_words.append(word)
            elif palabra.text in words_with_bad_lemmatization:
                lemmatized_words.append(palabra.text) 
            elif palabra.text in words_with_bad_lemmatization_2.keys():
                lemmatized_words.append(words_with_bad_lemmatization_2[palabra.text])
    lemmatized_text = " ".join(lemmatized_words)
    #transform using our tfidf object
    features=tfidf.transform([lemmatized_text]).toarray()
    return features
