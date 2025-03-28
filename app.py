from flask import Flask, render_template, request, jsonify
from utils import calculate_population_from_api, calculate_distance, calculate_railway_metrics, calculate_population, calculate_ridership, revenue, travel_time, yearly_cost, yearly_profit, years_to_profit

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
    ninjas_api_key = 'YOUR_NINJAS_API_KEY'  # Replace with your actual API key

    road_distance = calculate_distance(origin, destination, api_key)
    if isinstance(road_distance, str):
        return jsonify({'error': road_distance}), 400

    railway_metrics = calculate_railway_metrics(road_distance)
    populationA = calculate_population_from_api(origin, ninjas_api_key)  # Replace with actual coordinates
    print(populationA)

    populationB = calculate_population_from_api(destination, ninjas_api_key)  # Replace with actual coordinates
    ridership = calculate_ridership(populationA, populationB, road_distance)
    yearly_revenue_value = revenue(ridership) # CHANGED
    yearly_cost_value = yearly_cost(road_distance) # CHANGED
    yearly_profit_value = yearly_profit(yearly_cost_value, yearly_revenue_value) #CHANGED
    travel_time_value = travel_time(road_distance) #CHANGED
    years_to_even = years_to_profit(railway_metrics.get("estimated_cost"), yearly_profit_value) #CHANGED

    return jsonify({
        'estimated_cost': railway_metrics.get("estimated_cost"),
        'ridership': ridership,
        'road_distance': road_distance,
        'travel_time': travel_time_value,
        'yearly_cost': yearly_cost_value,
        'years_to_even': years_to_even,
        'profit': yearly_profit_value,
        'populationA': populationA,
        'populationB': populationB
    })

if __name__ == '__main__':
    app.run(debug=True)
