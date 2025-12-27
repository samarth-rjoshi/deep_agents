
"""
Full Multi-Agent Research System

This module integrates all components of the research system:
- User clarification and scoping
- Research brief generation  
- Multi-agent research coordination
- Final report generation

The system orchestrates the complete research workflow from initial user
input through final report delivery.
"""

from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END

from deep_research.utils.common import get_today_str, init_model
from deep_research.prompts import final_report_generation_prompt
from deep_research.state.scope import AgentState, AgentInputState
from deep_research.agents.research_scope import clarify_with_user, write_research_brief
from deep_research.agents.supervisor import supervisor_agent
from deep_research.utils.logger import logger

# ===== Config =====

import os
from langchain_openai import ChatOpenAI
writer_model = init_model(model=os.getenv("GENERATION_MODEL", "gpt-4o"), max_tokens=32000)

# ===== FINAL REPORT GENERATION =====

from deep_research.state.scope import AgentState

async def final_report_generation(state: AgentState):
    """
    Final report generation node.

    Synthesizes all research findings into a comprehensive final report
    """
    try:
        logger.info("Generating final report")
        notes = state.get("notes", [])

        findings = "\n".join(notes)

        final_report_prompt = final_report_generation_prompt.format(
            research_brief=state.get("research_brief", ""),
            findings=findings,
            date=get_today_str()
        )

        final_report = await writer_model.ainvoke([HumanMessage(content=final_report_prompt)])

        return {
            "final_report": final_report.content, 
            "messages": ["Here is the final report: " + final_report.content],
        }
    except Exception as e:
        logger.error(f"Error in final_report_generation: {e}", exc_info=True)
        raise e

# ===== GRAPH CONSTRUCTION =====
# Build the overall workflow
deep_researcher_builder = StateGraph(AgentState, input_schema=AgentInputState)

# Add workflow nodes
deep_researcher_builder.add_node("clarify_with_user", clarify_with_user)
deep_researcher_builder.add_node("write_research_brief", write_research_brief)
deep_researcher_builder.add_node("supervisor_subgraph", supervisor_agent)
deep_researcher_builder.add_node("final_report_generation", final_report_generation)

# Add workflow edges
deep_researcher_builder.add_edge(START, "clarify_with_user")
deep_researcher_builder.add_edge("write_research_brief", "supervisor_subgraph")
deep_researcher_builder.add_edge("supervisor_subgraph", "final_report_generation")
deep_researcher_builder.add_edge("final_report_generation", END)

# Compile the full workflow
agent = deep_researcher_builder.compile()
