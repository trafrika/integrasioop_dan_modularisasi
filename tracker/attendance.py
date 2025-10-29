"""
Modul: tracker.attendance
Fungsi: Membaca dan menghitung tingkat kehadiran mahasiswa
"""

import csv

def load_attendance(path="data/attendance.csv"):
    data = []
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                attendance = [int(row.get(f"meet{i}", 0)) for i in range(1, 6)]
                data.append({
                    "student_id": row.get("student_id", "").strip(),
                    "name": row.get("name", "").strip(),
                    "attendance": attendance
                })
    except FileNotFoundError:
        print("⚠️ File attendance.csv belum ditemukan.")
    return data


def compute_attendance_rate(attendance):
    """Hitung persentase kehadiran"""
    if not attendance:
        return 0.0
    total = sum(attendance)
    return (total / len(attendance)) * 100
