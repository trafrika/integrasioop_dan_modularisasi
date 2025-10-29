"""Mahasiswa model (OOP, enkapsulasi).

Kelas Mahasiswa menyimpan nim, nama, dan hadir_persen (dengan validasi 0..100).
"""

class Mahasiswa:
    """Represent a student with NIM, name and attendance percentage."""

    def __init__(self, nim, nama):
        self.nim = nim
        self.nama = nama
        self._hadir_persen = 0.0

    @property
    def hadir_persen(self):
        """Return attendance percentage (0..100)."""
        return self._hadir_persen

    @hadir_persen.setter
    def hadir_persen(self, v):
        """Set attendance percentage, validate 0..100."""
        if v is None:
            v = 0
        try:
            v = float(v)
        except Exception:
            raise ValueError('hadir_persen harus berupa angka')
        if v < 0 or v > 100:
            raise ValueError('hadir_persen harus 0..100')
        self._hadir_persen = round(v, 2)

    def info(self):
        """Return a brief profile string for display."""
        return f"{self.nim} - {self.nama} (Hadir: {self.hadir_persen}%)"

    def __repr__(self):
        return f"<Mahasiswa {self.nim} {self.nama} hadir={self.hadir_persen}>"