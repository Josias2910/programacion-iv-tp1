from models.users import User, UserData


class UsersRepository:
    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self._usuarios = [
            User(id=1, name="Juan Pérez"),
            User(id=2, name="Ana López", is_active=False),
        ]

    def listar(self, is_active: bool | None = None) -> list[User]:
        if is_active is None:
            return list(self._usuarios)
        return [usuario for usuario in self._usuarios if usuario.is_active == is_active]

    def buscar(self, id: int) -> User | None:
        return next((usuario for usuario in self._usuarios if usuario.id == id), None)

    def crear(self, usuario: User) -> bool:
        if self.buscar(usuario.id) is not None:
            return False
        self._usuarios.append(usuario)
        return True

    def actualizar(self, id: int, datos: UserData) -> User | None:
        usuario = self.buscar(id)
        if usuario is not None:
            usuario.name = datos.name
            usuario.is_active = datos.is_active
        return usuario

    def eliminar(self, id: int) -> bool:
        usuario = self.buscar(id)
        if usuario is None:
            return False
        self._usuarios.remove(usuario)
        return True


usuarios_repo = UsersRepository()
