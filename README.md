# Ledina FC — Aplikacija za rekreativni nogomet

> **Za Claude:** To je kontekstna datoteka projekta. Preberi jo na začetku vsakega pogovora da veš kje smo.

---

## Kaj aplikacija dela

Spletna PWA aplikacija za beleženje statistike rekreativnega nogometa (skupina Ledina). Omogoča:
- Beleženje rezultatov tekem
- Lestvico igralcev od najboljšega do najslabšega
- Generiranje enakovrednih ekip na podlagi statistike
- Upravljanje seznama igralcev

Hostitng: Netlify (povezano z GitHub repom)
Jezik: Vanilla HTML + CSS + JavaScript (ena datoteka `index.html`)
Shramba: `localStorage` v brskalniku (ni backenda, ni baze)

---

## Struktura projekta

```
ledina-pwa/
├── index.html      # Celotna aplikacija (HTML + CSS + JS v eni datoteki)
├── manifest.json   # PWA manifest
├── sw.js           # Service worker (offline podpora)
├── icon-192.png    # Ikona za telefon
├── icon-512.png    # Ikona za telefon (velika)
└── README.md       # Ta datoteka
```

---

## Struktura podatkov

### Igralec (localStorage key: `ledina_igralci`)
```js
// Array of strings
['Janez', 'Jaka', 'Luka', ...]
```

### Tekma (localStorage key: `ledina_tekme`)
```js
{
  datum: '2026-04-18',          // ISO string YYYY-MM-DD
  rezultat: 'zmaga_beli',       // 'zmaga_beli' | 'zmaga_crni' | 'neodloceno'
  beli: ['Janez', 'Luka'],      // array imen — bela ekipa
  crni: ['Jaka', 'Lev'],        // array imen — črna ekipa
  opomba: ''                    // poljubno besedilo
}
```

**Pomembni dogovori:**
- `'rnd'` v ekipi = naključni gost, se ne šteje v statistiko
- Če je bila tekma 2:0 (2 zmagi iste ekipe), se shrani kot **2 ločeni tekmi** z istim datumom
- Rezultat beleži zmage/poraze, **ne golov**
- Domen = Fišer (ista oseba, povsod zapisano kot `'Domen'`)

### Verzija podatkov (localStorage key: `ledina_version`)
Trenutna verzija: `'v3'` — ob spremembi se localStorage samodejno ponastavi na defaultne podatke.

---

## Algoritmi

### Ocena igralca
```js
function ocenaIgralca(stats) {
  const winRate = zmage / tekme;
  const drawRate = neodloceno / tekme;

  // Forma: zadnjih 5 tekem, novejše dobijo večjo težo
  zadnjih5.forEach((r, i) => {
    const weight = (i + 1) / 5;
    if (r === 'W') formaBonus += weight * 0.3;
    if (r === 'D') formaBonus += weight * 0.1;
  });

  return winRate * 100 + drawRate * 30 + formaBonus * 100;
}
```

### Generiranje ekip
Serpentinsko razporejanje po oceni:
- Razvrsti prisotne po oceni (najboljši prvo)
- Par 0: 1→beli, 2→črni
- Par 1: 3→črni, 4→beli
- Par 2: 5→beli, 6→črni ... (izmenjuje)

---

## Strani (navigacija)

| Stran | ID | Opis |
|---|---|---|
| Lestvica | `lestvica` | Tabela vseh igralcev, filter: vsi / vsaj 5 tekem |
| Ekipe | `ekipe` | Izbira prisotnih + generiranje enakovrednih ekip |
| Tekme | `tekme` | Kronološki seznam vseh odigranih tekem |
| Vnos | `vnos` | Dodajanje nove tekme |
| Igralci | `igralci` | Dodajanje/odstranjevanje stalnih članov |

---

## Dizajn

- Tema: temna (dark mode), zelena (`#2ECC71`) kot akcijska barva
- Fonti: `Bebas Neue` (naslovi) + `DM Sans` (besedilo)
- CSS variables v `:root` za barve
- Mobilno prilagojeno, safe area za iPhone (notch/home bar)
- Install banner za Android (beforeinstallprompt)

---

## Že implementirano ✅

