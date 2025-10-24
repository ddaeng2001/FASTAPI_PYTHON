from fastapi import FastAPI, HTTPException, status, Query, Path, Header, Cookie, UploadFile, File, Form, Response, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional, Dict

app = FastAPI(title="FastAPI Minimal Step-by-Step")
      # title 생성 후 object를 연결하는 시점에서 웹 서버가 연결됨!



#----------------------------------------------
# 0) HealthCheck
# GET /health
# Postman: GET http://localhost:8000/health
#----------------------------------------------
@app.get("/health") # 엔드 포인트 생성하는 FASTAPI의 데코레이터 - 웹 요청(GET,POST...)처리 핸들러 등록
def health():
    return{"status" : "Helloworld!"} # return값 : JSON 데이터 반환




#----------------------------------------------
# 1) 기본 라우트
# GET /
# Postman: GET http://localhost:8000/
#----------------------------------------------
# 메인위치 잡기
@app.get("/")
def root():
    return{"message" : "Fast API Main Endpoint!"} 




#----------------------------------------------
# 2) Query 파라미터
# GET /echo?name=Alice
# Postman : GET http://localhost:8000/echo?name=Alice
#----------------------------------------------
# 외부값 받아오기
@app.get("/echo")
def echo(name : str = Query(..., min_length=1, description="이름")): # 파라미터를 query질의 형태로 받겠다!
        #파라미터명 : 자료형 = 파라미터를 어떤식으로 받을지 정의(...[필수파라미터 여부], 최소길이, swagger에 표시할 내용[==description])
    return{"hello" :name} # 파라미터 받은 name return



# ---------------------------------------------------------
# in SB에서 아래의 코드와 유사한 형식으로
# @GetMapping("/endpoint/{paht1}")
# public void test(@Pathvariable("path1") String path1 ){}
# ---------------------------------------------------------
# Endpoint: GET /items/{item_id}?q=fastapi
# 설명: Path와 Query 동시 사용
# 테스트: GET http://localhost:8000/items/123?q=fastapi

@app.get("/items/{item_id}")
def read_item(
    item_id : int = Path(..., ge=1), # 경로 기반의 파라미터를 받겠다! {item_id}와 연결되어있는 상태
                              #ge=1 : 1보다 커야함(<->le=1)
    q: Optional[str] = Query(None, max_length=50),
       #NULL체크용도         #None : 필수 파라미터는 아님   -> 쿼리 파라미터에 값을 넣지 않아도 문제 제기 X
): # 파라미터
    return {"item_id":item_id, "q": q}





# -----------------------------------------------
# DTO 생성
# -----------------------------------------------

class ItemIn(BaseModel):                    # 사용자로부터 전달받는 내용 저장하는 DTO
# ItemIn이 BaseModel을 상속받고 있음!
                                            # BaseModel(JSON -> Python 변환 / 유효성 검증)

    name : str=Field(..., min_length=1)     # 상품명
    price : float = Field(..., gt=0)        # 상품가격
    tags: List[str] = []                    # 태그 - 배열형태(리스트)로 문자열 담을 용도
    in_stock : bool = True                  # 재고여부


class ItemOut(BaseModel):                    
    id : int
    name : str=Field(..., min_length=1)     
    price : float = Field(..., gt=0)        
    tags: List[str] = []                    
    in_stock : bool = True                  



#id는 받아오는 것이 아니기에 id를 생성하려면
_next_id = 1                # id 기본값 생성
def _gen_id() -> int:       # -> int : return값을 int(정수형데이터)로 해주겠다고 명시
    global _next_id         # id 전역변수화
    val = _next_id
    _next_id += 1
    return val

# -------------------------
#엔드 포인트 지정(POST방식)
# -------------------------
                    #반환형 자료형을 명시해주면 내부적으로 찾는 작업이 생략되고 이 클래스를 그대로 사용하게 됨
@app.post("/items", response_model=ItemOut,status_code=status.HTTP_201_CREATED)        #응답에 대한 상태코드
def create_item(payload: ItemIn):               # payload: ItemIn -> request의 body내용(payload)전달
    new_id = _gen_id()
    item = ItemOut(id=new_id, name=payload.name, price=payload.price, tags=payload.tags, in_stock=payload.in_stock) #ItemOut객체 생성
    # print("payload", payload)
    return item

# ':' = type hint 문법
DB : Dict[int,ItemOut] = {} # 딕셔너리 생성 [key는 int, value값은 ItemOut으로 제한] -> 자료형 제한 및 초기값 생성

@app.post("/items", response_model=ItemOut,status_code=status.HTTP_201_CREATED)        #응답에 대한 상태코드
def create_item(payload: ItemIn):               # payload: ItemIn -> request의 body내용(payload)전달
    new_id = _gen_id()
    item = ItemOut(id=new_id, name=payload.name, price=payload.price, tags=payload.tags, in_stock=payload.in_stock) #ItemOut객체 생성
    DB[new_id] = item
    # print("payload", payload)
    return item

# cookie setup, file updownload도 가능함!




















