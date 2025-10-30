import yaml    

def prepare_prompt(prompt_name, prompt=None):
    if prompt is None:
        with open("backend/prompts.yml", "r") as f:
            prompt_data = yaml.safe_load(f)
        prompt = prompt_data[prompt_name]["content"]
        return prompt
    else:
        return prompt