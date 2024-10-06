from typing import List, Tuple

import nltk
import numpy as np
from nltk import sent_tokenize
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import pipeline

nltk.download("stopwords")
nltk.download("punkt_tab")


class DreamAnalyzer:
    """
    A class for analyzing dreams and extracting relevant information.

    Attributes:
        ner_pipeline (pipeline): A pipeline for named entity recognition using the BERT model.
        sentiment_pipeline (pipeline): A pipeline for sentiment analysis using the DistilBERT model.
        vectorizer (TfidfVectorizer): A vectorizer for text data using TF-IDF.

    Methods:
        __init__(self): Initializes the DreamAnalyzer class.
        extract_named_entity(self, text: str) -> List[str]: Extracts named entities from the given text.
        analyze_sentiment(self, text: str) -> Tuple[str, float]: Analyzes the sentiment of the given text and returns the emotion and score.
        extract_keywords(self, text: List[str], num_keywords: int = 10) -> List[str]: Extracts the top keywords from the given text.
        get_themes(self, text: List[str]) -> List[List[str]]: Identifies the main themes in the given text using NMF.
        analyze_dream(
            self, text: str
        ) -> Tuple[List[str], Tuple[str, float], List[str], List[List[str]]]: Analyzes a dream by extracting named entities, sentiment, keywords, and themes.
    """

    def __init__(self):
        """
        Initialize the DreamAnalyzer class.

        :return: None
        """
        self.ner_pipeline = pipeline(
            model="dbmdz/bert-large-cased-finetuned-conll03-english",
            grouped_entities=True,
        )
        self.sentiment_pipeline = pipeline(
            model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
        )
        self.vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)

    def extract_named_entity(self, text: str) -> List[str]:
        """
        Extracts named entities from the given text.

        :param text: The input text.
        :type text: str

        :return: A list of unique named entities found in the text.
        :rtype: List[str]
        """
        entities = self.ner_pipeline(text)
        themes = [entity["word"] for entity in entities]
        unique_themes = list(set(themes))
        return unique_themes

    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """
        Extracts named entities from the given text.

        :param text: The input text.
        :type text: str

        :return: A list of unique named entities found in the text.
        :rtype: List[str]
        """
        sentiment = self.sentiment_pipeline(text)[0]
        emotion = sentiment["label"]
        score = sentiment["score"]
        return emotion, score

    def extract_keywords(self, text: List[str], num_keywords: int = 10) -> List[str]:
        """
        Extracts named entities from the given text.

        :param text: The input text.
        :type text: str

        :return: A list of unique named entities found in the text.
        :rtype: List[str]
        """
        tfidf_matrix = self.vectorizer.fit_transform(text)
        feature_names = self.vectorizer.get_feature_names_out()
        scores = np.asarray(tfidf_matrix.sum(axis=0)).ravel()
        feature_names = self.vectorizer.get_feature_names_out()
        keyword_scores = dict(zip(feature_names, scores))
        sorted_keywords = sorted(
            keyword_scores.items(), key=lambda x: x[1], reverse=True
        )
        top_keywords = [keyword for keyword, score in sorted_keywords[:num_keywords]]
        return top_keywords

    def get_themes(self, text: List[str]):
        """
        Extracts named entities from the given text.

        :param text: The input text.
        :type text: str

        :return: A list of unique named entities found in the text.
        :rtype: List[str]
        """
        tfidf_matrix = self.vectorizer.fit_transform(text)
        num_topics = 2
        nmf_model = NMF(n_components=num_topics, init="random", random_state=42)
        nmf_matrix = nmf_model.fit_transform(tfidf_matrix)
        feature_names = np.array(self.vectorizer.get_feature_names_out())
        top_feature_indices = np.argsort(nmf_model.components_, axis=1)[:, :-11:-1]
        top_features = [list(feature) for feature in feature_names[top_feature_indices]]

        return top_features

    def analyze_dream(
        self, text: str
    ) -> Tuple[List[str], Tuple[str, float], List[str], List[List[str]]]:
        """
        Extracts named entities from the given text.

        :param text: The input text.
        :type text: str

        :return: A list of unique named entities found in the text.
        :rtype: List[str]
        """
        named_entity = self.extract_named_entity(text)
        sentiment = self.analyze_sentiment(text)
        document = sent_tokenize(text)
        keywords = self.extract_keywords(document)
        themes = self.get_themes(document)
        return named_entity, sentiment, keywords, list(themes)
