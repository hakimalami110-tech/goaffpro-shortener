import os
import random
import string
import subprocess

# === CONFIG ===
DOCS_DIR = "docs"
OUTPUT_FILE = "22.txt"
REDIRECT_DELAY = 5
GITHUB_USER = "hakimalami110-tech"
GITHUB_REPO = "goaffpro-shortener"

# === Liens leurres possibles ===
FAKE_LINKS = [
    ("YouTube", "https://www.youtube.com"),
    ("Google", "https://www.google.com"),
    ("Facebook", "https://www.facebook.com"),
    ("Wikipedia", "https://www.wikipedia.org"),
    ("Twitter", "https://twitter.com")
]

# === FONCTIONS ===

def random_code(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_html(filename, target_url, fake_mode=False):
    os.makedirs(DOCS_DIR, exist_ok=True)
    selected_fakes = random.sample(FAKE_LINKS, k=min(3, len(FAKE_LINKS))) if fake_mode else []

    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="{REDIRECT_DELAY};url={target_url}">
    <title>Redirection...</title>
    <style>
        body {{ font-family: Arial, sans-serif; text-align: center; padding: 60px; background-color: #f7f7f7; }}
        h1 {{ color: #0b74de; }}
        a {{ text-decoration: none; color: #0b74de; }}
        .small {{ color: #777; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <h1>Redirection en cours...</h1>
    <p>Merci de patienter quelques secondes.</p>
"""

    if fake_mode and selected_fakes:
        html_content += "<div class='fake-links'><p>Quelques liens :</p>\n"
        for name, url in selected_fakes:
            html_content += f"<p><a href='{url}' target='_blank'>{name}</a></p>\n"
        html_content += "</div>\n"

    html_content += f"""
    <script>
        setTimeout(function() {{
            window.location.href = "{target_url}";
        }}, {REDIRECT_DELAY * 1000});
    </script>
</body>
</html>"""

    filepath = os.path.join(DOCS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)

    return filepath

def get_full_url(filename):
    return f"https://{GITHUB_USER}.github.io/{GITHUB_REPO}/{DOCS_DIR}/{filename}"

def update_index(files):
    with open("index.html", "w", encoding="utf-8") as index:
        index.write("<!DOCTYPE html><html lang='fr'><head><meta charset='UTF-8'><title>Mes Shortlinks</title></head><body>")
        index.write("<h1>Mes Shortlinks</h1><ul>")
        for file in files:
            index.write(f"<li><a href='{get_full_url(file)}' target='_blank'>{get_full_url(file)}</a></li>")
        index.write("</ul></body></html>")

def save_to_txt(shortlinks):
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        for link in shortlinks:
            f.write(link + "\n")

def delete_html_files():
    if not os.path.exists(DOCS_DIR):
        print("Aucun dossier docs trouvé.")
        return
    for file in os.listdir(DOCS_DIR):
        if file.endswith(".html"):
            os.remove(os.path.join(DOCS_DIR, file))
    print("✅ Tous les fichiers HTML ont été supprimés.")

def git_push_auto():
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-update shortlinks"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("🚀 Changements poussés automatiquement sur GitHub Pages.")
    except Exception as e:
        print(f"⚠️ Erreur lors du push automatique : {e}")

def main():
    print("=== MENU ===")
    print("1️⃣  Créer des shortlinks simples")
    print("2️⃣  Créer des shortlinks avec liens leurres")
    print("3️⃣  Supprimer tous les fichiers HTML")
    choice = input("Choisis une option (1-3) : ")

    if choice == "3":
        delete_html_files()
        git_push_auto()
        return

    if not os.path.exists("links.txt"):
        print("⚠️  Fichier links.txt introuvable.")
        return

    with open("links.txt", "r", encoding="utf-8") as f:
        links = [line.strip() for line in f if line.strip()]

    if not links:
        print("⚠️  Aucun lien trouvé dans links.txt")
        return

    nb = int(input("Combien de shortlinks veux-tu générer ? "))
    nb = min(nb, len(links))

    shortlinks = []
    for i in range(nb):
        target_url = links[i]
        filename = random_code() + ".html"
        create_html(filename, target_url, fake_mode=(choice == "2"))
        full_url = get_full_url(filename)
        shortlinks.append(full_url)
        print(f"✅ Lien créé : {full_url}")

    update_index([os.path.basename(url.split('/')[-1]) for url in shortlinks])
    save_to_txt(shortlinks)
    git_push_auto()

    print(f"\n✅ {len(shortlinks)} shortlinks créés et enregistrés dans {OUTPUT_FILE}.")

if __name__ == "__main__":
    main()
