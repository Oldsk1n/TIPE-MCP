import pandas as pd

def concatenate_csv(file1, file2, output_file='output.csv', has_header=True):
    # Lire les fichiers CSV
    df1 = pd.read_csv(file1, header=0 if has_header else None)
    df2 = pd.read_csv(file2, header=0 if has_header else None)

    # Concaténer les fichiers
    concatenated_df = pd.concat([df1, df2], ignore_index=True)

    # Sauvegarde du résultat
    concatenated_df.to_csv(output_file, index=False, header=has_header)
    print(f"Fichier fusionné enregistré sous '{output_file}'.")


# %%

import csv

def text_to_csv(input_file, output_file="output.csv"):
    opened = open(input_file, 'r')
    text= opened.read()
    pairs = text.split(" | ")  # Séparation des paires

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["X", "Y"])  # Écriture de l'en-tête

        for pair in pairs:
            pair = pair.strip()  # Nettoyer les espaces
            if "," in pair:  # Vérifier que la paire est valide
                x, y = pair.split(",")
                writer.writerow([x.strip(), y.strip()])
            else:
                print(f"Erreur : donnée incorrecte détectée -> {pair}")

    print(f"Fichier CSV '{output_file}' généré avec succès.")

# %%

def text_to_csv_ajout(input_file, output_file="output.csv"):
    opened = open(input_file, 'r')
    text= opened.read()
    pairs = text.split(" | ")  # Séparation des paires

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["X", "Y"])  # Écriture de l'en-tête

        for pair in pairs:
            pair = pair.strip()  # Nettoyer les espaces
            if "," in pair:  # Vérifier que la paire est valide
                x, y = pair.split(",")
                x_val = float(x)
                x = str(x_val + 5190)
                writer.writerow([x.strip(), y.strip()])
            else:
                print(f"Erreur : donnée incorrecte détectée -> {pair}")

    print(f"Fichier CSV '{output_file}' généré avec succès.")

