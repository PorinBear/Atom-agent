# ATOM Agent

ATOM on tiimin sisäinen, itsenäisesti työskentelevä selainagentti. Se suorittaa verkkotehtäviä pysyvässä selainprofiilissa, pitää eri yritysten tiedot erillisissä työtiloissa ja pysähtyy hyväksyntään ennen ulkoisia tai vaikeasti peruttavia toimia.

## Nyt mukana

- Playwright/Chromium-selain ja LLM-suunnittelija
- jatkuva SQLite-tehtäväjono
- puhelimella käytettävä ATOM Control -hallintasivu
- iPhonen kotinäyttöön asennettava PWA-äppi ilman App Storea
- puheesta tekstiksi -ohjaus ja vastausten lukeminen ääneen puhelimessa
- oppimismuisti päätöksille, mieltymyksille, kontakteille ja työn opeille
- työtilat `tommi-hq`, `ewalahti` ja `future-atom`
- pysyvät selainprofiilit, lataukset, screenshotit ja lokit työtiloittain
- turvallinen upload vain työtilan `files`-kansiosta
- URL/SSRF-suojaus ja polkujen rajaus
- kertakäyttöinen hyväksyntä maksuun, ostoon, lähetykseen, julkaisuun, uploadiin, poistoon, sopimukseen ja käyttöoikeusmuutokseen
- tekstipohjainen yhteydenpito verkkopalveluissa hyväksynnän kautta
- Codespaces-valmis kehitysympäristö ja testit

## Nopein käynnistys iPhonelta: GitHub Codespaces

1. Avaa repo GitHubissa ja valitse **Code → Codespaces → Create codespace**.
2. Lisää Codespaces secret `OPENAI_API_KEY` GitHubin asetuksissa. Älä tallenna avainta repoon.
3. Codespaces asentaa riippuvuudet ja Chromiumin automaattisesti.
4. Käynnistä terminalissa:

```bash
chmod +x start.sh
./start.sh
```

5. Avaa ilmoitettu portti **8000**. ATOM Control toimii iPhonen selaimessa.
6. Valitse Safarissa **Jaa → Lisää Koti-valikkoon**, jolloin ATOM avautuu omana appinaan.

Pidä Codespace-portti yksityisenä. Kirjautumiset ja MFA tehdään ihmisen toimesta; agentti ei vastaanota eikä tallenna salasanoja tai vahvistuskoodeja.

## Maksuton käyttö ilman korttia

Repo sisältää **ATOM Free Worker** -GitHub Actions -ajon. Avaa GitHubissa **Actions → ATOM Free Worker → Run workflow**, kirjoita tehtävä ja valitse työtila. Työ käynnistyy erillisessä selaimessa, ja tulos näkyy ajon Summary-näkymässä.

Maksuton tila käyttää GitHub Copilot CLI:tä sisäänrakennetulla `GITHUB_TOKEN`-tunnuksella. Se sopii tutkimiseen, vertailuun, tarkistuksiin ja luonnosteluun. Kirjautumista tai ihmisen hyväksyntää vaativat ulkoiset toimet pysähtyvät turvallisesti. Jatkuvasti hereillä oleva PWA tarvitsee myöhemmin palvelimen tai oman aina päällä olevan tietokoneen.

## Paikallinen käynnistys

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
python -m uvicorn server:app --host 127.0.0.1 --port 8000
```

Toisessa terminalissa:

```bash
python agent.py --worker
```

Yksittäinen tehtävä ilman jonoa:

```bash
python agent.py --workspace ewalahti "Avaa yrityksen sivu ja tee laadunvarmistus"
```

## Turvaraja

ATOM saa lukea, hakea, vertailla, luonnostella ja navigoida itsenäisesti. Ulospäin vaikuttavat toimet hyväksytään ATOM Controlissa yksi kerrallaan. CAPTCHAa, käyttöoikeuksia tai muita turvarajoja ei kierretä.
