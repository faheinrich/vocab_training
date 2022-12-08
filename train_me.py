import pandas as pd
import random
import sys


def print_vocab(current_vocab: dict, lang_mode: str):
    def ask_deutsch():
        print(current_vocab["deutsch"], end="")
        input("")
        print(current_vocab["hiragana"], current_vocab["kanji"], "\n")

    def ask_japanisch():
        # if current_vocab["kanji"] != "":
        #     print(current_vocab["hiragana"], ", ", current_vocab["kanji"], end="")
        # else:
        print(current_vocab["hiragana"], end="")
        input("")
        print(current_vocab["deutsch"], "\n")

    if lang_mode == "japanisch":
        ask_japanisch()
    elif lang_mode == "deutsch":
        ask_deutsch()
    elif lang_mode == "mix": 
        if random.random() > 0.5:
            ask_japanisch()
        else:
            ask_japanisch()

def print_scorebreak(idx):
    br = '============'
    mid = '=' * (len(str(idx)) + 2)
    print(f"\n{br}{mid}{br}\n{br} {idx} {br}\n{br}{mid}{br}\n\n")

def main():
    lang_mode = None
    if len(sys.argv) > 1:
            lang_mode = sys.argv[1]
    while lang_mode is None:
        user_input = input("Sprache eingeben [japanisch | deutsch | mix]: ")
        if user_input in {"japanisch", "deutsch", "mix"}:
            lang_mode = user_input

    file_paths = []
    file_paths.append("vocab_data/A1T1.xlsx")
    file_paths.append("vocab_data/Vok1.xlsx")
    file_paths.append("vocab_data/Vok2.xlsx")
    file_paths.append("vocab_data/Vok3.xlsx")
    file_paths.append("vocab_data/Vok4.xlsx")
    file_paths.append("vocab_data/Vok5.xlsx")
    file_paths.append("vocab_data/Vok6.xlsx")
    file_paths.append("vocab_data/Zaehlen.xlsx")
    file_paths.append("vocab_data/Verben.xlsx")
    file_paths.append("vocab_data/mehr_verben.xlsx")
    file_paths.append("vocab_data/noch_mehr_verben.xlsx")

    vocab_filtered = []

    print("Lade Vokabeln...")
    for fp in file_paths:
        df = pd.read_excel(fp)
        assert df.shape[1] == 3, "Too many columns in file."
        for idx, hiragana, kanji, deutsch in df.itertuples():

            if not isinstance(hiragana, str) or not isinstance(deutsch, str):
                continue
            if not isinstance(kanji, str):
                kanji = ""

            vocab_dict = {"hiragana": hiragana,
                          "kanji": kanji,
                          "deutsch": deutsch}
            vocab_filtered.append(vocab_dict)

    num_vocab = len(vocab_filtered)
    print(f"{num_vocab} Vokabeln geladen.\n")
    
    vocab_count = 0
    while True:
        vocab_dict = random.choice(vocab_filtered)
        print_vocab(vocab_dict, lang_mode)

        if vocab_count % 20 == 0 and vocab_count > 0:
            print_scorebreak(vocab_count)
        vocab_count += 1
    

if __name__ == "__main__":
    main()
