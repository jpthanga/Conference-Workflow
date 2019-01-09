def normalise(word):
    """Normalise word into lower case and lemmatizes it."""
    import nltk
    lemmatizer = nltk.WordNetLemmatizer()
    stemmer = nltk.stem.porter.PorterStemmer()
    #from nltk.corpus import stopwords
    #stopwords = stopwords.words('english')

    delim = '\t'
    word = word.lower()
    word = lemmatizer.lemmatize(word)
    word = stemmer.stem(word)
    return word

def acceptable_word(word):
    """Checks conditions for acceptable word: length, stopword."""
    from nltk.corpus import stopwords
    stopwords = stopwords.words('english')
    accepted = bool(2 <= len(word) <= 40
        and word.lower() not in stopwords)
    return accepted

def extract_stem_words(str):
    import nltk
    words = list()
    for sentence in nltk.tokenize.sent_tokenize(str):
        sentence = sentence.replace('---', ' ')
        sentence = sentence.replace('/', ' ')
        sentence = sentence.replace('-', ' ')
        sentence = sentence.replace("``", ' ')
        sentence = sentence.replace("`", ' ')
        sentence = sentence.replace("''", ' ')
        sentence = sentence.replace("'", ' ')
        sentence = sentence.replace("e.g.", ' ')
#        sentence = sentence.replace('''', ' ')
        for word in nltk.tokenize.word_tokenize(sentence):
            wrd = normalise(word)
            if acceptable_word(wrd):
                words.append(wrd)
    return words