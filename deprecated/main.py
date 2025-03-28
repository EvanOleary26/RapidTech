import os
import logging
from flask import Flask, render_template, request, jsonify
from utils import calculate_distance, calculate_railway_metrics

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

# Get API key from environment variable
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    logger.error("Google API key is not configured")
else:
    logger.debug("Google API key is present")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        if not GOOGLE_API_KEY:
            logger.error("API key missing when attempting calculation")
            return jsonify({"error": "Google API key is not configured. Please configure the API key in environment variables."}), 500

        origin = request.form.get("origin")
        destination = request.form.get("destination")

        if not origin or not destination:
            return jsonify({"error": "Both origin and destination are required"}), 400

        logger.debug(f"Calculating distance between {origin} and {destination}")

        # Calculate road distance
        road_distance = calculate_distance(origin, destination, GOOGLE_API_KEY)

        if isinstance(road_distance, str):
            logger.error(f"Distance calculation failed: {road_distance}")
            return jsonify({"error": road_distance}), 400

        logger.debug(f"Successfully calculated road distance: {road_distance}")

        # Calculate railway metrics
        railway_metrics = calculate_railway_metrics(road_distance)

        return jsonify({
            "road_distance": road_distance,
            "railway_metrics": railway_metrics
        })

    except Exception as e:
        logger.error(f"Error in calculate route: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)