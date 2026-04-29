from database import get_connection

def get_all_repairs():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM repairs").fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_repair_by_id(repair_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM repairs WHERE id = ?", (repair_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def create_repair(data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO repairs (car_model, issue, estimated_cost, phone_number, is_completed) VALUES (?, ?, ?, ?, ?)",
        (data["car_model"], data["issue"], data["estimated_cost"], data["phone_number"], int(data["is_completed"]))
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def update_repair(repair_id: int, data: dict):
    conn = get_connection()
    conn.execute(
        "UPDATE repairs SET car_model=?, issue=?, estimated_cost=?, phone_number=?, is_completed=? WHERE id=?",
        (data["car_model"], data["issue"], data["estimated_cost"], data["phone_number"], int(data["is_completed"]), repair_id)
    )
    conn.commit()
    conn.close()

def close_repair(repair_id: int):
    conn = get_connection()
    conn.execute("UPDATE repairs SET is_completed=1 WHERE id=?", (repair_id,))
    conn.commit()
    conn.close()

def delete_repair(repair_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM repairs WHERE id = ?", (repair_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

def delete_multiple_repairs(repair_ids: list[int]):
    if not repair_ids:
        return 0
    conn = get_connection()
    cursor = conn.cursor()
    placeholders = ','.join('?' * len(repair_ids))
    cursor.execute(f"DELETE FROM repairs WHERE id IN ({placeholders})", repair_ids)
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    return deleted

def delete_all_repairs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM repairs")
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    return deleted