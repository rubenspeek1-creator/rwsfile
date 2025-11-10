from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/traffic.geojson")
def traffic_geojson():
    url = "https://api.rwsverkeersinfo.nl/api/traffic/"
    r = requests.get(url)
    data = r.json()

    # Zet om naar GeoJSON-features
    features = []
    for event in data.get("events", []):
        start = event.get("start", {})
        if "lat" in start and "lon" in start:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [start["lon"], start["lat"]]
                },
                "properties": {
                    "id": event.get("id"),
                    "type": event.get("type"),
                    "road": event.get("road"),
                    "from": event.get("from"),
                    "to": event.get("to"),
                    "length": event.get("distance"),
                    "delay": event.get("delay"),
                }
            }
            features.append(feature)

    geojson = {"type": "FeatureCollection", "features": features}
    return jsonify(geojson)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
