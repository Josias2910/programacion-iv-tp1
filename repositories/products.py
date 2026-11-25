from models.products import Product, ProductData


class ProductsRepository:
    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self._productos: list[Product] = []

    def listar(self, categoria: str | None = None) -> list[Product]:
        if categoria is None:
            return list(self._productos)
        buscada = categoria.strip().casefold()
        return [
            producto for producto in self._productos
            if producto.categoria.casefold() == buscada
        ]

    def buscar(self, id: int) -> Product | None:
        return next((producto for producto in self._productos if producto.id == id), None)

    def crear(self, producto: Product) -> bool:
        if self.buscar(producto.id) is not None:
            return False
        self._productos.append(producto)
        return True

    def actualizar(self, id: int, datos: ProductData) -> Product | None:
        producto = self.buscar(id)
        if producto is not None:
            producto.nombre = datos.nombre
            producto.categoria = datos.categoria
            producto.precio = datos.precio
            producto.stock = datos.stock
        return producto

    def eliminar(self, id: int) -> bool:
        producto = self.buscar(id)
        if producto is None:
            return False
        self._productos.remove(producto)
        return True


productos_repo = ProductsRepository()
