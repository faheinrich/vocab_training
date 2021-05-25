import numpy as np
import pandas as pd
import random
import sys
import glob



# printed je nach Flags eine zufällige Vokabel aus und wartet auf Enter
def print_vocab(current_vocab, lang_mode):

    if lang_mode == "japanisch":
        print(current_vocab[0], end="")
        input("")
        print(current_vocab[2], "\n")
    elif lang_mode == "deutsch":
        print(current_vocab[2], end="")
        input("")
        print(current_vocab[0], "\n")
    elif lang_mode == "mix": 
        if(bool(random.getrandbits(1))):
            print(current_vocab[0], end="")
            input("")
            print(current_vocab[2], "\n")
        else:
            print(current_vocab[2], end="")
            input("")
            print(current_vocab[0], "\n")



def main():
    try:
        if sys.argv[1] in {"japanisch", "deutsch", "mix"}:
            lang_mode = sys.argv[1]
    except:
        language_given = False
        while not language_given:
            lang_mode = input("Sprache eingeben [japanisch | deutsch | mix]: ")
            if lang_mode in {"japanisch", "deutsch", "mix"}:
                language_given = True
        
    # entweder alle Dateien im Ordner suchen oder eigene Auswahl benutzen
    all_files = False
    nur_verben = False

    if all_files:
        # alle Dateien in ./vocab_data suchen
        file_paths = glob.glob("vocab_data/*")
    else:
        # eigene Auswahl an Dateien
        file_paths = []

        file_paths.append("vocab_data/A1T1.xlsm")

        file_paths.append("vocab_data/Vok1.xlsx")
        file_paths.append("vocab_data/Vok2.xlsx")
        file_paths.append("vocab_data/Vok3.xlsx")
        file_paths.append("vocab_data/Vok4.xlsx")
        file_paths.append("vocab_data/Vok5.xlsx")
        file_paths.append("vocab_data/Vok6.xlsx")
        
        file_paths.append("vocab_data/Zaehlen.xlsx")
        file_paths.append("vocab_data/Verben.xlsx")
        
        file_paths.append("vocab_data/mehr_verben.xlsx")


    vocab_filtered = []

    print("Lade Vokabeln,")
    # alle Dateien in file_paths einlesen
    for fp in file_paths:
        # print(fp)
        # Excel Datei als pandas-dataframe einlesen
        df = pd.read_excel(fp)

        # dataframe zu np array
        vocab_raw = df.to_numpy()

        # alles aussortieren, was nicht alle werte der vokabeln ausfuellt
        for c, i in enumerate(vocab_raw):
            # gibt fehler wenn ein feld leer ist, landet somit im except Fall
            try:
                if(np.isnan(np.float(i[2]))):
                    0
            except:
                vocab_filtered.append(i)

    num_vocab = len(vocab_filtered)
    print(num_vocab, "Vokabeln geladen.\n")

    batch_size = 20
    
    for i in range(1, 1000000000):

        for index in np.random.choice(num_vocab, batch_size):
            print_vocab(vocab_filtered[index], lang_mode)	

        
        br = '============'
        c = i * batch_size
        mid = '='*(len(str(c))+2)
        print(f"\n{br}{mid}{br}\n{br} {c} {br}\n{br}{mid}{br}\n\n")

    

if __name__ == "__main__":
    main()