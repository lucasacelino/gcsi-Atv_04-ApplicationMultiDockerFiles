from flask import Flask, jsonify, request
import os
import psycopg2
app = Flask(__name__)

def conectar():
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )
    
    return conn

@app.get("/")
def index():
    try:
        conn = conectar()
        return "Conectado ao banco com sucesso!"
    except Exception as e:
        return f"Erro ao conectar: {e}"
    

@app.route('/produtos', methods=['POST'])
def criar_produto():
    dados = request.get_json()
    restaurant = dados.get('restaurant')
    customer = dados.get('customer')
    order_value = dados.get('order_value')
    payment_method = dados.get('payment_method')
    status = dados.get('status')
    order_date = dados.get('order_date')

    try:
        conn = conectar()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO produtos (restaurant, customer, order_value, payment_method, status, order_date) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
            (restaurant, customer, order_value, payment_method, status, order_date)
        )

        novo_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"mensagem": "Produto criado!", "id": novo_id}), 201

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.get("/produtos")
def listarProdutos():
    try:
        conn = conectar()
        cur = conn.cursor()

        cur.execute("SELECT id, restaurant, customer, order_value, payment_method, status, order_date FROM produtos")
        produtos = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify([
            {"id": p[0], "restaurant": p[1], "costumer": p[2], "order_value": p[3], "payment_method": p[4], "status": p[5], "order_date": p[6]} for p in produtos
        ])
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)