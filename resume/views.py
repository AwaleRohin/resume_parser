from django.shortcuts import render
import re
import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import textract
import spacy
from spacy.matcher import Matcher
import pandas as pd
import nltk

nlp = spacy.load('en_core_web_sm')


def extract_text_from_doc(doc_path):
    temp = textract.process(doc_path)
    text = str(temp, 'utf-8')
    name = extract_education(text)
    return name


def extract_name(resume_text):
    # initialize matcher with a vocab
    matcher = Matcher(nlp.vocab, validate=True)

    nlp_text = nlp(resume_text)

    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

    matcher.add('NAME', None, pattern)

    matches = matcher(nlp_text)

    for match_id, start, end in matches:
        span = nlp_text[start:end]
        print(span.text)


def extract_mobile_number(text):
    phone = re.findall(re.compile(
        r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), text)

    if phone:
        number = ''.join(phone[0])
        if len(number) > 10:
            return '+' + number
        else:
            return number


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

    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]

    data = pd.read_csv("skills.csv")
    skills = list(data.columns.values)
    skillset = []

    # # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)

    # # check for bi-grams and tri-grams (example: machine learning)
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)

    return [i.capitalize() for i in set([i.lower() for i in skillset])]


def extract_education(resume_text):
    nltk.download('stopwords')
    nltk_stopwords = nltk.corpus.stopwords.words('english')

    EDUCATION = [
        'BIM','BACHELORS IN INFORMATION MANAGEMENT', 'Bsc.CSIT', 'BBA', 'BBS', 'BCA',
        'ME', 'M.E', 'M.E.', 'MS', 'M.S',
        'BTECH', 'B.TECH', 'M.TECH', 'MTECH'
    ]
    nlp_text = nlp(resume_text)

    # Sentence Tokenizer
    nlp_text = [sent.string.strip() for sent in nlp_text.sents]
    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
            # Replace all special symbols
            # tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if text.upper() in EDUCATION and text not in nltk_stopwords:
                edu[text] = text + nlp_text[index + 1]
    print(edu)
    # Extract year
    education = []
    for key in edu.keys():
        print('key')
        year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
        if year:
            education.append((key, ''.join(year[0])))
        else:
            education.append(key)
    return education


# a = extract_text_from_doc('RohinAwaleCV.pdf')
# print(a)
# extract_skills()
def home(request):
    return render(request,'home.html')