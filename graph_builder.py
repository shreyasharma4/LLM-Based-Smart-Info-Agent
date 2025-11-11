import re
import json
import traceback
from langgraph.graph import StateGraph, END
from app.llm_client import get_llm, get_tools


def build_graph():
    """
    AzureOpenAI + Tools agent.
    The LLM decides when to use a tool (like weather or crypto)
    and summarizes naturally — no rule-based logic.
    """

    llm = get_llm()
    tools = get_tools()

    graph = StateGraph(dict)

    def call_tool(tool_obj, args: dict):
        """Safely execute a tool whether it's a StructuredTool or a plain Python function."""
        try:
            if hasattr(tool_obj, "invoke"):
                return tool_obj.invoke(args)
            elif callable(tool_obj):
                return tool_obj(**args)
            else:
                return f"Invalid tool type: {type(tool_obj)}"
        except Exception as e:
            return f"Error while executing tool: {e}"

    def llm_node(state):
        query = state.get("query", "").strip()
        if not query:
            state["response"] = "Please type something."
            return state

        try:
            # 🧠 System message guiding the LLM to use tools intelligently
            system_prompt = (
                "You are a smart assistant that can use external tools when needed. "
                "If the user’s query requires real or external data (like weather, crypto price, "
                "comparisons, or history), respond **only** in this JSON format:\n"
                '{"tool": "<tool_name>", "args": {"key": "value"}}\n\n'
                "Available tools and examples:\n"
                "- get_weather → {'tool': 'get_weather', 'args': {'city': 'Noida'}}\n"
                "- compare_weather → {'tool': 'compare_weather', 'args': {'cities': ['Delhi', 'Mumbai']}}\n"
                "- get_crypto_price → {'tool': 'get_crypto_price', 'args': {'symbol': 'bitcoin'}}\n"
                "- compare_crypto_prices → {'tool': 'compare_crypto_prices', 'args': {'symbols': ['bitcoin', 'ethereum']}}\n"
                "- get_crypto_history → {'tool': 'get_crypto_history', 'args': {'symbol': 'bitcoin', 'period': '3months'}}\n\n"
                "If no tool is required, reply directly in natural human language."
            )

            # 🧩 Step 1: Ask LLM to reason and decide whether to call a tool
            response = llm.chat.completions.create(
                model="o3-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query},
                ],
            )

            raw = response.choices[0].message.content.strip()

            # 🧩 Step 2: Check for tool call pattern
            if '"tool"' in raw:
                try:
                    parsed_match = re.search(r"\{.*\}", raw, re.S)
                    if not parsed_match:
                        state["response"] = "Tool call format invalid."
                        return state

                    parsed = json.loads(parsed_match.group())
                    tool_name = parsed.get("tool")
                    args = parsed.get("args", {})

                    if tool_name not in tools:
                        state["response"] = f"Unknown tool '{tool_name}'."
                        return state

                    # 🧩 Step 3: Run the requested tool safely
                    tool_obj = tools[tool_name]
                    result = call_tool(tool_obj, args)

                    # 🧩 Step 4: Let the LLM summarize the tool’s result conversationally
                    followup = llm.chat.completions.create(
                        model="o3-mini",
                        messages=[
                            {
                                "role": "system",
                                "content": "You summarize tool outputs conversationally and naturally for the user.",
                            },
                            {
                                "role": "user",
                                "content": f"Tool '{tool_name}' returned: {result}. Summarize naturally for the user.",
                            },
                        ],
                    )

                    state["response"] = followup.choices[0].message.content.strip()
                    return state

                except Exception:
                    state["response"] = f"Could not parse tool JSON. Raw output: {raw}"
                    return state

            # 🧩 Step 5: Otherwise, treat it as a direct LLM response
            state["response"] = raw
            return state

        except Exception as e:
            traceback.print_exc()
            state["response"] = f"Error calling Azure LLM: {e}"
            return state

    # 🔗 Graph configuration
    graph.add_node("llm_agent", llm_node)
    graph.add_edge("llm_agent", END)
    graph.set_entry_point("llm_agent")

    return graph.compile()
