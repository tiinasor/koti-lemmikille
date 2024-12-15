# Koti lemmikille -sovellus

Sovelluksen avulla käyttäjä, joka on luopumassa lemmikkieläimestään, voi etsiä sille uutta kotia ja käyttäjä, joka haluaa tarjota lemmikille kodin, voi etsiä lemmikkejä ja ottaa yhteyttä niiden omistajiin. Rekisteröityneet käyttäjät ovat joko peruskäyttäjiä tai ylläpitäjiä.

Sovelluksen ominaisuudet:
* Käyttäjä voi luoda uuden tunnuksen sekä kirjautua sisään ja ulos.
* Käyttäjä näkee kategoriat, joihin kotia etsivät lemmikit on lajiteltu (koirat, kissat, jyrsijät, linnut, matelijat, muut) ja voi katsoa ilmoituksia kategorioittain sen jälkeen kun ilmoituksia on lisätty. Käyttäjä näkee myös jokaisessa kategoriassa olevien ilmoitusten lukumäärän.
* Sisäänkirjautunut peruskäyttäjä pystyy lisäämään ilmoituksen kotia etsivästä lemmikistä täyttämällä lomakkeen, jossa kysytään eläimen perustiedot. Lisäksi lomakkeessa on tekstikenttä, johon käyttäjä voi kirjoittaa tarkemman esittelyn lemmikistä.
* Ilmoituksen tehnyt käyttäjä pystyy poistamaan tekemänsä ilmoituksen. Ylläpitäjä pystyy poistamaan kenen tahansa käyttäjän tekemän ilmoituksen.
* Ilmoituksen kautta peruskäyttäjä voi lähettää yksityisviestin ilmoituksen lisänneelle käyttäjälle. Käyttäjä ei voi lähettää viestiä ilmoituksen kautta jos ilmoitus on hänen itsensä lisäämä tai hän on jo lähettänyt viestin kyseisen ilmoituksen kautta.
* Kun ensimmäinen viesti on lähetetty ilmoituksen kautta, viestin lähettäjän ja ilmoituksen tekijän välille aukeaa viestiketju. Käyttäjä pystyy näkemään viestiketjuissa saamansa ja lähettämänsä viestit sekä poistamaan itse lähettämiään viestejä.

Sovelluksen testaaminen:

Sovellus ei ole testattavissa Fly.iossa, ohjeet sovelluksen käynnistämiseen paikallisesti:
* Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:
    ```
    DATABASE_URL=<tietokannan-paikallinen-osoite>
    SECRET_KEY=<salainen-avain>
    ```
* Aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet seuraavilla komennoilla:
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