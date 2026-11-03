from fastapi import APIRouter, HTTPException, status
from models.users import GetUsersResponse, MessageResponse, User, UserData

router = APIRouter(prefix="/user", tags=["Usuarios"])
usuarios: list[User] = [
    User(id=1, name="Juan Pérez"),
    User(id=2, name="Ana López", is_active=False),
]


def buscar_usuario(id: int) -> User:
    for usuario in usuarios:
        if usuario.id == id:
            return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.get("", response_model=GetUsersResponse)
def get_users(is_active: bool | None = None):
    if is_active is None:
        return GetUsersResponse(users=usuarios)
    return GetUsersResponse(
        users=[usuario for usuario in usuarios if usuario.is_active == is_active]
    )


@router.get("/{id}", response_model=User)
def get_user(id: int):
    return buscar_usuario(id)


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    if any(usuario.id == user.id for usuario in usuarios):
        raise HTTPException(status_code=409, detail="Ya existe un usuario con ese id")
    usuarios.append(user)
    return user


@router.put("/{id}", response_model=User)
def update_user(id: int, datos: UserData):
    usuario = buscar_usuario(id)
    usuario.name = datos.name
    usuario.is_active = datos.is_active
    return usuario


@router.delete("/{id}", response_model=MessageResponse)
def delete_user(id: int):
    usuario = buscar_usuario(id)
    usuarios.remove(usuario)
    return MessageResponse(message="Usuario eliminado")
