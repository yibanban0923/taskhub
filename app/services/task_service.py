from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.task import Task, TaskPriority, TaskStatus
from app.repositories import task_repository
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(db: Session, *, user_id: int, payload: TaskCreate) -> Task:
    return task_repository.create(db, user_id=user_id, payload=payload)


def get_task_or_404(db: Session, *, task_id: int, user_id: int) -> Task:
    task = task_repository.get_owned(db, task_id=task_id, user_id=user_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


def list_tasks(
    db: Session,
    *,
    user_id: int,
    page: int,
    page_size: int,
    status_filter: TaskStatus | None,
    priority: TaskPriority | None,
    keyword: str | None,
    sort_by: str,
    order: str,
) -> tuple[list[Task], int]:
    return task_repository.list_owned(
        db,
        user_id=user_id,
        page=page,
        page_size=page_size,
        status=status_filter,
        priority=priority,
        keyword=keyword,
        sort_by=sort_by,
        order=order,
    )


def update_task(db: Session, *, task: Task, payload: TaskUpdate) -> Task:
    return task_repository.update(db, task=task, payload=payload)


def delete_task(db: Session, *, task: Task) -> None:
    task_repository.delete(db, task=task)
