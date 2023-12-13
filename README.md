# README - Script di Configurazione Rete Nebula - CyberProject
Progetto del corso di Cybersecurity, Laurea Magistrale in Informatica , Università di Bologna 2023-2024
- Giuseppe Pio Salcuni - matr. 1100090
- Manuel Placella - matr. 1099701

Questo script in Python automatizza il processo di configurazione per la creazione di una rete Nebula, semplificando e gestendo in modo efficiente i dati in input. Lo script definisce e implementa tre funzioni cruciali per il processo di configurazione della rete Nebula:

## Funzioni

### `generate_organization_ca`

- Responsabile per la creazione di una struttura di directory dedicata all'organizzazione.
- Si occupa della generazione dell'Autorità di Certificazione (CA) specifica per l'organizzazione utilizzando l'utilità `nebula-cert`.

### `generate_certificates`

- Focalizzata sulla generazione di certificati per gli host all'interno della rete Nebula, inclusi il faro (lighthouse) e i client.
- Utilizza la CA precedentemente creata per firmare i certificati necessari tramite l'utilità `nebula-cert`.

### `generate_config`

- Ha il compito di generare file di configurazione YAML per ciascun host nella rete Nebula.
- Questi file di configurazione contengono impostazioni chiave utilizzate da Nebula per la configurazione, tra cui CA, certificati, indirizzi IP e impostazioni di sicurezza.

## Utilizzo

1. Esegui lo script con il comando `python nebulap.py`.
2. Lo script interagisce con l'utente per raccogliere informazioni essenziali per personalizzare la configurazione della rete Nebula.
3. L'utente fornisce dettagli chiave come il nome dell'organizzazione, i nomi e gli indirizzi IP dei vari client nella rete.

**Nota:** Assicurati di avere l'utilità `nebula-cert` installata e accessibile nel tuo ambiente per l'esecuzione riuscita dello script.

**Avviso:** Lo script presuppone una comprensione di base dei concetti e dei prerequisiti della rete Nebula. Consulta la documentazione di Nebula per ulteriori dettagli sulle opzioni di configurazione specifiche e impostazioni avanzate.

