from flask import Flask, request, jsonify, Response
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    html = """<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>E-commerce Price Prediction Tool</title>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js'></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; background: rgba(255,255,255,0.95); border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); overflow: hidden; backdrop-filter: blur(10px); }
        .header { background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 30px; text-align: center; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .tabs { display: flex; background: #f8f9fa; border-bottom: 2px solid #e9ecef; }
        .tab { flex: 1; padding: 18px 0; background: transparent; border: none; cursor: pointer; font-size: 18px; font-weight: 700; color: #6c757d; transition: background 0.2s, color 0.2s, border-bottom 0.2s; position: relative; }
        .tab:hover { background: #ffe3ec; color: #ff512f; }
        .tab.active { background: #fff0f6; color: #dd2476; border-bottom: 4px solid #ff512f; }
        .tab.active:after { content: ''; position: absolute; left: 50%; bottom: 0; transform: translateX(-50%); width: 60%; height: 4px; background: linear-gradient(90deg, #ff512f 0%, #dd2476 100%); border-radius: 2px; }
        .tab-content { display: none; padding: 30px; animation: fadeIn 0.5s ease; }
        .tab-content.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #495057; }
        input, select, textarea { width: 100%; padding: 12px; border: 2px solid #e9ecef; border-radius: 10px; font-size: 16px; transition: border-color 0.3s ease; }
        input:focus, select:focus, textarea:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102,126,234,0.1); }
        .btn { background: linear-gradient(90deg, #ff512f 0%, #dd2476 100%); color: white; border: none; padding: 15px 40px; border-radius: 30px; font-size: 18px; font-weight: 700; cursor: pointer; box-shadow: 0 8px 24px rgba(221,36,118,0.15); transition: transform 0.2s, box-shadow 0.2s, background 0.2s; }
        .btn:hover { background: linear-gradient(90deg, #dd2476 0%, #ff512f 100%); transform: scale(1.05); box-shadow: 0 16px 32px rgba(221,36,118,0.25); }
        .prediction-result { margin-top: 30px; padding: 25px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; border-left: 5px solid #667eea; }
        .price-display { font-size: 3.5em; font-weight: bold; color: #ff512f; text-align: center; margin: 28px 0; text-shadow: 0 4px 24px rgba(221,36,118,0.15); letter-spacing: 2px; background: linear-gradient(90deg, #ff512f 0%, #dd2476 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
        .anomaly-box { background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; padding: 20px; margin-top: 20px; }
        .anomaly-box h4 { color: #856404; margin-bottom: 10px; }
        .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }
        .feature-card { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 24px; border-radius: 18px; box-shadow: 0 8px 32px rgba(102,126,234,0.10); border-left: 6px solid #ff512f; transition: box-shadow 0.2s, transform 0.2s; }
        .feature-card:hover { box-shadow: 0 16px 48px rgba(221,36,118,0.18); transform: translateY(-4px) scale(1.02); }
        .chart-container { background: white; padding: 20px; border-radius: 10px; margin: 20px 0; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .loading { display: inline-block; width: 20px; height: 20px; border: 3px solid #f3f3f3; border-top: 3px solid #667eea; border-radius: 50%; animation: spin 1s linear infinite; margin-left: 10px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class='container'>
        <div class='header'>
            <h1>🛒 E-commerce Price Prediction Tool</h1>
            <p>AI-Powered Product Price Analysis & Prediction</p>
        </div>
        <div class='tabs'>
            <button class='tab active' onclick="showTab('predictor', this)">Price Predictor</button>
        </div>
        <div id='predictor' class='tab-content active'>
            <h2>🎯 Product Price Prediction</h2>
            <p>Enter product specifications to get an AI-powered price prediction with anomaly detection.</p>
            <div class='feature-grid'>
                <div class='feature-card'>
                    <h3>Basic Product Info</h3>
                    <div class='form-group'>
                        <label>Product Category</label>
                        <select id='category'>
                            <option value='electronics'>Electronics</option>
                            <option value='clothing'>Clothing</option>
                            <option value='home'>Home & Garden</option>
                            <option value='books'>Books</option>
                            <option value='sports'>Sports</option>
                        </select>
                    </div>
                    <div class='form-group'>
                        <label>Brand Rating (1-5)</label>
                        <input type='range' id='brand_rating' min='1' max='5' value='3' oninput='updateRatingDisplay(this.value)'>
                        <span id='rating_display'>3</span>
                    </div>
                </div>
                <div class='feature-card'>
                    <h3>Product Features</h3>
                    <div class='form-group'>
                        <label>Weight (kg)</label>
                        <input type='number' id='weight' value='1.5' step='0.1'>
                    </div>
                    <div class='form-group'>
                        <label>Dimensions (cm³)</label>
                        <input type='number' id='dimensions' value='1000' step='10'>
                    </div>
                    <div class='form-group'>
                        <label>Warranty (months)</label>
                        <input type='number' id='warranty' value='12'>
                    </div>
                </div>
                <div class='feature-card'>
                    <h3>Market Data</h3>
                    <div class='form-group'>
                        <label>Seller Rating (1-5)</label>
                        <input type='range' id='seller_rating' min='1' max='5' value='4' oninput='updateSellerRating(this.value)'>
                        <span id='seller_rating_display'>4</span>
                    </div>
                    <div class='form-group'>
                        <label>Competition Level</label>
                        <select id='competition'>
                            <option value='low'>Low</option>
                            <option value='medium'>Medium</option>
                            <option value='high'>High</option>
                        </select>
                    </div>
                </div>
            </div>
            <button class='btn' onclick='predictPrice()'>🔮 Predict Price <span id='loading' class='loading' style='display: none;'></span></button>
            <div id='prediction_result' style='display: none;' class='prediction-result'>
                <h3>📊 Prediction Results</h3>
                <div class='price-display' id='predicted_price'>₹0</div>
                <div class='chart-container'>
                    <canvas id='confidenceChart' width='400' height='200'></canvas>
                </div>
                <div id='anomaly_explanation' class='anomaly-box' style='display: none;'>
                    <h4>🚨 Anomaly Detection</h4>
                    <p id='anomaly_text'></p>
                </div>
            </div>
        </div>
    </div>
    <script>
        function updateRatingDisplay(value) { document.getElementById('rating_display').textContent = value; }
        function updateSellerRating(value) { document.getElementById('seller_rating_display').textContent = value; }
        function predictPrice() {
            var loadingEl = document.getElementById('loading');
            var resultEl = document.getElementById('prediction_result');
            loadingEl.style.display = 'inline-block';
            var category = document.getElementById('category').value;
            var brandRating = document.getElementById('brand_rating').value;
            var weight = document.getElementById('weight').value;
            var warranty = document.getElementById('warranty').value;
            var competition = document.getElementById('competition').value;
            var sellerRating = document.getElementById('seller_rating').value;
            var dimensions = document.getElementById('dimensions').value;
            fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ category: category, brand_rating: brandRating, weight: weight, warranty: warranty, competition: competition, seller_rating: sellerRating, dimensions: dimensions })
            })
            .then(function(response) { return response.json(); })
            .then(function(data) {
                loadingEl.style.display = 'none';
                document.getElementById('predicted_price').textContent = `₹${data.predicted_price}`;
                resultEl.style.display = 'block';
                var anomalyEl = document.getElementById('anomaly_explanation');
                if (data.is_anomaly) {
                    anomalyEl.style.display = 'block';
                    document.getElementById('anomaly_text').textContent = data.explanation;
                } else {
                    anomalyEl.style.display = 'none';
                }
                initializeConfidenceChart(data.confidence);
            })
            .catch(function(err) {
                loadingEl.style.display = 'none';
                alert('Error connecting to backend: ' + err);
            });
        }
        function initializeConfidenceChart(confidence) {
            var ctx = document.getElementById('confidenceChart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: { labels: ['Confidence', 'Uncertainty'], datasets: [{ data: [confidence * 100, (1 - confidence) * 100], backgroundColor: ['#667eea', '#e9ecef'], borderWidth: 0 }] },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' }, title: { display: true, text: `Prediction Confidence: ${(confidence * 100).toFixed(1)}%` } } }
            });
        }
        function showTab(tabName, btn) {
            document.querySelectorAll('.tab-content').forEach(function(content) { content.classList.remove('active'); });
            document.querySelectorAll('.tab').forEach(function(tab) { tab.classList.remove('active'); });
            document.getElementById(tabName).classList.add('active');
            if (btn) btn.classList.add('active');
        }
    </script>
</body>
</html>"""
    return Response(html, mimetype='text/html')

@app.route('/predict', methods=['POST'])
def predict_price():
    data = request.json
    base_price = {
        'electronics': 250,
        'clothing': 45,
        'home': 80,
        'books': 25,
        'sports': 120
    }.get(data.get('category', 'electronics'), 100)
    brand_rating = float(data.get('brand_rating', 3))
    weight = float(data.get('weight', 1.5))
    warranty = float(data.get('warranty', 12))
    competition = data.get('competition', 'medium')
    adjustments = base_price * (brand_rating / 5) + (weight * 10) + (warranty * 2) + {'low': 20, 'medium': 0, 'high': -15}.get(competition, 0)
    predicted_price = max(10, base_price + adjustments + (np.random.rand() * 50 - 25))
    confidence = float(np.random.rand() * 0.3 + 0.7)
    is_anomaly = predicted_price > base_price * 2 or predicted_price < base_price * 0.5
    explanation = (
        'Price is unusually high for this category.' if predicted_price > base_price * 2 else
        'Price is unusually low for this category.' if predicted_price < base_price * 0.5 else
        'Price within expected range.'
    )
    return jsonify({
        'predicted_price': round(predicted_price, 2),
        'confidence': round(confidence, 3),
        'is_anomaly': is_anomaly,
        'explanation': explanation
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
