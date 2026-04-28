from fastapi import FastAPI, HTTPException, status
from database import init_db
import crud
from schemas import RepairCreate, RepairRead

app = FastAPI(title="Autoservice API")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/repairs", response_model=list[RepairRead])
def read_repairs():
    return crud.get_all_repairs()

@app.get("/repairs/{repair_id}", response_model=RepairRead)
def read_repair(repair_id: int):
    repair = crud.get_repair_by_id(repair_id)
    if not repair:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    return repair

@app.post("/repairs", status_code=status.HTTP_201_CREATED)
def add_repair(repair: RepairCreate):
    repair_id = crud.create_repair(repair.model_dump())
    return {"message": "Заявка создана", "id": repair_id}

@app.put("/repairs/{repair_id}")
def update_repair_endpoint(repair_id: int, repair: RepairCreate):
    if not crud.get_repair_by_id(repair_id):
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    crud.update_repair(repair_id, repair.model_dump())
    return {"message": "Заявка обновлена"}

@app.patch("/repairs/{repair_id}/close")
def close_repair_endpoint(repair_id: int):
    if not crud.get_repair_by_id(repair_id):
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    crud.close_repair(repair_id)
    return {"message": "Заявка закрыта"}

@app.delete("/repairs/{repair_id}", status_code=status.HTTP_200_OK)
def remove_repair(repair_id: int):
    if not crud.delete_repair(repair_id):
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    return {"message": "Заявка успешно удалена"}