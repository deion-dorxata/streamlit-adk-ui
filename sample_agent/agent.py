from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from typing import Optional

from .general_tools import GeneralToolset
general_toolset = GeneralToolset()

def set_initial_state(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Callback function to set the initial state of the tool
    """
    # Handle the initialized key safely
    if callback_context.state.get("initialized", False):
        print("State already initialized, skipping.")   
    else:
        print("Setting initial state for the agent.")
        callback_context.state["initialized"] = True
        callback_context.state["session_id"] = callback_context._invocation_context.session.id
        callback_context.state["id"] = callback_context._invocation_context.user_id
    return None

def before_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Callback function to update the toolset based on the current state of the agent.
    """

    ## Set the initial state if not already set
    set_initial_state(callback_context)
    print("Before agent callback triggered.")
    print(f"Current state: {callback_context.state}")

    # Update the toolset based on the current state
    general_tools = general_toolset.get_tools(callback_context.state)
    root_agent.tools = general_tools

    return None

root_agent = Agent(
    name="basic_agent",
    model="gemini-2.0-flash",
    description="An agent that has access to different tools such as time and weather lookup",
    instruction="""
You are an AI agent that can perform various tasks using tools. Some of these tools are dependent on the user's plan.
The Basic Plan has access to the tools:
- get_current_time
- send_support_link
- retrieve_user_plan
- upgrade_user_plan
The Pro Plan has access to all tools, including:
- get_weather
Always start by listing all the tools available to the user based on their current plan. Use the retrieve_user_plan tool to get the user's current plan and display it to them.
If the request needs a tool that is not available in the current plan, you should inform the user and suggest upgrading their plan.
    """,
    before_agent_callback=before_agent_callback,
)