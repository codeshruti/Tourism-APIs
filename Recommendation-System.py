from flask import Flask, request, jsonify
import pandas as pd
import folium
from streamlit_folium import folium_static

app = Flask(__name__)

def generate_recommendations(destination, category):
    # load recommendations data
    recommendations = pd.read_csv('recommendations.csv')

    # filter recommendations based on user input
    filtered_recommendations = recommendations[(recommendations['Destination'] == destination) &
                                               (recommendations['Category'] == category)]

    # create map with recommendations
    map_center = filtered_recommendations[['Latitude', 'Longitude']].mean().values.tolist()
    my_map = folium.Map(location=map_center, zoom_start=12, tiles='OpenStreetMap')
    for _, row in filtered_recommendations.iterrows():
        folium.Marker([row['Latitude'], row['Longitude']],
                      popup=row['Name'],
                      tooltip=row['Name']).add_to(my_map)

    # create HTML table with recommendations
    table = filtered_recommendations[['Name', 'Description', 'Reviews', 'Google Rating(out of 5)']]
    table_html = table.to_html(index=False, escape=False)

    return my_map, table_html


@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    destination = data['destination']
    category = data['category']

    if destination and category:
        map_obj, table_html = generate_recommendations(destination, category)
        map_obj.save('recommendations_map.html')

        response = {
            'map_html': map_obj.get_root().render(),
            'table_html': table_html
        }

        return jsonify(response)
    else:
        return jsonify({'error': 'Please provide destination and category.'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

