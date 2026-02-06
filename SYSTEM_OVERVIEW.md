# System Overview 

This document is the **mental model and guardrail** for the entire codebase.  

---

## What This System Is

A **backend service** that processes unstructured customer reviews into
**deterministic, auditable decisions**, using an LLM strictly as a
*constrained reasoning dependency*.

---

## Core Principle

> **LLM reasons → Code decides → Database remembers**

- LLM suggests
- Code validates and controls flow
- DB stores truth and history

---

## High-Level Flow

1. API receives unstructured review
2. Input is normalized and validated
3. LLM produces *candidate* structured output
4. Code validates schema + business rules
5. Final decision is produced
6. State is updated (if valid)
7. Decision is logged (always)

Every request ends in **exactly one terminal outcome**.

---

## Components (Responsibility Boundaries)

### API Layer
- Owns request validation and idempotency
- Never returns raw LLM output

### LLM Interface
- Extracts structure, intent, escalation
- **Never** controls retries, state, or persistence

### Validation Layer
- Rejects invalid or unsafe LLM output
- All validation is deterministic

### State Manager
- Holds *current truth*
- Overwrite-only
- Single path for all mutations

### Audit Log
- Holds *history*
- Append-only
- Enables full decision reconstruction

---

## Persistence Model

- **State = current truth** (mutable)
- **Logs = history** (immutable)

Restart-safe by design.  
Crashes must not corrupt truth.

---

## Failure Model

Each request resolves to one terminal status, e.g.:

- `SUCCESS`
- `LLM_TIMEOUT`
- `LLM_SCHEMA_VIOLATION`
- `VALIDATION_REJECTED`
- `DB_WRITE_FAILED`

Retries are decided **only by code**.

---

## Non-Negotiable Invariants

These must always hold:

- LLM output is never persisted directly
- LLM never mutates state
- All state changes go through the state manager
- Validation happens before persistence
- Logs are append-only
- State is overwrite-only
- One request → one terminal outcome
- Same input + same state → same result

If any invariant is violated, it is a bug.

---

## What “Correct” Means

The system is correct if:

- Invalid LLM output cannot affect state
- State reflects only validated decisions
- Logs fully explain how state was reached
- Restarts do not lose or corrupt truth

Model quality is secondary to correctness.

---

## How to Use This Doc

When adding or changing anything, ask:

1. Does this preserve invariants?
2. Does code still own control flow?
3. Is state mutation explicit and auditable?
4. Can this fail safely?

If any answer is **no**, stop and redesign.