# -*- coding: utf-8 -*-
"""Iz research/konkurenca-2026-09.json zgradi DEFAULT_DATA v konkurenca.html (verzija 4).

Ohrani ročno kurirane VVV vnose (študije primerov, portfolio, CRM) in obstoječe vnose konkurentov
iz prejšnje verzije; doda vse, kar je raziskava prinesla. Zaženi iz korena repa:
    python research/build-liga-data.py
"""
import json, re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HTML = ROOT / "konkurenca.html"
JSONP = ROOT / "research" / "konkurenca-2026-09.json"
DATUM = "2026-09-22"
VIR_R = "research/konkurenca-2026-09.json"

D = json.loads(JSONP.read_text(encoding="utf-8"))
A = D["agencije"]
html = HTML.read_text(encoding="utf-8")

# ---------------------------------------------------------------- pomožno
def js(s):
    return json.dumps(s, ensure_ascii=False)

def norm(s):
    s = s.lower()
    for a, b in (("š", "s"), ("č", "c"), ("ž", "z"), ("ö", "o"), ("é", "e"), ("’", "'")):
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]", "", s)[:8]

BIG = ["samsung", "telekom", "triglav", "nlb", "gorenje", "mercator", "lidl", "spar", "red bull", "argeta", "poli", "podravka",
       "nivea", "lesnina", "btc", "wolt", "terme čatež", "deichmann", "mömax", "momax", "hisense", "eucerin", "ljubljanske mlekarne",
       "mladinska knjiga", "intersport", "l'étape", "letape", "merkur", "gls", "krups", "rowenta", "tefal", "dormeo", "afrodita",
       "curaprox", "t-2", "cineplexx", "hse", "gzs", "gospodarska zbornica", "mestna občina", "filharmonija", "varnost prometa",
       "sport vision", "sava resort", "mimovrste", "borotalco", "turizem ljubljana", "visit ljubljana", "stop shop", "adria",
       "pošta slovenije", "ljubljanska borza", "eventim", "zavarovalnica"]
MID = ["proteini", "leanpay", "fibran", "bravia", "vitapur", "golden tree", "bird buddy", "speech blubs", "lelosi", "lux-factor",
       "luxfactor", "polleo", "rimske terme", "equa", "štartaj", "terme snovik", "škerjanc", "visit pomurje", "avant2go", "hs plus",
       "hs+", "tedx", "biotehniška", "univerz", "kingsbox", "treecelet", "drinkopoly", "mjob", "naturavit", "malinca", "spinalis",
       "amour parfums", "expano", "akademija uspeha", "adizes", "avtodomar", "unikatoy", "preis", "actinia", "euroton", "nest",
       "sladoled niki", "kavarna niki", "byrokko", "5ka", "založba", "telemach", "a1", "autobroker", "homeso", "tasty dose",
       "meetminded", "fitocanin", "esstera", "artisana", "bach", "kriptomat", "dines", "float center", "e-študentski", "emporium",
       "stadionshop", "nk domžale", "nk triglav", "umag", "sport media focus", "špas", "diplomska", "trgofina", "filaplast", "reborn",
       "kreja", "e-hrana", "art tehnika", "moji mediji", "agrinextgen", "sivili", "orsa", "fern"]

def velikost(name):
    n = name.lower()
    if any(b in n for b in BIG): return "big", True
    if any(m in n for m in MID): return "mid", False
    return "micro", False

# ---------------------------------------------------------------- 1. agencije
IME = {"vvv": "VVV Digital", "tiktokspace": "TikTok SPACE", "vividista": "Vividista", "envision": "Envision Collective",
       "tiktokerija": "Tiktokerija", "apmarketing": "A.P. Marketing", "ziya": "Ziya Agency", "createable": "Createable",
       "katapult": "Katapult Media", "watt": "Outpace (prej We Are TikTok / WATT)", "buzztik": "BuzzTik", "3amedia": "3A Media", "xod": "XOD Agency"}
WEB = {"vvv": "vvv-digital.com", "tiktokspace": "tiktok-space.si", "vividista": "vividista.si", "envision": "envisioncollective.si",
       "tiktokerija": "tiktokerija.com", "apmarketing": "ap-marketing.si", "ziya": "ziya.agency (domena od 2025 v tujih rokah)",
       "createable": "createable.si", "katapult": "katapult.si/storitve/katapult-media", "watt": "outpaceagency.com",
       "buzztik": "buzztik.com", "3amedia": "3a-media.com", "xod": "xodagency.com"}
