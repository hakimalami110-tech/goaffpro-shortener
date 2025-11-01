import os
import random
import string
import subprocess

# ===== CONFIG =====
DOCS_DIR = "docs"
OUTPUT_FILE = "22.txt"
REDIRECT_DELAY = 8  # ← 8 secondes
GITHUB_USER = "hakimalami110-tech"
GITHUB_REPO = "goaffpro-shortener"

# ===== Liens leurres =====
FAKE_LINKS = [
    ("YouTube", "https://www.youtube.com"),
    ("Google", "https://www.google.com"),
    ("Gmail", "https://mail.google.com"),
    ("Wikipedia", "https://www.wikipedia.org"),
    ("Facebook", "https://www.facebook.com"),
    ("Twitter", "https://twitter.com")
]

def random_code(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_html(filename, target_url, fake_mode=False):
    os.makedirs(DOCS_DIR, exist_ok=True)
    selected_fakes = random.sample(FAKE_LINKS, k=min(3, len(FAKE_LINKS))) if fake_mode else []
    leurre_url = selected_fakes[0][1] if selected_fakes else "https://mail.google.com"

    # === HTML + JS (échappement des accolades avec {{}} → {{\\}} ===
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="robots" content="noindex">
  <title>Chargement…</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    :root{{--primary:#0b74de;--muted:#666;--bg:#f7f7f7}}
    body{{font-family:Inter,Arial,Helvetica,sans-serif;background:var(--bg);margin:0;display:flex;align-items:center;justify-content:center;height:100vh}}
    .card{{width:92%;max-width:720px;background:#fff;border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,0.08);padding:28px;text-align:center}}
    h1{{margin:0 0 10px 0;font-size:22px;color:var(--primary)}}
    p.desc{{color:var(--muted);margin:6px 0 18px 0}}
    .buttons{{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin:10px 0 18px 0}}
    .btn{{display:inline-block;padding:12px 18px;border-radius:10px;background:#fff;border:2px solid #eee;min-width:160px;text-align:center;text-decoration:none;color:#222;font-weight:600;box-shadow:0 6px 18px rgba(11,116,222,0.08);transition:transform .12s,box-shadow .12s}}
    .btn:hover{{transform:translateY(-4px);box-shadow:0 12px 28px rgba(11,116,222,0.12)}}
    .btn.primary{{background:var(--primary);color:#fff;border:0}}
    .small{{color:var(--muted);font-size:0.9rem;margin-top:12px}}
    .count{{font-weight:700;color:var(--primary)}}
    .optin{{margin-top:20px}}
    .btn-action{{padding:10px 20px;margin:5px;border:none;border-radius:8px;color:#fff;cursor:pointer;font-weight:600}}
    .btn-continue{{background:#1a73e8}}
    .btn-cancel{{background:#d93025}}
    @media (max-width:480px){{.btn{{min-width:120px;padding:10px 12px}}}}
  </style>
</head>
<body>
  <div class="card" role="main" aria-live="polite">
    <h1>Un instant…</h1>
    <p class="desc">Nous préparons la page — quelques liens utiles ci‑dessous :</p>
    <div class="buttons">
"""

    if selected_fakes:
        for i, (name, url) in enumerate(selected_fakes, start=1):
            cls = "btn primary" if i == 1 else "btn"
            html += f'      <a class="{cls}" href="{url}" target="_blank" rel="noopener noreferrer">{name}</a>\n'
    else:
        html += '      <a class="btn primary" href="#" onclick="return false;">Continuer</a>\n'

    html += f"""    </div>
    <p class="small">Redirection automatique dans <span class="count" id="count">{REDIRECT_DELAY}</span> secondes.</p>

    <div class="optin">
      <button class="btn-action btn-continue" id="continueBtn">Continuer maintenant</button>
      <button class="btn-action btn-cancel" id="cancelBtn">Annuler</button>
    </div>
  </div>

  <script>
    const finalUrl = "{target_url}";
    const leurre = "{leurre_url}";
    let timeLeft = {REDIRECT_DELAY};
    const countEl = document.getElementById('count');
    const continueBtn = document.getElementById('continueBtn');
    const cancelBtn = document.getElementById('cancelBtn');

    // === LEURRE EN ARRIÈRE-PLAN (INVISIBLE) ===
    const fakeTab = window.open(leurre, '_blank');
    if (fakeTab) fakeTab.blur();
    window.focus();

    const iframe = document.createElement('iframe');
    iframe.src = leurre;
    iframe.style.position = 'absolute';
    iframe.style.width = '1px';
    iframe.style.height = '1px';
    iframe.style.opacity = '0';
    iframe.style.pointerEvents = 'none';
    iframe.style.left = '-9999px';
    document.body.appendChild(iframe);

    // === COMPTE À REBOURS ===
    const timer = setInterval(() => {{
      timeLeft--;
      countEl.textContent = timeLeft;
      if (timeLeft <= 0) {{
        clearInterval(timer);
        redirectNow();
      }}
    }}, 1000);

    function redirectNow() {{
      if (fakeTab) fakeTab.close();
      window.location.href = finalUrl;
    }}

    continueBtn.onclick = () => {{ clearInterval(timer); redirectNow(); }};
    cancelBtn.onclick = () => {{
      clearInterval(timer);
      document.body.innerHTML = '<div class="card"><h1>Annulé.</h1><p>Vous pouvez fermer cette page.</p></div>';
      if (fakeTab) fakeTab.close();
    }};

    // === Fallback si JS bloqué ===
    setTimeout(() => {{ window.location.href = finalUrl; }}, {REDIRECT_DELAY}000);
  </script>
</body>
</html>
"""

    path = os.path.join(DOCS_DIR, filename)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    return path

# === FONCTIONS INCHANGÉES ===
def get_full_url(filename):
    return f"https://{GITHUB_USER}.github.io/{GITHUB_REPO}/{filename}"

def update_index(files):
    index_path = os.path.join(DOCS_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as index:
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
    removed = 0
    for file in os.listdir(DOCS_DIR):
        if file.endswith(".html"):
            os.remove(os.path.join(DOCS_DIR, file))
            removed += 1
    print(f"{removed} fichiers HTML supprimés.")

def git_push_auto():
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-update shortlinks"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("Changements poussés sur GitHub Pages.")
    except Exception as e:
        print(f"Erreur push : {e}")

# ===== MENU =====
def main():
    print("=== MENU ===")
    print("1) Shortlinks simples")
    print("2) Avec leurres visibles")
    print("3) Supprimer HTML")
    choice = input("Choix (1-3) : ").strip()

    if choice == "3":
        delete_html_files()
        git_push_auto()
        return

    if not os.path.exists("links.txt"):
        print("links.txt manquant.")
        return

    with open("links.txt", "r", encoding="utf-8") as f:
        links = [line.strip() for line in f if line.strip()]

    if not links:
        print("Aucun lien dans links.txt")
        return

    nb = int(input("Combien de shortlinks ? "))
    nb = min(nb, len(links))

    shortlinks = []
    for i in range(nb):
        target_url = links[i]
        filename = random_code() + ".html"
        create_html(filename, target_url, fake_mode=(choice == "2"))
        full_url = get_full_url(filename)
        shortlinks.append(full_url)
        print(f"Créé : {full_url}")

    update_index([os.path.basename(url.split('/')[-1]) for url in shortlinks])
    save_to_txt(shortlinks)
    git_push_auto()
    print(f"\n{len(shortlinks)} shortlinks créés → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()