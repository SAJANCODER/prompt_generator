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
        """Build a comprehensive knowledge graph of technical domains."""
        return {
            "machine learning": {
                "levels": {
                    "beginner": ["basic concepts", "supervised learning", "scikit-learn"],
                    "intermediate": ["neural networks", "model evaluation", "feature engineering"],
                    "advanced": ["transformers", "reinforcement learning", "GANs"]
                },
                "tools": ["TensorFlow", "PyTorch", "Keras"],
                "applications": ["computer vision", "NLP", "predictive analytics"],
                "subtleties": [
                    "data leakage prevention",
                    "hyperparameter tuning nuances",
                    "model interpretation challenges"
                ]
            },
            "python": {
                "levels": {
                    "beginner": ["syntax", "basic data structures", "functions"],
                    "intermediate": ["decorators", "generators", "context managers"],
                    "advanced": ["metaclasses", "concurrency", "performance optimization"]
                },
                "tools": ["Django", "Flask", "FastAPI"],
                "applications": ["web development", "data analysis", "automation"],
                "subtleties": [
                    "GIL implications",
                    "memory management",
                    "duck typing nuances"
                ]
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
        """Perform deep analysis using expert techniques."""
        doc = self.nlp(user_input)

        # Extract conceptual depth
        depth_terms = {
            "surface": ["basic", "intro", "overview"],
            "deep": ["advanced", "in-depth", "comprehensive"],
            "master": ["cutting-edge", "state-of-the-art", "research"]
        }

        depth = "deep"
        for token in doc:
            for level, terms in depth_terms.items():
                if token.text.lower() in terms:
                    depth = level

        # Detect learning objectives
        objectives = []
        for chunk in doc.noun_chunks:
            if chunk.root.pos_ in ("NOUN", "PROPN") and chunk.text.lower() not in ["i", "you"]:
                objectives.append(chunk.text)

        return {
            "primary_topic": objectives[0] if objectives else "technology",
            "depth_level": depth,
            "learning_style": self._detect_expert_learning_style(doc),
            "cognitive_load": self._assess_cognitive_load(doc),
            "preferred_modalities": self._detect_modalities(doc)
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