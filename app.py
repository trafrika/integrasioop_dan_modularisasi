"""
Aplikasi: Student Performance Tracker
Fungsi: Mengelola data presensi dan nilai mahasiswa berbasis CSV
Modul terkait: tracker.attendance, tracker.grades, tracker.report
"""

import os
from tracker.attendance import load_attendance, compute_attendance_rate
from tracker.grades import load_grades, compute_final_grade
from tracker.report import build_markdown_report, build_html_report, save_text, letter_grade

ATTENDANCE_FILE = "data/attendance.csv"
GRADES_FILE = "data/grades.csv"


def save_attendance(attendance_data, filename=ATTENDANCE_FILE):
    """Simpan ulang data presensi ke CSV"""
    import csv
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        header = ["student_id", "name"] + [f"meet{i}" for i in range(1, 6)]
        writer.writerow(header)
        for student in attendance_data:
            row = [student["student_id"], student["name"]] + student["attendance"]
            writer.writerow(row)


def save_grades(grades_data, filename=GRADES_FILE):
    """Simpan ulang data nilai ke CSV"""
    import csv
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        header = ["student_id", "name", "quiz", "tugas", "uts", "uas"]
        writer.writerow(header)
        for student in grades_data:
            row = [student["student_id"], student["name"], *student["grades"]]
            writer.writerow(row)


def tampilkan_rekap(attendance_data, grades_data):
    """Menampilkan rekap gabungan ke layar"""
    print("\n=== Rekap Data Mahasiswa ===")
    print(f"{'ID':<10} {'Nama':<15} {'Hadir%':<8} {'Nilai Akhir':<12} {'Predikat':<8}")
    print("-" * 55)

    # Mapping grades berdasar student_id
    grades_map = {g["student_id"]: g for g in grades_data}

    for att in attendance_data:
        sid = att["student_id"]
        nama = att["name"]
        hadir_persen = compute_attendance_rate(att["attendance"])
        g = grades_map.get(sid)
        if g:
            nilai_akhir = compute_final_grade(g["grades"])
            pred = letter_grade(nilai_akhir)
        else:
            nilai_akhir = 0.0
            pred = letter_grade(0)
        print(f"{sid:<10} {nama:<15} {hadir_persen:<8.1f} {nilai_akhir:<12.1f} {pred:<8}")
    print()


def tambah_mahasiswa(attendance_data, grades_data):
    """Tambah mahasiswa baru lengkap dengan presensi & nilai.
    
    Akan menolak input jika ID mahasiswa (NIM) sudah ada di data.
    """
    sid = input("ID Mahasiswa: ").strip()
    
    # Cek apakah NIM sudah ada
    existing_ids = {m["student_id"] for m in attendance_data}
    if sid in existing_ids:
        print(f"⚠️ NIM {sid} sudah ada! Mahasiswa tidak bisa ditambahkan lagi.")
        return  # keluar dari fungsi tanpa menambah data

    name = input("Nama: ").strip()

    print("Isi kehadiran (1=hadir, 0=tidak):")
    attendance = [int(input(f"Pertemuan {i+1}: ")) for i in range(5)]

    print("Masukkan nilai:")
    grades = [float(input(f"Nilai {x}: ")) for x in ["Quiz", "Tugas", "UTS", "UAS"]]

    attendance_data.append({"student_id": sid, "name": name, "attendance": attendance})
    grades_data.append({"student_id": sid, "name": name, "grades": grades})

    save_attendance(attendance_data)
    save_grades(grades_data)
    print("✅ Mahasiswa baru berhasil ditambahkan ke CSV.")



def main():
    """Fungsi utama aplikasi"""
    attendance_data = []
    grades_data = []

    while True:
        print("\n=== Student Performance Tracker ===")
        print("1) Muat data dari CSV")
        print("2) Tambah mahasiswa")
        print("3) Ubah presensi")
        print("4) Ubah nilai")
        print("5) Lihat rekap")
        print("6) Simpan laporan Markdown (out/report.md)")
        print("7) Ekspor HTML (out/report.html)")
        print("8) Tampilkan mahasiswa nilai < 70")
        print("9) Keluar")

        pilihan = input("Pilih: ")

        if pilihan == "1":
            try:
                attendance_data = load_attendance(ATTENDANCE_FILE)
                grades_data = load_grades(GRADES_FILE)
                print("✅ Data berhasil dimuat dari CSV!")
                tampilkan_rekap(attendance_data, grades_data)
            except Exception as e:
                print("Error:", e)

        elif pilihan == "2":
            tambah_mahasiswa(attendance_data, grades_data)

        elif pilihan == "3":
            sid = input("Masukkan ID Mahasiswa: ")
            for m in attendance_data:
                if m["student_id"] == sid:
                    print("Isi kehadiran (1=hadir, 0=tidak):")
                    m["attendance"] = [int(input(f"Pertemuan {i+1}: ")) for i in range(5)]
                    save_attendance(attendance_data)
                    print("✅ Data presensi disimpan!")
                    break
            else:
                print("❌ Mahasiswa tidak ditemukan.")

        elif pilihan == "4":
            sid = input("Masukkan ID Mahasiswa: ")
            for g in grades_data:
                if g["student_id"] == sid:
                    print("Masukkan nilai baru:")
                    g["grades"] = [float(input(f"Nilai {x}: ")) for x in ["Quiz", "Tugas", "UTS", "UAS"]]
                    save_grades(grades_data)
                    print("✅ Nilai berhasil disimpan!")
                    break
            else:
                print("❌ Mahasiswa tidak ditemukan.")

        elif pilihan in ["5"]:
            tampilkan_rekap(attendance_data, grades_data)

        elif pilihan in ["6", "7"]:
            # Cek data
            if not attendance_data or not grades_data:
                print("⚠️ Data kosong. Silakan pilih opsi 1 untuk memuat CSV terlebih dahulu.")
                continue

            # Mapping grades berdasar student_id
            grades_map = {g["student_id"]: g for g in grades_data}
            rows = []
            for att in attendance_data:
                sid = att["student_id"]
                nama = att["name"]
                hadir_persen = compute_attendance_rate(att["attendance"])
                g = grades_map.get(sid)
                if g:
                    nilai_akhir = compute_final_grade(g["grades"])
                    pred = letter_grade(nilai_akhir)
                else:
                    nilai_akhir = 0.0
                    pred = letter_grade(0)
                rows.append({
                    "student_id": sid,
                    "name": nama,
                    "attendance_rate": hadir_persen,
                    "final_score": nilai_akhir,
                    "grade": pred,
                })

            if pilihan == "6":
                md = build_markdown_report(rows)
                save_text("out/report.md", md)
                print("✅ Laporan Markdown disimpan di out/report.md")
            else:
                html = build_html_report(rows)
                save_text("out/report.html", html)
                print("✅ Laporan HTML disimpan di out/report.html")

        elif pilihan == "8":
            print("\n=== Mahasiswa Nilai < 70 ===")
            for g in grades_data:
                nilai_akhir = compute_final_grade(g["grades"])
                if nilai_akhir < 70:
                    print(f"{g['student_id']} - {g['name']} ({nilai_akhir:.1f})")
            print()

        elif pilihan == "9":
            print("Terima kasih! Program selesai.")
            break

        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()
