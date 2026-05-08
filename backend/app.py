from flask import Flask, jsonify, request
from flasgger import Swagger
from flask_cors import CORS
from database import init_db, get_connection

app = Flask(__name__)
CORS(app)

# Inicializamos Swagger para la documentación de la API
swagger = Swagger(app)

init_db()
# --- Base de datos en memoria ---
# Catálogo de productos disponibles
#PRODUCTOS = [
#    {"id": 1, "nombre": "Espresso", "precio": 1500},
#    {"id": 2, "nombre": "Latte Macchiato", "precio": 2200},
#    {"id": 3, "nombre": "Flat White", "precio": 2000},
#]

# Carrito de compras
#CARRITO = []

# --- Endpoints ---

@app.route('/api/carrito', methods=['GET'])
def obtener_carrito():
    """
    Obtiene el carrito actual.
    ---
    responses:
      200:
        description: Carrito actual
    """
    connection = get_connection()

    items = connection.execute("""
        SELECT 
            carrito.id,
            productos.id AS producto_id,
            productos.nombre,
            productos.precio,
            carrito.cantidad,
            productos.precio * carrito.cantidad AS subtotal
        FROM carrito
        JOIN productos ON carrito.producto_id = productos.id
    """).fetchall()

    connection.close()

    carrito_json = []

    for item in items:
        carrito_json.append({
            "id": item["id"],
            "producto_id": item["producto_id"],
            "nombre": item["nombre"],
            "precio": item["precio"],
            "cantidad": item["cantidad"],
            "subtotal": item["subtotal"]
        })

    return jsonify(carrito_json), 200

@app.route('/api/productos', methods=['GET'])
def listar_productos():
    """
    Lista todos los productos disponibles.
    ---
    responses:
      200:
        description: Una lista de productos
    """
    connection = get_connection()
    productos = connection.execute("SELECT * FROM productos").fetchall()
    connection.close()

    productos_json = []

    for producto in productos:
        productos_json.append({
            "id": producto["id"],
            "nombre": producto["nombre"],
            "precio": producto["precio"]
        })

    return jsonify(productos_json), 200


@app.route('/api/carrito', methods=['POST'])
def agregar_al_carrito():
    """
    Agrega un producto al carrito.
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - id
          properties:
            id:
              type: integer
              description: ID del producto a agregar en el catálogo
            cantidad:
              type: integer
              description: Cantidad a agregar
    responses:
      201:
        description: Producto agregado exitosamente
      400:
        description: Datos inválidos
      404:
        description: Producto no encontrado
    """
    data = request.get_json()

    if not data or "id" not in data:
        return jsonify({"error": "Falta el ID del producto"}), 400

    producto_id = data.get("id")
    cantidad = data.get("cantidad", 1)

    if not isinstance(cantidad, int) or cantidad <= 0:
        return jsonify({"error": "La cantidad debe ser un número entero mayor a 0"}), 400

    connection = get_connection()

    producto = connection.execute(
        "SELECT * FROM productos WHERE id = ?",
        (producto_id,)
    ).fetchone()

    if producto is None:
        connection.close()
        return jsonify({"error": "Producto no encontrado en el catálogo"}), 404

    item_existente = connection.execute(
        "SELECT * FROM carrito WHERE producto_id = ?",
        (producto_id,)
    ).fetchone()

    if item_existente:
        nueva_cantidad = item_existente["cantidad"] + cantidad

        connection.execute(
            "UPDATE carrito SET cantidad = ? WHERE producto_id = ?",
            (nueva_cantidad, producto_id)
        )
    else:
        connection.execute(
            "INSERT INTO carrito (producto_id, cantidad) VALUES (?, ?)",
            (producto_id, cantidad)
        )

    connection.commit()
    connection.close()

    return jsonify({"mensaje": "Producto agregado al carrito"}), 201


@app.route('/api/carrito/<int:producto_id>', methods=['DELETE'])
def eliminar_del_carrito(producto_id):
    """
    Elimina un producto del carrito.
    ---
    parameters:
      - in: path
        name: producto_id
        type: integer
        required: true
        description: ID del producto a eliminar
    responses:
      200:
        description: Producto eliminado exitosamente
      404:
        description: Producto no encontrado en el carrito
    """
    connection = get_connection()

    item = connection.execute(
        "SELECT * FROM carrito WHERE producto_id = ?",
        (producto_id,)
    ).fetchone()

    if item is None:
        connection.close()
        return jsonify({"error": "Producto no encontrado en el carrito"}), 404

    connection.execute(
        "DELETE FROM carrito WHERE producto_id = ?",
        (producto_id,)
    )

    connection.commit()
    connection.close()

    return jsonify({"mensaje": "Producto eliminado del carrito"}), 200

@app.route('/api/carrito/total', methods=['GET'])
def calcular_total():
    """
    Calcula el total de la compra.
    ---
    responses:
      200:
        description: Total calculado exitosamente
    """
    connection = get_connection()

    resultado = connection.execute("""
        SELECT 
            SUM(productos.precio * carrito.cantidad) AS total,
            SUM(carrito.cantidad) AS cantidad_items
        FROM carrito
        JOIN productos ON carrito.producto_id = productos.id
    """).fetchone()

    connection.close()

    total = resultado["total"] if resultado["total"] is not None else 0
    cantidad_items = resultado["cantidad_items"] if resultado["cantidad_items"] is not None else 0

    return jsonify({
        "total": total,
        "moneda": "ARS",
        "cantidad_items": cantidad_items
    }), 200

if __name__ == '__main__':
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)