"""
Prompt templates for the deep research system.

This module contains all prompt templates used across the research workflow components,
including user clarification, research brief generation, and report synthesis.
"""

from langsmith import Client

# Load the prompt from prompt hub
client = Client()
clarify_with_user_instructions = client.pull_prompt("clarify_with_user_instructions")
transform_messages_into_research_topic_prompt = client.pull_prompt("transform_messages_into_research_topic_prompt")
research_agent_prompt = client.pull_prompt("research_agent_prompt")
summarize_webpage_prompt = client.pull_prompt("summarize_webpage_prompt")
compress_research_system_prompt = client.pull_prompt("compress_research_system_prompt")
compress_research_human_message = client.pull_prompt("compress_research_human_message")
lead_researcher_prompt = client.pull_prompt("lead_researcher_prompt")