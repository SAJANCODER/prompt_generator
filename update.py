import re
import json
import os
from collections import defaultdict
from fuzzywuzzy import process  # For fuzzy matching


class PromptGenerator:
    def __init__(self):
        # Predefined rules for intent recognition and prompt structuring
        self.intent_keywords = {
            "learn": ["learn", "teach", "explain", "understand", "know"],
            "create": ["write", "create", "make", "compose", "design"],
            "solve": ["solve", "fix", "resolve", "answer", "help with"],
            "explore": ["explore", "discover", "find out", "research", "investigate"]
        }
        self.context_keywords = {
            "machine learning": ["machine learning", "ml", "supervised learning", "unsupervised learning",
                                 "reinforcement learning", "neural networks"],
            "artificial intelligence": ["AI", "artificial intelligence", "neural networks", "deep learning",
                                        "natural language processing"],
            "technology": ["technology", "robotics", "quantum computing", "blockchain", "internet of things", "IoT"],
            "science": ["space", "physics", "chemistry", "biology", "astronomy", "geology"],
            "business": ["market trends", "e-commerce", "startups", "finance", "entrepreneurship", "marketing"],
            "creative": ["story", "poem", "art", "music", "design", "photography"]
        }
        self.tone_keywords = {
            "formal": ["formal", "professional", "academic"],
            "casual": ["casual", "informal", "friendly"],
            "technical": ["technical", "detailed", "scientific"],
            "creative": ["creative", "imaginative", "artistic"]
        }

        # Custom sentiment analysis (basic rule-based)
        self.sentiment_words = {
            "positive": ["good", "great", "awesome", "amazing", "love"],
            "negative": ["bad", "terrible", "awful", "hate", "dislike"]
        }

        # User profiles storage
        self.user_profiles = {}
        self.load_user_profiles()

        # Custom stopwords list
        self.stopwords = self._get_stopwords()

    def load_user_profiles(self):
        """
        Load user profiles from a JSON file.
        """
        if os.path.exists("user_profiles.json"):
            with open("user_profiles.json", "r") as file:
                self.user_profiles = json.load(file)

    def save_user_profiles(self):
        """
        Save user profiles to a JSON file.
        """
        with open("user_profiles.json", "w") as file:
            json.dump(self.user_profiles, file, indent=4)

    def analyze_input(self, user_input):
        """
        Analyze the user's input to identify intent, context, tone, and sentiment.
        """
        intent = self._identify_intent(user_input)
        context = self._identify_context(user_input)
        tone = self._identify_tone(user_input)
        sentiment = self._analyze_sentiment(user_input)
        entities = self._extract_entities(user_input)
        return intent, context, tone, sentiment, entities

    def _identify_intent(self, user_input):
        """
        Identify the user's intent based on keywords.
        """
        for intent, keywords in self.intent_keywords.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                return intent
        return "explore"  # Default intent if no specific intent is found

    def _identify_context(self, user_input):
        """
        Identify the context of the user's input using fuzzy matching.
        """
        # Flatten the context_keywords dictionary into a list of phrases
        all_phrases = [phrase for phrases in self.context_keywords.values() for phrase in phrases]

        # Use fuzzy matching to find the best match
        best_match, score = process.extractOne(user_input.lower(), all_phrases)

        # If the match score is above a threshold, return the corresponding context
        if score > 70:  # Adjust threshold as needed
            for context, phrases in self.context_keywords.items():
                if best_match in phrases:
                    return context
        return "general"  # Default context if no specific context is found

    def _identify_tone(self, user_input):
        """
        Identify the desired tone based on keywords.
        """
        for tone, keywords in self.tone_keywords.items():
            if any(keyword.lower() in user_input.lower() for keyword in keywords):
                return tone
        return "neutral"  # Default tone if no specific tone is found

    def _analyze_sentiment(self, user_input):
        """
        Perform basic sentiment analysis on the user's input.
        """
        positive_count = sum(user_input.lower().count(word) for word in self.sentiment_words["positive"])
        negative_count = sum(user_input.lower().count(word) for word in self.sentiment_words["negative"])
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"

    def _extract_entities(self, user_input):
        """
        Extract key entities (nouns) from the user's input, excluding stopwords and irrelevant words.
        """
        words = re.findall(r'\b\w+\b', user_input)
        # Focus on meaningful keywords
        meaningful_words = [word for word in words if word.lower() not in self.stopwords and len(word) > 2]
        return meaningful_words

    def _get_stopwords(self):
        """
        Get a list of common stopwords.
        """
        return {"a", "an", "the", "is", "are", "in", "on", "at", "for", "with", "to", "of", "i", "want", "it", "need",
                "know", "about", "learn", "me", "my", "you", "your"}

    def generate_prompt(self, intent, context, tone, sentiment, entities):
        """
        Generate a prompt based on the identified intent, context, tone, sentiment, and entities.
        """
        prompt = ""

        # Define prompt templates based on intent
        if intent == "learn":
            prompt = f"Provide a comprehensive explanation of {context}, covering all key concepts and practical examples. Ensure the explanation is {tone} and easy to understand."
        elif intent == "create":
            prompt = f"Write a {tone} {context} piece, focusing on creativity and originality. Include vivid descriptions and engaging content."
        elif intent == "solve":
            prompt = f"Provide a step-by-step solution to a problem related to {context}. Ensure the solution is {tone} and includes detailed explanations."
        elif intent == "explore":
            prompt = f"Explore {context} in a {tone} way, highlighting interesting facts, insights, and real-world applications."
        else:
            prompt = f"Provide a {tone} overview of {context}, covering key aspects and examples."

        # Add sentiment and entities to the prompt
        if sentiment != "neutral":
            prompt += f" The response should have a {sentiment} tone."
        if entities:
            prompt += f" Focus on the following: {', '.join(entities)}."

        return prompt

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
            intent, context, tone, sentiment, entities = self.analyze_input(user_input)

            # Update user preferences based on the current input
            user_profile["preferences"]["tone"] = tone
            user_profile["preferences"]["context"] = context
            user_profile["preferences"]["intent"] = intent

            # Generate the initial prompt
            prompt = self.generate_prompt(intent, context, tone, sentiment, entities)
            print(f"\nGenerated Prompt: {prompt}")

            # Simulate generative AI response
            ai_response = self.simulate_ai_response(prompt)
            print(f"\nAI Response: {ai_response}")

            # Save interaction history
            user_profile["history"].append({"input": user_input, "prompt": prompt, "response": ai_response})

    def simulate_ai_response(self, prompt):
        """
        Simulate a generative AI response (for testing purposes).
        """
        # Simulate a detailed response based on the prompt
        if "Provide a comprehensive explanation" in prompt:
            return f"Here's a detailed explanation based on your request: {prompt}. For example, machine learning involves algorithms that improve automatically through experience. Key concepts include supervised learning, unsupervised learning, and reinforcement learning. Practical examples include image recognition, natural language processing, and recommendation systems."
        elif "Write a" in prompt:
            return f"Here's a creative piece based on your request: {prompt}. Once upon a time, in a world of {prompt.split()[-1]}..."
        elif "Provide a step-by-step solution" in prompt:
            return f"Here's a step-by-step solution: {prompt}. First, identify the problem. Then, brainstorm possible solutions..."
        else:
            return f"Here's an overview: {prompt}. This topic covers a wide range of ideas and concepts."


# Run the Prompt Generator with User Profiles
if __name__ == "__main__":
    generator = PromptGenerator()

    # Simulate user interaction
    user_id = input("Enter your user ID: ").strip()
    generator.interact_with_user(user_id)