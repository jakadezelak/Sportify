# Navodilo za dopolnitev raziskave konkurence (nova seja)

Kopiraj besedilo pod črto kot prvi prompt v novi seji na veji
`claude/vvv-digital-competitive-ranking-dz2zd9` (okolje s polnim omrežnim
dostopom ali lokalni Claude Code).

---

Delaš na veji `claude/vvv-digital-competitive-ranking-dz2zd9` (projekt VVV Liga).
Tvoja edina naloga: DOPOLNI obstoječo datoteko `research/konkurenca-2026-09.json`
z neposrednim branjem spletnih strani. NE spreminjaj konkurenca.html, README.md
ali index.html. Ne začenjaj od začetka: obstoječe vrednosti obdrži, razen če jih
na primarnem viru ovržeš (potem popravi in v "opombe" zapiši staro in novo vrednost).

## 1. Preveri dostop
Zaženi `curl -sS -o /dev/null -w '%{http_code}\n' https://www.bizi.si/`.
Če dobiš 000 ali 403, ne nadaljuj: v JSON zapiši `"dostop": "blokiran"` in
razlog, commitaj, potisni in povej uporabniku, da je treba v nastavitvah
okolja (claude.ai/code, Environments, Network access) omogočiti poln dostop
ali pa sejo zagnati lokalno.

## 2. Preberi obstoječi JSON
Odpri `research/konkurenca-2026-09.json`. Vsaka agencija ima polje "opombe",
kjer piše, kaj manjka. Najprej zapolni tiste luknje (null vrednosti).

## 3. Viri in orodja
- Registri: bizi.si, companywall.si, ebonitete.si, ajpes.si (brezplačni
  pogled). Uporabi WebFetch ali curl; če stran zahteva JavaScript, uporabi
  Playwright/Chromium (`PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`).
- Družbena omrežja: Instagram, TikTok, LinkedIn. Najprej poskusi meta oznake
  (`og:description` pogosto vsebuje število sledilcev), nato Playwright.
  Če stran blokira, zapiši "ni dostopno" in nadaljuj.
- Google ocene: poskusi Google Maps iskanje po imenu agencije.
- Spletne strani agencij: noga (pravna oseba), politika zasebnosti, strani
  Reference / Portfolio / Projekti / Ekipa / O nas.

## 4. Kaj konkretno manjka (po prioriteti)
1. Pravne osebe za: tiktokspace (tiktok-space.si, Celovška cesta 69C),
   vividista (vividista.si), ziya (ziya.agency), createable (createable.si).
   Preveri nogo strani in politiko zasebnosti; nato poišči v bizi/companywall
   po firmi ali naslovu.
2. Sledilci za vseh 10: IG, TT, LI (število + ročaj + datum odčitka
   2026-09-DD). Trenutno so znani samo VVV (IG, LI), Tiktokerija (TT),
   A.P. Marketing (IG), Createable (IG).
3. Google ocene (število in povprečje) za vseh 10.
4. Stranke: preberi strani z referencami in zadnjih ~20 objav na IG/TT/LI
   vsake agencije. Za vsako stranko: ime, opis dela, približen datum prve
   omembe (YYYY-MM-DD), URL vira. Trenutno imajo stranke samo VVV,
   Tiktokerija, A.P. Marketing in WATT.
5. Finance: manjkajoča leta 2022–2025 (prihodki, čisti dobiček, zaposleni)
   za VVV, BlendCreative, Andrej Pavličević s.p., Kaching, Katapult. Za
   Katapult določi leto vnosa "neznano_leto" in ga preimenuj v pravo leto.
6. Ekipa: število oseb po strani "Ekipa"/"O nas" ali LinkedIn za tiste,
   ki imajo null (tiktokspace, vividista, envision, ziya).
7. Nagrade in omembe: preveri sof.si, diggit.si, websi.si, effie.si,
   marketingmagazin.si za vsako agencijo. Za Tiktokerijo preveri, ali je
   vpis V4007S26 (Deichmann Adria) finalist ali nagrajenec.

## 5. Pravila
- Ne izmišljuj. Kjer podatka ni, pusti null in v "opombe" napiši, zakaj.
- Številke so cela števila brez ločil.
- V polje "dostop" zapiši "ok" ali "delno" in v "opombe" na vrhu posodobi
  opis, kaj je bilo tokrat prebrano neposredno in kaj ostaja iz iskalnih
  izvlečkov.
- Datoteka mora ostati veljaven JSON (preveri s `python3 -m json.tool`).

## 6. Zaključek
`git add research/konkurenca-2026-09.json`, commit s sporočilom
"Raziskava konkurence 2026-09: dopolnitev s primarnimi viri",
`git push -u origin claude/vvv-digital-competitive-ranking-dz2zd9`
(ob omrežni napaki poskusi še 3-krat z zamikom). Na koncu v enem odstavku
povzemi, kaj si dopolnil in kaj še vedno manjka.
