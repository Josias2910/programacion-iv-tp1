from fastapi import APIRouter, HTTPException, Query, status
from models.products import Product, ProductData
from models.users import MessageResponse
from repositories.products import productos_repo

router = APIRouter(prefix="/products", tags=["Productos"])


@router.get("", response_model=list[Product])
def get_products(categoria: str | None = Query(default=None, min_length=1)):
    return productos_repo.listar(categoria)


@router.get("/{id}", response_model=Product)
def get_product(id: int):
    producto = productos_repo.buscar(id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.post("", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    if not productos_repo.crear(product):
        raise HTTPException(status_code=409, detail="Ya existe un producto con ese id")
    return product


@router.put("/{id}", response_model=Product)
def update_product(id: int, datos: ProductData):
    producto = productos_repo.actualizar(id, datos)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.delete("/{id}", response_model=MessageResponse)
def delete_product(id: int):
    if not productos_repo.eliminar(id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return MessageResponse(message="Producto eliminado")
