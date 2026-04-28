import requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
API_URL = "http://127.0.0.1:8000"


def extract_error_msg(response):
    try:
        err_data = response.json()
        detail = err_data.get('detail', 'Ошибка сохранения данных')
        if isinstance(detail, list):
            msg = detail[0].get('msg', 'Некорректные данные')
            return msg.replace('Value error, ', '')
        return detail
    except:
        return "Неизвестная ошибка сервера"


@app.route("/")
def index():
    response = requests.get(f"{API_URL}/repairs")
    repairs = response.json() if response.status_code == 200 else []
    return render_template("index.html", repairs=repairs)


@app.route("/create", methods=["GET", "POST"])
def create_repair():
    if request.method == "POST":
        data = {
            "car_model": request.form.get("car_model"),
            "issue": request.form.get("issue"),
            "phone_number": request.form.get("phone_number"),
            "estimated_cost": float(request.form.get("estimated_cost") or 0),
            "is_completed": request.form.get("is_completed") == "on"
        }
        response = requests.post(f"{API_URL}/repairs", json=data)

        if response.status_code == 201:
            return redirect("/")

        error_msg = extract_error_msg(response)
        return render_template("form.html", error=error_msg, data=data)

    return render_template("form.html", data=None)


@app.route("/edit/<int:repair_id>", methods=["GET", "POST"])
def edit_repair(repair_id):
    if request.method == "POST":
        data = {
            "car_model": request.form.get("car_model"),
            "issue": request.form.get("issue"),
            "phone_number": request.form.get("phone_number"),
            "estimated_cost": float(request.form.get("estimated_cost") or 0),
            "is_completed": request.form.get("is_completed") == "on"
        }
        response = requests.put(f"{API_URL}/repairs/{repair_id}", json=data)

        if response.status_code == 200:
            return redirect("/")

        error_msg = extract_error_msg(response)
        data['id'] = repair_id
        return render_template("edit.html", error=error_msg, data=data)

    resp = requests.get(f"{API_URL}/repairs/{repair_id}")
    if resp.status_code != 200:
        return redirect("/")

    return render_template("edit.html", data=resp.json(), error=None)


@app.route("/close/<int:repair_id>", methods=["POST"])
def close_repair(repair_id):
    requests.patch(f"{API_URL}/repairs/{repair_id}/close")
    return redirect("/")


@app.route("/delete/<int:repair_id>", methods=["POST"])
def delete_repair(repair_id):
    requests.delete(f"{API_URL}/repairs/{repair_id}")
    return redirect("/")


if __name__ == "__main__":
    app.run(port=5000)