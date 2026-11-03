from pydantic import BaseModel, ConfigDict, Field


class ProductData(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nombre: str = Field(min_length=1, max_length=100)
    categoria: str = Field(min_length=1, max_length=60)
    precio: float = Field(ge=0, allow_inf_nan=False)
    stock: int = Field(ge=0)


class Product(ProductData):
    id: int = Field(gt=0)
