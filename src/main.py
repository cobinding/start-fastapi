from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def health_check_handler():
    return {"ping":"pong"}


# DB 대신 딕셔너리로 데이터 관리
# return 값
todo_data = {
    1: {
        "id": 1,
        "contents": "실전! FastAPI 섹션 0 수강",
        "is_done": True,
    },
    2: {
        "id": 2,
        "contents": "실전! FastAPI 섹션 1 수강",
        "is_done": False,
    },
    3: {
        "id": 3,
        "contents": "실전! FastAPI 섹션 2 수강",
        "is_done": False,
    }
}

@app.get("/")
def get_todos_handler() -> list:
    return list(todo_data.values())

"""Query Parameter(/todos?query=apple)
직접 작성하지 않고, 인자를 통해 정의
"""
@app.get("/todos")
# 쿼리 파라미터 값을 Optional로 지정,
# default = None
def get_todos_handler(order: str | None = None):
    result = list(todo_data.values())
    if order == "DESC":
        return result[::-1]
    return result