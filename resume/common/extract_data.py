from django.conf import settings
import re
import textract
import spacy
from spacy.matcher import Matcher
import pandas as pd
import nltk
from resume import forms
from fuzzywuzzy import process
from resume import models
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.collocations import *


nlp = spacy.load('en_core_web_sm')
nltk.download('punkt')
nltk.download('stopwords')


def extract_text(doc_path):
    temp = textract.process(doc_path)
    text = str(temp, 'utf-8')
    name = extract_name(text)
    phone_number = extract_mobile_number(text)
    email = extract_email(text)
    education = extract_education(text)
    skills = extract_skills(text)
    resume_data = models.ResumeData.objects.create(name=name,
                                                   mobile=phone_number,
                                                   email=email,
                                                   education=education,
                                                   skills=skills)
    resume_data.save()


def extract_name(resume_text):
    matcher = Matcher(nlp.vocab, validate=True)
    nlp_text = nlp(resume_text)
    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    matcher.add('NAME', None, pattern)
    matches = matcher(nlp_text)
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text.capitalize()


def extract_mobile_number(text):
    pattern = [{"ORTH": "+", "OP": "?"}, {"SHAPE": "ddd", "OP": "?"}, {"ORTH": "-", "OP": "?"}, {"SHAPE": "dddd", "LENGTH": 10}]
    nlp_text = nlp(text)    
    matcher = Matcher(nlp.vocab)
    matcher.add("PHONE_NUMBER", None, pattern)
    matches = matcher(nlp_text)
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text


def extract_email(email):
    email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", email)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None


def extract_skills(resume_text):
    nlp_text = nlp(resume_text)
    noun_chunks = nlp_text.noun_chunks
    tokens = [token.text for token in nlp_text if not token.is_stop]
    data = pd.read_csv(settings.BASE_DIR + "/skills.csv")
    skills = list(data.columns.values)
    skillset = []

    # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)

    # check for bi-grams and tri-grams (example: machine learning)
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)

    return [i.capitalize() for i in set([i.lower() for i in skillset])]


def extract_education(resume_text):
    nltk_stopwords = nltk.corpus.stopwords.words('english')

    data = pd.read_csv(settings.BASE_DIR + "/education.csv")
    EDUCATION = list(data.columns.values)
    nlp_text = nlp(resume_text)
    nlp_text = [sent.string.strip() for sent in nlp_text.sents]
    edu = []
    for index, text in enumerate(nlp_text):
        highest = process.extractOne(text.upper(), EDUCATION)
        edu.append(highest)
    education = None
    threshold = 0
    for i in edu:
        if threshold < int(i[1]):
            threshold = int(i[1])
            education = i[0]
    return education
