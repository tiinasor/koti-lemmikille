# Koti lemmikille -sovellus

Sovelluksen avulla käyttäjä, joka on luopumassa lemmikkieläimestään, voi etsiä sille uutta kotia ja käyttäjä, joka haluaa tarjota lemmikille kodin, voi etsiä lemmikkejä ja ottaa yhteyttä niiden omistajiin. Rekisteröityneet käyttäjät ovat joko peruskäyttäjiä tai ylläpitäjiä.

Tämänhetkiset ominaisuudet:
* Käyttäjä voi luoda uuden tunnuksen sekä kirjautua sisään ja ulos.
* Käyttäjä näkee sovelluksen etusivulla kategoriat, joihin kotia etsivät lemmikit on lajiteltu (koirat, kissat, jyrsijät, linnut, matelijat, muut) ja voi katsoa ilmoituksia kategorioittain sen jälkeen kun ilmoituksia on lisätty.
* Sisäänkirjautunut käyttäjä pystyy lisäämään ilmoituksen kotia etsivästä lemmikistä täyttämällä lomakkeen, jossa kysytään eläimen perustiedot (nimi, ikä, sukupuoli, sijainti). Lisäksi lomakkeessa on tekstikenttä, johon käyttäjä voi kirjoittaa tarkemman esittelyn lemmikistä.

Tulevat ominaisuudet:
* Käyttäjä näkee sovelluksen etusivulla jokaisessa kategoriassa olevien ilmoitusten lukumäärän.
* Ilmoituksen tehnyt käyttäjä pystyy poistamaan tekemänsä ilmoituksen. Ylläpitäjä pystyy poistamaan kenen tahansa käyttäjän tekemän ilmoituksen.
* Ilmoituksen kautta toinen käyttäjä voi aloittaa yksityisen viestiketjun ilmoituksen lisänneen käyttäjän kanssa.
* Käyttäjä pystyy lähettämään yksityisviestin ylläpitäjälle ja ylläpitäjä pystyy lähettämään yksityisviestin kenelle tahansa käyttäjälle.

Sovelluksen testaaminen:

Sovellus ei ole testattavissa Fly.iossa, ohjeet sovelluksen käynnistämiseen paikallisesti:
* Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:
    ```
    DATABASE_URL=<tietokannan-paikallinen-osoite>
    SECRET_KEY=<salainen-avain>
    ```
* aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet seuraavilla komennoilla:
    ```
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install -r ./requirements.txt
    ```
* Määritä tietokannan skeema ja oletusdata seuraavilla komennolla:
    ```
    $ psql < schema.sql
    $ psql < default_data.sql
    ```
* Käynnistä sovellus seuraavalla komennolla:
    ```
    $ flask run
    ```
