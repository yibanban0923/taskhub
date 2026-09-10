from sqlalchemy import asc, desc, func, or_, select
from sqlalchemy.orm import Session

from app.models.task import Task, TaskPriority, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate

SORT_COLUMNS = {
    "created_at": Task.created_at,
    "updated_at": Task.updated_at,
    "due_date": Task.due_date,
    "priority": Task.priority,
    "status": Task.status,
    "title": Task.title,
}


def create(db: Session, *, user_id: int, payload: TaskCreate) -> Task:
    task = Task(user_id=user_id, **payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_owned(db: Session, *, task_id: int, user_id: int) -> Task | None:
    return db.scalar(select(Task).where(Task.id == task_id, Task.user_id == user_id))


def list_owned(
    db: Session,
    *,
    user_id: int,
    page: int,
    page_size: int,
    status: TaskStatus | None,
    priority: TaskPriority | None,
    keyword: str | None,
    sort_by: str,
    order: str,
) -> tuple[list[Task], int]:
    filters = [Task.user_id == user_id]
    if status is not None:
        filters.append(Task.status == status)
    if priority is not None:
        filters.append(Task.priority == priority)
    if keyword:
        pattern = f"%{keyword.strip()}%"
        filters.append(or_(Task.title.ilike(pattern), Task.description.ilike(pattern)))

    total = db.scalar(select(func.count()).select_from(Task).where(*filters)) or 0

    sort_column = SORT_COLUMNS.get(sort_by, Task.created_at)
    ordering = desc(sort_column) if order == "desc" else asc(sort_column)

    stmt = (
        select(Task)
        .where(*filters)
        .order_by(ordering, desc(Task.id))
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    return list(db.scalars(stmt).all()), total


def update(db: Session, *, task: Task, payload: TaskUpdate) -> Task:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete(db: Session, *, task: Task) -> None:
    db.delete(task)
    db.commit()
