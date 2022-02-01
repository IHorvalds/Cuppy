# Documentatie de utilizare - Cuppy

[TOC]

## 1. Autentificarea in interfata web

Autentificarea se face la adresa `/auth/login` printr-un `POST` care contine credentialele utilizatorului.

Credentialele default sunt `admin/f!WY3GGJrNJ^oeDBmyL6B$`.

## 2. Inregistrarea unei plante in aplicatie

Exista mai multe specii de plante cu valori optime pentru parametrii predefinite.

In functie de nivelul de experienta al utilizatorului, initializarea se poate face in 2 moduri.

### 2.1. Initializarea unei plante cu valori default

La adresa `/initialize`, se poate initializa o planta regasita in baza de date, putand fi date valori custom pentru parametrii optimi, insa valorile default fiind cele predefinite.

### 2.2. Initializarea unei plante personalizabile

Daca utilizatorul detine o planta care nu se afla in baza d date, acesta o poate initializa la adresa `initialize_custom`, fiind necesara specificarea:

* tipului de planta
* valorile optime pentru fiecare parametru

## 3. Crearea unui hub central

Fiecare planta va apartine unui hub. Deci utilizatorul trebuie sa initializeze cel putin un hub care sa contina planta initializata anterior.

Initializarea hub-ului se face la adresa `/central`.

## 4. Pornirea/oprirea hub-ului central

Hub-ul central trebuie pornit/oprit o data cu dispozitivele de actionare pentru a mentine integritatea sistemului.

Controlarea acestuia se face la adresa `/central_control`.

## 5. Adaugarea senzorilor

Cuppy ofera 3 tipuri de senzori:

* luminozitate
* umiditate
* temperatura

Fiecare senzor trebuie definit individual la adresa `/sensors`.

## 6. Adaugarea dispozitivelor de actionare

Pentru fiecare senzor definit, utilizatorul trebuie sa adauge un dispozitiv de actionare asociat. Initializarea acestora se face la dresa `/sensors`.

## 7. Controlarea senzorilor si dispozitivelor de actionare

Senzorii si dispozitivele de actionare pot fi pornite/oprite in vederea operatiunilor de mentenanta la adresa `/sensor_control`, respectiv `/actuator/control`.

## 8. Alerte

Cuppy permite utilizatorului sa monitorizeze in permanenta starea plantei prin intermediul alertelor.

Acestea sunt transmise in mod automat in momentul in care starea plantei iese din parametrii optimi definiti.



