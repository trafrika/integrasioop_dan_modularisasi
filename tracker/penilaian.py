"""Penilaian model: component scores + weighted final calculation.

Validasi nilai 0..100 via properties.
"""

DEFAULT_WEIGHTS = {
    'quiz': 0.15,
    'tugas': 0.25,
    'uts': 0.25,
    'uas': 0.35,
}

class Penilaian:
    """Store components and compute weighted final score."""

    def __init__(self, quiz=0, tugas=0, uts=0, uas=0):
        self._quiz = self._tugas = self._uts = self._uas = 0.0
        self.quiz = quiz
        self.tugas = tugas
        self.uts = uts
        self.uas = uas

    def _validate(self, v):
        try:
            v = float(v)
        except Exception:
            raise ValueError('nilai harus berupa angka')
        if v < 0 or v > 100:
            raise ValueError('nilai harus 0..100')
        return float(v)

    @property
    def quiz(self):
        return self._quiz

    @quiz.setter
    def quiz(self, v):
        self._quiz = self._validate(v)

    @property
    def tugas(self):
        return self._tugas

    @tugas.setter
    def tugas(self, v):
        self._tugas = self._validate(v)

    @property
    def uts(self):
        return self._uts

    @uts.setter
    def uts(self, v):
        self._uts = self._validate(v)

    @property
    def uas(self):
        return self._uas

    @uas.setter
    def uas(self, v):
        self._uas = self._validate(v)

    def nilai_akhir(self, weights=None):
        """Compute weighted final score (rounded to 2 decimals)."""
        if weights is None:
            weights = DEFAULT_WEIGHTS
        score = (
            self.quiz * weights['quiz'] +
            self.tugas * weights['tugas'] +
            self.uts * weights['uts'] +
            self.uas * weights['uas']
        )
        return round(score, 2)

    def __repr__(self):
        return f"<Penilaian q={self.quiz} t={self.tugas} uts={self.uts} uas={self.uas}>"