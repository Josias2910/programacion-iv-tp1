from fastapi import FastAPI
from routers import products, users

app = FastAPI(title="TP1 - Usuarios y productos")
app.include_router(users.router)
app.include_router(products.router)


@app.get("/")
def read_root():
    return {"message": "API de usuarios y productos. Documentación en /docs"}
