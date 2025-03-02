# Rapid.Tech Railway Simulator

## Overview
The Rapid.Tech Railway Simulator is a project that calculates the distance between two locations based on current roads and estimates the cost of building a high-speed railway between them. It also analyzes the population and potential ridership benefits.

## Features
- Calculate road distance using Google Distance Matrix API
- Estimate railway construction costs
- Analyze population and potential ridership
- Adjustable parameters for population radius, ticket price, and max speed

## Setup Instructions
1. Clone the repository:
   ```sh
   git clone https://github.com/EvanOleary26/RapidTech.git
   cd RapidTech
   ```

2. Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Reassemble the population cache file:
   ```sh
   python scripts/reassemble_population_cache.py
   ```

5. Set up environment variables:
   ```sh
   export GOOGLE_API_KEY='YOUR_GOOGLE_API_KEY'
   ```

6. Run the Flask application:
   ```sh
   python app.py
   ```

## Usage Instructions
1. Open a web browser and navigate to `http://127.0.0.1:5000/`.
2. Enter the origin and destination locations.
3. Adjust the parameters as needed in the "Map" tab.
4. Click "Calculate" to see the results.

## Contributors
- [Isabelle Hageman](https://www.linkedin.com/in/isabelle-hageman/)
- [Evan O'Leary](https://www.linkedin.com/in/evan-o-leary-8509812bb)
- [Reece Whitacker](https://www.linkedin.com/in/reece-whitaker/)

## Acknowledgments
- Thanks to KineticVision and Major League Hacking for their informational sessions on APIs and Machine Learning Usage during the Hackathon.
- Thanks to Revolution UC and all their sponsors for hosting the event.
