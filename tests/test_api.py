import pytest
from fastapi.testclient import TestClient
from main import app
from models.users import User
from routers.products import productos
from routers.users import usuarios

client = TestClient(app)


@pytest.fixture(autouse=True)
def reiniciar_datos():
    usuarios[:] = [
        User(id=1, name="Juan Pérez"),
        User(id=2, name="Ana López", is_active=False),
    ]
    productos.clear()
    yield
    productos.clear()


def test_documentacion():
    assert client.get("/").status_code == 200
    assert client.get("/docs").status_code == 200
    assert client.get("/openapi.json").status_code == 200


def test_filtro_usuarios():
    assert len(client.get("/user").json()["users"]) == 2
    assert [u["id"] for u in client.get("/user?is_active=true").json()["users"]] == [1]
    assert [u["id"] for u in client.get("/user?is_active=false").json()["users"]] == [2]
    assert client.get("/user?is_active=otro").status_code == 422


def test_crud_usuario():
    response = client.post("/user", json={"id": 3, "name": "Luis"})
    assert response.status_code == 201
    assert response.json()["is_active"] is True
    assert client.get("/user/3").json()["name"] == "Luis"
    response = client.put("/user/3", json={"name": "Luisa", "is_active": False})
    assert response.status_code == 200
    assert response.json() == {"id": 3, "name": "Luisa", "is_active": False}
    assert client.get("/user/3").json()["name"] == "Luisa"
    assert client.delete("/user/3").status_code == 200
    assert client.get("/user/3").status_code == 404


def test_usuario_duplicado():
    assert client.post("/user", json={"id": 1, "name": "Otro"}).status_code == 409
    assert len(usuarios) == 2


@pytest.mark.parametrize("datos", [
    {"id": 0, "name": "Ana"}, {"id": 3, "name": "   "}, {"id": 3},
])
def test_usuario_invalido(datos):
    assert client.post("/user", json=datos).status_code == 422
    assert len(usuarios) == 2


def test_usuario_no_encontrado():
    assert client.get("/user/99").status_code == 404
    assert client.put("/user/99", json={"name": "Ana"}).status_code == 404
    assert client.delete("/user/99").status_code == 404


def producto(id=1, categoria="Librería"):
    return {"id": id, "nombre": "Cuaderno", "categoria": categoria, "precio": 2500, "stock": 10}


def test_crud_producto():
    assert client.get("/products").json() == []
    response = client.post("/products", json=producto())
    assert response.status_code == 201
    assert set(response.json()) == {"id", "nombre", "categoria", "precio", "stock"}
    assert client.get("/products/1").json() == producto()
    datos = {"nombre": "Cuaderno A4", "categoria": "Escolar", "precio": 2800, "stock": 4}
    response = client.put("/products/1", json=datos)
    assert response.status_code == 200
    assert response.json() == {"id": 1, **datos}
    assert client.get("/products/1").json()["stock"] == 4
    assert client.delete("/products/1").status_code == 200
    assert client.get("/products/1").status_code == 404
    assert client.get("/products").json() == []


def test_filtrar_productos():
    client.post("/products", json=producto())
    client.post("/products", json=producto(2, "Oficina"))
    assert len(client.get("/products").json()) == 2
    assert [p["id"] for p in client.get("/products", params={"categoria": "librería"}).json()] == [1]
    assert client.get("/products", params={"categoria": "Hogar"}).json() == []


def test_producto_duplicado():
    client.post("/products", json=producto())
    assert client.post("/products", json=producto()).status_code == 409
    assert len(productos) == 1


@pytest.mark.parametrize("campo,valor", [
    ("id", 0), ("nombre", " "), ("categoria", ""), ("precio", -1), ("stock", -1), ("stock", 1.5),
])
def test_producto_invalido(campo, valor):
    datos = producto()
    datos[campo] = valor
    assert client.post("/products", json=datos).status_code == 422
    assert productos == []


def test_actualizacion_invalida_no_modifica():
    client.post("/products", json=producto())
    datos = producto()
    datos.pop("id")
    datos["precio"] = -10
    assert client.put("/products/1", json=datos).status_code == 422
    assert client.get("/products/1").json()["precio"] == 2500
    assert client.put("/user/1", json={"name": ""}).status_code == 422
    assert client.get("/user/1").json()["name"] == "Juan Pérez"


def test_producto_no_encontrado():
    datos = producto()
    datos.pop("id")
    assert client.get("/products/99").status_code == 404
    assert client.put("/products/99", json=datos).status_code == 404
    assert client.delete("/products/99").status_code == 404
