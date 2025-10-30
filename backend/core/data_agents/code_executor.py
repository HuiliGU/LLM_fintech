from backend.utils.prompt_utils import prepare_prompt
from backend.core.llm_client import QwenV3

class codeExecutor:
    
    def __init__(self, prompt=None):
        self.prompt = prepare_prompt(prompt_name="code_fix_prompt", prompt=prompt)
        
    def excecute_code(self, code):
        code = code.strip().replace("```python", "").replace("```", "")
        local_vars = {}
        try:
            exec(code, {}, local_vars)
            return local_vars, None
        except Exception as e:
            print(f"Code execution error: {e}")
            return self.fix_code(code, str(e))
        
    def fix_code(self, code, error_message):         
        prompt_filled = self.prompt\
                .replace("{code}", code)\
                .replace("{error message}", error_message)
        codes = ""
        response_generator = QwenV3().send_text_message(
            messages=[
                {"role": "user", "content": prompt_filled}
            ]
        )
        for chunk in response_generator:
            if chunk == "[[END]]":
                break
            codes += chunk
        return codes


    

        


