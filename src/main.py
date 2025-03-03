from fastapi import FastAPI, Body
from pydantic import BaseModel
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

""" 
[GET] Query Parameter(/todos?query=apple)
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

"""
[GET] ID를 통한 상세 조회
"""
@app.get("/todos/{todo_id}")
def get_todo_handler(todo_id: int):
    return todo_data.get(todo_id, {})

"""
[POST] post API로 todo 생성
 `pydentic` 모듈로 쉽게 Request Body 처리
"""
# request record 값
class CreateTodoRequest(BaseModel):
    id: int
    contents: str
    is_done: bool

@app.post("/todos")
def create_todo_handler(request: CreateTodoRequest):
    todo_data[request.id] = request.dict()
    return todo_data[request.id]

"""
[PATCH] id를 받아서 `is_done`을 수정
* 하나의 컬럼만 Body 형태로 수정하는 것 : fastapi.Body(embed=True) !!
embed=True라는게 요청 본문이 JSON으로 감싸져 있다는 뜻

=> 결론! patch를 통해서 is_done:bool을 받고, 수정하는 api
"""
@app.patch("/todos/{todo_id}")
def update_todo_handler(
    todo_id: int,
    is_done: bool = Body(..., embed=True),
):
    todo = todo_data.get(todo_id)
    if todo:
        todo["is_done"] = is_done
        return todo
    return {}

@app.delete("/todos/{todo_id}")
def delete_todo_handler(todo_id: int):
    # default를 None으로 넣어준다.
    todo_data.pop(todo_id, None)
    return todo_data