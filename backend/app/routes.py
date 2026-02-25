from flask import Flask, jsonify, request
from flask_cors import CORS
from app.models.dataset import GameDataset
from app.controllers.data_controller import DataController

app = Flask(__name__)
CORS(app)

dataset = GameDataset()
controller = DataController(dataset.get_df())

#Endpoint to know the games with top global sales
@app.route('/api/top-global-sales/', methods=['GET'])
def top_global():
    try:
        top_sales = controller.top_global_sales()
        return jsonify(top_sales)
    except Exception as e:
        return jsonify({'error':str(e)}), 500

#Endpoint to know the sales for each game genre
@app.route('/api/sales-by-genre/', methods=['GET'])
def sales_genre():
    try:
        sales_genre = controller.sales_by_genre()
        return jsonify(sales_genre)
    except Exception as e:
        return jsonify({'error':str(e)}),500
    
#Endpoint to know the top publishers of games
@app.route('/api/top-publishers/', methods=['GET'])
def top_publishers():
    try:
        top_pub = controller.top_publishers()
        return jsonify(top_pub)
    except Exception as e:
        return jsonify({'error':str(e)}), 500

#Endpoint to know the sales by region
@app.route('/api/sales-by-region/', methods=['GET'])
def sales_region():
    try:
        sale_reg = controller.sales_by_region()
        return jsonify(sale_reg)
    except Exception as e:
        return jsonify({'error':str(e)}), 500

#Endpoint to know the best games of community
@app.route('/api/best-games-users/', methods=['GET'])
def best_games():
    try:
        genre = request.args.get('genre')
        rating = request.args.get('rating')
        score = request.args.get('min_score', type=float)

        if genre is None or rating is None or score is None:
            return jsonify({
                'error': 'Parámetros inválidos o faltantes',
                'mensaje': 'Se requiere genero, clasificacion de edad y calificacion de usuario'
            }), 400
        
        try:
            min_score = float(score)
        except ValueError:
            return jsonify({"error": "calificacion de usuario debe ser decimal"}), 400
        
        result = controller.recommended_games(genre,rating,min_score)

        if not result:
            return jsonify({"mensaje":"No se encontaron juegos con esos criterios"})
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error':str(e)}), 500

