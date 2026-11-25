from fastapi import APIRouter, HTTPException, status
from models.users import GetUsersResponse, MessageResponse, User, UserData
from repositories.users import usuarios_repo

router = APIRouter(prefix="/user", tags=["Usuarios"])


@router.get("", response_model=GetUsersResponse)
def get_users(is_active: bool | None = None):
    return GetUsersResponse(users=usuarios_repo.listar(is_active))


@router.get("/{id}", response_model=User)
def get_user(id: int):
    usuario = usuarios_repo.buscar(id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    if not usuarios_repo.crear(user):
        raise HTTPException(status_code=409, detail="Ya existe un usuario con ese id")
    return user


@router.put("/{id}", response_model=User)
def update_user(id: int, datos: UserData):
    usuario = usuarios_repo.actualizar(id, datos)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.delete("/{id}", response_model=MessageResponse)
def delete_user(id: int):
    if not usuarios_repo.eliminar(id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return MessageResponse(message="Usuario eliminado")
