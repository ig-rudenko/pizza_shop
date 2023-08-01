import time

from celery import shared_task, Task
from pizza_shop.celery import app


@app.task(bind=True)
def some_func(self: Task, value: str, delay: int) -> dict:
    print("BEGIN SOME FUNC")

    for i in range(1, 11):
        time.sleep(delay)
        self.s()
        self.update_state(state="PROGRESS", meta={"progress": i*10, "result": None})

    print("END SOME FUNC")
    return {"progress": 100, "result": value}


@shared_task
def logging(*args, **kwargs):
    with open("text.txt", "w", encoding="utf-8") as f:
        f.write(str(args) + " " + str(kwargs))
    print(args)
    print(kwargs)


@shared_task
def create_object():
    print("*:8000")
