from typing import Annotated
from fastapi import Depends, Query, HTTPException, Request
from pydantic import BaseModel


from src.service.auth import AuthService


class PagePagination(BaseModel):
    page: Annotated[int | None, Query(default=1, ge=1, le=100)]
    per_page: Annotated[int | None, Query(default=None, ge=5, le=100)]

PaginationDepends = Annotated[PagePagination, Depends()]


def get_token(request: Request) -> str:
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token is missing")
    return access_token

def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().encode_access_token(token)
    user_id = data.get("user_id")
    if not isinstance(user_id, int):
        raise HTTPException(status_code=401, detail="Access token is invalid")
    return int(user_id)

UserIdDep = Annotated[int, Depends(get_current_user_id)]