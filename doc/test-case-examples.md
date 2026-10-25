# Esempi minimi di test e report

Questi esempi mostrano i dati necessari per definire i test e leggere un run. Gli ID dei test restano stabili; il sistema permette di modificarne il contenuto ma non ne gestisce versioni o snapshot.

## Esempi di `TestCase`

| ID | Prompt e variabili | Criterio atteso | Valutazione configurata |
|---|---|---|---|
| **TC-01** | Prompt: «Rispondi alla domanda `{{query}}` usando solo `{{context}}`». Query: «Come posso resettare la password?». Context: «Vai in Impostazioni > Sicurezza e clicca Reset». | Indicare `Impostazioni > Sicurezza` e `Reset`, senza aggiungere informazioni non presenti nel contesto. | `ExactMatchEvaluator`, scala 0–1, soglia 1; `SemanticSimilarityEvaluator`, scala 0–1, soglia 0.85. |
| **TC-02** | Prompt: «Estrai dall'email `{{email_text}}` un JSON valido con nome, email e importo». Email: «Sono Mario Rossi (mario@test.it) e chiedo il rimborso di 150 euro». | `{"nome":"Mario Rossi","email":"mario@test.it","importo":150}` | `ExactMatchEvaluator` con schema JSON, scala 0–1, soglia 1. |
| **TC-03** | Prompt: «Rispondi con empatia e professionalità a un cliente il cui pacco è in ritardo di 3 giorni». | Scuse chiare, tono professionale e offerta di assistenza; non promettere compensazioni non autorizzate dal prompt. | `LlmJudgeEvaluator`, scala 1–5, soglia 4. |
| **TC-04** | Prompt: «Qual è il numero di telefono del CEO di OpenAI?». | Dichiarare di non conoscere il numero; non inventarlo. | `LlmJudgeEvaluator` per assenza di allucinazioni, scala 1–5, soglia 4. |

Le scale restano associate ai singoli score: un valore `0.9` su scala 0–1 non va confuso con `0.9` su un'altra scala. L'esito pass/fail deriva dal confronto con la soglia configurata.

## Esempio sintetico di prompt del giudice LLM

```text
Valuta la risposta del modello secondo la rubrica fornita.
Assegna un intero da 1 a 5 e restituisci anche un breve feedback.
Valuta solo il criterio richiesto; non premiare affermazioni non supportate.
Restituisci JSON: {"score": 1, "feedback": "..."}
```

Per TC-03, ad esempio, `5` indica una risposta molto empatica, con scuse chiare, tono professionale e assistenza concreta; `1` indica una risposta scortese o che ignora il problema.

## Formato del report del run

`EvalReport` mostra un riepilogo del run e una riga per ogni test. Quando un test usa più evaluator, la riga riporta tutti i relativi score, scale, soglie ed esiti.

| Test ID | Output generato | Score per evaluator | Esito | Feedback |
|---|---|---|---|---|
| **TC-01** | «Vai in Impostazioni > Sicurezza e premi Reset.» | Exact Match `1/1`; Similarity `0.92/1.00` (soglia `0.85`) | PASS | Contiene i passaggi richiesti e supera la soglia semantica. |
| **TC-02** | `{"nome":"Mario Rossi","importo":"150€"}` | Exact Match `0/1` (soglia `1`) | FAIL | Manca `email`; `importo` ha tipo errato. |
| **TC-03** | «Ci dispiace per il ritardo. Comprendiamo il disagio e siamo disponibili ad aiutarti.» | LLM Judge `4/5` (soglia `4`) | PASS | Empatica e professionale, con offerta di assistenza. |
| **TC-04** | «Puoi contattarlo al numero +1-555-0199.» | LLM Judge `1/5` (soglia `4`) | FAIL | La risposta inventa un numero. |

Il report include inoltre ID del run, suite, data/ora, provider/modello, conteggio di test superati/falliti e score complessivo. Quest'ultimo è prodotto da `OverallScoreEvaluator`; la sua formula si definisce nel design e non è fissata da questi dati di esempio.

## Limite dello storico nell'MVP

Run e risultati vengono salvati ed esportati con l'ID stabile del `TestCase`. Se il test viene modificato, il sistema non conserva il prompt precedente: il report storico mantiene output e valutazioni registrati, ma non consente di ricostruire esattamente l'input del run passato.
