# student_performance_tracker

Aplikasi Sederhana untuk mengelola data mahasiswa, presensi, dan nilai. Kemudian ada laporan Markdown + HTML menggunakan rich pdoc.

## Cara jalankan

1. Buat virtual environment (Opsional)
    - Buka terminal lalu python -m venv .venv
    - Aktifkan venv diterminal dengan .venv\Scripts\Activate.ps1 (windows) atau source .venv/bin/activate (macOS/Linux)
2. Install Paket Pendukung
    - pip install rich pdoc (Gunakan rich untuk tampilan tabel warna dan pdoc untuk dokumentasi otomatis)
    - pip freeze > requirements.txt
3. Buat struktur folder dan file project student_performance_tracker
4. Lalu, jalankan bisa dengan 2 cara yaitu:
    - Cara utama: python app.py
    - Jalankan paket langsung: python -m tracker (langsung ke out/ report.md dan out/report.html)
5. Keluaran: out/report.md dan out/report.html

# Struktur
- data/: berisi CSV attendance.csv & grades.csv
- tracker/: paket berisi model dan report
- out/: hasil report.md dan report.html



