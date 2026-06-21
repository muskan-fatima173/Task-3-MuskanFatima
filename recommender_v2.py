"""
╔══════════════════════════════════════════════════════════════════╗
║   DecodeLabs · Project 3 · AI Recommendation Engine  v2.0      ║
║   Built with PyQt5 — Modern Dark UI                             ║
║   Author: Muskan | FA24-BAI-058 | COMSATS Islamabad             ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys, json, os, math

os.environ.setdefault("QT_AUTO_SCREEN_SCALE_FACTOR", "1")
os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "1")

from datetime import datetime
from collections import Counter
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QScrollArea, QFrame, QGridLayout,
    QGraphicsDropShadowEffect, QSizePolicy, QSpacerItem, QStackedWidget,
    QMessageBox, QDialog, QTextEdit
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve, QRect, QSize
from PyQt5.QtGui import (
    QColor, QFont, QPalette, QLinearGradient, QPainter, QPen,
    QBrush, QIcon, QPixmap, QPainterPath, QFontDatabase
)


C = {
    "bg":        "#0B0F1A",
    "panel":     "#111827",
    "card":      "#1A2236",
    "card2":     "#1E2D45",
    "border":    "#1F2D42",
    "accent":    "#7C3AED",
    "accent2":   "#06B6D4",
    "accent3":   "#10B981",
    "warn":      "#F59E0B",
    "danger":    "#EF4444",
    "text":      "#E2E8F0",
    "muted":     "#64748B",
    "white":     "#FFFFFF",
    "grad1":     "#7C3AED",
    "grad2":     "#06B6D4",
}

QSS = f"""
QMainWindow, QWidget#root {{
    background: {C['bg']};
}}
QScrollArea {{
    border: none;
    background: transparent;
}}
QScrollBar:vertical {{
    background: {C['panel']};
    width: 6px;
    border-radius: 5px;
}}
QScrollBar::handle:vertical {{
    background: {C['accent']};
    border-radius: 5px;
    min-height: 30px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{
    background: {C['panel']};
    height: 6px;
    border-radius: 5px;
}}
QScrollBar::handle:horizontal {{
    background: {C['accent']};
    border-radius: 5px;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
QLineEdit {{
    background: {C['card']};
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 12px;
    padding: 13px 20px;
    font-size: 17px;
    font-family: 'Segoe UI', sans-serif;
    selection-background-color: {C['accent']};
}}
QLineEdit:focus {{
    border: 1px solid {C['accent']};
}}
QToolTip {{
    background: {C['card2']};
    color: {C['text']};
    border: 1px solid {C['accent']};
    padding: 8px 13px;
    border-radius: 8px;
    font-size: 15px;
}}
"""


COURSES = [
    {"title":"Python for Data Science","tags":["python","data","machine learning","statistics","pandas","numpy"]},
    {"title":"Machine Learning A-Z","tags":["machine learning","python","algorithms","regression","classification"]},
    {"title":"Deep Learning Specialization","tags":["deep learning","neural networks","tensorflow","keras","ai"]},
    {"title":"Web Development Bootcamp","tags":["html","css","javascript","react","nodejs","web"]},
    {"title":"AWS Cloud Practitioner","tags":["aws","cloud","devops","infrastructure","serverless"]},
    {"title":"Docker & Kubernetes","tags":["docker","kubernetes","devops","containers","cloud"]},
    {"title":"SQL & Database Design","tags":["sql","database","postgresql","mysql","data"]},
    {"title":"NLP with Transformers","tags":["nlp","transformers","bert","huggingface","python","ai"]},
    {"title":"Computer Vision with OpenCV","tags":["computer vision","opencv","image processing","deep learning","python"]},
    {"title":"React & Next.js Mastery","tags":["react","nextjs","javascript","frontend","web","typescript"]},
    {"title":"Cybersecurity Fundamentals","tags":["security","networking","ethical hacking","linux","cryptography"]},
    {"title":"Data Structures & Algorithms","tags":["algorithms","data structures","python","problem solving"]},
    {"title":"Flutter Mobile Dev","tags":["flutter","dart","mobile","android","ios","ui"]},
    {"title":"LLM Engineering","tags":["llm","openai","langchain","ai","python","rag","transformers"]},
]

BOOKS = [
    {"title":"Hands-On Machine Learning (Géron)","tags":["machine learning","python","scikit-learn","tensorflow","algorithms"]},
    {"title":"Clean Code (Robert Martin)","tags":["software engineering","java","best practices","programming","refactoring"]},
    {"title":"Deep Learning (Goodfellow)","tags":["deep learning","neural networks","math","ai","research"]},
    {"title":"Designing Data-Intensive Applications","tags":["distributed systems","databases","backend","scalability","data"]},
    {"title":"Python Crash Course","tags":["python","beginner","programming","projects"]},
    {"title":"Introduction to Algorithms (CLRS)","tags":["algorithms","data structures","math","computer science"]},
    {"title":"You Don't Know JS","tags":["javascript","web","frontend","programming"]},
    {"title":"The DevOps Handbook","tags":["devops","automation","ci/cd","culture","operations"]},
    {"title":"Natural Language Processing with Python","tags":["nlp","python","text","ai","machine learning"]},
    {"title":"Cracking the Coding Interview","tags":["algorithms","interviews","problem solving","data structures","career"]},
    {"title":"AI: A Modern Approach","tags":["ai","algorithms","machine learning","search","planning"]},
]

MOVIES = [
    {"title":"The Social Network","tags":["startup","programming","entrepreneurship","web","silicon valley"]},
    {"title":"Ex Machina","tags":["ai","robotics","ethics","deep learning","future"]},
    {"title":"Her","tags":["ai","nlp","future","machine learning","human computer interaction"]},
    {"title":"The Matrix","tags":["programming","simulation","hacking","cybersecurity","philosophy"]},
    {"title":"Mr Robot","tags":["cybersecurity","hacking","social engineering","networking","linux"]},
    {"title":"Imitation Game","tags":["algorithms","history","machine learning","ai","mathematics"]},
    {"title":"Moneyball","tags":["data","statistics","machine learning","analytics","decision making"]},
    {"title":"iRobot","tags":["ai","robotics","ethics","future","automation"]},
    {"title":"Transcendence","tags":["ai","deep learning","singularity","future","neural networks"]},
    {"title":"Pirates of Silicon Valley","tags":["startup","entrepreneurship","apple","microsoft","silicon valley"]},
]

CAREERS = [
    {"title":"Data Scientist","tags":["python","machine learning","statistics","data","pandas","numpy","sql","research"],
     "salary":"PKR 150K–350K/mo","mode":"Remote / Hybrid","type":"Permanent","experience":"1–3 years",
     "region":"Islamabad, Lahore, Remote (Global)","companies":["Systems Ltd","Teradata","10Pearls","Arbisoft"]},
    {"title":"Machine Learning Engineer","tags":["machine learning","python","tensorflow","deep learning","algorithms","mlops"],
     "salary":"PKR 200K–500K/mo","mode":"Remote / On-site","type":"Permanent","experience":"2–4 years",
     "region":"Islamabad, Karachi, Remote (US/EU)","companies":["Microsoft","Google","Convex Interactive","Tkxel"]},
    {"title":"NLP Engineer","tags":["nlp","transformers","python","bert","huggingface","ai","text"],
     "salary":"PKR 200K–450K/mo","mode":"Remote","type":"Permanent / Contract","experience":"1–3 years",
     "region":"Remote (Global), Lahore","companies":["Afiniti","Semantics","Focusteck","VentureDive"]},
    {"title":"Backend Developer","tags":["python","nodejs","java","sql","rest api","backend","databases","docker"],
     "salary":"PKR 120K–300K/mo","mode":"On-site / Hybrid","type":"Permanent","experience":"1–3 years",
     "region":"Islamabad, Lahore, Karachi","companies":["Netsol Technologies","Arbisoft","Dastgyr"]},
    {"title":"Frontend Developer","tags":["javascript","react","nextjs","html","css","typescript","ui","web"],
     "salary":"PKR 100K–280K/mo","mode":"Remote / On-site","type":"Permanent","experience":"0–2 years",
     "region":"Islamabad, Remote (US)","companies":["Tkxel","Technosoft","Sapient Corp","NetSolutions"]},
    {"title":"DevOps Engineer","tags":["devops","docker","kubernetes","aws","ci/cd","linux","automation","cloud"],
     "salary":"PKR 180K–420K/mo","mode":"Remote / Hybrid","type":"Permanent","experience":"2–4 years",
     "region":"Remote (Global), Islamabad","companies":["Mobilink","Jazz","10Pearls","Systems Ltd"]},
    {"title":"Cybersecurity Analyst","tags":["security","networking","ethical hacking","linux","cryptography","soc"],
     "salary":"PKR 150K–350K/mo","mode":"On-site / Hybrid","type":"Permanent","experience":"1–3 years",
     "region":"Islamabad, Rawalpindi","companies":["PTCL","Jazz","FBR-IT","National CERT Pakistan"]},
    {"title":"Cloud Architect","tags":["aws","cloud","architecture","serverless","devops","kubernetes","infrastructure"],
     "salary":"PKR 300K–700K/mo","mode":"Remote","type":"Permanent","experience":"4–6 years",
     "region":"Remote (Global)","companies":["Microsoft","AWS","Contour Software","Folio3"]},
    {"title":"AI Research Intern","tags":["ai","machine learning","python","research","deep learning","math"],
     "salary":"PKR 30K–80K/mo","mode":"On-site / Remote","type":"Internship","experience":"0 years",
     "region":"Islamabad, Lahore","companies":["NCAI NUST","ITU Punjab","Afiniti","VentureDive","DecodeLabs"]},
    {"title":"Data Engineer","tags":["data","sql","python","spark","etl","cloud","pipeline","databases"],
     "salary":"PKR 150K–380K/mo","mode":"Hybrid / Remote","type":"Permanent","experience":"2–4 years",
     "region":"Islamabad, Karachi","companies":["Teradata","Sapient","Systems Ltd","Zones"]},
    {"title":"Mobile App Developer","tags":["flutter","dart","mobile","android","ios","react native","ui"],
     "salary":"PKR 100K–250K/mo","mode":"On-site / Remote","type":"Permanent","experience":"1–2 years",
     "region":"Islamabad, Lahore, Remote","companies":["Siemens Pakistan","NetSolutions"]},
    {"title":"LLM / GenAI Engineer","tags":["llm","openai","langchain","rag","python","ai","transformers","prompt engineering"],
     "salary":"PKR 250K–600K/mo","mode":"Remote","type":"Permanent / Fellowship","experience":"1–3 years",
     "region":"Remote (Global / US startups)","companies":["Anthropic (Remote)","Scale AI","Hugging Face"]},
    {"title":"AI Fellowship (PIAIC / NCAI)","tags":["ai","python","machine learning","deep learning","student","fellowship"],
     "salary":"Subsidized / Scholarship","mode":"On-site / Hybrid","type":"Fellowship","experience":"0 years",
     "region":"Islamabad, Lahore, Karachi","companies":["PIAIC","NCAI","COMSATS","NED University"]},
]

ALL_DATA = {"Careers": CAREERS, "Courses": COURSES, "Books": BOOKS, "Movies": MOVIES}
POPULAR_SKILLS = ["Python","Machine Learning","Deep Learning","JavaScript","React","SQL",
                   "Docker","AWS","NLP","Data Science","TensorFlow","Cybersecurity","DevOps",
                   "Flutter","LLM","Algorithms","Cloud","Kubernetes","Transformers","Web Development",
                   "PyTorch","Statistics","Java","Node.js","MongoDB"]
HISTORY_FILE = "search_history.json"
CAT_ICONS = {"Careers":"💼","Courses":"📚","Books":"📖","Movies":"🎬"}
TYPE_COLORS = {"Permanent":"#10B981","Internship":"#F59E0B","Fellowship":"#7C3AED","Contract":"#06B6D4"}


def compute_tfidf(corpus):
    N = len(corpus)
    df = Counter()
    for doc in corpus:
        for term in set(doc): df[term] += 1
    tfidf_matrix = []
    for doc in corpus:
        tf = Counter(doc); total = len(doc); vec = {}
        for term in tf:
            vec[term] = (tf[term]/total) * (math.log(N/(df[term]+1))+1)
        tfidf_matrix.append(vec)
    return tfidf_matrix

def cosine_sim(v1, v2):
    common = set(v1) & set(v2)
    dot = sum(v1[k]*v2[k] for k in common)
    n1 = math.sqrt(sum(x**2 for x in v1.values()))
    n2 = math.sqrt(sum(x**2 for x in v2.values()))
    return 0.0 if n1==0 or n2==0 else dot/(n1*n2)

def get_recommendations(skills_weighted, category, top_n=5):
    items = ALL_DATA[category]
    corpus = [" ".join(i["tags"]).lower().split() for i in items]
    user_tokens = " ".join(skills_weighted).lower().split()
    tfidf = compute_tfidf(corpus + [user_tokens])
    user_vec = tfidf[-1]; item_vecs = tfidf[:-1]
    user_set = set(t.lower() for t in skills_weighted)
    scored = []
    for item, vec in zip(items, item_vecs):
        score = cosine_sim(user_vec, vec)
        matched = list(user_set & set(t.lower() for t in item["tags"]))
        scored.append({"item": item, "score": score, "matched": matched})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_n]

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE) as f: return json.load(f)
        except: pass
    return []

def save_history(entry):
    h = load_history(); h.insert(0, entry)
    with open(HISTORY_FILE, "w") as f: json.dump(h[:50], f, indent=2)


def shadow(widget, blur=20, color="#000000", dx=0, dy=4):
    eff = QGraphicsDropShadowEffect()
    eff.setBlurRadius(blur)
    eff.setColor(QColor(color))
    eff.setOffset(dx, dy)
    widget.setGraphicsEffect(eff)
    return eff


class GradientLabel(QLabel):
    def __init__(self, text, color1="#7C3AED", color2="#06B6D4", size=22, bold=True):
        super().__init__(text)
        self._c1, self._c2 = color1, color2
        f = QFont("Segoe UI", size)
        f.setBold(bold)
        self.setFont(f)
        self.setStyleSheet("background:transparent; color:#E2E8F0;")

class ScoreBar(QWidget):
    def __init__(self, score, parent=None):
        super().__init__(parent)
        self.score = score
        self.setFixedHeight(8)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        # background
        p.setBrush(QBrush(QColor(C["border"])))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(self.rect(), 3, 3)
        # fill
        w = int(self.width() * min(self.score, 1.0))
        if w > 0:
            grad = QLinearGradient(0, 0, w, 0)
            if self.score >= 0.5:
                grad.setColorAt(0, QColor("#10B981"))
                grad.setColorAt(1, QColor("#06B6D4"))
            elif self.score >= 0.2:
                grad.setColorAt(0, QColor("#F59E0B"))
                grad.setColorAt(1, QColor("#EF8C0B"))
            else:
                grad.setColorAt(0, QColor("#EF4444"))
                grad.setColorAt(1, QColor("#DC2626"))
            p.setBrush(QBrush(grad))
            r = self.rect(); r.setWidth(w)
            p.drawRoundedRect(r, 3, 3)


class SkillChip(QPushButton):
    def __init__(self, text, active=False, parent=None):
        super().__init__(text, parent)
        self.active = active
        self._update_style()
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(36)

    def _update_style(self):
        if self.active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {C['accent3']}; color: white;
                    border: none; border-radius: 18px;
                    padding: 0 18px; font-size: 16px; font-weight: bold;
                    font-family: 'Segoe UI', sans-serif;
                }}
                QPushButton:hover {{ background: #0ea271; }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {C['card2']}; color: {C['muted']};
                    border: 1px solid {C['border']}; border-radius: 18px;
                    padding: 0 18px; font-size: 16px;
                    font-family: 'Segoe UI', sans-serif;
                }}
                QPushButton:hover {{
                    background: {C['accent']}; color: white; border-color: {C['accent']};
                }}
            """)

    def set_active(self, v):
        self.active = v
        self._update_style()


class StarRating(QWidget):
    rating_changed = pyqtSignal(int)

    def __init__(self, initial=3, parent=None):
        super().__init__(parent)
        self.rating = initial
        self.setFixedSize(132, 30)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        for i in range(5):
            x = i * 24
            p.setPen(Qt.NoPen)
            if i < self.rating:
                p.setBrush(QBrush(QColor(C["warn"])))
            else:
                p.setBrush(QBrush(QColor(C["border"])))
            # draw star polygon
            path = QPainterPath()
            cx, cy, ro, ri = x+11, 14, 10, 5
            import math as m
            for j in range(5):
                ao = m.radians(j*72-90)
                ai = m.radians(j*72-90+36)
                if j == 0:
                    path.moveTo(cx+ro*m.cos(ao), cy+ro*m.sin(ao))
                else:
                    path.lineTo(cx+ro*m.cos(ao), cy+ro*m.sin(ao))
                path.lineTo(cx+ri*m.cos(ai), cy+ri*m.sin(ai))
            path.closeSubpath()
            p.drawPath(path)

    def mousePressEvent(self, event):
        r = max(1, min(5, int(event.x()//24)+1))
        self.rating = r
        self.update()
        self.rating_changed.emit(r)


class CardFrame(QFrame):
    def __init__(self, parent=None, color=None, radius=16):
        super().__init__(parent)
        bg = color or C["card"]
        self.setStyleSheet(f"""
            QFrame {{
                background: {bg};
                border-radius: {radius}px;
                border: 1px solid {C['border']};
            }}
        """)
        shadow(self, blur=18, color="#000000", dy=4)


class PillButton(QPushButton):
    def __init__(self, text, color=None, text_color="white", size=13, parent=None):
        super().__init__(text, parent)
        bg = color or C["accent"]
        self.setFixedHeight(45)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background: {bg}; color: {text_color};
                border: none; border-radius: 22px;
                padding: 0 28px; font-size: {size}px; font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
            }}
            QPushButton:hover {{ background: {bg}dd; }}
            QPushButton:pressed {{ background: {bg}aa; }}
        """)


class SectionHeader(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        f = QFont("Segoe UI", 13); f.setBold(True)
        self.setFont(f)
        self.setStyleSheet(f"color: {C['muted']}; background: transparent; letter-spacing: 1px;")


class ResultCard(QFrame):
    RANK_COLORS = {1:"#F59E0B", 2:"#94A3B8", 3:"#CD7F32", 4:"#475569", 5:"#334155"}

    def __init__(self, rank, entry, category, parent=None):
        super().__init__(parent)
        item = entry["item"]; score = entry["score"]; matched = entry["matched"]
        self.setStyleSheet(f"""
            QFrame {{
                background: {C['card']};
                border-radius: 19px;
                border: 1px solid {C['border']};
            }}
        """)
        shadow(self, blur=24, dy=6)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        banner = QFrame()
        rc = self.RANK_COLORS.get(rank, "#334155")
        banner.setStyleSheet(f"background: {rc}; border-radius: 19px 16px 0 0; border: none;")
        banner.setFixedHeight(8)
        root.addWidget(banner)

        body = QVBoxLayout()
        body.setContentsMargins(20, 16, 20, 18)
        body.setSpacing(10)
        root.addLayout(body)

        title_row = QHBoxLayout()

        rank_lbl = QLabel(f"#{rank}")
        rank_lbl.setStyleSheet(f"""
            color: {rc}; font-size: 24px; font-weight: 900;
            font-family: 'Segoe UI', sans-serif; background: transparent;
        """)
        rank_lbl.setFixedWidth(43)
        title_row.addWidget(rank_lbl)

        title_lbl = QLabel(item["title"])
        title_lbl.setStyleSheet(f"color:{C['text']}; font-size:20px; font-weight:bold; background:transparent;")
        title_lbl.setWordWrap(True)
        title_row.addWidget(title_lbl, 1)

        pct = int(score*100)
        s_color = ("#10B981" if score>=0.5 else "#F59E0B" if score>=0.2 else "#EF4444")
        score_lbl = QLabel(f"{pct}%")
        score_lbl.setStyleSheet(f"""
            color: {s_color}; font-size: 29px; font-weight: 900;
            font-family: 'Segoe UI', sans-serif; background: transparent;
        """)
        score_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        title_row.addWidget(score_lbl)

        body.addLayout(title_row)

        bar = ScoreBar(score)
        body.addWidget(bar)

        match_lbl = QLabel(f"Match Score: {pct}%  ·  {'Excellent' if pct>=50 else 'Good' if pct>=25 else 'Low'} Alignment")
        match_lbl.setStyleSheet(f"color:{C['muted']}; font-size:15px; background:transparent;")
        body.addWidget(match_lbl)

        if category == "Careers":
            meta = QFrame()
            meta.setStyleSheet(f"background:{C['card2']}; border-radius:12px; border:none;")
            meta_layout = QGridLayout(meta)
            meta_layout.setContentsMargins(14, 12, 14, 12)
            meta_layout.setSpacing(8)

            fields = [
                ("💰", "Salary",     item.get("salary","—")),
                ("📍", "Region",     item.get("region","—")),
                ("🏢", "Work Mode",  item.get("mode","—")),
                ("🎓", "Experience", item.get("experience","—")),
            ]
            for i, (icon, label, val) in enumerate(fields):
                r, c = divmod(i, 2)
                cell = QVBoxLayout()
                top = QLabel(f"{icon} {label}")
                top.setStyleSheet(f"color:{C['muted']}; font-size:13px; background:transparent;")
                val_lbl = QLabel(val)
                val_lbl.setStyleSheet(f"color:{C['text']}; font-size:16px; font-weight:bold; background:transparent;")
                val_lbl.setWordWrap(True)
                cell.addWidget(top); cell.addWidget(val_lbl)
                w = QWidget(); w.setLayout(cell); w.setStyleSheet("background:transparent;")
                meta_layout.addWidget(w, r, c)

            jtype = item.get("type","Permanent").split("/")[0].strip()
            tc = TYPE_COLORS.get(jtype, C["accent"])
            type_badge = QLabel(f"  📋 {item.get('type','—')}  ")
            type_badge.setStyleSheet(f"""
                background:{tc}22; color:{tc}; border:1px solid {tc};
                border-radius:10px; font-size:15px; font-weight:bold; padding: 4px 8px;
            """)
            meta_layout.addWidget(type_badge, 2, 0, 1, 2)
            body.addWidget(meta)

            companies = item.get("companies", [])
            if companies:
                co_row = QHBoxLayout()
                co_lbl = QLabel("🏭")
                co_lbl.setStyleSheet("color:#64748B; font-size:16px; background:transparent;")
                co_row.addWidget(co_lbl)
                for co in companies[:4]:
                    cb = QLabel(f" {co} ")
                    cb.setStyleSheet(f"""
                        background:{C['accent']}22; color:{C['accent']};
                        border:1px solid {C['accent']}55; border-radius:8px;
                        font-size:13px; font-weight:bold; padding: 4px 6px;
                    """)
                    co_row.addWidget(cb)
                co_row.addStretch()
                body.addLayout(co_row)

        exp = QFrame()
        exp.setStyleSheet(f"background:{C['panel']}; border-radius:12px; border:none;")
        exp_layout = QVBoxLayout(exp)
        exp_layout.setContentsMargins(12, 10, 12, 10)
        exp_layout.setSpacing(6)

        why_lbl = QLabel("✦  Why this match?")
        why_lbl.setStyleSheet(f"color:{C['accent2']}; font-size:15px; font-weight:bold; background:transparent;")
        exp_layout.addWidget(why_lbl)

        tags_row = QHBoxLayout(); tags_row.setSpacing(6)
        if matched:
            for t in matched:
                tl = QLabel(f" ✓ {t} ")
                tl.setStyleSheet(f"""
                    background:{C['accent3']}33; color:{C['accent3']};
                    border:1px solid {C['accent3']}66; border-radius:8px;
                    font-size:13px; font-weight:bold; padding: 4px 6px;
                """)
                tags_row.addWidget(tl)
            other = [t for t in item["tags"] if t not in matched]
            for t in other[:3]:
                tl = QLabel(f" {t} ")
                tl.setStyleSheet(f"""
                    background:{C['card2']}; color:{C['muted']};
                    border:1px solid {C['border']}; border-radius:8px;
                    font-size:13px; padding: 4px 6px;
                """)
                tags_row.addWidget(tl)
        else:
            note = QLabel("Matched via TF-IDF vector alignment (semantic similarity)")
            note.setStyleSheet(f"color:{C['muted']}; font-size:15px; background:transparent;")
            tags_row.addWidget(note)
        tags_row.addStretch()
        exp_layout.addLayout(tags_row)
        body.addWidget(exp)


class HistoryCard(QFrame):
    rerun = pyqtSignal(dict)

    def __init__(self, entry, parent=None):
        super().__init__(parent)
        self.entry = entry
        self.setStyleSheet(f"""
            QFrame {{
                background: {C['card']};
                border-radius: 14px;
                border: 1px solid {C['border']};
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(4)

        hdr = QHBoxLayout()
        cat_icon = CAT_ICONS.get(entry.get("category",""), "📦")
        cat_lbl = QLabel(f"{cat_icon} {entry.get('category','')}")
        cat_lbl.setStyleSheet(f"color:{C['accent2']}; font-size:16px; font-weight:bold; background:transparent;")
        hdr.addWidget(cat_lbl)
        hdr.addStretch()
        ts = QLabel(entry.get("timestamp",""))
        ts.setStyleSheet(f"color:{C['muted']}; font-size:13px; background:transparent;")
        hdr.addWidget(ts)
        layout.addLayout(hdr)

        skills_text = ", ".join(entry.get("skills",[])[:4])
        if len(entry.get("skills",[])) > 4: skills_text += " …"
        sl = QLabel(f"🔑  {skills_text}")
        sl.setStyleSheet(f"color:{C['text']}; font-size:15px; background:transparent;")
        sl.setWordWrap(True)
        layout.addWidget(sl)

        top = QLabel(f"🥇  {entry.get('top_result','—')}")
        top.setStyleSheet(f"color:{C['accent3']}; font-size:15px; font-weight:bold; background:transparent;")
        top.setWordWrap(True)
        layout.addWidget(top)

        btn = QPushButton("↺  Re-run")
        btn.setFixedHeight(31)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; color: {C['accent']};
                border: 1px solid {C['accent']}; border-radius: 8px;
                font-size: 13px; font-weight: bold;
            }}
            QPushButton:hover {{ background: {C['accent']}22; }}
        """)
        btn.clicked.connect(lambda: self.rerun.emit(self.entry))
        layout.addWidget(btn, alignment=Qt.AlignRight)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DecodeLabs · AI Recommendation Engine · Project 3")
        self.setMinimumSize(1280, 800)
        screen = QApplication.primaryScreen().availableGeometry()
        target_w = min(int(screen.width() * 0.90), 1920)
        target_h = min(int(screen.height() * 0.90), 1200)
        self.resize(max(target_w, 1280), max(target_h, 800))
        self.move(
            screen.x() + (screen.width() - self.width()) // 2,
            screen.y() + (screen.height() - self.height()) // 2,
        )
        self.setStyleSheet(QSS)

        self._selected_skills = []
        self._ratings = {}
        self._category = "Careers"
        self._skill_chips = {}
        self._cat_buttons = {}

        central = QWidget(); central.setObjectName("root")
        central.setStyleSheet(f"background:{C['bg']};")
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self._build_navbar(root_layout)
        body = QHBoxLayout()
        body.setContentsMargins(12, 12, 12, 12)
        body.setSpacing(12)
        root_layout.addLayout(body, 1)

        self._build_left(body)
        self._build_center(body)
        self._build_right(body)
        self._refresh_history()

    def _build_navbar(self, parent):
        nav = QFrame()
        nav.setFixedHeight(69)
        nav.setStyleSheet(f"background:#080C16; border-bottom: 1px solid {C['border']};")
        nl = QHBoxLayout(nav); nl.setContentsMargins(24, 0, 24, 0)

        logo = QLabel("⬡  DecodeLabs")
        logo.setStyleSheet(f"color:{C['accent']}; font-size:24px; font-weight:900; font-family:'Segoe UI';")
        nl.addWidget(logo)

        sep = QLabel("·")
        sep.setStyleSheet(f"color:{C['border']}; font-size:24px;")
        nl.addWidget(sep)

        sub = QLabel("AI Recommendation Engine — Project 3")
        sub.setStyleSheet(f"color:{C['muted']}; font-size:17px; font-family:'Segoe UI';")
        nl.addWidget(sub)
        nl.addStretch()

        for text, color in [("TF-IDF", C["accent"]), ("Cosine Similarity", C["accent2"]), ("Content-Based Filtering", C["accent3"])]:
            b = QLabel(f"  {text}  ")
            b.setStyleSheet(f"""
                background: {color}22; color: {color};
                border: 1px solid {color}55; border-radius: 12px;
                font-size: 15px; font-weight: bold; padding: 6px 10px;
                font-family: 'Segoe UI', sans-serif;
            """)
            nl.addWidget(b)
            nl.addSpacing(6)

        parent.addWidget(nav)

    def _build_left(self, parent):
        panel = QFrame()
        panel.setFixedWidth(440)
        panel.setStyleSheet(f"background:{C['panel']}; border-radius:19px;")
        outer = QVBoxLayout(panel)
        outer.setContentsMargins(16, 16, 16, 16)
        outer.setSpacing(12)
        parent.addWidget(panel)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("background:transparent; border:none;")

        content = QWidget()
        content.setStyleSheet("background:transparent;")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 4, 0)
        layout.setSpacing(14)
        scroll.setWidget(content)
        outer.addWidget(scroll, 1)

        self._add_section(layout, "📦  Category")
        cat_grid = QGridLayout(); cat_grid.setSpacing(8)
        for i, (cat, icon) in enumerate(CAT_ICONS.items()):
            b = QPushButton(f"{icon}  {cat}")
            b.setFixedHeight(46)
            b.setCursor(Qt.PointingHandCursor)
            self._cat_buttons[cat] = b
            b.clicked.connect(lambda _, c=cat: self._set_category(c))
            cat_grid.addWidget(b, i//2, i%2)
        layout.addLayout(cat_grid)
        self._update_cat_buttons()

        self._add_section(layout, "🔍  Search & Add Skills")
        search_row = QHBoxLayout(); search_row.setSpacing(8)
        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("Type a skill and press Enter…")
        self._search_input.setFixedHeight(44)
        self._search_input.returnPressed.connect(self._add_from_search)
        self._search_input.textChanged.connect(self._filter_chips)
        search_row.addWidget(self._search_input)
        add_btn = PillButton("Add", C["accent2"])
        add_btn.setFixedWidth(72)
        add_btn.clicked.connect(self._add_from_search)
        search_row.addWidget(add_btn)
        layout.addLayout(search_row)

        self._add_section(layout, "⚡  Popular Skills")
        self._chips_widget = QWidget()
        self._chips_widget.setStyleSheet("background:transparent;")
        self._chips_layout = QVBoxLayout(self._chips_widget)
        self._chips_layout.setContentsMargins(0, 0, 0, 0)
        self._chips_layout.setSpacing(8)
        layout.addWidget(self._chips_widget)
        self._render_chips(POPULAR_SKILLS)

        self._add_section(layout, "⭐  Your Skills & Ratings")
        self._sel_widget = QWidget()
        self._sel_widget.setStyleSheet("background:transparent;")
        self._sel_layout = QVBoxLayout(self._sel_widget)
        self._sel_layout.setContentsMargins(0, 0, 0, 0)
        self._sel_layout.setSpacing(6)
        layout.addWidget(self._sel_widget)

        self._sel_placeholder = QLabel("No skills selected yet.\nClick chips or search above.")
        self._sel_placeholder.setAlignment(Qt.AlignCenter)
        self._sel_placeholder.setStyleSheet(f"color:{C['muted']}; font-size:16px; background:transparent;")
        self._sel_layout.addWidget(self._sel_placeholder)

        layout.addStretch()
        run_btn = QPushButton("🚀   Get Recommendations")
        run_btn.setFixedHeight(55)
        run_btn.setCursor(Qt.PointingHandCursor)
        run_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {C['accent']},stop:1 {C['accent2']});
                color: white; border: none; border-radius: 27px;
                font-size: 19px; font-weight: bold; font-family: 'Segoe UI', sans-serif;
            }}
            QPushButton:hover {{ opacity: 0.9; }}
            QPushButton:pressed {{ opacity: 0.7; }}
        """)
        shadow(run_btn, blur=20, color=C["accent"], dy=4)
        run_btn.clicked.connect(self._run)
        outer.addWidget(run_btn)

        clear_btn = QPushButton("🗑  Clear All")
        clear_btn.setFixedHeight(41)
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; color: {C['muted']};
                border: 1px solid {C['border']}; border-radius: 20px;
                font-size: 16px; font-family: 'Segoe UI', sans-serif;
            }}
            QPushButton:hover {{ color: {C['danger']}; border-color: {C['danger']}; }}
        """)
        clear_btn.clicked.connect(self._clear)
        outer.addWidget(clear_btn)

    def _build_center(self, parent):
        panel = QWidget()
        panel.setStyleSheet("background:transparent;")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        parent.addWidget(panel, 1)

        
        hdr = QHBoxLayout()
        self._res_title = QLabel("Top 5 Recommendations")
        self._res_title.setStyleSheet(f"color:{C['text']}; font-size:29px; font-weight:900; font-family:'Segoe UI'; background:transparent;")
        hdr.addWidget(self._res_title)
        hdr.addStretch()
        self._res_meta = QLabel("")
        self._res_meta.setStyleSheet(f"color:{C['muted']}; font-size:16px; background:transparent;")
        hdr.addWidget(self._res_meta)
        layout.addLayout(hdr)

        self._stack = QStackedWidget()
        self._stack.setStyleSheet("background:transparent;")
        layout.addWidget(self._stack, 1)

        welcome = QWidget(); welcome.setStyleSheet("background:transparent;")
        wl = QVBoxLayout(welcome); wl.setAlignment(Qt.AlignCenter)
        icon = QLabel("⬡"); icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet(f"color:{C['accent']}; font-size:84px; background:transparent;")
        wl.addWidget(icon)
        wt = QLabel("Select skills on the left\nthen click  🚀 Get Recommendations")
        wt.setAlignment(Qt.AlignCenter)
        wt.setStyleSheet(f"color:{C['muted']}; font-size:21px; background:transparent;")
        wl.addWidget(wt)
        sub = QLabel("Powered by TF-IDF Weighting + Cosine Similarity")
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet(f"color:{C['border']}; font-size:16px; background:transparent;")
        wl.addWidget(sub)
        self._stack.addWidget(welcome)  

       
        results_scroll = QScrollArea()
        results_scroll.setWidgetResizable(True)
        results_scroll.setStyleSheet("background:transparent; border:none;")
        self._results_widget = QWidget()
        self._results_widget.setStyleSheet("background:transparent;")
        self._results_layout = QVBoxLayout(self._results_widget)
        self._results_layout.setContentsMargins(4, 4, 4, 4)
        self._results_layout.setSpacing(14)
        results_scroll.setWidget(self._results_widget)
        self._stack.addWidget(results_scroll)  
        self._stack.setCurrentIndex(0)

    def _build_right(self, parent):
        panel = QFrame()
        panel.setFixedWidth(331)
        panel.setStyleSheet(f"background:{C['panel']}; border-radius:19px;")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(14, 16, 14, 14)
        layout.setSpacing(10)
        parent.addWidget(panel)

        self._add_section(layout, "📂  Recent Sessions")

        hist_scroll = QScrollArea()
        hist_scroll.setWidgetResizable(True)
        hist_scroll.setStyleSheet("background:transparent; border:none;")
        self._hist_widget = QWidget()
        self._hist_widget.setStyleSheet("background:transparent;")
        self._hist_layout = QVBoxLayout(self._hist_widget)
        self._hist_layout.setContentsMargins(0,0,0,0)
        self._hist_layout.setSpacing(8)
        hist_scroll.setWidget(self._hist_widget)
        layout.addWidget(hist_scroll, 1)

        clear_hist = QPushButton("🗑  Clear History")
        clear_hist.setFixedHeight(41)
        clear_hist.setCursor(Qt.PointingHandCursor)
        clear_hist.setStyleSheet(f"""
            QPushButton {{
                background: transparent; color: {C['muted']};
                border: 1px solid {C['border']}; border-radius: 20px;
                font-size: 16px; font-family: 'Segoe UI', sans-serif;
            }}
            QPushButton:hover {{ color: {C['danger']}; border-color: {C['danger']}; }}
        """)
        clear_hist.clicked.connect(self._clear_history)
        layout.addWidget(clear_hist)

    def _add_section(self, layout, text):
        lbl = QLabel(text.upper())
        lbl.setStyleSheet(f"""
            color: {C['muted']}; font-size: 13px; font-weight: bold;
            letter-spacing: 1.5px; background: transparent;
            font-family: 'Segoe UI', sans-serif;
            padding-top: 6px;
        """)
        layout.addWidget(lbl)

    def _set_category(self, cat):
        self._category = cat
        self._update_cat_buttons()

    def _update_cat_buttons(self):
        for cat, btn in self._cat_buttons.items():
            active = (cat == self._category)
            if active:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background: {C['accent']}; color: white;
                        border: none; border-radius: 12px;
                        font-size: 16px; font-weight: bold;
                        font-family: 'Segoe UI', sans-serif;
                    }}
                """)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background: {C['card2']}; color: {C['muted']};
                        border: 1px solid {C['border']}; border-radius: 12px;
                        font-size: 16px; font-family: 'Segoe UI', sans-serif;
                    }}
                    QPushButton:hover {{
                        background: {C['accent']}33; color: {C['text']};
                        border-color: {C['accent']};
                    }}
                """)

    def _render_chips(self, skills):
        for i in reversed(range(self._chips_layout.count())):
            w = self._chips_layout.itemAt(i).widget()
            if w: w.deleteLater()

        row_widget = None
        row_layout = None
        for i, skill in enumerate(skills):
            if i % 2 == 0:
                row_widget = QWidget(); row_widget.setStyleSheet("background:transparent;")
                row_layout = QHBoxLayout(row_widget)
                row_layout.setContentsMargins(0,0,0,0); row_layout.setSpacing(8)
                self._chips_layout.addWidget(row_widget)

            active = skill.lower() in [s.lower() for s in self._selected_skills]
            chip = SkillChip(skill, active)
            chip.setMinimumWidth(150)
            self._skill_chips[skill] = chip
            chip.clicked.connect(lambda _, s=skill: self._toggle_skill(s))
            row_layout.addWidget(chip)
        if row_layout: row_layout.addStretch()

    def _filter_chips(self, text):
        q = text.strip().lower()
        filtered = [s for s in POPULAR_SKILLS if q in s.lower()] if q else POPULAR_SKILLS
        self._render_chips(filtered)

    def _add_from_search(self):
        val = self._search_input.text().strip()
        if val:
            self._toggle_skill(val)
            self._search_input.clear()
            self._render_chips(POPULAR_SKILLS)

    def _toggle_skill(self, skill):
        low = skill.lower()
        existing = [s.lower() for s in self._selected_skills]
        if low in existing:
            self._selected_skills = [s for s in self._selected_skills if s.lower() != low]
            self._ratings.pop(low, None)
        else:
            self._selected_skills.append(skill)
            self._ratings[low] = 3
        self._render_chips([s for s in POPULAR_SKILLS
                            if not self._search_input.text() or
                            self._search_input.text().lower() in s.lower()])
        self._render_selected()

    def _render_selected(self):
        for i in reversed(range(self._sel_layout.count())):
            w = self._sel_layout.itemAt(i).widget()
            if w: w.deleteLater()

        if not self._selected_skills:
            self._sel_layout.addWidget(self._sel_placeholder)
            return

        for skill in self._selected_skills:
            row = QFrame()
            row.setStyleSheet(f"""
                QFrame {{
                    background: {C['card2']}; border-radius: 12px;
                    border: 1px solid {C['border']};
                }}
            """)
            rl = QHBoxLayout(row); rl.setContentsMargins(10, 6, 10, 6); rl.setSpacing(8)

            rm = QPushButton("✕")
            rm.setFixedSize(24, 24)
            rm.setCursor(Qt.PointingHandCursor)
            rm.setStyleSheet(f"""
                QPushButton {{
                    background: transparent; color: {C['danger']};
                    border: none; font-size: 15px; font-weight: bold;
                }}
                QPushButton:hover {{ background: {C['danger']}22; border-radius: 6px; }}
            """)
            rm.clicked.connect(lambda _, s=skill: self._toggle_skill(s))
            rl.addWidget(rm)

            lbl = QLabel(skill)
            lbl.setStyleSheet(f"color:{C['text']}; font-size:16px; background:transparent;")
            rl.addWidget(lbl, 1)

            sr = StarRating(self._ratings.get(skill.lower(), 3))
            sr.rating_changed.connect(lambda r, s=skill: self._set_rating(s, r))
            rl.addWidget(sr)

            self._sel_layout.addWidget(row)

    def _set_rating(self, skill, rating):
        self._ratings[skill.lower()] = rating

    def _clear(self):
        self._selected_skills = []
        self._ratings = {}
        self._render_chips(POPULAR_SKILLS)
        self._render_selected()
        self._stack.setCurrentIndex(0)
        self._res_title.setText("Top 5 Recommendations")
        self._res_meta.setText("")

    def _run(self):
        if not self._selected_skills:
            QMessageBox.warning(self, "No Skills", "Please select at least one skill first.")
            return

        weighted = []
        for s in self._selected_skills:
            r = self._ratings.get(s.lower(), 3)
            weighted.extend([s] * r)

        results = get_recommendations(weighted, self._category, top_n=5)

        entry = {
            "timestamp": datetime.now().strftime("%d %b %Y  %H:%M"),
            "category": self._category,
            "skills": self._selected_skills,
            "ratings": {k: v for k, v in self._ratings.items()
                        if k in [s.lower() for s in self._selected_skills]},
            "top_result": results[0]["item"]["title"] if results else "—"
        }
        save_history(entry)
        self._refresh_history()
        self._show_results(results)

    def _show_results(self, results):
        for i in reversed(range(self._results_layout.count())):
            item = self._results_layout.itemAt(i)
            if item.widget(): item.widget().deleteLater()

        self._res_title.setText(f"Top 5  ·  {CAT_ICONS.get(self._category,'')} {self._category}")
        self._res_meta.setText(f"{len(self._selected_skills)} skills  ·  {datetime.now().strftime('%H:%M')}")

        if not results:
            nl = QLabel("No matches found. Try different skills.")
            nl.setAlignment(Qt.AlignCenter)
            nl.setStyleSheet(f"color:{C['muted']}; font-size:19px;")
            self._results_layout.addWidget(nl)
        else:
            for rank, entry in enumerate(results, 1):
                card = ResultCard(rank, entry, self._category)
                self._results_layout.addWidget(card)
        self._results_layout.addStretch()
        self._stack.setCurrentIndex(1)

    def _refresh_history(self):
        for i in reversed(range(self._hist_layout.count())):
            w = self._hist_layout.itemAt(i).widget()
            if w: w.deleteLater()

        history = load_history()
        if not history:
            ph = QLabel("No sessions yet.\nRun a search to see history.")
            ph.setAlignment(Qt.AlignCenter)
            ph.setStyleSheet(f"color:{C['muted']}; font-size:16px; background:transparent;")
            self._hist_layout.addWidget(ph)
        else:
            for h in history[:12]:
                hc = HistoryCard(h)
                hc.rerun.connect(self._rerun)
                self._hist_layout.addWidget(hc)
        self._hist_layout.addStretch()

    def _rerun(self, entry):
        self._selected_skills = entry.get("skills", [])
        self._ratings = entry.get("ratings", {})
        self._set_category(entry.get("category", "Careers"))
        self._render_chips(POPULAR_SKILLS)
        self._render_selected()
        self._run()

    def _clear_history(self):
        reply = QMessageBox.question(self, "Clear History",
                                     "Delete all search history?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            with open(HISTORY_FILE, "w") as f: json.dump([], f)
            self._refresh_history()


if __name__ == "__main__":
    
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 11)) 
    p = app.palette()
    p.setColor(QPalette.Window,          QColor(C["bg"]))
    p.setColor(QPalette.WindowText,      QColor(C["text"]))
    p.setColor(QPalette.Base,            QColor(C["card"]))
    p.setColor(QPalette.AlternateBase,   QColor(C["panel"]))
    p.setColor(QPalette.Text,            QColor(C["text"]))
    p.setColor(QPalette.Button,          QColor(C["card"]))
    p.setColor(QPalette.ButtonText,      QColor(C["text"]))
    p.setColor(QPalette.Highlight,       QColor(C["accent"]))
    p.setColor(QPalette.HighlightedText, QColor(C["white"]))
    app.setPalette(p)
    app.setStyleSheet(QSS)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
