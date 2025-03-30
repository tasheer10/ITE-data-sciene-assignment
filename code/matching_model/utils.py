import re
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.data import find

def download_nltk_resource(resource):
    """Check if an NLTK resource is downloaded, and download it if not."""
    try:
        find(resource)  # Check if resource exists
    except LookupError:
        nltk.download(resource.split('/')[-1])  # Download only if not found

# Ensure required resources are available
download_nltk_resource('corpora/wordnet')
lemmatizer = WordNetLemmatizer()

def get_lemmatized_words(text):
    """Lemmatize words in the input text."""
    if not isinstance(text, str):
        return ""
    
    # Tokenize the text into words
    words = text.split()
    
    # Lemmatize each word and join them back into a string
    lemmatized_text = " ".join([lemmatizer.lemmatize(word) for word in words])
    
    return lemmatized_text



def clean_text(text):
    """Lowercase, strip whitespace, remove leading numbers/punctuation, stop words, and special characters."""
    if not isinstance(text, str):
        return ""
    
    # Convert to lowercase and strip whitespace
    text = text.lower().strip()
    
    # Remove patterns like "1. ", "1.1 ", "10. " etc. from the start
    text = re.sub(r"^\d+(\.\d+)*\s*[-\.]?\s*", "", text)
    
    # Remove special characters (except alphanumeric and spaces)
    text = re.sub(r"[^\w\s]", "", text)
    
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    text = " ".join(word for word in text.split() if word not in stop_words)

    return text


def get_visitor_interests(visitor_email, processed_visitors_df,RELEVANT_QUESTIONS):
    """
    Extracts a set of cleaned interest terms for a visitor based on their answers
    to relevant questions.
    """
    if processed_visitors_df is None or visitor_email is None:
        return set()

    visitor_answers = processed_visitors_df[
        (processed_visitors_df['visitor_email'] == visitor_email) &
        (processed_visitors_df['questionText'].isin(RELEVANT_QUESTIONS))
    ]

    interests = set()
    for answer in visitor_answers['answerText'].dropna():
        cleaned = clean_text(answer)
        if cleaned:
            interests.add(cleaned)
            # Adding splitted words and lemmatized words to the set
            # This is to ensure that we have all the words in the cleaned text as well
            interests.update(cleaned.split())
            interests.update([lemmatizer.lemmatize(word) for word in cleaned.split()])  
    return interests


def get_exhibitor_category_info(processed_exhibitors_df):
    """
    Processes exhibitor data to get cleaned category sets and total counts per exhibitor.

    Returns:
        tuple: (
            exhibitor_categories_map: dict {exhibitorid: {set of cleaned category names}},
            exhibitor_category_counts: dict {exhibitorid: total unique category count}
        )
    """
    if processed_exhibitors_df is None:
        return {}, {}

    exhibitor_categories_map = {}

    for exhibitor_id, group in processed_exhibitors_df.groupby('exhibitorid'):
        cleaned_categories = set()
        for cat_name in group['categoryName'].unique():
              cleaned = clean_text(cat_name)
              if cleaned:
                    cleaned_categories.add(cleaned)
                    # Adding splitted words and lemmatized words to the set
                    # This is to ensure that we have all the words in the cleaned text as well
                    cleaned_categories.update(cleaned.split())
                    cleaned_categories.update([lemmatizer.lemmatize(word) for word in cleaned.split()])  
        exhibitor_categories_map[exhibitor_id] = cleaned_categories

    # Calculate total *unique* parent categories per exhibitor for penalty
    exhibitor_category_counts = processed_exhibitors_df.groupby('exhibitorid')['parentCategory'].nunique()

    return exhibitor_categories_map, exhibitor_category_counts.to_dict()

def calculate_match_score(visitor_interests_set, exhibitor_categories_set, total_exhibitor_categories, penalty_alpha=0.5, penalty_threshold=6):
    """
    Calculates a match score between visitor interests and exhibitor categories,
    applying a penalty for exhibitors with many categories.

    Note:
    This scoring function is purely based on the word overlap between the visitor's interests and the exhibitor's categories post the cleaning of the text and adding lemmatized words.
    The cleaning function is also basic with only stop words removal, special character removal, and lowercasing.
    More advanced NLP techniques like word/sentence embeddings could be used for better matching.
    A more advanced scoring function can also be implemented which uses both the word overlap and the semantic similarity between the visitor's interests and the exhibitor's categories.
    For the penalty, I have considered the unique parent categories for the exhibitor as a measure of how many categories they have.
    The penalty is applied linearly above a threshold of 6 (Due to the 75th Percentile across all exhibitors) categories. This can be adjusted based on the distribution of categories in the dataset.

    Args:
        visitor_interests_set (set): Cleaned visitor interest terms.
        exhibitor_categories_set (set): Cleaned exhibitor category names.
        total_exhibitor_categories (int): Total number of unique categories for the exhibitor.
        penalty_alpha (float): Controls the strength of the penalty. Higher = stronger penalty.
        penalty_threshold (int): Number of categories above which the penalty starts increasing.

    Returns:
        tuple: (score, num_matches, matched_categories_set)
    """
    if not visitor_interests_set or not exhibitor_categories_set:
        return 0.0, 0, set()

    # Simple intersection based matching
    matched_categories_set = visitor_interests_set.intersection(exhibitor_categories_set)
    num_matches = len(matched_categories_set)

    if num_matches == 0:
        return 0.0, 0, set()

    # Penalty Calculation: Penalize exhibitors exceeding the threshold

    # Using a linear penalty above threshold (since we know the 75 percentile is 6, let's stick with that, whenever it is more let's penalize gradually):
    penalty_factor = 1.0 / (1.0 + penalty_alpha * max(0, total_exhibitor_categories - penalty_threshold))

    # Other options to use are a logarithmic penalty or a simple inverse power penalty:
    # Alternative: Logarithmic penalty (less aggressive than linear)
    # penalty_factor = 1.0 / (1.0 + penalty_alpha * np.log(max(1, total_exhibitor_categories)))
    # Alternative: Inverse power penalty (more aggressive than linear)
    # penalty_factor = 1.0 / (max(1, total_exhibitor_categories) ** penalty_alpha)

    score = num_matches * penalty_factor

    return score, num_matches, matched_categories_set