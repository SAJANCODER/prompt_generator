import re
import json
import os
from collections import defaultdict
from fuzzywuzzy import process  # For fuzzy matching

class PromptGenerator:
    def __init__(self):
        # Custom stopwords list
        self.stopwords = self._get_stopwords()

        # User profiles storage
        self.user_profiles = {}
        self.load_user_profiles()

    def load_user_profiles(self):
        """
        Load user profiles from a JSON file.
        """
        if os.path.exists("../user/user_profiles.json"):
            with open("../user/user_profiles.json", "r") as file:
                self.user_profiles = json.load(file)

    def save_user_profiles(self):
        """
        Save user profiles to a JSON file.
        """
        with open("../user/user_profiles.json", "w") as file:
            json.dump(self.user_profiles, file, indent=4)

    def analyze_input(self, user_input):
        """
        Analyze the user's input to identify key themes and intent.
        """
        # Extract meaningful keywords
        keywords = self._extract_keywords(user_input)

        # Infer intent based on keywords
        intent = self._infer_intent(keywords)

        # Infer context based on keywords
        context = self._infer_context(keywords)

        return intent, context, keywords

    def _extract_keywords(self, user_input):
        """
        Extract meaningful keywords from the user's input.
        """
        words = re.findall(r'\b\w+\b', user_input)
        meaningful_words = [word for word in words if word.lower() not in self.stopwords and len(word) > 2]
        return meaningful_words

    def _infer_intent(self, keywords):
        """
        Infer the user's intent based on keywords.
        """
        if any(word in ["learn", "teach", "explain", "understand"] for word in keywords):
            return "learn"
        elif any(word in ["create", "write", "make", "design"] for word in keywords):
            return "create"
        elif any(word in ["solve", "fix", "resolve", "answer"] for word in keywords):
            return "solve"
        elif any(word in ["explore", "discover", "research", "investigate"] for word in keywords):
            return "explore"
        else:
            return "general"

    def _infer_context(self, keywords):
        """
        Infer the context based on keywords.
        """
        # Use fuzzy matching to find the most relevant context
        known_contexts = [
            "machine learning", "artificial intelligence", "technology", "science",
            "business", "creative", "python", "programming", "data science"
        ]
        best_match, score = process.extractOne(" ".join(keywords), known_contexts)
        return best_match if score > 70 else "general"

    def generate_prompt(self, intent, context, keywords):
        """
        Generate a prompt based on the inferred intent, context, and keywords.
        """
        if intent == "learn":
            prompt = f"Explain {context} in a clear and detailed manner, covering all key concepts and practical examples."
        elif intent == "create":
            prompt = f"Write a creative piece about {context}, focusing on originality and engaging content."
        elif intent == "solve":
            prompt = f"Provide a step-by-step solution to a problem related to {context}, including detailed explanations."
        elif intent == "explore":
            prompt = f"Explore {context} in depth, highlighting interesting facts, insights, and real-world applications."
        else:
            prompt = f"Provide a comprehensive overview of {context}, covering key aspects and examples."

        # Add keywords to the prompt for focus
        if keywords:
            prompt += f" Focus on the following: {', '.join(keywords)}."

        return prompt

    def simulate_ai_response(self, prompt):
        """
        Simulate a generative AI response (for testing purposes).
        """
        if "Explain" in prompt:
            return f"Here's a detailed explanation based on your request: {prompt}. For example, if you're learning about {prompt.split()[1]}, it involves..."
        elif "Write" in prompt:
            return f"Here's a creative piece based on your request: {prompt}. Once upon a time, in a world of {prompt.split()[-1]}..."
        elif "Provide a step-by-step solution" in prompt:
            return f"Here's a step-by-step solution: {prompt}. First, identify the problem. Then, brainstorm possible solutions..."
        else:
            return f"Here's an overview: {prompt}. This topic covers a wide range of ideas and concepts."

    def interact_with_user(self, user_id):
        """
        Interact with the user to refine the prompt and save user preferences.
        """
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                "preferences": {"tone": "neutral", "context": "general", "intent": "explore"},
                "history": []
            }

        user_profile = self.user_profiles[user_id]
        print(f"Welcome back, User {user_id}!" if user_profile["history"] else f"Welcome, User {user_id}!")

        while True:
            user_input = input("\nWhat would you like to ask or explore? (Type 'exit' to quit): ").strip()
            if user_input.lower() == "exit":
                print("Thank you for using the AI Prompt Generator. Goodbye!")
                self.save_user_profiles()
                break

            # Analyze the input
            intent, context, keywords = self.analyze_input(user_input)

            # Generate the initial prompt
            prompt = self.generate_prompt(intent, context, keywords)
            print(f"\nGenerated Prompt: {prompt}")

            # Simulate generative AI response
            ai_response = self.simulate_ai_response(prompt)
            print(f"\nAI Response: {ai_response}")

            # Save interaction history
            user_profile["history"].append({"input": user_input, "prompt": prompt, "response": ai_response})

    def _get_stopwords(self):
        """
        Get a list of common stopwords.
        """
        return {"a", "an", "the", "is", "are", "in", "on", "at", "for", "with", "to", "of", "i", "want", "it", "need", "know", "about", "learn", "me", "my", "you", "your"}

# Run the Prompt Generator with User Profiles
if __name__ == "__main__":
    generator = PromptGenerator()

    # Simulate user interaction
    user_id = input("Enter your user ID: ").strip()
    generator.interact_with_user(user_id)