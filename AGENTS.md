# Language rule

Specifications must be written in Italian to make them understandable to the non-technical client. Code and all material intended exclusively for engineers must be written in English, including this file.

# Design rule

This project is a school exercise in object-oriented programming. Every TypeScript class must explicitly declare that it implements one or more interfaces exposing its public contract, even when there is only one implementation.

Python domain classes must explicitly declare and implement one or more public contracts using `Protocol`, even when there is only one implementation. Test support classes and data types are not domain classes.

# Implementation rule

Implement every feature in both TypeScript and Python, sequentially rather than simultaneously. Both implementations must provide the same set of functions and share the same basic architecture and logic. Only minimal implementation details required by the language may differ; logical discrepancies are not allowed.
