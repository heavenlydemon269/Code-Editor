# ai_manager.py
import ast

class AIManager:
    def __init__(self, project="calculator"):
        self.project = project
        self.required_funcs = {
            "calculator": ["add", "subtract", "multiply", "divide"]
        }

    def analyze_code(self, code: str) -> str:
        feedback = []
        try:
            tree = ast.parse(code)
            funcs = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            
            required = self.required_funcs.get(self.project, [])
            missing = [f for f in required if f not in funcs]

            if missing:
                feedback.append(f"❌ Missing functions: {', '.join(missing)}")
            else:
                feedback.append("✅ All required functions are implemented!")

            # Style check example
            if "print(" not in code:
                feedback.append("⚠️ You should include test prints to show output.")
        except Exception as e:
            feedback.append(f"Error analyzing code: {e}")
        
        return "\n".join(feedback)
