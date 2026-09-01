"""
Reasoning Module

This module provides reasoning and inference capabilities for knowledge graph
analysis and query answering, supporting multiple reasoning strategies including
rule-based inference via Rete, SPARQL reasoning, abductive and deductive reasoning,
and native Datalog evaluation.
"""

from .reasoner import Reasoner, InferenceResult, Rule, Fact, RuleType
from .reasoner import (
    Action,
    AssertAction,
    RetractAction,
    CallAction,
    EmitEventAction,
)
from .explanation_generator import (
    Explanation,
    ExplanationGenerator,
    Justification,
    ReasoningPath,
    ReasoningStep,
)
from .rete_engine import (
    AlphaNode,
    BetaNode,
    Match,
    ReteEngine,
    ReteNode,
    TerminalNode,
)
from .sparql_reasoner import SPARQLQueryResult, SPARQLReasoner

from .datalog_reasoner import DatalogReasoner, DatalogFact, DatalogRule

# ---------------------------------------------------------------------------
# Lazily loaded members (PEP 562).
#
# Everything above is standard-library-only: the Rete network, the Datalog
# evaluator, forward chaining, the SPARQL parser and the explanation generator
# import nothing outside ``re``/``uuid``/``typing``/``dataclasses``/
# ``collections``/``datetime``/``enum``. Two members were the exception and they
# pulled the whole heavy stack into ``import semantica.reasoning``:
#
#   * the temporal trio  -> ``semantica.temporal_reasoning`` is a shim over
#                           ``semantica.kg``, whose ``__init__`` eagerly imports
#                           ``centrality_calculator`` -> ``numpy``. This is the
#                           edge that made the whole package numpy-dependent.
#   * ``GraphReasoner``   -> ``semantica.semantic_extract.providers``. This one
#                           costs no third-party import today, but it is the
#                           LLM-backed reasoner: keeping it out of the eager path
#                           is what makes "no model calls in this module" a
#                           property you can verify rather than a claim.
#
# Deferring these two keeps the deterministic engines importable in an
# environment with no third-party packages at all, which is what makes them
# usable as an audit/policy layer underneath other stacks. The public API is
# unchanged: ``from semantica.reasoning import GraphReasoner`` still works and
# still returns the same object -- it is resolved on first access instead of at
# import time.
# ---------------------------------------------------------------------------

_LAZY_MEMBERS = {
    "GraphReasoner": ".graph_reasoner",
    "IntervalRelation": ".temporal_reasoning",
    "TemporalInterval": ".temporal_reasoning",
    "TemporalReasoningEngine": ".temporal_reasoning",
}


def __getattr__(name):
    """Resolve the deferred members on first access (PEP 562)."""
    module_name = _LAZY_MEMBERS.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    from importlib import import_module

    module = import_module(module_name, __name__)
    value = getattr(module, name)
    globals()[name] = value  # cache: subsequent lookups skip __getattr__
    return value


def __dir__():
    return sorted(set(globals()) | set(_LAZY_MEMBERS))


__all__ = [
    # Reasoner facade
    "Reasoner",
    "GraphReasoner",
    "InferenceResult",
    "Rule",
    "Fact",
    "RuleType",
    # Rule-driven actions
    "Action",
    "AssertAction",
    "RetractAction",
    "CallAction",
    "EmitEventAction",
    # Rete engine
    "ReteEngine",
    "ReteNode",
    "AlphaNode",
    "BetaNode",
    "TerminalNode",
    "Match",
    # SPARQL reasoning
    "SPARQLReasoner",
    "SPARQLQueryResult",
    # Datalog reasoning
    "DatalogReasoner",
    "DatalogFact",
    "DatalogRule",
    "TemporalInterval",
    "IntervalRelation",
    "TemporalReasoningEngine",
    # Explanation
    "ExplanationGenerator",
    "Explanation",
    "ReasoningStep",
    "ReasoningPath",
    "Justification",
]
