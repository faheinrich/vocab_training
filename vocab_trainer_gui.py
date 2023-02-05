from pathlib import Path
# import pandas as pd
import random
import sys
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QApplication, QPushButton, QLabel, QCheckBox
from PyQt6.QtGui import QFont
import csv

def get_file_paths_csv():
    path_to_data = Path(sys.argv[0]).parent / Path("vocab_data")
    file_paths = path_to_data.glob("*.csv")

    return file_paths

# def get_file_paths_xlsx():
#     path_to_data = Path(sys.argv[0]).parent / Path("vocab_data/xlsx")
#     file_paths = path_to_data.glob("*.xlsx")
#
#     return file_paths

# def convert_xlsx_to_csv(fp):
#
#     print("Orig", fp)
#     new_fp = fp.parent / Path(str(fp.stem) + ".csv")
#
#     with open(new_fp, 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#
#         df = pd.read_excel(fp)
#         for idx, hiragana, kanji, deutsch in df.itertuples():
#             writer.writerow([deutsch, hiragana, kanji])
#
#     print("Converting excel file to csv.")
#
# def load_vocab_data_xlsx(file_paths):
#
#     vocab_filtered = []
#
#     for fp in file_paths:
#         df = pd.read_excel(fp)
#         for idx, hiragana, kanji, deutsch in df.itertuples():
#
#             if not isinstance(hiragana, str) or not isinstance(deutsch, str):
#                 continue
#             if not isinstance(kanji, str):
#                 kanji = ""
#
#             vocab_dict = {"hiragana": hiragana,
#                           "kanji": kanji,
#                           "deutsch": deutsch}
#             vocab_filtered.append(vocab_dict)
#
#     return vocab_filtered


def load_vocab_data_csv(file_paths):
    vocab_filtered = []

    for fp in file_paths:

        with open(fp, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='|')

            for row in reader:
                if len(row) == 3:
                    vocab_dict = {"hiragana": row[1],
                                  "kanji": row[2],
                                  "deutsch": row[0]}
                    vocab_filtered.append(vocab_dict)

    return vocab_filtered

