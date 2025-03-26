from flask import Flask, render_template, request, jsonify
from utils import calculate_distance, calculate_railway_metrics, calculate_population, calculate_ridership, revenue, travel_time, yearly_cost, yearly_profit

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    origin = request.form.get('origin')
    destination = request.form.get('destination')
    api_key = 'YOUR_GOOGLE_API_KEY'  # Replace with your actual API key

    road_distance = calculate_distance(origin, destination, api_key)
    if isinstance(road_distance, str):
        return jsonify({'error': road_distance}), 400

    railway_metrics = calculate_railway_metrics(road_distance)
    populationA = calculate_population(0, 0, 50)  # Replace with actual coordinates
    populationB = calculate_population(0, 0, 50)  # Replace with actual coordinates
    ridership = calculate_ridership(populationA, populationB, road_distance)
    yearly_revenue = 1 # CHANGED
    yearly_cost_value = 1 # CHANGED
    yearly_profit_value = 1 #CHANGED

    return jsonify({
        'road_distance': road_distance,
        'railway_metrics': railway_metrics,
        'ridership': ridership,
        'yearly_revenue': yearly_revenue,
        'yearly_cost': yearly_cost_value,
        'yearly_profit': yearly_profit_value
    })

if __name__ == '__main__':
    app.run(debug=True)
