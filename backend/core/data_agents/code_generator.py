from backend.utils.prompt_utils import prepare_prompt
from backend.core.llm_client import QwenV3

class codeGenerator:
    
    def __init__(self, prompt=None):
        self.prompt = prepare_prompt(prompt_name="code_generator_prompt", prompt=prompt)
        
    def generate_code(self, user_request, input_data):         
        prompt_filled = self.prompt\
                .replace("{user_request}", user_request)\
                .replace("{input_data}", input_data)
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
        print(codes)
        return codes
    

        


