# TP1 - ABM de usuarios y productos

API realizada a partir del ejemplo `clase-fastapi` de Programación IV.
Usa FastAPI, modelos Pydantic y listas en memoria. Los cambios se pierden
al reiniciar el servidor. Requiere Python 3.10 o superior.

## Instalación y ejecución

Desde la carpeta del proyecto:

```bash
python -m venv .venv
```

Activar el entorno:

```powershell
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
```

```bash
# Linux / macOS
source .venv/bin/activate
```

```bash
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Abrir http://127.0.0.1:8000/docs para probar los endpoints con Swagger.

## Usuarios

- `GET /user`: listar todos.
- `GET /user?is_active=true`: listar activos (`false` para inactivos).
- `GET /user/{id}`: buscar por id.
- `POST /user`: crear con `id`, `name` e `is_active` (opcional, por defecto `true`).
- `PUT /user/{id}`: reemplazar `name` e `is_active`; el id no cambia.
- `DELETE /user/{id}`: eliminar.

## Productos

La entidad propia tiene cinco campos: `id`, `nombre`, `categoria`, `precio` y `stock`.

- `GET /products`: listar.
- `GET /products?categoria=Librería`: filtrar por categoría, sin distinguir mayúsculas.
- `GET /products/{id}`: obtener un producto.
- `POST /products`: crear un producto.
- `PUT /products/{id}`: reemplazar sus datos, excepto el id.
- `DELETE /products/{id}`: eliminar.

Ejemplo para crear:

```json
{"id": 1, "nombre": "Cuaderno", "categoria": "Librería", "precio": 2500, "stock": 10}
```

Para modificar se envían los mismos datos sin `id`. Los identificadores se ingresan
al crear cada registro y no pueden repetirse. Los datos inválidos devuelven 422;
los ids repetidos, 409; y los registros inexistentes, 404.

## Pruebas

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Consigna: https://github.com/ffumaneri/utn-tup-2026-python/blob/main/trabajos_practicos/TP1-fastapi-abm-usuarios.md
