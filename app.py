# app.py

import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote
import random

# Define the AIStudyPlanner class
class AIStudyPlanner:
    def __init__(self, search_engine="google"):
        self.search_engine = search_engine
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def search_web(self, query, num_results=5):
        if self.search_engine == "google":
            url = f"https://www.google.com/search?q={quote(query)}&num={num_results}"
        elif self.search_engine == "duckduckgo":
            url = f"https://duckduckgo.com/search?q={quote(query)}&kl=wt-wt&df=y&no_redirect=1&num={num_results}"
        else:
            raise ValueError("Unsupported search engine")

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            results = []
            if self.search_engine == "google":
                for g in soup.find_all('div', class_='g'):
                    anchors = g.find_all('a')
                    if anchors:
                        href = anchors[0]['href']
                        if href.startswith("http"):
                            results.append(href)
            elif self.search_engine == "duckduckgo":
                for a in soup.find_all('a', class_='result__a'):
                    if a and a.has_attr('href'):
                        href = a['href']
                        if href.startswith("http"):
                            results.append(href)
            return results
        except requests.exceptions.RequestException as e:
            st.error(f"Error during web search: {e}")
            return []

    def search_youtube(self, query, num_results=3):
        youtube_query = f"{query} tutorial"
        url = f"https://www.youtube.com/results?search_query={quote(youtube_query)}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            video_ids = re.findall(r"\"videoId\":\"([a-zA-Z0-9_-]{11})\"", str(soup))
            video_urls = [f"https://www.youtube.com/watch?v={video_id}" for video_id in video_ids[:num_results]]
            return video_urls
        except requests.exceptions.RequestException as e:
            st.error(f"Error during YouTube search: {e}")
            return []

    def generate_study_plan(self, topic):
        st.write(f"Generating study plan for: **{topic}**...")
        web_resources = self.search_web(topic, num_results=10)
        youtube_resources = self.search_youtube(topic)

        st.write("### Web Resources:")
        unique_web = []
        for i, url in enumerate(web_resources):
            if url not in unique_web:
                unique_web.append(url)
                st.write(f"{len(unique_web)}. [{url}]({url})")

        st.write("### YouTube Resources:")
        for i, url in enumerate(youtube_resources):
            st.write(f"{i + 1}. [{url}]({url})")

        if not unique_web and not youtube_resources:
            st.warning("No resources found. Try a more specific topic.")
        return {"web_resources": unique_web, "youtube_resources": youtube_resources}

    def generate_6week_plan(self, topic):
        st.write(f"Generating 6-week study plan for: **{topic}**...")
        resources = self.generate_study_plan(topic)
        web_resources = resources["web_resources"]
        youtube_resources = resources["youtube_resources"]

        weeks = [
            "Week 1: Introduction and Fundamentals",
            "Week 2: Core Concepts and Principles",
            "Week 3: Advanced Topics and Applications",
            "Week 4: Practical Exercises and Projects",
            "Week 5: Review and Consolidation",
            "Week 6: Final Preparation and Practice",
        ]

        random.shuffle(web_resources)

        for i, week in enumerate(weeks):
            st.write(f"#### {week}:")
            st.write("**Study from these resources:**")
            week_resources = web_resources[i::6]
            for j, url in enumerate(week_resources):
                st.write(f"{j + 1}. [{url}]({url})")
            if len(youtube_resources) > 0:
                st.write("**Watch these videos:**")
                for j, url in enumerate(youtube_resources):
                    if j % 6 == i:
                        st.write(f"{j + 1}. [{url}]({url})")

            st.write("**Activities:**")
            if i == 0:
                st.write("- Define key terms and concepts.")
                st.write("- Create a mind map of the topic.")
            elif i == 1:
                st.write("- Work through examples and solve practice problems.")
                st.write("- Compare and contrast different approaches.")
            elif i == 2:
                st.write("- Explore real-world applications.")
                st.write("- Research related subtopics.")
            elif i == 3:
                st.write("- Start a small project related to the topic.")
                st.write("- Complete coding exercises or practice problems.")
            elif i == 4:
                st.write("- Review notes and key concepts.")
                st.write("- Create flashcards for important terms.")
            elif i == 5:
                st.write("- Take practice quizzes and exams.")
                st.write("- Focus on areas where you need improvement.")

# Streamlit App
def main():
    st.title("AI Study Planner 🚀")
    st.write("Welcome to the AI Study Planner! Enter a topic, and we'll generate a personalized study plan for you.")

    # User input for the topic
    topic = st.text_input("Enter the topic you want to study:")

    if st.button("Generate Study Plan"):
        if topic:
            planner = AIStudyPlanner()
            planner.generate_6week_plan(topic)
        else:
            st.warning("Please enter a topic to generate a study plan.")

# Run the Streamlit app
if __name__ == "__main__":
    main()