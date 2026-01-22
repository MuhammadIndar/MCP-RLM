import sys
import yaml
import os
from dotenv import load_dotenv
from llm_factory import LLMBackend
from prompts import RLM_SYSTEM_PROMPT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")
ENV_PATH = os.path.join(BASE_DIR, ".env")


load_dotenv(ENV_PATH)

try:
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)
except Exception as e:
    sys.stderr.write(f"CRITICAL ERROR: Gagal load config di {CONFIG_PATH}: {e}\n")
    sys.exit(1)

root_backend = LLMBackend(config['agents']['root'], config['providers'])
sub_backend = LLMBackend(config['agents']['sub'], config['providers'])

def worker_query(query: str, context_chunk: str) -> str:
    """Fungsi yang dipanggil oleh kode Python Root LM"""
    sys_msg = "You are a specialized data extractor. Be concise and direct."
    usr_msg = f"Context snippet:\n{context_chunk}\n\nTask: {query}"
    return sub_backend.generate(sys_msg, usr_msg)

class RLMSession:
    def __init__(self, context_text: str):
        self.output_buffer = []
        self.globals = {
            "context": context_text,
            "llm_query": worker_query,
            "print": self._capture_print,
            "len": len, "range": range, "enumerate": enumerate,
            "min": min, "max": max, "int": int, "str": str, "list": list,
            "__builtins__": {}
        }
    def _capture_print(self, *args, **kwargs):
        output = " ".join(map(str, args))
        self.output_buffer.append(output)
    def execute(self, code: str) -> str:
        self.output_buffer = []
        try:
            exec(code, self.globals)
            return "\n".join(self.output_buffer) if self.output_buffer else "(Code ran successfully, no print output)"
        except Exception as e:
            return f"Runtime Error: {str(e)}"
        
def run_rlm(user_query: str, file_content: str) -> str:
    """Jantung dari RLM: Loop antara Planner (Root) dan Executor (REPL)"""
    session = RLMSession(file_content)
    history = f"User Query: {user_query}\n\nContext Info: String variable `context` loaded. Length: {len(file_content)} chars.\n"
    max_loops = config['system'].get('max_loops', 5)
    print(f"Starting RLM for query: {user_query} (Doc len: {len(file_content)})")
    for i in range(max_loops):
        print(f"--- [Turn {i+1}] Root Agent Thinking ---")
        plan = root_backend.generate(RLM_SYSTEM_PROMPT, history)
        if "```python" in plan:
            try:
                code_block = plan.split("```python")[1].split("```")[0].strip()
            except IndexError:
                code_block = plan.split("```")[1].split("```")[0].strip()
            
            print(f"--- [Turn {i+1}] Executing Code ---")
            exec_result = session.execute(code_block)
            history += f"\nAssistant Plan:\n{plan}\n\nREPL Output:\n{exec_result}\n"
            print(f"Output Preview: {exec_result[:150]}...")
        else:
            return plan
    return f"RLM limit reached. Last context:\n{history[-2000:]}"