"""
tracker package: Mahasiswa tracker dengan rekap nilai & kehadiran.

Module ini sekaligus entry point `python -m tracker`.
"""

import os
from pathlib import Path
from .mahasiswa import Mahasiswa
from .penilaian import Penilaian
from .rekap_kelas import RekapKelas
from .report import build_markdown_report, save_text, build_html_report, letter_grade
from .attendance import load_attendance, compute_attendance_rate
from .grades import load_grades, compute_final_grade

__all__ = [
    "Mahasiswa", "Penilaian", "RekapKelas",
    "build_markdown_report", "save_text", "build_html_report", "letter_grade"
]

def main():
    """Titik masuk (entry point) untuk menjalankan paket `tracker` 
    menggunakan `python -m tracker`."""
    base = Path.cwd()
    att_path = base / "data" / "attendance.csv"
    grd_path = base / "data" / "grades.csv"
    out_dir = base / "out"
    out_dir.mkdir(exist_ok=True)
    out_md = out_dir / "report.md"
    out_html = out_dir / "report.html"

    # Muat CSV
    attendance_data = load_attendance(str(att_path))
    grades_data = load_grades(str(grd_path))

    # Buat objek rekap
    r = RekapKelas()

    # Mapping grades berdasarkan student_id
    grades_map = {g["student_id"]: g for g in grades_data}

    for att in attendance_data:
        sid = att["student_id"]
        nama = att["name"]

        # Tambah mahasiswa
        r.tambah_mahasiswa(Mahasiswa(sid, nama))

        # Hitung attendance
        hadir = compute_attendance_rate(att["attendance"])
        r.set_hadir(sid, hadir)

        # Hitung nilai akhir jika ada
        g = grades_map.get(sid)
        if g:
            akhir = compute_final_grade(g["grades"])
            r.set_penilaian(
                sid,
                quiz=g["grades"][0],
                tugas=g["grades"][1],
                uts=g["grades"][2],
                uas=g["grades"][3]
            )

    # Ambil data rekap
    rows = r.rekap()

    # Tambahkan predikat
    for row in rows:
        row["grade"] = letter_grade(row["final_score"])

    # Tampilkan rekap di terminal
    print("\n=== Rekap Mahasiswa ===")
    print(f"{'ID':<10} {'Nama':<15} {'Hadir%':<8} {'Nilai Akhir':<12} {'Predikat':<8}")
    print("-"*55)
    for row in rows:
        print(f"{row['student_id']:<10} {row['name']:<15} {row['attendance_rate']:<8.1f} {row['final_score']:<12.1f} {row['grade']}")

    # Simpan laporan
    md = build_markdown_report(rows)
    save_text(str(out_md), md)
    html = build_html_report(rows)
    save_text(str(out_html), html)

    print(f"\n✅ Generated reports:\n- {out_md}\n- {out_html}")
