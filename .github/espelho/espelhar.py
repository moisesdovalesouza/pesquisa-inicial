"""Copia a Pesquisa Inicial avulsa publicada pelo Termo Inicial para este repositório (GitHub Pages).

O Termo gera os arquivos a cada build em https://termoinicial.vercel.app/avulsa/pesquisa-inicial/
e lista tudo em arquivos.json. Aqui só se baixa quando a versão muda; arquivos que saíram da lista são apagados.
"""
import json, os, sys, urllib.request

BASE = "https://termoinicial.vercel.app/"
LISTA = BASE + "avulsa/pesquisa-inicial/arquivos.json"
PRESERVAR = {".github", ".git"}

def baixar(url):
    req = urllib.request.Request(url, headers={"User-Agent": "espelho-pesquisa-inicial", "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

lista = json.loads(baixar(LISTA))
atual = None
if os.path.exists("versao.json"):
    try: atual = json.load(open("versao.json", encoding="utf-8")).get("versao")
    except Exception: atual = None
if atual == lista["versao"] and "--forcar" not in sys.argv:
    print(f"Já está na versão {atual}.")
    sys.exit(0)

destinos = set()
for a in lista["arquivos"]:
    dados = baixar(BASE + a["origem"])
    os.makedirs(os.path.dirname(a["destino"]) or ".", exist_ok=True)
    with open(a["destino"], "wb") as f: f.write(dados)
    destinos.add(os.path.normpath(a["destino"]))

for raiz, pastas, arquivos in os.walk(".", topdown=True):
    pastas[:] = [p for p in pastas if not (raiz == "." and p in PRESERVAR)]
    for n in arquivos:
        c = os.path.normpath(os.path.join(raiz, n))
        if c not in destinos: os.remove(c); print("removido:", c)

print(f"Atualizado de {atual} para {lista['versao']} ({len(destinos)} arquivos).")
