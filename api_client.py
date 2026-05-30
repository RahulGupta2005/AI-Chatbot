from groq import Groq
from PIL import Image

# =====================================================
# GROQ CLIENT
# =====================================================

client = Groq(

    api_key="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"

)

# =====================================================
# TEXT RESPONSE
# =====================================================

def get_api_response(user_message):

    try:

        completion = client.chat.completions.create(

            model="llama-3.1-8b-instant",

        messages=[

                {
                    "role": "user",
                    "content": user_message
                }

            ],

            temperature=0.7,

            max_tokens=1024
        )

        return completion.choices[0].message.content

    except Exception as e:

        return f"Error: {e}"

# =====================================================
# IMAGE ANALYSIS PLACEHOLDER
# =====================================================

def analyze_image(image, prompt):

    return "Image analysis requires Gemini Vision API."