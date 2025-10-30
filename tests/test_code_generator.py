from backend.core.data_agents.code_generator import codeGenerator
import pandas as pd

def test_code_generator():
    cg = codeGenerator()
    user_request = "Load a CSV file and display the first 5 rows."
    input_data = pd.read_csv(r"tests/sample_data/test.csv").to_string()
    generated_code = cg.generate_code(user_request, input_data)
    assert "head(5)" in generated_code

    