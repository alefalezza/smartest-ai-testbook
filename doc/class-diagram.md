# Diagramma delle classi — POC

La lettura principale è **test → run → eval → report**. Il diagramma mostra le responsabilità e i tre pattern; gli attributi di persistenza e i dettagli del report restano nei [requisiti](./requirements.md).

```mermaid
classDiagram
    direction LR

    class TestSuite
    class TestCase {
        +prompt: String
    }
    class TestCaseBuilder {
        +build() TestCase
    }
    class EvaluatorConfig {
        +evaluatorType: String
        +threshold: Number?
    }

    class EvalRunner {
        +run(suite: TestSuite, provider: ModelProvider) EvalRun
    }
    class ModelProvider {
        <<interface>>
        +generateResponse(prompt: String) String
    }
    class ProviderAdapter
    class EvalRun
    class EvalResult {
        +output: String?
        +error: String?
        +scores: List~EvalScore~
    }

    class Evaluator {
        <<interface>>
        +evaluate(test: TestCase, output: String, config: EvaluatorConfig) EvalScore
    }
    class ExactMatchEvaluator
    class SemanticSimilarityEvaluator
    class LlmJudgeEvaluator
    class EvalReport {
        +fromRun(run: EvalRun) EvalReport$
    }

    TestSuite "1" -- "1..*" TestCase : contiene
    TestCaseBuilder ..> TestCase : costruisce (Builder)
    TestCase "1" -- "1..*" EvaluatorConfig : configura
    TestSuite "1" --> "0..*" EvalRun : eseguita in

    EvalRunner ..> TestSuite : esegue
    EvalRunner ..> ModelProvider : interroga il SUT
    ProviderAdapter ..|> ModelProvider : Adapter
    EvalRunner ..> EvalRun : produce
    EvalRun "1" *-- "1..*" EvalResult : registra

    EvalRunner ..> EvaluatorConfig : seleziona per tipo
    EvalRunner ..> Evaluator : applica
    ExactMatchEvaluator ..|> Evaluator : Strategy
    SemanticSimilarityEvaluator ..|> Evaluator : Strategy
    LlmJudgeEvaluator ..|> Evaluator : Strategy
    EvalRunner ..> EvalReport : genera al termine
    EvalRun "1" --> "1" EvalReport : riepilogato in
```

- **Builder:** `TestCaseBuilder` costruisce un `TestCase`; la suite raccoglie i test creati.
- **Adapter:** `ModelProvider` è l'interfaccia interna verso il **SUT (System Under Test)**, cioè il provider/modello scelto per il run. `ProviderAdapter` adatta la sua API a questa interfaccia.
- **Strategy:** ogni `TestCase` configura uno o più evaluator. `EvalRunner` sceglie l'implementazione di `Evaluator` in base a `evaluatorType`, la applica all'output e registra gli score nel risultato.
- **Report:** al termine delle valutazioni, `EvalRunner` chiama il metodo statico `EvalReport.fromRun(run)`, che raccoglie risultati e score del run e restituisce il report. Il giudizio complessivo usa `OverallScoreEvaluator`, omesso dal disegno.

Le frecce tratteggiate indicano dipendenze o realizzazioni; il flusso test → run → eval → report è descritto dalle responsabilità, non da una sequenza temporale UML.