OPOMBA = {
    "vvv": "Kratki videi, vodenje profilov, paid, splet. Dir. Andraž Mrzlikar. Ekipa 12 (LinkedIn).",
    "tiktokspace": "Butična SMM agencija (TikTok, IG, FB). Nosilec APPOLO PRO d.o.o. (reg. sedež Brežice, posl. Celovška 69C). Edina znana oseba Rimma Arshinova, zaposlitev po LinkedInu končana jun. 2026; IG/TT računa agencije ni.",
    "vividista": "Agencija za Gen Z. s.p. vpisan 1. 6. 2026, profili skoraj prazni (IG 4, TT 3 sledilcev).",
    "envision": "Zunanja ekipa za družbena omrežja, Murska Sobota. Ekipa 5 (stran /ekipa). Google 5,0 (10 mnenj).",
    "tiktokerija": "TikTok in Reels, storytelling. Ust. Rebeka Tomc, ekipa 3–4. Največji doseg na TT (povp. 6,9k ogledov/video), objave ~2/mesec.",
    "apmarketing": "Kratki videi, UGC oglasi. Model influencer + agencija (Andrej Pavličević TT 112k, Gaja Hribernik TT 90k). IG neaktiven od apr. 2026; AJPES: poročilo samo za 2025.",
    "ziya": "Butična TikTok agencija, Ljubljana, Founder Tia Uršič (maj 2023 – mar. 2025). UGASNILA 2025; domena ziya.agency je danes jordansko AI podjetje. Pravne osebe ni bilo.",
    "createable": "Video in UGC agencija (do 2024 TikTokable). Nosilec BondBeyond d.o.o. Ekipa 8–10. Objavlja dnevno, a prodaja lasten tečaj; Google 5,0 (14).",
    "katapult": "Enota pospeševalnika Katapult (Trbovlje). Ekipa 2–4. IG mrtev od sredine 2024. Finance = celotna družba Katapult d.o.o. (2024–25 v izgubi).",
    "watt": "Preimenovan v Outpace (performance/UGC oglasi za tuje trge, Kaching d.o.o.). Slovenske korpo stranke iz 2023–25 niso več potrjene. Prihodki 2025 (3,7 mio €) so večinoma pretočni oglasni proračuni; 2022 podjetje praktično neaktivno.",
    "buzztik": "Platforma mikro-ustvarjalcev + SMM (CLUEKIT d.o.o., Novo mesto, Irena Žagar). Finance = celo podjetje (3 produkti). TT 5,3k, a od jun. 2026 tiho.",
    "3amedia": "Lev Glumac s.p. (Domžale, vpis maj 2025), ekipa 3 (19 let). Brez agencijskih IG/TT računov in brez financ. Reference: Borut Pahor, Vitapur, AVP.",
    "xod": "Video in foto produkcija dogodkov (XOD Group d.o.o., vpis jul. 2025, prej skupina od 2023). Ekipa 14. 5 od 12 projektov podizvajalstvo za Herman & partnerji. Edina z živim LinkedInom.",
}
STRANK = {"vvv": "100+ (LinkedIn, 4. obletnica, feb. 2026); 48 znamk (about-us)", "tiktokerija": "50+ znamk (tiktokerija.com), 30+ projektov (arhiv 2026)",
          "watt": "30+ aktivnih naročnikov, 15 FTE, 100k € MRR (LinkedIn oglas 2025)", "buzztik": "140+ znamk, 2.500+ ustvarjalcev (buzztik.com)",
          "createable": "80+ znamk, 50 mio ogledov (createable.si)", "envision": "35+ naročnikov, 10M+ ogledov (envisioncollective.si)",
          "tiktokspace": "", "vividista": "", "apmarketing": "5 let+ ustvarjanja (ap-marketing.si)", "ziya": "", "katapult": "", "3amedia": "", "xod": ""}

EXCL = {("3amedia", "ig")}  # osebni profil direktorja (@leoglumac), ne agencije; v ligo dosega ne sodi

def handle(k, a, ch):
    s = a["sledilci"][ch]
    h = s.get("handle")
    if not h or s.get("n") is None or (k, ch) in EXCL: return ""
    return h.replace("company/", "").split(" ")[0]

agencije = []
for k, a in A.items():
    p = a["pravna"]
    kraj = p["naslov"].split(" (")[0].split(",")[-1].strip() if p.get("naslov") else ""
    kraj = re.sub(r"^\d{4}\s+", "", kraj)
    deli = [x for x in (kraj, f"ust. {p['ustanovitev'][:10]}" if p.get("ustanovitev") else "") if x]
    pr = (p.get("ime") or "brez pravne osebe") + (f" ({'; '.join(deli)})" if deli else "")
    if k == "ziya": pr = "brez pravne osebe (Ljubljana; Founder Tia Uršič, maj 2023 – mar. 2025)"
    row = {"id": k, "ime": IME[k], "pravna": pr, "opomba": OPOMBA[k], "ig": handle(k, a, "ig"), "tt": handle(k, a, "tt"), "li": handle(k, a, "li"), "web": WEB[k], "strank": STRANK[k]}
    agencije.append(row)

