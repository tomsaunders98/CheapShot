#################################################
### Clean Training data before Training Model ###
#################################################



import itertools
import unicodedata
import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import string



contractions = {
"ain't": "are not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he'll've": "he will have",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"I'd": "I had",
"I'd've": "I would have",
"I'll": "I will",
"I'll've": "I will have",
"I'm": "I am",
"I've": "I have",
"isn't": "is not",
"it'd": "it would",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "it will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she would",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as",
"that'd": "that would",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there would",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they would",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who'll've": "who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"you've": "you have"
}
smileys = {
    ":-)": "happy",
    ":-]": "happy",
    ":-3": "happy",
    ":->": "happy",
    "8-)": "happy",
    ":-}": "happy",
    ":)": "happy",
    ";)": "happy",
    ":]": "happy",
    ":3": "happy",
    ":>": "happy",
    "8)": "happy",
    ":}": "happy",
    ":o)": "happy",
    ":c)": "happy",
    ":^)": "happy",
    "=]": "happy",
    "=)": "happy",
    ":-))": "happy",
    ":‑D": "happy",
    "8‑D": "happy",
    "x‑D": "happy",
    "X‑D": "happy",
    ":D": "happy",
    "8D": "happy",
    "xD": "happy",
    "XD": "happy",
    ":‑(": "sad",
    ":‑c": "sad",
    ":‑<": "sad",
    ":‑[": "sad",
    ":(": "sad",
    ":c": "sad",
    ":<": "sad",
    ":[": "sad",
    ":-||": "sad",
    ">:[": "sad",
    ":{": "sad",
    ":@": "sad",
    ">:(": "sad",
    ":'‑(": "sad",
    ":'(": "sad",
    ":‑P": "playful",
    "X‑P": "playful",
    "x‑p": "playful",
    ":‑p": "playful",
    ":‑Þ": "playful",
    ":‑þ": "playful",
    ":‑b": "playful",
    ":P": "playful",
    "XP": "playful",
    "xp": "playful",
    ":p": "playful",
    ":Þ": "playful",
    ":þ": "playful",
    ":b": "playful",
    "<3": "love"
}

def clean_accents(text):
    # first, normalize strings:
    nfkd_str = unicodedata.normalize('NFKD', text)

    # Keep chars that has no other char combined (i.e. accents chars)
    with_out_accents = u"".join([c for c in nfkd_str if not unicodedata.combining(c)])
    return with_out_accents

def removedict(text, dict):
    text = text.replace("’", "'")
    pattern = re.compile(r'(?<!\w)(' + '|'.join(re.escape(key) for key in dict.keys()) + r')(?!\w)')
    return pattern.sub(lambda x: dict[x.group()], text)

def spell(text):
    return ''.join(''.join(s)[:2] for _, s in itertools.groupby(text))

def removesmiley(text, dict):
    text = (re.sub('[\U0001F602-\U0001F64F]', lambda m: unicodedata.name(m.group()), text)).lower()
    text = removedict(text, smileys)
    return text


def detweet(text):
    #remove html
    text = text.replace("#", "")
    text = text.replace('\u2044', ' or ')
    text = BeautifulSoup(text,features="html.parser").get_text()
    text = text.replace('\x92', "'")

    #remove hashtags (but just hashtags, they can be quite informative about sentiment)

    #remove mentions
    text = ' '.join(re.sub("(@[A-Za-z0-9]+)", "", text).split(" "))
    # remove web adress
    text = ' '.join(re.sub("(\w+:\/\/\S+)", " ", text).split())
    return text


def removepunctuation(text):
    #remove punctuation
    return text.translate(str.maketrans('', '', string.punctuation))

def removestop(text):
    stops = set(stopwords.words("english-sent"))
    filtered_words = ' '.join([word for word in text.split() if word not in stops])
    return filtered_words

def correct(text):
    #1 remove capitals
    text = text.lower()
    # 2 accents
    text = clean_accents(text)
    #3 remove links/hastags/mentions/html characters
    text = detweet(text)
    #4 remove smileys
    text = removesmiley(text, smileys)
    #5 remove contractions
    text = removedict(text, contractions)
    #6 remove punctuation
    text = removepunctuation(text)
    #7 correct spellings
    text = spell(text)
    #8 remove stopwords
    text = removestop(text)
    #9 remove any non ascii characters
    text = re.sub(r'[^\x00-\x7f]', r'', text)
    return text

