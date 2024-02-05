import requests
import json

class TextFileHandler:
    def __init__(self, input_folder, output_file_path, num_files):
        self.input_folder = input_folder
        self.output_file_path = output_file_path
        self.num_files = num_files

    def combine_text_files(self):
        with open(self.output_file_path, "w") as output_file:
            for i in range(self.num_files):
                input_file_path = f"{self.input_folder}/{i}.txt"

                try:
                    with open(input_file_path, "r") as input_file:
                        text_content = input_file.read()
                        output_file.write(text_content + "\n")
                except FileNotFoundError:
                    print(f"File {input_file_path} not found. Skipping.")

        print(f"Text from all files combined and saved to {self.output_file_path}")

class CloudflareAPI:
    def __init__(self, api_key, account_id):
        self.API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def run_model(self, model, input_text):
        response = requests.post(f"{self.API_BASE_URL}{model}", headers=self.headers, json={"text": input_text})
        return response.json()

# Replace "your_api_key" and "your_account_id" with your actual Cloudflare API key and account ID
api_key = ""
account_id = ""

# Initialize TextFileHandler and CloudflareAPI
text_file_handler = TextFileHandler("scholly", "scholly/combined_text.txt", 85)
output_json_file_path = 'idream/model_output.json'

cloudflare_api = CloudflareAPI(api_key, account_id)

# Combine text files
text_file_handler.combine_text_files()

# Read the combined text file and run the model
with open(text_file_handler.output_file_path, "r") as file:
    input_text = file.read()

model_name = "@cf/baai/bge-large-en-v1.5"
output = cloudflare_api.run_model(model_name, input_text)
print(output)

# Save the model output to a JSON file
with open(output_json_file_path, 'w') as file:
    json.dump(output['result'], file)

print(f"Model output saved to {output_json_file_path}")