# ---------------------------------------------------------------- 2. snapshot
vred = {}
for k, a in A.items():
    s = a["sledilci"]; v = {}
    for ch in ("ig", "tt", "li"):
        if s[ch].get("n") is not None and (k, ch) not in EXCL: v[ch] = s[ch]["n"]
    if s["google"].get("n") is not None: v["gr"] = s["google"]["n"]
    if v: vred[k] = v
snapshot = {"vir": "Neposredni odčitek 21.–22. 9. 2026 (IG meta opis, TikTok JSON, LinkedIn prijavljen pogled, Google Maps); " + VIR_R, "vrednosti": vred}

# ---------------------------------------------------------------- 3. finance
finance = {}
for k, a in A.items():
    if not a["finance"]: continue
    finance[k] = {}
    for y, f in sorted(a["finance"].items()):
        vir = f["vir"]
        src = "AJPES JOLP" if "AJPES JOLP" in vir else ("companywall.si / ebonitete.si (AJPES)" if "companywall" in vir or "ebonitete" in vir else vir[:60])
        finance[k][y] = {"prihodki": f["prihodki"], "dobicek": f["dobicek"], "zaposleni": f["zaposleni"], "vir": src + ", " + DATUM}

# ---------------------------------------------------------------- 4. nagrade
m_def = re.search(r"  nagrade: \[\n(.*?)\n  \],", html, re.S)
old_nagrade = m_def.group(1)
old_vir = set(re.findall(r"vir: '([^']+)'", old_nagrade))
SKIP = ("LinkedIn zaposlitveni oglas", "Lastna navedba", "razpis za zaposlitev", "Pridružitev")
nag_lines = []
n = 6
for k, a in A.items():
    for o in a["omembe"]:
        vir = (o.get("vir") or "").split(" (")[0].split(" ;")[0]
        if not vir or vir in old_vir or any(s in o["naziv"] for s in SKIP): continue
        old_vir.add(vir); n += 1
        nag_lines.append(f"    {{ id: 'n{n}', agId: {js(k)}, datum: {js(o.get('datum') or DATUM)}, naziv: {js(o['naziv'][:220])}, tocke: 1, vir: {js(vir)} }}")
nagrade_js = old_nagrade + (",\n" + ",\n".join(nag_lines) if nag_lines else "")

# ---------------------------------------------------------------- 5. projekti
m_seed = re.search(r"function seedProjekti\(\) \{\n(.*?)\n  return P;\n\}", html, re.S)
seed_old = m_seed.group(1)
i_tt = seed_old.index("  // --- Tiktokerija (javno)")
vvv_block = seed_old[:i_tt]
comp_block = seed_old[i_tt:]

def existing_names(block, ag=None):
    names = set()
    pat = r"add\('%s', '([^']+)'" % (ag or r"[a-z0-9]+")
    for s in re.findall(pat, block): names.add(norm(s))
    if ag == "vvv":
        for s in re.findall(r"\['([^']+)', '\d{4}-", block): names.add(norm(s))
        for arr in re.findall(r"\n  \[(.*?)\]\n\s*\.forEach", block, re.S):
            for s in re.findall(r"'([^']+)'|\"([^\"]+)\"", arr): names.add(norm(s[0] or s[1]))
    return names

lines = []
def add_line(k, e, konec=None, javno=True):
    v, z = velikost(e["ime"])
    opis = (e.get("opis") or "")[:160]
    if e.get("zadnja_omemba"): opis += f" [zadnja omemba {e['zadnja_omemba']}]"
    vir = (e.get("vir") or "").split(" ; ")[0]
    o = f"v: {js(v)}"
    if z: o += ", z: true"
    if not javno: o += ", javno: false"
    o += f", opis: {js(opis.strip())}, vir: {js(vir)}"
    if konec: o += f", konec: {js(konec)}"
    lines.append(f"  add({js(k)}, {js(e['ime'][:70])}, {js((e.get('datum') or DATUM)[:10])}, {{ {o} }});")

# VVV: javne reference s spletne strani, ki jih še ni
have = existing_names(vvv_block, "vvv")
lines.append("  // --- VVV: javne reference na vvv-digital.com (WP REST API, 22. 9. 2026); datum = objava zapisa")
for e in A["vvv"]["stranke"]:
    if norm(e["ime"]) in have: continue
    have.add(norm(e["ime"]))
    konec = None
    m = re.search(r"–\s*(?:(\w+)\s+)?(\d{4})\b(?!–)", e.get("opis") or "")
    add_line("vvv", e, konec)

