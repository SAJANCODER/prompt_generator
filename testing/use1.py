import re
import json
import os
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Set, Any
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

    def _initialize_nlp(self):
        """Initialize NLP with the most comprehensive model."""
        try:
            nlp = spacy.load("en_core_web_lg")
        except OSError:
            warnings.warn("Downloading advanced language model...")
            spacy_download("en_core_web_lg")
            nlp = spacy.load("en_core_web_lg")
        return nlp

    def _build_knowledge_graph(self) -> Dict[str, Any]:
        """A globally comprehensive knowledge graph of programming languages and technical domains."""
        return {
            # === Mainstream General-Purpose Languages ===
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
            "javascript": {
                "levels": {
                    "beginner": ["DOM manipulation", "ES6 syntax", "callbacks"],
                    "intermediate": ["React/Vue", "Node.js", "WebSockets"],
                    "advanced": ["WebAssembly", "V8 optimizations", "microfrontends"],
                    "expert": ["JIT compilation", "memory leaks debugging", "low-latency systems"]
                },
                "paradigms": ["event-driven", "OOP", "functional"],
                "use_cases": ["frontend", "backend", "mobile (React Native)"],
                "tools": ["Next.js", "Express", "TypeScript", "Webpack"],
                "subtleties": ["hoisting", "this binding", "event loop quirks"]
            },
            "java": {
                "levels": {
                    "beginner": ["OOP", "collections", "JDBC"],
                    "intermediate": ["Spring Boot", "concurrency", "JVM tuning"],
                    "advanced": ["bytecode manipulation", "GraalVM", "distributed systems"],
                    "expert": ["HotSpot internals", "GC algorithms", "JIT optimizations"]
                },
                "paradigms": ["OOP", "functional (streams)"],
                "use_cases": ["enterprise apps", "Android", "big data"],
                "tools": ["Hibernate", "Kafka", "Maven", "Quarkus"],
                "subtleties": ["classloading", "memory leaks in JNI", "biased locking"]
            },
            "c++": {
                "levels": {
                    "beginner": ["syntax", "pointers", "OOP"],
                    "intermediate": ["templates", "RAII", "STL"],
                    "advanced": ["move semantics", "constexpr", "template metaprogramming"],
                    "expert": ["undefined behavior", "memory model", "lock-free programming"]
                },
                "paradigms": ["OOP", "procedural", "generic", "low-level"],
                "use_cases": ["game dev", "embedded", "HFT"],
                "tools": ["CMake", "Boost", "Qt", "Unreal Engine"],
                "subtleties": ["ODR violations", "exception safety", "ABI compatibility"]
            },

            # === Emerging Languages ===
            "rust": {
                "levels": {
                    "beginner": ["ownership", "borrowing", "basic syntax"],
                    "intermediate": ["async/await", "FFI", "macros"],
                    "advanced": ["unsafe code", "compiler plugins", "embedded Rust"],
                    "expert": ["no_std", "WASM optimization", "custom allocators"]
                },
                "paradigms": ["systems", "functional influences"],
                "use_cases": ["blockchain", "OS dev", "performance-critical apps"],
                "tools": ["Tokio", "Actix", "Serde"],
                "subtleties": ["lifetime elision", "zero-cost abstractions", "pin/unpin"]
            },
            "go": {
                "levels": {
                    "beginner": ["goroutines", "channels", "interfaces"],
                    "intermediate": ["context handling", "profiling", "testing"],
                    "advanced": ["compiler optimizations", "embedding Go", "WASM"],
                    "expert": ["runtime hacking", "custom schedulers", "GC tuning"]
                },
                "paradigms": ["procedural", "concurrent"],
                "use_cases": ["cloud services", "CLI tools", "microservices"],
                "tools": ["Gin", "Echo", "Kubernetes"],
                "subtleties": ["escape analysis", "interface costs", "nil behavior"]
            },

            # === Specialized Languages ===
            "sql": {
                "levels": {
                    "beginner": ["SELECT", "JOINs", "GROUP BY"],
                    "intermediate": ["indexing", "window functions", "CTEs"],
                    "advanced": ["query optimization", "partitioning", "materialized views"],
                    "expert": ["distributed SQL", "lock contention", "MVCC internals"]
                },
                "paradigms": ["declarative"],
                "use_cases": ["databases", "analytics", "ETL"],
                "tools": ["PostgreSQL", "MySQL", "SQLite", "Snowflake"],
                "subtleties": ["N+1 problem", "transaction isolation levels", "deadlocks"]
            },
            "r": {
                "levels": {
                    "beginner": ["vectors", "data frames", "basic stats"],
                    "intermediate": ["dplyr", "ggplot2", "shiny apps"],
                    "advanced": ["Rcpp", "performance tuning", "custom DSLs"],
                    "expert": ["memory-mapped data", "parallel computing", "R internals"]
                },
                "paradigms": ["functional", "vectorized"],
                "use_cases": ["statistics", "bioinformatics", "financial modeling"],
                "tools": ["Tidyverse", "data.table", "Shiny"],
                "subtleties": ["lazy evaluation", "copy-on-modify", "S3 vs S4"]
            },

            # === Functional Languages ===
            "haskell": {
                "levels": {
                    "beginner": ["syntax", "recursion", "ADTs"],
                    "intermediate": ["monads", "lenses", "concurrency"],
                    "advanced": ["type families", "GHC plugins", "DSL design"],
                    "expert": ["category theory", "compiler hacking", "dependent types"]
                },
                "paradigms": ["pure functional", "lazy"],
                "use_cases": ["compilers", "formal methods", "FP research"],
                "tools": ["Stack", "Lens", "Yesod"],
                "subtleties": ["lazy evaluation pitfalls", "space leaks", "TH quirks"]
            },

            # === Historical Languages ===
            "cobol": {
                "levels": {
                    "beginner": ["division structure", "data division", "procedural code"],
                    "intermediate": ["file handling", "legacy DB integration", "batch processing"],
                    "advanced": ["mainframe optimization", "CICS", "VSAM"],
                    "expert": ["Y2K remediation", "emulation layers", "migration strategies"]
                },
                "paradigms": ["procedural"],
                "use_cases": ["banking", "government", "legacy systems"],
                "tools": ["IBM COBOL", "GnuCOBOL", "Micro Focus"],
                "subtleties": ["fixed-format syntax", "EBCDIC issues", "decimal arithmetic"]
            },

            # === Esoteric Languages ===
            "brainfuck": {
                "levels": {
                    "beginner": ["syntax (8 commands)", "basic loops"],
                    "intermediate": ["Turing completeness proofs", "I/O handling"],
                    "advanced": ["self-interpreters", "code golf optimizations"],
                    "expert": ["compiler construction", "obfuscation techniques"]
                },
                "paradigms": ["minimalist", "Turing tarpit"],
                "use_cases": ["challenges", "art", "education"],
                "tools": ["BF interpreters", "optimizers"],
                "subtleties": ["cell wrapping", "EOF handling", "pointer bounds"]
            },

            # === AI/LLM-Specific ===
            "prompt_engineering": {
                "levels": {
                    "beginner": ["basic prompting", "few-shot learning"],
                    "intermediate": ["chain-of-thought", "self-consistency"],
                    "advanced": ["red teaming", "activation engineering"],
                    "expert": ["latent space manipulation", "multi-agent systems"]
                },
                "paradigms": ["declarative", "iterative refinement"],
                "use_cases": ["AI assistants", "knowledge extraction"],
                "tools": ["LangChain", "LlamaIndex", "DSPy"],
                "subtleties": ["tokenization edge cases", "positional bias", "hallucination control"]
            }
        }

    def _load_data(self) -> None:
        """Load user profiles and conversation history from JSON files."""
        try:
            os.makedirs("../user", exist_ok=True)

            # Load user profiles
            if os.path.exists("../user/user_profiles.json"):
                with open("../user/user_profiles.json", "r", encoding="utf-8") as f:
                    self.user_profiles = json.load(f)

            # Load conversation history
            if os.path.exists("../user/conversation_history.json"):
                with open("../user/conversation_history.json", "r", encoding="utf-8") as f:
                    self.conversation_history = json.load(f)

        except Exception as e:
            warnings.warn(f"Could not load data: {str(e)}")
            self.user_profiles = {}
            self.conversation_history = defaultdict(list)

    def _save_data(self) -> None:
        """Save both user profiles and conversation history to JSON files."""
        try:
            # Save user profiles
            with open("../user/user_profiles.json", "w", encoding="utf-8") as f:
                json.dump(self.user_profiles, f, indent=2, ensure_ascii=False)

            # Save conversation history
            with open("../user/conversation_history.json", "w", encoding="utf-8") as f:
                json.dump(dict(self.conversation_history), f, indent=2, ensure_ascii=False)

        except Exception as e:
            warnings.warn(f"Could not save data: {str(e)}")

    def _analyze_with_expertise(self, user_input: str) -> Dict[str, Any]:
        """Perform master-level technical analysis with multi-dimensional assessment.

        Features:
        - Hierarchical depth detection (Bloom's Taxonomy + research levels)
        - Domain-aware concept extraction
        - Cognitive load estimation (Paas & Sweller model)
        - Learning style profiling (Felder-Silverman model)
        - Multi-modal preference detection
        """
        doc = self.nlp(user_input)

        # === Conceptual Depth Analysis ===
        depth_indicators = {
            "surface": {
                "terms": ["basic", "intro", "overview", "explain like I'm 5"],
                "syntax_threshold": 0.3  # Simple sentence structures
            },
            "intermediate": {
                "terms": ["implement", "optimize", "debug", "best practices"],
                "syntax_threshold": 0.6
            },
            "advanced": {
                "terms": ["low-level", "concurrency", "distributed", "kernel"],
                "syntax_threshold": 0.8
            },
            "research": {
                "terms": ["novel", "SOTA", "arXiv", "peer-reviewed", "formal proof"],
                "syntax_threshold": 0.95
            }
        }

        # Multi-factor depth assessment
        depth = "intermediate"  # Technical default
        max_depth_score = 0
        for level, indicators in depth_indicators.items():
            term_score = sum(1 for t in doc if t.text.lower() in indicators["terms"])
            syntax_score = self._calculate_syntax_complexity(doc.text)
            level_score = term_score * 0.7 + (syntax_score > indicators["syntax_threshold"]) * 0.3

            if level_score > max_depth_score:
                max_depth_score = level_score
                depth = level

        # === Domain-Aware Concept Extraction ===
        technical_stopwords = {"thing", "stuff", "way", "method", "technology"}
        objectives = []
        domain_keywords = {
            "AI/ML": ["model", "training", "neural", "transformer", "loss"],
            "Systems": ["memory", "CPU", "kernel", "scheduler", "concurrency"],
            "Frontend": ["UI", "component", "render", "DOM", "React"],
            "Data": ["query", "join", "ETL", "pipeline", "warehouse"]
        }

        for ent in doc.ents:
            if ent.label_ == "TECH_CONCEPT":
                domain = next((d for d, kws in domain_keywords.items()
                               if any(kw in ent.text.lower() for kw in kws)), "General")
                objectives.append({
                    "concept": ent.text,
                    "domain": domain,
                    "is_actionable": any(t.dep_ == "dobj" for t in ent),  # Direct object
                    "complexity": self._estimate_concept_complexity(ent.text)
                })

        # Fallback to noun chunks if no entities
        if not objectives:
            for chunk in doc.noun_chunks:
                chunk_text = chunk.text.lower()
                if (chunk.root.pos_ in ("NOUN", "PROPN") and
                        chunk_text not in technical_stopwords and
                        not chunk.root.is_stop):
                    domain = next((d for d, kws in domain_keywords.items()
                                   if any(kw in chunk_text for kw in kws)), "General")
                    objectives.append({
                        "concept": chunk.text,
                        "domain": domain,
                        "is_actionable": any(t.dep_ == "dobj" for t in chunk),
                        "complexity": 0.5  # Default medium complexity
                    })

        # === Cognitive Load Analysis ===
        cognitive_profile = {
            "load_level": self._assess_cognitive_load(doc),
            "working_memory_estimate": self._estimate_working_memory(doc),
            "prior_knowledge_index": self._estimate_prior_knowledge(doc),
            "chunking_recommendation": self._suggest_chunking_strategy(doc)
        }

        # === Multi-Modal Learning Detection ===
        modalities = self._detect_modalities(doc)
        if not modalities:  # Smart defaults based on depth
            modalities = (["visual", "kinesthetic"] if depth in ("surface", "intermediate")
                          else ["literature", "kinesthetic"])

        return {
            "primary_topic": objectives[0]["concept"] if objectives else None,
            "detailed_concepts": objectives,
            "depth_level": depth,
            "cognitive_profile": cognitive_profile,
            "preferred_modalities": modalities,
            "expert_recommendations": {
                "pedagogical_approach": self._determine_pedagogical_strategy(depth, cognitive_profile),
                "resource_types": self._suggest_resource_types(depth, objectives),
                "prerequisites": self._infer_prerequisites(objectives)
            },
            "analysis_metadata": {
                "technical_term_density": len([t for t in doc if t.text in self.tech_lexicon]) / len(doc),
                "query_complexity_score": self._calculate_query_complexity(doc),
                "temporal_context": self._detect_temporal_context(doc)  # Legacy vs cutting-edge
            }
        }

    def _detect_expert_learning_style(self, doc) -> str:
        """Detect expert-level learning preferences."""
        styles = {
            "conceptual scaffolding": ["theory", "framework", "structure"],
            "problem-based": ["solve", "fix", "debug", "issue"],
            "case-study": ["example", "case", "real-world", "application"]
        }

        for token in doc:
            for style, terms in styles.items():
                if token.text.lower() in terms:
                    return style
        return "conceptual scaffolding"

    def _assess_cognitive_load(self, doc) -> str:
        """Determine appropriate cognitive complexity."""
        indicators = {
            "low": ["intro", "basic", "simple"],
            "medium": ["understand", "implement", "apply"],
            "high": ["optimize", "master", "research", "develop"]
        }

        for token in doc:
            for load, terms in indicators.items():
                if token.text.lower() in terms:
                    return load
        return "medium"

    def _detect_modalities(self, doc) -> str:
        """Detect preferred presentation formats."""
        modalities = {
            "visual": ["see", "diagram", "visualize", "chart"],
            "mathematical": ["equation", "formula", "math", "proof"],
            "code": ["implement", "code", "program", "script"]
        }

        found = []
        for token in doc:
            for modality, terms in modalities.items():
                if token.text.lower() in terms and modality not in found:
                    found.append(modality)

        return " + ".join(found) if found else "balanced multimodal"

    def _craft_master_prompt(self, analysis: Dict[str, Any]) -> str:
        """Generate a master-level prompt using expert techniques."""
        topic = analysis["primary_topic"]
        domain_knowledge = self.knowledge_graph.get(topic.lower(), {})

        prompt = f"""
        As a world-class expert with decades of experience in {topic}, create an elite learning resource that:

        [Contextual Foundation]
        - Targets {analysis['depth_level']} understanding level
        - Incorporates {analysis['cognitive_load']} cognitive complexity
        - Uses {analysis['learning_style']} pedagogical approach

        [Technical Depth]
        - Cover these core aspects: {self._get_domain_aspects(topic, analysis['depth_level'])}
        - Include advanced techniques: {self._select_advanced_techniques(topic)}
        - Address these subtle complexities: {self._identify_subtleties(topic)}

        [Expert Delivery]
        - Employ these master techniques: {self._select_master_techniques()}
        - Structure with: {analysis['preferred_modalities']}
        - Include nuanced examples demonstrating:
          * Real-world implementation challenges
          * Professional-grade solutions
          * Cutting-edge applications

        [Output Requirements]
        - Depth comparable to academic survey papers
        - Practicality of industry best practices
        - Clarity of elite technical instruction
        """
        return self._refine_prompt(prompt)

    def _select_master_techniques(self, count: int = 3) -> str:
        """Select appropriate master-level prompting techniques."""
        return ", ".join(self.master_techniques[:count])

    def _get_domain_aspects(self, topic: str, depth: str) -> str:
        """Get relevant domain aspects based on depth level."""
        domain = self.knowledge_graph.get(topic.lower(), {})
        levels = domain.get("levels", {})
        aspects = []

        if depth == "surface":
            aspects = levels.get("beginner", [])
        elif depth == "deep":
            aspects = levels.get("intermediate", []) + levels.get("advanced", [])
        else:  # master level
            aspects = levels.get("advanced", []) + domain.get("applications", [])

        return ", ".join(aspects[:5]) if aspects else "core principles and advanced applications"

    def _select_advanced_techniques(self, topic: str) -> str:
        """Select relevant advanced techniques for the topic."""
        techniques = {
            "machine learning": [
                "attention mechanisms",
                "transfer learning",
                "neural architecture search"
            ],
            "python": [
                "metaprogramming",
                "asynchronous programming",
                "performance profiling"
            ]
        }
        return ", ".join(techniques.get(topic.lower(), ["domain-specific advanced methods"]))

    def _identify_subtleties(self, topic: str) -> str:
        """Identify subtle aspects experts should address."""
        domain = self.knowledge_graph.get(topic.lower(), {})
        return ", ".join(domain.get("subtleties", ["expert-level considerations"]))

    def _refine_prompt(self, prompt: str) -> str:
        """Refine the prompt to elite standards."""
        # Remove excessive whitespace
        prompt = re.sub(r'\n\s+', '\n', prompt).strip()
        # Ensure consistent terminology
        prompt = prompt.replace("explain", "elucidate")
        prompt = prompt.replace("show", "demonstrate")
        return prompt

    def _update_expert_knowledge(self, user_id: str, user_input: str, prompt: str, analysis: Dict[str, Any]) -> None:
        """Update the expert knowledge base with new interaction."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "analysis": analysis,
            "generated_prompt": prompt,
            "expertise_level": "master"
        }

        self.conversation_history[user_id].append(entry)

        # Update user profile if needed
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                "expertise": {},
                "preferences": {}
            }

        # Track topic expertise
        topic = analysis["primary_topic"].lower()
        self.user_profiles[user_id]["expertise"][topic] = self.user_profiles[user_id]["expertise"].get(topic, 0) + 1

    def interact(self):
        """Master-level interaction loop."""
        user_id = input("Enter your expert ID: ").strip() or "expert_user"

        print(f"\nWelcome to Master Prompt Engineering System, {user_id}!")
        print("This system generates world-class learning prompts using expert techniques.\n")

        while True:
            user_input = input("State your advanced learning request:\n> ").strip()

            if user_input.lower() == 'exit':
                self._save_data()
                print("\nSession archived in expert knowledge base.")
                break

            expert_analysis = self._analyze_with_expertise(user_input)
            master_prompt = self._craft_master_prompt(expert_analysis)

            print("\n[MASTER PROMPT]")
            print(master_prompt)

            # Save to expert knowledge base
            self._update_expert_knowledge(user_id, user_input, master_prompt, expert_analysis)


if __name__ == "__main__":
    try:
        expert_system = MasterPromptEngineer()
        expert_system.interact()
    except Exception as e:
        print(f"Expert system error: {str(e)}")