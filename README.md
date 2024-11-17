# Koti lemmikille -sovellus

Sovelluksen avulla käyttäjä, joka on luopumassa lemmikkieläimestään, voi etsiä sille uutta kotia ja käyttäjä, joka haluaa tarjota lemmikille kodin, voi etsiä lemmikkejä.


Sovelluksen nykyinen tilanne:

* Käyttäjä voi luoda uuden tunnuksen sekä kirjautua sisään ja ulos.
* Sisäänkirjautunut käyttäjä pystyy lisäämään ilmoituksen kotia etsivästä lemmikistä täyttämällä lomakkeen, jossa kysytään eläimen tiedot.
* Käyttäjä näkee sovelluksen etusivulla kategoriat, joihin ilmoitukset lajitellaan ja voi katsoa ilmoituksia kategorioittain sen jälkeen kun ilmoituksia on lisätty.

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
