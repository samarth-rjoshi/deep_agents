
from pathlib import Path

def _load_prompt(filename: str) -> str:
    """Load a prompt from a markdown file in the current directory."""
    try:
        current_dir = Path(__file__).parent
        file_path = current_dir / filename
        return file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error loading prompt {filename}: {e}")
        return ""

# Load prompts
clarify_with_user_instructions = _load_prompt("clarify_with_user_instructions.md")
transform_messages_into_research_topic_prompt = _load_prompt("transform_messages_into_research_topic.md")
research_agent_prompt = _load_prompt("research_agent.md")
summarize_webpage_prompt = _load_prompt("summarize_webpage.md")
research_agent_prompt_with_mcp = _load_prompt("research_agent_with_mcp.md")
lead_researcher_prompt = _load_prompt("lead_researcher.md")
compress_research_system_prompt = _load_prompt("compress_research_system.md")
compress_research_human_message = _load_prompt("compress_research_human.md")
final_report_generation_prompt = _load_prompt("final_report_generation.md")
BRIEF_CRITERIA_PROMPT = _load_prompt("brief_criteria.md")
BRIEF_HALLUCINATION_PROMPT = _load_prompt("brief_hallucination.md")
