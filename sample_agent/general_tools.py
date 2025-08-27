from datetime import datetime
from google.adk.tools import ToolContext, FunctionTool, BaseTool
from typing import List, Dict, Optional, Callable
from enum import IntEnum

class ToolTier(IntEnum):
    """Tool access tiers based on user plan"""
    BASIC = 1
    PRO = 2
    TEAM = 3

def requires_tier(minimum_tier: ToolTier):
    """Decorator to mark functions with minimum tier requirements"""
    def decorator(func: Callable):
        func._minimum_tier = minimum_tier
        return func
    return decorator

@requires_tier(ToolTier.BASIC)
def get_current_time():
    """
    Returns the current time as a string in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@requires_tier(ToolTier.BASIC)
def send_support_link():
    """
    Returns the support page link.
    """
    support_link = "https://help.openai.com/en"
    return support_link

@requires_tier(ToolTier.BASIC)
def retrieve_user_plan(tool_context: ToolContext) -> dict:
    """
    Returns the current user plan
    """
    plan_name = tool_context.state.get("plan_name", "Basic Plan")

    return plan_name

@requires_tier(ToolTier.BASIC)
def upgrade_user_plan(tool_context: ToolContext) -> dict:
    """
    Upgrades the user's plan to a Pro.
    """
    tool_context.state["plan_name"] = "Pro Plan"
    tool_context.state["plan"] = 2
    return {"message": "User plan upgraded to Pro."}

@requires_tier(ToolTier.PRO)
def get_weather(city: str, tool_context: ToolContext) -> dict:
    """
    Returns the current weather in a specific location
    """
    return {    
        "city": city,
        "temperature": "22°C",
        "condition": "Sunny"
    }

class GeneralToolset():
    """Manages tool access based on user plan using tier decorators"""
    
    def __init__(self):
        self.toolset = [
            FunctionTool(func=get_current_time),
            FunctionTool(func=send_support_link),
            FunctionTool(func=retrieve_user_plan),
            FunctionTool(func=upgrade_user_plan),
            FunctionTool(func=get_weather),
        ]
        self._log("Toolset initialized")

    def get_tools(self, state: Optional[Dict] = None) -> List[BaseTool]:
        """Return appropriate tools based on user state and plan"""
        user_tier = self._get_user_tier(state)

        # Filter tools based on tier requirements
        available_tools = []
        for tool in self.toolset:
            required_tier = getattr(tool.func, '_minimum_tier', ToolTier.BASIC)
            if user_tier >= required_tier:
                available_tools.append(tool)
        
        self._log(f"User tier: {user_tier.name}, returning {len(available_tools)} tools: {[t.name for t in available_tools]}")
        return available_tools
    
    def get_all_tools(self) -> List[BaseTool]:
        """Return all available tools (bypasses tier filtering)"""
        self._log(f"Returning all {len(self.toolset)} tools: {[t.name for t in self.toolset]}")
        return self.toolset
    
    def _get_user_tier(self, state: Optional[Dict]) -> ToolTier:
        """Determine user tier based on state"""
        plan_id = state.get('plan', 1)
        try:
            user_tier = ToolTier(plan_id)  # Direct conversion
        except ValueError:
            user_tier = ToolTier.BASIC
        
        return user_tier
    
    def _log(self, message: str) -> None:
        """Centralized logging"""
        print(message)