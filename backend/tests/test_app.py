import pytest
from app import app
from database import get_connection, init_db


@pytest.fixture
def client():
    app.config["TESTING"] = True

    init_db()

    # Limpiamos el carrito antes de cada test
    connection = get_connection()
    connection.execute("DELETE FROM carrito")
    connection.commit()
    connection.close()

    with app.test_client() as client:
        yield client


def test_listar_productos(client):
    response = client.get("/api/productos")

    assert response.status_code == 200

    productos = response.get_json()

    assert isinstance(productos, list)
    assert len(productos) > 0
    assert productos[0]["id"] == 1
    assert "nombre" in productos[0]
    assert "precio" in productos[0]


def test_obtener_carrito_vacio(client):
    response = client.get("/api/carrito")

    assert response.status_code == 200
    assert response.get_json() == []


def test_agregar_producto_al_carrito(client):
    response = client.post("/api/carrito", json={
        "id": 1,
        "cantidad": 2
    })

    assert response.status_code == 201

    data = response.get_json()
    assert data["mensaje"] == "Producto agregado al carrito"

    carrito_response = client.get("/api/carrito")
    carrito = carrito_response.get_json()

    assert len(carrito) == 1
    assert carrito[0]["producto_id"] == 1
    assert carrito[0]["cantidad"] == 2


def test_agregar_producto_inexistente(client):
    response = client.post("/api/carrito", json={
        "id": 999,
        "cantidad": 1
    })

    assert response.status_code == 404

    data = response.get_json()
    assert "error" in data


def test_agregar_producto_cantidad_invalida(client):
    response = client.post("/api/carrito", json={
        "id": 1,
        "cantidad": 0
    })

    assert response.status_code == 400

    data = response.get_json()
    assert "error" in data


def test_calcular_total(client):
    client.post("/api/carrito", json={
        "id": 1,
        "cantidad": 2
    })

    response = client.get("/api/carrito/total")

    assert response.status_code == 200

    data = response.get_json()

    assert data["total"] == 3000
    assert data["moneda"] == "ARS"
    assert data["cantidad_items"] == 2


def test_eliminar_producto_del_carrito(client):
    client.post("/api/carrito", json={
        "id": 1,
        "cantidad": 1
    })

    response = client.delete("/api/carrito/1")

    assert response.status_code == 200

    data = response.get_json()
    assert data["mensaje"] == "Producto eliminado del carrito"

    carrito_response = client.get("/api/carrito")
    carrito = carrito_response.get_json()

    assert carrito == []


def test_eliminar_producto_inexistente_del_carrito(client):
    response = client.delete("/api/carrito/999")

    assert response.status_code == 404

    data = response.get_json()
    assert "error" in data