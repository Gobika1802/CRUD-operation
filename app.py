import os
from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

TABLE = "students"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/students", methods=["GET"])
def get_students():
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 50))
        offset = (page - 1) * per_page

        result = (
            supabase.table(TABLE)
            .select("*", count="exact")
            .range(offset, offset + per_page - 1)
            .order("id", desc=False)
            .execute()
        )

        return jsonify({
            "students": result.data,
            "total": result.count,
            "page": page,
            "per_page": per_page,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/students", methods=["POST"])
def create_student():
    try:
        data = request.get_json()
        required = ["name", "email", "age", "course"]
        for field in required:
            if field not in data or not str(data[field]).strip():
                return jsonify({"error": f"Missing field: {field}"}), 400

        result = (
            supabase.table(TABLE)
            .insert({
                "name": data["name"],
                "email": data["email"],
                "age": int(data["age"]),
                "course": data["course"],
            })
            .execute()
        )

        return jsonify({"student": result.data[0]}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    try:
        data = request.get_json()
        update_data = {}
        for key in ["name", "email", "age", "course"]:
            if key in data:
                update_data[key] = int(data[key]) if key == "age" else data[key]

        if not update_data:
            return jsonify({"error": "No fields to update"}), 400

        result = (
            supabase.table(TABLE)
            .update(update_data)
            .eq("id", student_id)
            .execute()
        )

        return jsonify({"student": result.data[0]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    try:
        supabase.table(TABLE).delete().eq("id", student_id).execute()
        return jsonify({"message": "Student deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
