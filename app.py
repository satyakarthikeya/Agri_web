from flask import Flask, render_template, request, redirect, url_for
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

# State-specific crops data
state_crops = {
    "Andhra Pradesh": ["Onion", "Sunflower", "Sugarcane", "Soybean", "Sorghum", "Sesamum", "Maize", "Redgram", "Paddy", "Cotton", "Finger Millet", "Greengram", "Groundnut", "Blackgram", "Chickpea"],
    "Assam": ["Jute", "Paddy", "Potato", "Rapeseed-Mustard"],
    "Bihar": ["Chickpea", "Greengram", "Jute", "Lentil", "Maize", "Paddy", "Potato", "Rapeseed-Mustard", "Redgram", "Sugarcane", "Sunflower", "Wheat"],
    "Gujarat": ["Blackgram", "Chickpea", "Cotton", "Greengram", "Groundnut", "Maize", "Onion", "Paddy", "Pearl Millet", "Potato", "Rapeseed-Mustard", "Redgram", "Sesamum", "Soybean", "Sugarcane", "Wheat"],
    "Haryana": ["Chickpea", "Cotton", "Paddy", "Pearl Millet", "Rapeseed-Mustard", "Sugarcane", "Wheat"],
    "Himachal Pradesh": ["Barley", "Blackgram", "Maize", "Paddy", "Potato", "Rapeseed-Mustard", "Sesamum", "Soybean", "Wheat"],
    "Karnataka": ["Greengram", "Groundnut", "Maize", "Onion", "Paddy", "Pearl Millet", "Potato", "Redgram", "Safflower", "Sesamum", "Sorghum", "Soybean", "Sugarcane", "Sunflower", "Wheat"],
    "Kerala": ["Groundnut", "Paddy", "Sesamum"],
    "Madhya Pradesh": ["Barley", "Blackgram", "Chickpea", "Cotton", "Greengram", "Groundnut", "Lentil", "Maize", "Nigerseed", "Onion", "Paddy", "Potato", "Rapeseed-Mustard", "Redgram", "Sesamum", "Sorghum", "Soybean", "Wheat"],
    "Punjab": ["Chickpea", "Cotton", "Greengram", "Lentil", "Maize", "Paddy", "Potato", "Rapeseed-Mustard", "Sugarcane", "Wheat"],
    "Rajasthan": ["Barley", "Blackgram", "Chickpea", "Cotton", "Greengram", "Groundnut", "Lentil", "Maize", "Onion", "Pearl Millet", "Rapeseed-Mustard", "Sesamum", "Sorghum", "Soybean", "Wheat"],
    "Tamil Nadu": ["Greengram", "Groundnut", "Maize", "Onion", "Paddy", "Pearl Millet", "Redgram", "Sesamum", "Sorghum", "Sugarcane"],
    "Telangana": ["Groundnut", "Maize", "Paddy", "Redgram", "Sesamum", "Sorghum", "Soybean", "Sunflower"],
    "Uttarakhand": ["Barley", "Blackgram", "Chickpea", "Greengram", "Groundnut", "Lentil", "Maize", "Paddy", "Pea", "Pearl Millet", "Potato", "Rapeseed-Mustard", "Wheat"]
}

# Load the corpus text from a file
with open("crop_profitability.txt", "r", encoding="utf-8") as file:
    CORPUS_TEXT = file.read()

def extract_keywords_nlp(corpus, crop, state):
    user_query = f"How to maximize profits for {crop} in {state}"
    doc_query = nlp(user_query)
    keywords = [token.text.lower() for token in doc_query if token.pos_ in ['NOUN', 'PROPN']]
    paragraphs = corpus.split('\n')

    for para in paragraphs:
        if all(keyword in para.lower() for keyword in keywords):
            return para.strip()
    return "No matching information found."

# Route for home page
@app.route("/")
def home():
    return render_template("home.html")

# Route for crop profit maximizer page
@app.route("/app", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        crop = request.form.get("crop")
        state = request.form.get("state")
        result = extract_keywords_nlp(CORPUS_TEXT, crop, state)
    return render_template("index.html", state_crops=state_crops, result=result)

if __name__ == "__main__":
    app.run(debug=True)
