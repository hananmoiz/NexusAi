from flask import Flask, request, jsonify, send_file
from flask_cors import CORS  # Import CORS for cross-origin requests
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import logging

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for cross-origin requests
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Logging the start of the app
logging.info("Starting Flask application...")

# Load the tokenizer and model for Falcon-7B
try:
    logging.info("Loading tokenizer...")

    # Load tokenizer and model (force to use CPU for now)
    tokenizer = AutoTokenizer.from_pretrained("tiiuae/Falcon3-7B-Instruct")
    logging.info("Tokenizer loaded successfully.")

    logging.info("Loading model...")
    model = AutoModelForCausalLM.from_pretrained("tiiuae/Falcon3-7B-Instruct")
    logging.info("Model loaded successfully.")

    # Force to use CPU for large models
    device = torch.device("cpu")
    model.to(device)
    logging.info("Model is on device (CPU).")
except Exception as e:
    logging.error(f"Error loading model or tokenizer: {str(e)}")
    raise

# Function to generate a response based on the user's input
def generate_response(user_message):
    try:
        logging.info("Generating response...")

        # Tokenize the user's message
        inputs = tokenizer(user_message, return_tensors="pt").to(device)

        # Generate a response from the model
        outputs = model.generate(inputs["input_ids"], max_length=100, num_return_sequences=1, no_repeat_ngram_size=2)

        # Decode the generated response and return it
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        logging.info("Response generated successfully.")
        return response
    except Exception as e:
        logging.error(f"Error generating response: {str(e)}")
        return f"An error occurred: {str(e)}"

# API route for chat messages
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if user_message:
        response = generate_response(user_message)
        return jsonify({"response": response})
    else:
        return jsonify({"response": "No message received"}), 400

# Route for downloading templates (replace with your template logic)
@app.route('/download/template', methods=['GET'])
def download_template():
    try:
        # You can generate or provide a path to your template file
        return send_file('path_to_template.zip', as_attachment=True)
    except Exception as e:
        logging.error(f"Error downloading template: {str(e)}")
        return f"Error downloading template: {str(e)}", 500

if __name__ == '__main__':
    # Running Flask on a different port (if 5000 is busy)
    app.run(debug=True, port=5001)
