from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import nltk

nltk.download('punkt')
nltk.download('stopwords')


def preprocess_search_query(queryset):
    # Initialize NLTK components
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()

    preprocessed_search_history = []

    # Iterate over queryset and preprocess each search query
    for query in queryset:
        # Tokenization
        tokens = word_tokenize(query)
        # Normalization (lowercasing) and stopwords removal
        tokens = [stemmer.stem(token.lower()) for token in tokens if token.lower() not in stop_words]
        # Join tokens back into a single string
        preprocessed_query = ' '.join(tokens)
        preprocessed_search_history.append(preprocessed_query)

    return preprocessed_search_history