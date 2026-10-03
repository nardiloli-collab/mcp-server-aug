from mcp.server.mcpserver import MCPServer
import requests
import yfinance as yf

mcp = MCPServer("crypto-stock")

@mcp.tool()
def get_crypto_price(crypto:str)->str:
    """
        Get the current USD price of a cryptocurrency.
        Pass the coingeco coin id (lower case full name), not  the ticker symbol
        - bitcoin not (not BTC)
        - ethereum not ETH
        - solana
        - dogecoin
    """
    coin_id = crypto.strip().lower()
    
    aliases = {
        "btc":"bitcoin",
        "eth":"ethereum",
        "sol":"solana",
        "ada":"cardano",
        "xrp":"ripple"
        
    }
    
    coin_id = aliases.get(coin_id, coin_id)
    
    url = "https://api.coingecko.com/api/v3/simple/price"
    
    try:
        response = requests.get(
            url, 
            params = {"ids":coin_id,"vs_currencies":"usd"},
            timeout = 10
        )
        response.raise_for_status()
        data = response.json()
        if coin_id not in data:
            return (
                f"Cryptocurrency '{crypto}' not found."
            )
        return f"{coin_id} price: ${data[coin_id]['usd']} USD"
    except Exception as e:
        return str(e)

@mcp.resource(
    "market analysis"
) 
def supported_assets()->str:
    """
    Provides information about the assets supported by the MCP server.

    A resource is DATA that the MCP client can read.
    """

    return """
SUPPORTED CRYPTOCURRENCIES
==========================

Bitcoin
  CoinGecko ID: bitcoin
  Ticker: BTC

Ethereum
  CoinGecko ID: ethereum
  Ticker: ETH

Solana
  CoinGecko ID: solana
  Ticker: SOL

Cardano
  CoinGecko ID: cardano
  Ticker: ADA

Ripple
  CoinGecko ID: ripple
  Ticker: XRP

Dogecoin
  CoinGecko ID: dogecoin
  Ticker: DOGE


SUPPORTED STOCKS
================

The server uses Yahoo Finance through yfinance.

Examples:

AAPL  - Apple
MSFT  - Microsoft
NVDA  - NVIDIA
GOOGL - Alphabet
AMZN  - Amazon
META  - Meta
TSLA  - Tesla


AVAILABLE TOOLS
===============

get_crypto_price(crypto)
    Get the current cryptocurrency price.

get_stock_price(symbol)
    Get the latest stock price.
"""

@mcp.prompt(
    name="analyze_market",
    title="Analyze Market",
    description="Generate a market analysis request for a cryptocurrency or stock"
)
def analyze_market(
    symbol: str,
    asset_type: str = "stock"
) -> str:
    """
    Generate a reusable market-analysis prompt.

    This is a PROMPT, not a tool.

    The user can select this prompt from an MCP client
    and provide the asset symbol.
    """

    if asset_type.lower() == "crypto":

        return f"""
Analyze the cryptocurrency {symbol}.

Please:

1. Get its current USD price.
2. Identify the cryptocurrency.
3. Explain the current market context.
4. Discuss important factors that could affect its price.
5. Identify key risks.
6. Provide a concise summary.

Use the MCP tool get_crypto_price to retrieve
the current price before performing the analysis.

Do not invent market data.
Clearly distinguish current data from general analysis.
"""

    else:

        return f"""
Analyze the stock {symbol}.

Please:

1. Get the latest stock price.
2. Identify the company.
3. Explain the current market context.
4. Discuss important factors affecting the stock.
5. Identify key risks.
6. Provide a concise summary.

Use the MCP tool get_stock_price to retrieve
the latest price before performing the analysis.

Do not invent market data.
Clearly distinguish current data from general analysis.
"""
    
@mcp.tool()
def get_stock_price(symbol:str)->str:
    """ Get the latest stock price 
    examples
    APPL, NVDA, MSFT
    """
    
    try:
        ticker = yf.Ticker(symbol.upper())
        hist = ticker.history(period = '1d')
        
        if hist.empty:
            return f"Stock '{symbol}' not found"
        price = round(hist["Close"].iloc[-1],2)
        
        return f"{symbol.upper()} stock price : {price}"
    
    except Exception as e:
        return str(e)
        
    
if __name__=="__main__":
    mcp.run()
        