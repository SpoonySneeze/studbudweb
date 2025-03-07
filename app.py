from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import BertTokenizer, BertForSequenceClassification
import torch

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=4)

# Example dataset
data = {
    "goal": [
        "Improve math skills",
        "Learn Python programming",
        "Prepare for history exam",
        "Read 10 research papers",
    ],
    "study_plan": [
        "Study algebra for 2 hours daily, solve 10 problems, and review notes.",
        "Complete 1 Python tutorial daily, practice coding for 1 hour.",
        "Read 2 chapters daily, create summary notes, and take quizzes.",
        "Read 1 paper daily, summarize key points, and discuss with peers.",
    ],
}

# Function to generate study plan
def generate_study_plan(goal):
    inputs = tokenizer(goal, return_tensors="pt", padding=True, truncation=True, max_length=128)
    outputs = model(**inputs)
    predicted_label = torch.argmax(outputs.logits, dim=1).item()
    return data["study_plan"][predicted_label]

# API endpoint to generate study plan
@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    data = request.json
    goal = data.get("goal", "")
    study_plan = generate_study_plan(goal)
    return jsonify({"study_plan": study_plan})

if __name__ == "__main__":
    app.run(debug=True)