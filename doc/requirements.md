# Requisiti MVP — Smartest AI Testbook

## Obiettivo e core value

Il sistema consente a un team di definire test per un'applicazione basata su LLM, eseguirli su un modello e ottenere una valutazione leggibile delle risposte. Il valore centrale è trasformare output LLM variabili in risultati misurabili e consultabili.

Il progetto  descrive un MVP. Si progettano SOLO funzioni che servono a definire una suite, eseguire un run, valutare le risposte, consultare i risultati o esportare i dati.

## Requisiti funzionali

### FR-1 — Gestire suite e test case

- L'utente può creare e modificare una `TestSuite` con nome e descrizione.
- Una suite raccoglie uno o più `TestCase`.
- Ogni `TestCase` ha un ID stabile, un prompt, eventuali variabili e un criterio di valutazione (golden reference e/o rubrica).
- L'utente può configurare per il test uno o più evaluator e le relative soglie.
- I test sono modificabili, ma il sistema **non gestisce versioni dei test né snapshot del prompt**. I risultati storici conservano il riferimento all'ID del test e l'esito registrato; non consentono di ricostruire il contenuto del test al momento di un run precedente.

### FR-2 — Eseguire una suite

- L'utente può avviare una suite selezionando un `ModelProvider`.
- Il sistema invia al provider il prompt del test con le sue variabili e raccoglie l'output generato.
- Ogni esecuzione è rappresentata da un `EvalRun`, collegato alla suite e ai risultati prodotti.
- Un errore su un singolo test viene registrato nel relativo `EvalResult` e non cancella gli altri risultati del run.

### FR-3 — Valutare le risposte

- Ogni output generato può essere valutato da uno o più `Evaluator`.
- Ogni score registra valore, scala, feedback e, se configurata, soglia con esito pass/fail.
- L'MVP prevede tre strategie iniziali:
  - `ExactMatchEvaluator`: controllo deterministico di contenuto o schema;
  - `SemanticSimilarityEvaluator`: similarità semantica rispetto alla golden reference;
  - `LlmJudgeEvaluator`: valutazione con rubrica tramite LLM.
- Gli score individuali mantengono la propria scala; non si assume che scale diverse siano direttamente confrontabili.

### FR-4 — Consultare il report

- Al termine di un run, `EvalReport` aggrega i relativi `EvalResult` e presenta un giudizio complessivo prodotto da una strategia dedicata (`OverallScoreEvaluator`).
- Il report rende consultabili: suite, data del run, modello/provider, ID del test, output generato, evaluator applicati, score con scala, soglia/esito e feedback.
- Il valore complessivo è prodotto dalla strategia, ma la formula di aggregazione è parte dell'esercizio di design e non viene fissata qui.

### FR-5 — Persistenza ed export

- Suite, test case, run e risultati sono salvati nel database.
- L'utente può esportare una suite in JSON. L'export comprende la suite, i test e la relativa cronologia di run e risultati.
- Il file esportato può essere salvato e versionato all'esterno del sistema; non è versionato il singolo test all'interno dell'applicazione.

## Requisiti non funzionali essenziali

- **Estensibilità:** si può aggiungere un evaluator o un adapter per un provider senza modificare la logica principale del runner.
- **Isolamento degli errori:** un errore relativo a un test viene registrato senza perdere i risultati degli altri test del run.
- **Tracciabilità minima:** ogni run registra data/ora e provider/modello; ogni risultato conserva l'ID del test, output e valutazioni ottenute.

## Fuori perimetro MVP

Versionamento interno o snapshot dei test, confronto automatico con baseline/regressioni, dashboard e aggiornamenti live, account e permessi, import/export CSV, CI/CD e CLI, esecuzione concorrente, retry/backoff, ottimizzazione costi e scelta di tecnologie specifiche per database o code.
