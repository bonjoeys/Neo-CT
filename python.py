import sys
from bs4 import BeautifulSoup

# --- Configuration ---
# (Assurez-vous que ce fichier est votre 'index.html' actuel,
# celui qui contient déjà les données SimplyBook, ITEC et Nexius)
INPUT_FILE = 'index.html'
OUTPUT_FILE = 'index_modifie_FINAL_COMPLET.html' # Nom du fichier final
# ---------------------

def remplir_support_agendize_actency(soup):
    """Met à jour la ligne "Support" avec les données d'Agendize et Actency."""
    print(f"-> Remplissage 'Support' pour Agendize et Actency dans '{INPUT_FILE}'...")

    # 1. Trouver la ligne "Support"
    support_header_cell = soup.find('td', string=lambda t: t and 'Support (Portail, Niveaux, Langue)' in t)
    if not support_header_cell:
        print("   [ERREUR] Impossible de trouver la ligne 'Support (Portail, Niveaux, Langue)'.")
        print("   L'opération a échoué.")
        return False

    support_row = support_header_cell.find_parent('tr')
    if not support_row:
        print("   [ERREUR] Impossible de trouver le <tr> parent pour 'Support'.")
        print("   L'opération a échoué.")
        return False

    all_data_cells = support_row.find_all('td', class_='ao-tooltip-container')
    
    if len(all_data_cells) < 5:
        print(f"   [ERREUR] La structure de la ligne 'Support' est incorrecte (attendu 5 cellules, trouvé {len(all_data_cells)}).")
        print("   L'opération a échoué.")
        return False

    # 2. Remplir AGENDIZE (Index 1)
    try:
        agendize_cell = all_data_cells[1]
        visible_span = agendize_cell.find('span', style=True)
        tooltip_span = agendize_cell.find('span', class_='ao-tooltip-text')

        if "compléter" in visible_span.get_text():
            visible_span.string = 'Point fort (Multi-canal 8-18h, GTR 4h)'
            visible_span['style'] = "font-size: 0.9em; word-wrap: break-word; white-space: normal;"
            tooltip_span.string = 'Source: Réponse Agendize (Accompagnement)'
            print("   [OK] Remplissage d'Agendize.")
        else:
            print("   [INFO] La colonne Agendize semble déjà remplie.")
            
    except Exception as e:
        print(f"   [ERREUR] Impossible de remplir Agendize : {e}")
        return False

    # 3. Remplir ACTENCY (Index 4)
    try:
        actency_cell = all_data_cells[4]
        visible_span = actency_cell.find('span', style=True)
        tooltip_span = actency_cell.find('span', class_='ao-tooltip-text')

        if "compléter" in visible_span.get_text():
            visible_span.string = 'Bon (GLPI 9-18h, SLA contractuels)'
            visible_span['style'] = "font-size: 0.9em; word-wrap: break-word; white-space: normal;"
            tooltip_span.string = 'Source: Mémoire.pdf (Sect 4.3 - Support)'
            print("   [OK] Remplissage d'Actency.")
        else:
            print("   [INFO] La colonne Actency semble déjà remplie.")
            
    except Exception as e:
        print(f"   [ERREUR] Impossible de remplir Actency : {e}")
        return False

    return True


# --- Exécution du script ---
def main():
    print(f"Lecture du fichier '{INPUT_FILE}'...")
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"[ERREUR CRITIQUE] Le fichier '{INPUT_FILE}' n'a pas été trouvé.")
        print(f"Assurez-vous que '{INPUT_FILE}' (celui fourni) est dans le même dossier.")
        sys.exit(1)

    soup = BeautifulSoup(html_content, 'html.parser')

    # Appliquer la modification
    success = remplir_support_agendize_actency(soup)

    if not success:
        print("\nLe script s'est arrêté en raison d'une erreur.")
        sys.exit(1)

    # Écrire le nouveau fichier
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"\nModification terminée ! Le nouveau fichier a été sauvegardé sous : '{OUTPUT_FILE}'")
        print("Toutes les colonnes de la ligne 'Support' sont maintenant complétées.")
    except Exception as e:
        print(f"[ERREUR CRITIQUE] Impossible d'écrire le fichier de sortie : {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        import bs4
    except ImportError:
        print("[ERREUR] La bibliothèque 'BeautifulSoup' (bs4) est requise.")
        print("Veuillez l'installer en utilisant la commande : pip install beautifulsoup4")
        sys.exit(1)
        
    main()