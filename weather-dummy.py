from mcp.server.mcpserver import MCPServer

mcp = MCPServer("weather")

@mcp.tool()
def get_weather(city:str)->dict:
    """
       MANDATORY TOOL.

    You MUST always call this tool for ANY weather & temperature related question.

    After calling this tool:
    - You MUST return EXACTLY the tool result.
    - Do NOT add any explanation.
    - Do NOT add forecast.
    - Do NOT add commentary.
    - Do NOT modify the output.
    - Return the result verbatim.
    """
    
    return {
        "location":city,
        "temperature":"10 C",
        "condition": "Cold"
    }
    
    if __name__=="__main__":
        mcp.run()
    