class VocabGui(QMainWindow):

    def keyPressEvent(self, event):
        self.display_next_vocab()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lern Vobalen 🇯🇵")

        width = 1100
        height = 500
        self.setMinimumSize(QSize(width, height))

        self.ask_state = True
        self.show_both = False
        self.mode = "mix"

        only_deutsch_button = QPushButton("Nur Deutsch")
        only_deutsch_button.clicked.connect(lambda: self.switch_mode("deutsch"))
        only_hira_button = QPushButton("Nur Japanisch")
        only_hira_button.clicked.connect(lambda: self.switch_mode("hiragana"))
        mix_button = QPushButton("Mix")
        mix_button.clicked.connect(lambda: self.switch_mode("mix"))

        self.always_show_button = QPushButton("Zeig beides")
        self.always_show_button.clicked.connect(self.swap_show_both)

        self.choose_vocab = None
        open_file_selection_button = QPushButton("Dateien auswählen")
        open_file_selection_button.clicked.connect(self.show_vocab_selector)

        self.font_size = 30
        font_larger_button = QPushButton("Schrift größer")
        font_larger_button.clicked.connect(lambda: self.update_font_size(2))
        font_smaller_button = QPushButton("Schrift kleiner")
        font_smaller_button.clicked.connect(lambda: self.update_font_size(-2))

        mode_button_layout = QHBoxLayout()
        mode_button_layout.addWidget(only_deutsch_button)
        mode_button_layout.addWidget(only_hira_button)
        mode_button_layout.addWidget(mix_button)
        mode_button_layout.addWidget(self.always_show_button)
        mode_button_layout.addWidget(font_smaller_button)
        mode_button_layout.addWidget(font_larger_button)
        mode_button_layout.addWidget(open_file_selection_button)

        self.vocab_promt = QLabel()
        self.vocab_promt.setText("-")

        self.vocab_answer = QLabel()
        self.vocab_answer.setText("-")

        self.next_vocab_button = QPushButton("Weiter")
        self.next_vocab_button.clicked.connect(self.display_next_vocab)

        vocab_display = QHBoxLayout()
        vocab_display.addWidget(self.vocab_promt)
        vocab_display.addWidget(self.vocab_answer)

        main_layout = QVBoxLayout()

        main_layout.addLayout(mode_button_layout)
        main_layout.addLayout(vocab_display)
        main_layout.addWidget(self.next_vocab_button)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.vocabs = load_vocab_data_csv(get_file_paths_csv())
        self.update_font_size(0)
        self.display_next_vocab()

    def update_font_size(self, change: int):
        self.font_size = min(max(self.font_size+change, 5), 100)
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(self.font_size)
        self.vocab_promt.setFont(font)
        self.vocab_answer.setFont(font)

    def update_vocab_list(self, file_paths):
        self.vocabs = load_vocab_data_csv(file_paths)

    def show_vocab_selector(self):
        if self.choose_vocab is None:
            self.choose_vocab = AnotherWindow(self)
        self.choose_vocab.show()

    def switch_mode(self, mode):
        self.mode = mode
        self.display_next_vocab()

    def swap_show_both(self):
        if self.show_both:
            self.always_show_button.setText("Zeig nur eins")
            self.show_both = False
        else:
            self.always_show_button.setText("Zeig beide")
            self.show_both = True

    def display_next_vocab(self):

        if self.ask_state:
            self.vocab_answer.hide()
            self.ask_state = False
            vocab_dict = random.choice(self.vocabs)

            if self.mode == "deutsch":
                self.vocab_promt.setText(f"{vocab_dict['deutsch']}")
                self.vocab_answer.setText(f"{vocab_dict['hiragana']}")
            elif self.mode == "hiragana":
                self.vocab_promt.setText(f"{vocab_dict['hiragana']}")
                self.vocab_answer.setText(f"{vocab_dict['deutsch']}")
            elif self.mode == "mix":
                if random.random() > 0.5:
                    self.vocab_promt.setText(f"{vocab_dict['hiragana']}")
                    self.vocab_answer.setText(f"{vocab_dict['deutsch']}")
                else:
                    self.vocab_promt.setText(f"{vocab_dict['deutsch']}")
                    self.vocab_answer.setText(f"{vocab_dict['hiragana']}")
        else:
            self.vocab_answer.show()
            self.ask_state = True

        if self.show_both:
            self.vocab_answer.show()
            self.ask_state = True


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, maingui: VocabGui):
        super().__init__()

        width = 550
        height = 400
        self.setMinimumSize(QSize(width, height))

        self.main_gui = maingui

        self.warn_empty = QLabel("Mindestens eine Datei auswählen!")
        self.warn_empty.setStyleSheet("color: red;")
        self.warn_empty.hide()

        self.file_paths = [i for i in get_file_paths_csv()]
        self.checkboxes = []

        selector_layout = QVBoxLayout()
        for fp in self.file_paths:
            l = QHBoxLayout()
            f_label = QLabel(str(fp.name))
            box = QCheckBox()
            self.checkboxes.append(box)
            l.addWidget(f_label)
            l.addWidget(box)
            selector_layout.addLayout(l)

        self.select_all()

        submit_button = QPushButton("Übernehmen")
        submit_button.clicked.connect(self.submit_and_close)

        all_button = QPushButton("Alle wählen")
        all_button.clicked.connect(self.select_all)
        notall_button = QPushButton("Alle abwählen")
        notall_button.clicked.connect(self.deselect_all)
        buttons_l = QHBoxLayout()
        buttons_l.addWidget(all_button)
        buttons_l.addWidget(notall_button)

        layout = QVBoxLayout()
        layout.addWidget(self.warn_empty)
        layout.addLayout(selector_layout)
        layout.addLayout(buttons_l)
        layout.addWidget(submit_button)
        self.setLayout(layout)

    def select_all(self):
        for box in self.checkboxes:
            box.setChecked(True)

    def deselect_all(self):
        for box in self.checkboxes:
            box.setChecked(False)

    def submit_and_close(self):
        selected_files = []

        for fp, box in zip(self.file_paths, self.checkboxes):
            if box.isChecked():
                selected_files.append(fp)

        if len(selected_files) == 0:
            self.warn_empty.show()
        else:
            self.warn_empty.hide()
            self.main_gui.update_vocab_list(selected_files)
            self.main_gui.display_next_vocab()
            self.hide()
            return selected_files


def main():
    app = QApplication(sys.argv)
    window = VocabGui()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()

