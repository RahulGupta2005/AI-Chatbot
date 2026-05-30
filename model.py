# ========================= IMPORTS =========================

from SRC.utils import load_data
from SRC.preprocess import clean_text
from API.api_client import get_api_response

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ========================= CHATBOT CLASS =========================

class Chatbot:

    def __init__(self, path):

        # Load dataset
        self.data = load_data(path)

        # Clean all questions
        self.questions = [
            clean_text(q)
            for q in self.data['question']
        ]

        # Create TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer()

        # Convert questions into vectors
        self.X = self.vectorizer.fit_transform(self.questions)

    # ========================= RESPONSE FUNCTION =========================

    def get_response(self, user_input):

        try:

            # Clean user input
            user_input_clean = clean_text(user_input)

            # Convert user input into vector
            user_vec = self.vectorizer.transform([user_input_clean])

            # Calculate cosine similarity
            similarity = cosine_similarity(user_vec, self.X)

            # Find best matching question
            best_match_index = similarity.argmax()

            # Best similarity score
            best_score = similarity[0][best_match_index]

            # Convert confidence score into percentage
            confidence_score = round(float(best_score) * 100, 2)

            # Confidence level
            if confidence_score >= 80:
                confidence_level = "High"

            elif confidence_score >= 60:
                confidence_level = "Medium"

            else:
                confidence_level = "Low"

            # ========================= DATASET RESPONSE =========================

            if best_score > 0.6:

                response = self.data['answer'][best_match_index]

                return {
                    "response": response,
                    "confidence": f"{confidence_score}%",
                    "confidence_level": confidence_level,
                    "source": "Dataset"
                }

            # ========================= GEMINI FALLBACK =========================

            api_response = get_api_response(user_input)

            return {
                "response": api_response,
                "confidence": f"{confidence_score}%",
                "confidence_level": confidence_level,
                "source": "Gemini API"
            }

        # ========================= ERROR HANDLING =========================

        except Exception as e:

            return {
                "response": f"Error: {str(e)}",
                "confidence": "0%",
                "confidence_level": "Low",
                "source": "Error"
            }