# konkurenti: obstoječi vnosi ostanejo, dodamo nove
KONEC = {"ziya": "2025-03-31"}
HIST_WATT = {"afrodita", "dines", "float center", "kriptomat", "nivea", "podravka", "vigo shop", "vitapur", "estetika fabjan", "wolt", "terme čatež"}
for k, a in A.items():
    if k == "vvv": continue
    have = existing_names(comp_block, k)
    lines.append(f"  // --- {IME[k]} ({VIR_R}, {DATUM})")
    for e in a["stranke"]:
        if norm(e["ime"]) in have: continue
        have.add(norm(e["ime"]))
        konec = KONEC.get(k)
        if k == "watt" and any(h in e["ime"].lower() for h in HIST_WATT): konec = "2025-12-31"
        add_line(k, e, konec)

new_seed = vvv_block + comp_block + "\n\n  // ===== Dopolnitev iz raziskave " + DATUM + " (" + VIR_R + "). Velikost strank je presoja po prepoznavnosti znamke.\n" + "\n".join(lines) + "\n"

# ---------------------------------------------------------------- 6. sestavi DEFAULT_DATA
def fmt_agencije():
    out = []
    for r in agencije:
        out.append("    { " + ", ".join(f"{k}: {js(v)}" for k, v in r.items()) + " }")
    return ",\n".join(out)

def fmt_finance():
    out = []
    for k, yrs in finance.items():
        ys = ",\n".join(f"      {y}: {{ prihodki: {js(f['prihodki'])}, dobicek: {js(f['dobicek'])}, zaposleni: {js(f['zaposleni'])}, vir: {js(f['vir'])} }}" for y, f in yrs.items())
        out.append(f"    {js(k)}: {{\n{ys}\n    }}")
    return ",\n".join(out)

def fmt_snapshot():
    vs = ",\n".join(f"        {js(k)}: {json.dumps(v)}" for k, v in vred.items())
    return f"    '2026-09': {{\n      vir: {js(snapshot['vir'])},\n      vrednosti: {{\n{vs}\n      }}\n    }}"

metrike = re.search(r"  metrike: \[\n.*?\n  \],", html, re.S).group(0)
new_default = f"""const DEFAULT_DATA = {{
  verzija: 4,
  // Generirano s research/build-liga-data.py iz {VIR_R} ({DATUM}); ročno ne urejaj, popravi JSON in ponovno zaženi.
  agencije: [
{fmt_agencije()}
  ],
{metrike}
  snapshoti: {{
{fmt_snapshot()}
  }},
  projekti: [],   // napolni se v seedProjekti()
  nagrade: [
{nagrade_js}
  ],
  finance: {{
{fmt_finance()}
  }},
  uteziStebrov: {{ doseg: 20, posel: 45, finance: 35 }},
  nastavitve: {{ samoJavno: true }}
}};

// Register projektov. Datum = prva javna omemba (kjer ni znana, datum vira).
function seedProjekti() {{
{new_seed}
  return P;
}}"""

start = html.index("const DEFAULT_DATA = {")
end = html.index("DEFAULT_DATA.projekti = seedProjekti();")
html = html[:start] + new_default + "\n" + html[end:]

# ---------------------------------------------------------------- 7. migracija v4
MIG = """  if (d.verzija < 4) {
    // v4 (22. 9. 2026): raziskava s primarnimi viri; 13 agencij. Ročno vnesene projekte/nagrade (id z Date.now) ohrani,
    // začetne (id p<št>/n<št>) zamenja; snapshot 2026-09 zamenja z neposrednim odčitkom; finance in agencije prevzame iz DEFAULT_DATA.
    d.verzija = 4;
    DEFAULT_DATA.agencije.forEach(def => { const i = d.agencije.findIndex(x => x.id === def.id); if (i >= 0) d.agencije[i] = klon(def); else d.agencije.push(klon(def)); });
    d.snapshoti['2026-09'] = klon(DEFAULT_DATA.snapshoti['2026-09']);
    d.projekti = klon(DEFAULT_DATA.projekti).concat((d.projekti || []).filter(p => !/^p\\d+$/.test(p.id)));
    d.nagrade = klon(DEFAULT_DATA.nagrade).concat((d.nagrade || []).filter(x => !/^n\\d+$/.test(x.id)));
    d.finance = Object.assign({}, d.finance || {}, klon(DEFAULT_DATA.finance));
  }
"""
anchor = "  d.projekti = d.projekti || []; d.nagrade = d.nagrade || []; d.finance = d.finance || {};"
assert anchor in html
html = html.replace(anchor, MIG + anchor, 1)

HTML.write_text(html, encoding="utf-8", newline="\n")
print("agencije", len(agencije), "| snapshot", len(vred), "| finance", sum(len(v) for v in finance.values()), "| nove nagrade", len(nag_lines), "| novi projekti", len([l for l in lines if l.startswith("  add(")]))
