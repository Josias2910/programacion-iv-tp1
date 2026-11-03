from fastapi import APIRouter, HTTPException, Query, status
from models.products import Product, ProductData
from models.users import MessageResponse

router = APIRouter(prefix="/products", tags=["Productos"])
productos: list[Product] = []


def buscar_producto(id: int) -> Product:
    for producto in productos:
        if producto.id == id:
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")


@router.get("", response_model=list[Product])
def get_products(categoria: str | None = Query(default=None, min_length=1)):
    if categoria is None:
        return productos
    return [
        producto for producto in productos
        if producto.categoria.casefold() == categoria.strip().casefold()
    ]


@router.get("/{id}", response_model=Product)
def get_product(id: int):
    return buscar_producto(id)


@router.post("", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    if any(producto.id == product.id for producto in productos):
        raise HTTPException(status_code=409, detail="Ya existe un producto con ese id")
    productos.append(product)
    return product


@router.put("/{id}", response_model=Product)
def update_product(id: int, datos: ProductData):
    producto = buscar_producto(id)
    producto.nombre = datos.nombre
    producto.categoria = datos.categoria
    producto.precio = datos.precio
    producto.stock = datos.stock
    return producto


@router.delete("/{id}", response_model=MessageResponse)
def delete_product(id: int):
    producto = buscar_producto(id)
    productos.remove(producto)
    return MessageResponse(message="Producto eliminado")
