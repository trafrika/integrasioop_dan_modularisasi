"""
Modul: tracker.grades
Fungsi: Membaca data nilai, menyimpan, dan menghitung nilai akhir mahasiswa
"""

import csv

def load_grades(path="data/grades.csv"):
    """Membaca file CSV nilai dan mengembalikan list of dict"""
    data = []
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Pastikan semua kolom nilai ada
                quiz = safe_float(row.get("quiz"))
                tugas = safe_float(row.get("tugas"))
                uts = safe_float(row.get("uts"))
                uas = safe_float(row.get("uas"))

                data.append({
                    "student_id": row.get("student_id", "").strip(),
                    "name": row.get("name", "").strip(),
                    "grades": [quiz, tugas, uts, uas]
                })
    except FileNotFoundError:
        print("⚠️ File grades.csv belum ditemukan. Akan dibuat saat menambah data baru.")
    return data


def safe_float(value):
    """Konversi nilai ke float, jika kosong → 0.0"""
    try:
        if value in (None, "", " "):
            return 0.0
        return float(value)
    except ValueError:
        return 0.0


def compute_final_grade(grades):
    """Hitung nilai akhir dari [quiz, tugas, uts, uas]"""
    if not isinstance(grades, list) or len(grades) != 4:
        return 0.0
    quiz, tugas, uts, uas = grades
    return round(0.1 * quiz + 0.3 * tugas + 0.3 * uts + 0.3 * uas, 1)
