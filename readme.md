# Smartest AI Testbook

> Progettazione del dominio e del design object-oriented per un MVP di valutazione delle risposte generate da LLM.  
> Liberamente ispirato al progetto [yTestbook](https://ytestbook.intesys.it/)

## Scenario

Un team sta costruendo un'applicazione basata su un modello linguistico. Le risposte possono variare e non basta verificare che il programma non vada in errore: il team ha bisogno di definire esempi di prova, inviarli a un modello e valutare le risposte con criteri espliciti.

**Problema da esplorare:** come rendere la qualità delle risposte osservabile e misurabile?

Formula il **core value** dell'applicazione prima di proporre componenti o funzionalità. Una suite, un run e un report servono solo se aiutano a raggiungere quel valore.

## Perimetro MVP

L'utente crea e modifica una suite di test, avvia un run contro un provider LLM, consulta gli output con le relative valutazioni e può esportare suite e risultati in JSON. Il sistema persiste i dati.

I test hanno un'identità stabile e sono modificabili, ma il sistema non versiona il loro contenuto e non conserva snapshot dei prompt. La cronologia conserva l'ID del test e i risultati del run, non la configurazione esatta usata in passato.

Non progettare dashboard, login, code distribuite, report in tempo reale, CI/CD, CLI, concorrenza o strategie di retry: non sono necessari per dimostrare il core value dell'MVP.

## Lavoro richiesto nelle due pratiche

### Parte 1 — Comprendere il dominio

- Partire dai compiti dell'utente tipo (Prompt / AI Engineer): definire test, avviare un run e interpretare i risultati; individuare bisogni e punti in cui l'interfaccia deve aiutare.
- Individuare il problema e formulare il core value.
- Identificare attore, use case, dati persistenti e flusso principale.
- Analizzare quali informazioni servono nel report del run.
- Disegnare un wireframe a bassa fedeltà del flusso principale e fare una breve revisione UX tra pari.
- Disegnare il modello concettuale del dominio e discutere le relazioni.

### Parte 2 — Progettare classi e interfacce

- Trasformare il modello di dominio in classi e responsabilità.
- Definire l'interfaccia del runner e il confine con il provider.
- Derivare Strategy dagli evaluator intercambiabili e dal calcolo del giudizio complessivo.
- Derivare Adapter dalla necessità di isolare API diverse dei provider.
- Motivare le scelte e lasciare fuori i dettagli che non servono all'MVP.

### Wireframe e revisione UX

Il wireframe serve a verificare che il flusso sia comprensibile all'utente e che i dati del dominio e del report siano presentati quando servono. È sufficiente uno schizzo delle schermate principali: gestione di suite e test, avvio del run, consultazione del report. Non si richiede una UI rifinita né la progettazione visuale.

Verificare che siano comprensibili il passo successivo, i dati da inserire, la scala e l'esito degli score, e gli eventuali errori del provider. Ogni elemento del wireframe deve corrispondere a un use case o a un requisito MVP; non introdurre nuove funzioni solo per completare la schermata.

## Materiali

- [requirements.md](./doc/requirements.md): requisiti MVP e confini;
- [test-case-examples.md](./doc/test-case-examples.md): test, evaluator e esempio di report;

## Verifica del codice

Le specifiche in `openspec/` e i documenti in `doc/` sono condivisi. Le implementazioni e le rispettive dipendenze si trovano in `typescript/` e `python/`.

- Dalla radice, `npm ci` installa OpenSpec; `npx openspec validate --all` verifica le specifiche.
- In `typescript/`, `npm ci` installa le dipendenze, `npm test` esegue i test e `npm run typecheck` verifica i tipi.
- In `python/`, `python -m unittest discover -s tests` esegue i test con Python 3.12 o successivo, senza dipendenze aggiuntive.
- Dalla radice, `docker compose up --build typescript` avvia l'ambiente TypeScript; `docker compose run --build --rm python` esegue i test Python. I due servizi possono essere usati separatamente.

Quando si modifica una specifica, i task devono indicare l'implementazione e la verifica per ciascun linguaggio, segnalando eventuali differenze di avanzamento.
