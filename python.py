import os
from bs4 import BeautifulSoup

FILE_INDEX = "index.html"
FILE_PILOTE = "pilote.html"

def make_seamless():
    # --- 1. MODIFICATION DE PILOTE.HTML (L'EMETTEUR) ---
    if os.path.exists(FILE_PILOTE):
        print(f"🔧 Traitement de {FILE_PILOTE}...")
        with open(FILE_PILOTE, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        # Script qui calcule la hauteur et l'envoie au parent
        js_sender = """
        <script>
            // Fonction pour envoyer la hauteur au parent
            function sendHeightToParent() {
                const height = document.documentElement.scrollHeight;
                window.parent.postMessage({ type: 'resize-iframe', height: height }, '*');
            }

            // On écoute tout ce qui peut changer la taille de la page
            window.addEventListener('load', sendHeightToParent);
            window.addEventListener('resize', sendHeightToParent);
            
            // Observer les changements dans le DOM (ex: ouverture d'un accordéon)
            const observer = new MutationObserver(sendHeightToParent);
            observer.observe(document.body, { attributes: true, childList: true, subtree: true });
            
            // Envoi périodique par sécurité (toutes les secondes)
            setInterval(sendHeightToParent, 1000);
        </script>
        """
        
        # Vérifier si le script existe déjà pour ne pas le dupliquer
        if "sendHeightToParent" not in str(soup):
            soup_js = BeautifulSoup(js_sender, "html.parser")
            if soup.body:
                soup.body.append(soup_js)
                print("✅ Script d'envoi de hauteur ajouté à pilote.html")
                
                with open(FILE_PILOTE, "w", encoding="utf-8") as f:
                    f.write(str(soup.prettify()))
        else:
            print("ℹ️ pilote.html a déjà le script.")

    else:
        print(f"❌ Erreur : {FILE_PILOTE} introuvable.")

    # --- 2. MODIFICATION DE INDEX.HTML (LE RECEPTEUR) ---
    if os.path.exists(FILE_INDEX):
        print(f"🔧 Traitement de {FILE_INDEX}...")
        with open(FILE_INDEX, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        # 1. Modifier l'iframe pour enlever l'ascenseur et la hauteur fixe
        iframe = soup.find("iframe", src="pilote.html")
        if iframe:
            # On change le style pour retirer la hauteur fixe (85vh) et permettre l'extension
            iframe['style'] = "width: 100%; min-height: 100vh; border: none; overflow: hidden;"
            iframe['scrolling'] = "no" # Désactive l'ascenseur natif de l'iframe
            print("✅ Iframe ajustée (scrolling='no', hauteur dynamique).")

        # 2. Ajouter le script de réception
        js_receiver = """
        <script>
            // Écoute les messages venant de l'iframe pilote
            window.addEventListener('message', function(e) {
                if (e.data && e.data.type === 'resize-iframe') {
                    const iframe = document.querySelector('iframe[src="pilote.html"]');
                    if (iframe) {
                        iframe.style.height = e.data.height + 'px';
                    }
                }
            });
        </script>
        """

        if "resize-iframe" not in str(soup):
            soup_js = BeautifulSoup(js_receiver, "html.parser")
            if soup.body:
                soup.body.append(soup_js)
                print("✅ Script de réception de hauteur ajouté à index.html")

            with open(FILE_INDEX, "w", encoding="utf-8") as f:
                f.write(str(soup.prettify()))
        else:
            print("ℹ️ index.html a déjà le script.")

    else:
        print(f"❌ Erreur : {FILE_INDEX} introuvable.")

if __name__ == "__main__":
    make_seamless()
