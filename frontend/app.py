import requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
API_URL = "http://127.0.0.1:8000"

@app.route("/")
def index():
    # Получаем список заявок из FastAPI
    response = requests.get(f"{API_URL}/repairs")
    repairs = response.json() if response.status_code == 200 else []
    return render_template("index.html", repairs=repairs)

@app.route("/create", methods=["GET", "POST"])
def create_repair():
    if request.method == "POST":
        data = {
            "car_model": request.form.get("car_model"),
            "issue": request.form.get("issue"),
            "estimated_cost": float(request.form.get("estimated_cost")),
            "is_completed": request.form.get("is_completed") == "on"
        }
        # Отправляем JSON на backend [cite: 92]
        response = requests.post(f"{API_URL}/repairs", json=data)
        if response.status_code == 201:
            return redirect("/")
        return render_template("form.html", error=response.text)
    return render_template("form.html")

@app.route("/delete/<int:repair_id>", methods=["POST"])
def delete_repair(repair_id):
    # Flask отправляет DELETE-запрос к API
    requests.delete(f"{API_URL}/repairs/{repair_id}")
    return redirect("/")

if __name__ == "__main__":
    app.run(port=5000)