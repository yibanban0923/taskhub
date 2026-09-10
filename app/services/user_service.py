from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories import user_repository
from app.schemas.user import UserCreate


def register_user(db: Session, payload: UserCreate) -> User:
    if user_repository.get_by_email(db, str(payload.email)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    if user_repository.get_by_username(db, payload.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered")

    return user_repository.create(
        db,
        username=payload.username,
        email=str(payload.email),
        hashed_password=hash_password(payload.password),
    )


def authenticate_user(db: Session, identifier: str, password: str) -> User | None:
    user = user_repository.get_by_identifier(db, identifier)
    if user is None or not verify_password(password, user.hashed_password):
        return None
    return user
