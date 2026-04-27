def get_status_data():
    return {
        "status": "ok",
        "message": "Backend работает",
        "service": "backend-service",
        "items_count": 3
    }


def get_items_data():
    return [
        {"id": 1, "name": "Банан Желтый", "image": "banan_yellow.jpg"},
        {"id": 2, "name": "Банан Зеленый", "image": "banan_green.jpg"},
        {"id": 3, "name": "Банан Красный", "image": "banan_red.jpg"},
    ]