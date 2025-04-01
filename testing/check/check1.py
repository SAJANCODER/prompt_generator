import re
import json
import os
import random
from collections import defaultdict
from typing import Dict, List, Any, Set
import spacy
from datetime import datetime
from spacy.cli import download as spacy_download
import warnings


class MasterPromptEngineer:
    def __init__(self):
        self.nlp = self._initialize_nlp()
        self.knowledge_graph = self._build_knowledge_graph()
        self.user_profiles: Dict[str, Dict[str, Any]] = {}
        self.conversation_history: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self._load_data()

        # Master-level prompt engineering knowledge
        self.master_techniques = [
            "chain-of-thought prompting",
            "few-shot learning",
            "analogical reasoning",
            "Socratic questioning",
            "conceptual scaffolding",
            "metacognitive prompting"
        ]

        # Generative AI components
        self.tech_lexicon = self._build_tech_lexicon()
        self.creativity_factors = self._initialize_creativity_factors()

    def _initialize_nlp(self):
        """Initialize NLP with the most comprehensive model."""
        try:
            nlp = spacy.load("en_core_web_lg")
        except OSError:
            warnings.warn("Downloading advanced language model...")
            spacy_download("en_core_web_lg")
            nlp = spacy.load("en_core_web_lg")
        return nlp

    def _build_tech_lexicon(self) -> Set[str]:
        """Build a comprehensive technical lexicon for analysis."""
        lexicon = set()
        for lang, data in self.knowledge_graph.items():
            lexicon.update(data.get("tools", []))
            lexicon.update(data.get("paradigms", []))
            for level in data.get("levels", {}).values():
                lexicon.update(level)
        return lexicon

    def _initialize_creativity_factors(self) -> Dict[str, List[str]]:
        """Initialize components for creative prompt generation."""
        return {
            "analogies": [
                "quantum physics", "biological systems",
                "ancient civilizations", "artistic movements",
                "game theory", "cognitive architectures"
            ],
            "constraints": [
                "explain using only metaphors",
                "alternate between 3 expert personas",
                "use recursive reasoning",
                "structure as a Socratic dialogue",
                "present as a mathematical proof"
            ],
            "perspectives": [
                "futurist", "historian", "scientist",
                "artist", "philosopher", "engineer"
            ],
            "formats": [
                "haiku sequence", "interactive fiction",
                "visual diagram", "mathematical notation",
                "musical composition", "architectural blueprint"
            ]
        }

    def _build_knowledge_graph(self) -> Dict[str, Any]:
        """A globally comprehensive knowledge graph of programming languages and technical domains."""
        return {
            "python": {
                "levels": {
                    "beginner": ["syntax", "loops", "functions", "OOP basics"],
                    "intermediate": ["decorators", "async/await", "metaclasses", "context managers"],
                    "advanced": ["GIL workarounds", "C extensions", "JIT (Numba)", "distributed systems"],
                    "expert": ["CPython internals", "memory optimization", "compiler design", "security hardening"]
                },
                "paradigms": ["procedural", "OOP", "functional"],
                "use_cases": ["web dev", "data science", "automation", "AI/ML"],
                "tools": ["Django", "FastAPI", "PyTorch", "Pandas"],
                "subtleties": ["GIL limitations", "duck typing edge cases", "circular imports"]
            },
            "java": {
                "levels": {
                    "beginner": ["syntax", "classes", "inheritance", "interfaces"],
                    "intermediate": ["collections", "streams", "concurrency basics", "JVM"],
                    "advanced": ["bytecode manipulation", "GC tuning", "JNI", "performance optimization"],
                    "expert": ["JVM internals", "low-latency systems", "distributed JVM", "security exploits"]
                },
                "paradigms": ["OOP", "functional"],
                "use_cases": ["enterprise", "Android", "backend", "big data"],
                "tools": ["Spring", "Hibernate", "Maven", "Kafka"],
                "subtleties": ["JVM quirks", "memory leaks", "classloader issues"]
            },
            "r": {
                "levels": {
                    "beginner": ["vectors", "data frames", "basic stats"],
                    "intermediate": ["dplyr", "ggplot2", "statistical modeling"],
                    "advanced": ["S3/S4 systems", "Rcpp", "performance optimization"],
                    "expert": ["language internals", "memory management", "CRAN ecosystem"]
                },
                "paradigms": ["functional", "vectorized"],
                "use_cases": ["statistics", "data visualization", "bioinformatics"],
                "tools": ["tidyverse", "shiny", "rmarkdown"],
                "subtleties": ["lazy evaluation", "environment quirks", "S3/S4 dispatch"]
            },
            "rust": {
                "levels": {
                    "beginner": ["ownership", "borrowing", "traits"],
                    "intermediate": ["lifetimes", "unsafe", "macros"],
                    "advanced": ["FFI", "embedded", "compiler plugins"],
                    "expert": ["type system extensions", "formal verification", "language design"]
                },
                "paradigms": ["systems", "functional"],
                "use_cases": ["systems programming", "WASM", "blockchain"],
                "tools": ["Cargo", "Actix", "Tokio"],
                "subtleties": ["borrow checker edge cases", "unsafe interactions", "FFI complexities"]
            },
            "algorithms": {
                "levels": {
                    "beginner": ["sorting", "searching", "Big-O"],
                    "intermediate": ["graphs", "dynamic programming", "divide-and-conquer"],
                    "advanced": ["approximation", "randomized", "parallel"],
                    "expert": ["quantum", "parameterized", "computational geometry"]
                },
                "paradigms": ["imperative", "recursive"],
                "use_cases": ["problem solving", "optimization", "AI"],
                "tools": ["pseudocode", "visualization", "proof techniques"],
                "subtleties": ["constant factors", "cache behavior", "hidden assumptions"]
            },
            "machine learning": {
                "levels": {
                    "beginner": ["linear regression", "k-NN", "basic sklearn"],
                    "intermediate": ["neural networks", "SVM", "hyperparameter tuning"],
                    "advanced": ["attention", "GANs", "RL"],
                    "expert": ["theoretical limits", "novel architectures", "AI safety"]
                },
                "paradigms": ["supervised", "unsupervised", "reinforcement"],
                "use_cases": ["prediction", "generation", "classification"],
                "tools": ["TensorFlow", "PyTorch", "scikit-learn"],
                "subtleties": ["overfitting", "bias-variance", "adversarial examples"]
            },
            "operating systems": {
                "levels": {
                    "beginner": ["processes", "threads", "memory basics"],
                    "intermediate": ["scheduling", "paging", "file systems"],
                    "advanced": ["distributed", "real-time", "kernel hacking"],
                    "expert": ["formal verification", "security proofs", "novel architectures"]
                },
                "paradigms": ["systems", "concurrent"],
                "use_cases": ["performance", "security", "reliability"],
                "tools": ["Linux", "QEMU", "gdb"],
                "subtleties": ["race conditions", "deadlocks", "memory ordering"]
            }
        }

    def _load_data(self) -> None:
        """Load user profiles and conversation history from JSON files."""
        try:
            os.makedirs("../../user", exist_ok=True)

            if os.path.exists("../../user/user_profiles.json"):
                with open("../../user/user_profiles.json", "r", encoding="utf-8") as f:
                    self.user_profiles = json.load(f)

            if os.path.exists("../../user/conversation_history.json"):
                with open("../../user/conversation_history.json", "r", encoding="utf-8") as f:
                    self.conversation_history = json.load(f)

        except Exception as e:
            warnings.warn(f"Could not load data: {str(e)}")
            self.user_profiles = {}
            self.conversation_history = defaultdict(list)

    def _save_data(self) -> None:
        """Save both user profiles and conversation history to JSON files."""
        try:
            with open("../../user/user_profiles.json", "w", encoding="utf-8") as f:
                json.dump(self.user_profiles, f, indent=2, ensure_ascii=False)

            with open("../../user/conversation_history.json", "w", encoding="utf-8") as f:
                json.dump(dict(self.conversation_history), f, indent=2, ensure_ascii=False)

        except Exception as e:
            warnings.warn(f"Could not save data: {str(e)}")

    def _calculate_query_complexity(self, doc) -> float:
        """Calculate a comprehensive complexity score for the user query (0-1 scale)."""
        if not doc.text.strip():
            return 0.0

        syntactic_complexity = self._calculate_syntax_complexity(doc.text)
        concept_count = len([t for t in doc if t.text in self.tech_lexicon])
        normalized_concepts = min(concept_count / 5, 1.0)
        sentence_count = len(list(doc.sents))
        clause_count = sum(1 for token in doc if token.dep_ in ("advcl", "relcl", "ccomp", "xcomp"))
        structural_score = min((sentence_count * 0.3 + clause_count * 0.7) / 5, 1.0)
        depth_terms = sum(1 for t in doc if t.text.lower() in {
            "advanced", "expert", "deep", "complex", "optimize",
            "internals", "low-level", "theory", "fundamental"
        })
        depth_score = min(depth_terms / 3, 1.0)

        weights = {
            'syntax': 0.3,
            'concepts': 0.4,
            'structure': 0.2,
            'depth': 0.1
        }

        total_score = (
            weights['syntax'] * syntactic_complexity +
            weights['concepts'] * normalized_concepts +
            weights['structure'] * structural_score +
            weights['depth'] * depth_score
        )

        return min(max(total_score, 0.0), 1.0)

    def _calculate_syntax_complexity(self, text: str) -> float:
        """Calculate syntactic complexity score between 0-1."""
        doc = self.nlp(text)
        if len(list(doc.sents)) == 0:
            return 0.0

        avg_len = sum(len(sent) for sent in doc.sents) / len(list(doc.sents))
        clauses = sum(1 for token in doc if token.dep_ in ("advcl", "relcl", "ccomp", "xcomp"))
        clause_density = clauses / len(doc)
        max_depth = max(len(list(token.head.lefts)) + len(list(token.head.rights)) for token in doc)

        normalized = (avg_len / 30 + clause_density * 2 + max_depth / 5) / 3
        return min(max(normalized, 0), 1)

    def interact(self):
        """Master-level interaction loop."""
        user_id = input("Enter your expert ID: ").strip() or "expert_user"

        print(f"\nWelcome to Master Prompt Engineering System, {user_id}!")
        print("This system generates world-class learning prompts using expert techniques.\n")

        while True:
            try:
                user_input = input("State your advanced learning request (or 'exit' to quit):\n> ").strip()

                if user_input.lower() == 'exit':
                    self._save_data()
                    print("\nSession archived in expert knowledge base.")
                    break

                if user_input.lower().startswith("meta:"):
                    user_input = user_input[5:].strip()
                    meta_prompt = self._meta_prompt(user_input)
                    print("\n[META-PROMPT FOR SELF-IMPROVEMENT]")
                    print(meta_prompt)
                    continue

                expert_analysis = self._analyze_with_expertise(user_input)
                print(f"\n[ANALYSIS] Depth: {expert_analysis['depth_level'].upper()}, Style: {expert_analysis['learning_style']}")

                master_prompt = self._craft_master_prompt(expert_analysis)
                print("\n[MASTER PROMPT]")
                print(master_prompt)

                self._update_expert_knowledge(user_id, user_input, master_prompt, expert_analysis)

            except Exception as e:
                print(f"Error in prompt generation: {str(e)}")
                continue

if __name__ == "__main__":
    try:
        expert_system = MasterPromptEngineer()
        expert_system.interact()
    except Exception as e:
        print(f"Expert system error: {str(e)}")