- [x] Lestvica z oceno (W/D/L + forma zadnjih 5)
- [x] Filter lestvice: vsi / vsaj 5 tekem
- [x] Forma prikaz (barvne pike za zadnjih 5 tekem)
- [x] Generiranje enakovrednih ekip (serpentinsko)
- [x] Vnos novih tekem
- [x] Upravljanje igralcev (dodaj/odstrani)
- [x] PWA (manifest, service worker, ikone, iOS + Android)
- [x] Offline delovanje
- [x] Podatki shranjeni v localStorage
- [x] Uvožene vse pretekle tekme (sep 2025 – apr 2026)

---

## Ideje za naprej 💡

- [ ] Izvoz statistike v Excel/CSV
- [ ] Prikaz profila posameznega igralca (klik na ime)
- [ ] Statistika po mesecih / sezonah
- [ ] Beleženje strelcev golov
- [ ] Možnost urejanja/brisanja napačno vnesene tekme
- [ ] Prikaz "head to head" med dvema igralcema
- [ ] Skupinska raba podatkov (sync med telefoni)

---

## VVV Liga — konkurenčna lestvica (`konkurenca.html`)

Ločena, samostojna stran v istem repozitoriju (isti dizajn, brez povezave z Ledina podatki). Nogometna lestvica za **VVV Digital** proti 9 konkurentom: TikTok SPACE, Vividista, Envision Collective, Tiktokerija, A.P. Marketing, Ziya Agency, Createable, Katapult Media, We Are TikTok (WATT).

**Trije stebri**, vsak lastna liga s točkovanjem 3/1/0 in dvoboji vsak proti vsakemu po metriki. Dvoboj se odigra le, če imata obe agenciji podatek (manjkajoč podatek ni poraz).

| Steber | Kolo | Metrike | Primerjava |
|---|---|---|---|
| Doseg | mesec | IG, TikTok, LinkedIn sledilci (utež 1), Google ocene (0,5) | relativna rast, prag 1 o.t. za neodločeno |
| Posel | mesec | novi projekti (utež po velikosti stranke micro 1 / mini 1,5 / mid 2 / big 3, znamka +1), projekti skupaj (vse stranke od začetka), aktualni projekti (brez znanega konca), nagrade in omembe | absolutne vrednosti |
| Finance | leto | prihodki, rast, dobiček, marža, zaposleni, prihodki/zaposlenega (AJPES prek Bizi) | absolutne, rast v % |

**Skupni indeks** = utežena vsota deležev točk po stebrih (privzeto Posel 45 %, Finance 35 %, Doseg 20 %; 100 = prvi v vseh treh). Stebri brez podatkov se preskočijo.

- **Zavihki:** Skupno, Doseg (lestvica + trenutno stanje), Posel (lestvica, portfelj, register projektov), Finance (lestvica, bilanca po letih), + Vnos (snapshot, projekt, nagrada, letne finance, izvoz/uvoz), Agencije, Metodologija.
- **Shramba:** `localStorage` ključ `vvv_konkurenca_v1` (verzija 3, samodejna migracija iz v1/v2); izvoz/uvoz JSON.
- **Deklarirano število strank** (npr. "100+" na LinkedInu) je pri agenciji zapisano informativno in ni v ligi, ker ga ni mogoče preveriti.
- **Register VVV** vsebuje javne študije primerov, portfolio 2025 in interne posle iz CRM (označeni `javno: false`); filter "Samo javno vidni projekti" jih izključi za pošteno primerjavo.
- **Začetni podatki (5. 9. 2026)** so iz spletnega iskanja; viri so zapisani pri vsakem vnosu in v Metodologiji. Instagram/TikTok/LinkedIn/Bizi niso bili neposredno dostopni, zato snapshot dosega pokriva le del agencij.

Struktura podatkov:
```js
{
  agencije:  [{ id, ime, pravna, opomba, ig, tt, li, web, strank }],
  metrike:   [{ id, ime, utez }],
  snapshoti: { 'YYYY-MM': { vir, vrednosti: { [agId]: { [metId]: number } } } },
  projekti:  [{ id, agId, stranka, datum, velikost, znamka, javno, opis, vir, konec }],
  nagrade:   [{ id, agId, datum, naziv, tocke, vir }],
  finance:   { [agId]: { [leto]: { prihodki, dobicek, zaposleni, vir } } },
  uteziStebrov: { doseg, posel, finance },
  nastavitve: { samoJavno }
}
```

---

## Kako nadaljevati z Claudom

1. Odpri nov pogovor na claude.ai
2. Prilepi vsebino tega README kot prvo sporočilo
3. Priloži `index.html` (ali prilepi relevanten del kode)
4. Opiši kaj želiš spremeniti

Claude bo vedel točno kje smo in kaj je že narejeno.
