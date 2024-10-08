from fastapi import FastAPI, Path, HTTPException
from typing import Optional
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


# Tải các biến môi trường từ file .env
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả origins trong môi trường development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Sample in-memory "database" of students
students = {
    1: {
        "name": "John",
        "age": 17,
        "class": "year 12"
    },
    2: {
        "name": "Jane",
        "age": 16,
        "class": "year 11"
    }
}

class Student(BaseModel):
    name: str
    age: int
    year: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

@app.get("/")
def index():
    return {"message": "Hello, World"}

@app.get("/get-student/{student_id}")
def get_student(
    student_id: int = Path(
        ...,  # Ellipsis indicates that this path parameter is required
        description="The ID of the student you want to view",
        gt=0,  # Ensures student_id is greater than 0
        title="Student ID",
        example=1
    )
):
    student = students.get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.post("/get-by-name")
def get_student_by_name(*,name: Optional[str] = None, test : int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    raise HTTPException(status_code=404, detail="Student not found")

@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        raise HTTPException(status_code=400, detail="Student already exists")
    students[student_id] = student
    return students[student_id]   

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    if student.name != None:
        students[student_id]["name"] = student.name
    if student.age != None:
        students[student_id]["age"] = student.age
    if student.year != None:
        students[student_id]["year"] = student.year
    return students[student_id]

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[student_id]
    return {"message": "Student deleted successfully"}

@app.get("/testnum")
def get_testnum():
    # Đọc giá trị của my_number từ biến môi trường
    my_number = os.getenv("my_number")
    
    # Trả về giá trị dưới dạng JSON
    return {"test1": my_number}