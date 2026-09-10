from typing import Literal

from fastapi import APIRouter, Query, Response, status

from app.api.deps import CurrentUser, DbSession
from app.models.task import TaskPriority, TaskStatus
from app.schemas.task import TaskCreate, TaskListResponse, TaskRead, TaskUpdate
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: DbSession, current_user: CurrentUser) -> TaskRead:
    return task_service.create_task(db, user_id=current_user.id, payload=payload)


@router.get("", response_model=TaskListResponse)
def list_tasks(
    db: DbSession,
    current_user: CurrentUser,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    status_filter: TaskStatus | None = Query(default=None, alias="status"),
    priority: TaskPriority | None = None,
    keyword: str | None = Query(default=None, min_length=1, max_length=100),
    sort_by: Literal["created_at", "updated_at", "due_date", "priority", "status", "title"] = "created_at",
    order: Literal["asc", "desc"] = "desc",
) -> TaskListResponse:
    items, total = task_service.list_tasks(
        db,
        user_id=current_user.id,
        page=page,
        page_size=page_size,
        status_filter=status_filter,
        priority=priority,
        keyword=keyword,
        sort_by=sort_by,
        order=order,
    )
    return TaskListResponse(items=items, total=total, page=page, page_size=page_size)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: DbSession, current_user: CurrentUser) -> TaskRead:
    return task_service.get_task_or_404(db, task_id=task_id, user_id=current_user.id)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: DbSession,
    current_user: CurrentUser,
) -> TaskRead:
    task = task_service.get_task_or_404(db, task_id=task_id, user_id=current_user.id)
    return task_service.update_task(db, task=task, payload=payload)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: DbSession, current_user: CurrentUser) -> Response:
    task = task_service.get_task_or_404(db, task_id=task_id, user_id=current_user.id)
    task_service.delete_task(db, task=task)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
