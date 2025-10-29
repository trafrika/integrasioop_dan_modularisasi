"""Manager RekapKelas: menggabungkan Mahasiswa & Penilaian.

Menyediakan tambah_mahasiswa, set_hadir, set_penilaian, rekap, predikat,
and util untuk filter (nilai < threshold).
"""

from .mahasiswa import Mahasiswa
from .penilaian import Penilaian

class RekapKelas:
    """Manage collection of students and their scores."""

    def __init__(self):
        self._by_nim = {}

    def tambah_mahasiswa(self, mhs):
        """Add Mahasiswa instance. If existing nim, update name."""
        if mhs.nim in self._by_nim:
            self._by_nim[mhs.nim]['mhs'].nama = mhs.nama
        else:
            self._by_nim[mhs.nim] = {'mhs': mhs, 'nilai': Penilaian()}

    def set_hadir(self, nim, persen):
        """Set attendance % for nim."""
        item = self._by_nim.get(nim)
        if not item:
            raise KeyError('NIM tidak ditemukan')
        item['mhs'].hadir_persen = persen

    def set_penilaian(self, nim, quiz=None, tugas=None, uts=None, uas=None):
        """Set nilai components for student (only non-None applied)."""
        item = self._by_nim.get(nim)
        if not item:
            raise KeyError('NIM tidak ditemukan')
        p = item['nilai']
        if quiz is not None: p.quiz = quiz
        if tugas is not None: p.tugas = tugas
        if uts is not None: p.uts = uts
        if uas is not None: p.uas = uas

    def predikat(self, skor):
        """Return letter grade A..E."""
        if skor >= 85: return 'A'
        if skor >= 75: return 'B'
        if skor >= 65: return 'C'
        if skor >= 50: return 'D'
        return 'E'

    def rekap(self):
        """Return list of dict rows for all students."""
        rows = []
        for nim, d in sorted(self._by_nim.items()):
            m = d['mhs']; p = d['nilai']
            akhir = p.nilai_akhir()
            rows.append({
                'student_id': nim,
                'name': m.nama,
                'attendance_rate': m.hadir_persen,
                'final_score': akhir,
                'predikat': self.predikat(akhir),
            })
        return rows

    def find_below(self, threshold):
        """Return rows with final_score < threshold."""
        return [r for r in self.rekap() if r['final_score'] < threshold]