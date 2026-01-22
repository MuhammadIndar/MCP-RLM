from mcp.server.fastmcp import FastMCP
import os
import sys
from rlm_engine import run_rlm


mcp = FastMCP("RLM-Deep-Researcher")

@mcp.tool()
def analyze_massive_document(file_path: str, query: str) -> str:
    """
    Tools untuk menganalisis dokumen teks/kode yang SANGAT BESAR.
    """
    if not os.path.exists(file_path):
        return f"Error: File tidak ditemukan di path: {file_path}"
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        if not content:
            return "Error: File kosong."
        result = run_rlm(query, content)
        return result
    except Exception as e:
        return f"System Error: {str(e)}"

if __name__ == "__main__":
    sys.stderr.write("MCP RLM Server Started...\n") 
    mcp.run()


