import random

# -------------------------------
# INFORMACJE WSTĘPNE O PROGRAMIE
# -------------------------------
# Program ten służy do tworzenia sztucznej sekwencji DNA zawierającej tylko nukleotydy A, C, G oraz T.
# Użytkownik podaje żądaną długość sekwencji, identyfikator, opis oraz swoje imię.
# Imię to jest wstawiane losowo do środka sekwencji, ale nie ma wpływu na statystyki nukleotydów.
# Dane są zapisywane w pliku FASTA zgodnie z konwencją bioinformatyczną.
# Może być używany do nauki podstaw analizy sekwencji genetycznych i formatów biologicznych.

# --------------------------------------
# FUNKCJA: tworzenie losowej sekwencji DNA
# --------------------------------------
def build_sequence(length):
    return ''.join(random.choice("ACGT") for _ in range(length))  # Składanie ciągu z losowych liter A, C, G, T

# --------------------------------------
# FUNKCJA: analizuje skład nukleotydowy
# --------------------------------------
def dna_statistics(seq):
    total = len(seq)  # Całkowita liczba znaków w sekwencji
    count_map = {nuc: seq.count(nuc) for nuc in "ACGT"}  # Liczba wystąpień każdego nukleotydu
    percentages = {nuc: round((count / total) * 100, 1) for nuc, count in count_map.items()}  # Zawartość procentowa
    c_g = count_map['C'] + count_map['G']  # Liczba nukleotydów C i G
    a_t = count_map['A'] + count_map['T']  # Liczba nukleotydów A i T
    cg_vs_at = round((c_g / a_t) * 100, 1) if a_t > 0 else float('inf')  # Stosunek CG/AT, bez dzielenia przez zero
    return percentages, cg_vs_at

# --------------------------------------
# FUNKCJA: dodaje imię w losowym miejscu
# --------------------------------------
# ORIGINAL:
# def insert_name(sequence, name):
#     pos = random.randint(0, len(sequence))
#     return sequence[:pos] + name + sequence[pos:]
# MODIFIED (dodanie pozycji jako wartości zwrotnej, przydatne do późniejszego raportu):
def insert_name(sequence, name):
    position = random.randint(0, len(sequence))  # Wybranie losowej pozycji w sekwencji
    updated = sequence[:position] + name + sequence[position:]  # Wstawienie imienia
    return updated, position  # Zwracamy również pozycję

# --------------------------------------
# FUNKCJA: zapisuje dane do pliku FASTA
# --------------------------------------
# ORIGINAL:
# def save_to_fasta(filename, header, sequence_with_name):
#     with open(filename, 'w') as f:
#         f.write(f">{header}\n{sequence_with_name}\n")
# MODIFIED (zastosowanie łamania linii co 60 znaków, zgodnie z praktyką FASTA):
def save_to_fasta(file, header, full_sequence):
    with open(file, 'w') as fasta:
        fasta.write(f">{header}\n")
        for i in range(0, len(full_sequence), 60):  # Linia o maksymalnej długości 60 znaków
            fasta.write(full_sequence[i:i+60] + "\n")

# --------------------------------------
# GŁÓWNA FUNKCJA PROGRAMU – LOGIKA
# --------------------------------------
def main():
    # ---------------------------------
    # Pobranie danych wejściowych od użytkownika
    # ---------------------------------

    # ORIGINAL:
    # length = int(input("Podaj długość sekwencji: "))
    # MODIFIED (dodanie pętli do walidacji typu i wartości długości):
    while True:
        try:
            length = int(input("Podaj długość sekwencji: "))
            if length < 1:
                print("Wprowadź liczbę większą od zera.")
                continue
            break
        except ValueError:
            print("To nie jest liczba całkowita!")

    # ORIGINAL:
    # seq_id = input("Podaj ID sekwencji: ")
    # MODIFIED (dodanie .strip() usuwa zbędne spacje – poprawa estetyki):
    seq_id = input("Podaj ID sekwencji: ").strip()

    # ORIGINAL:
    # description = input("Podaj opis sekwencji: ")
    # MODIFIED (analogicznie dodanie .strip() dla czystości danych):
    description = input("Podaj opis sekwencji: ").strip()

    # ORIGINAL:
    # name = input("Podaj imię: ")
    # MODIFIED (usuwamy spacje na końcach i sprawdzamy, czy imię nie jest puste):
    while True:
        name = input("Podaj imię: ").strip()
        if name:
            break
        print("Imię nie może być puste.")

    # ---------------------------------
    # Generowanie danych i obliczenia
    # ---------------------------------
    original_seq = build_sequence(length)  # Bazowa sekwencja DNA
    stats, ratio = dna_statistics(original_seq)  # Obliczenie udziału % i stosunku CG/AT
    seq_with_name, name_pos = insert_name(original_seq, name)  # Dodanie imienia do sekwencji

    # ---------------------------------
    # Zapisanie danych do pliku w formacie FASTA
    # ---------------------------------
    fasta_name = f"{seq_id}.fasta"
    fasta_header = f"{seq_id} {description}"
    save_to_fasta(fasta_name, fasta_header, seq_with_name)

    # ---------------------------------
    # Wyświetlenie wyników dla użytkownika
    # ---------------------------------
    print(f"\nPlik {fasta_name} został utworzony.")
    print(f"Imię wstawiono na pozycji: {name_pos + 1} (licząc od 1)")
    print("\nStatystyki sekwencji (bez imienia):")
    for base in "ACGT":
        print(f"{base}: {stats[base]}%")
    print(f"Stosunek CG/AT: {ratio}%")

# --------------------------------------
# Uruchomienie programu głównego
# --------------------------------------
if __name__ == "__main__":
    main()
