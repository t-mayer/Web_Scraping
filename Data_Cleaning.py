"""
Date: 19.09.2020
This program contains a Cleaner class. The Cleaner takes text (such as a news article) as input.
The Cleaner class contains several methods:
- preliminary cleaning removes obvious unnecessary characters (such as unicode, brackets, etc.) left over from scraping
- clean sents: tokenizes the text into sentences, removes unnecessary sentences and punctuation
- remove stopwords: uses nltk stopwords list to remove stopwords from text
- tokenize: input can be the article with or without stopwords, splits the text into tokens, removes punctuation
- lemmatize: input can be the article with or without stopwords, uses spaCy lemmatizer to get lemmas, removes punctuation
"""

import pandas as pd
import re
import nltk
import spacy

# download stopword dictionary for German
# nltk.download('stopwords')
stop_words = nltk.corpus.stopwords.words('german')

# make lemmatizer object and load statistical model of your choice, e.g. de_core_news_md
lemmatizer = spacy.load('<Path to spaCy model>')

# pandas options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# read in csv containing news articles, drop unnecessary columns, drop dulicates based on article content
df = pd.read_csv('News.csv')
df = df.drop(columns='Unnamed: 0')
df = df.drop_duplicates(subset='Article', keep='first')


# Cleaner class
class Cleaner:
    def __init__(self, article_text):
        self.article_text = article_text

    def preliminary_cleaning(self):
        """
        Preliminary cleaning, deletes unnecessary characters
        :return: cleaned article as string
        """
        # removes brackets, parentheses, commas, numbers, semicolons, etc.
        # no removal of .!? due to sentence tokenizing later on
        re_pattern = re.compile('\[|\]|:|\(|\)|;|,|\'|"|[0-9]|\{|\}|/|\/')
        s = re.sub(re_pattern, '', self.article_text)

        # removes unicode chars left
        cleaned = s.replace('\xa0', ' ')
        cleaned = cleaned.replace('\\xa', ' ')
        return cleaned

    def clean_sents(self):
        """
        - splits article into sentences,
        - removes suggestion sentence
        - joins it back into string
        - removes punctuation: replace any single character not in brackets
        :return: article string, no punctuation
        """
        str_tokenize = nltk.sent_tokenize(self.article_text)
        str_remove = [sent for sent in str_tokenize if "Mehr zum Thema" not in sent]
        cleaned_string = ' '.join([str(sent) for sent in str_remove])
        sentences = re.sub(r'[^\w\s]', '', cleaned_string)
        return sentences

    def remove_stopwords(self):
        """
        Removes stopwords.
        :return: article without stopwords
        """
        stopwords_removed = ' '.join(word for word in self.article_text.split() if word.lower() not in stop_words)
        return stopwords_removed

    def tokenize_words(self):
        """
        - Tokenizes the article
        - Removes punctuation
        :return: list of word tokens
        """
        tokens = nltk.word_tokenize(self.article_text)

        # remove punctuation still left
        re_pattern2 = re.compile('\.|!|\?|-')
        cleaned_tokens = [re.sub(re_pattern2, '', token) for token in tokens]

        # remove empty replacement strings '', only keep words
        cleaned_tokens = [word for word in cleaned_tokens if word]
        return cleaned_tokens

    def lemmatize(self):
        """
        - Normalize vocab by lemmatizing
        - Remove punctuation + unnecessary whitespace, numbers
        :return: a list of lemmas
        """
        lemmas = lemmatizer(self.article_text)
        lemma_list = [token.lemma_ for token in lemmas]

        # remove punctuation still left
        re_pattern3 = re.compile('\.|!|\?|-')
        cleaned_lemmas = [re.sub(re_pattern3, '', lemma) for lemma in lemma_list]

        # remove empty replacement strings '', only keep words
        cleaned_lemmas = [word for word in cleaned_lemmas if word]
        return cleaned_lemmas


# perform preliminary cleaning in each row
df['Article'] = df['Article'].apply(lambda row: Cleaner(row).preliminary_cleaning())

# create new column "Cleaned Article" to split article into sentences + remove sentences not belonging to articles
df['Cleaned Article'] = df['Article'].apply(lambda row: Cleaner(row).clean_sents())

# create new column "No Stopwords" to get article text without stopwords and remove punctuation
df['No Stopwords'] = df['Cleaned Article'].apply(lambda row: Cleaner(row).remove_stopwords())

# create column "Tokens" to tokenize te article  without stopwords, remove punctuation, and return a list of tokens
df['Tokens'] = df['No Stopwords'].apply(lambda row: Cleaner(row).tokenize_words())

# create column "Lemmas" to lemmatize the article without stopwords, remove punctuation, and return a list of lemmas
df['Lemmas'] = df['No Stopwords'].apply(lambda row: Cleaner(row).lemmatize())


# save df as a serialized file format
df.to_pickle("./Cleaned_News.pkl")
