import os
import glob
import json
import logging
import requests
import openai

# Constants for API access
# --- Runpod API key can be obtained from https://runpod.ai/
RUNPOD_API_KEY = "your-runpod-api-key"
SERVERLESS_API_ID = "your-serverless-api-id"
# --- OpenAI API key can be obtained from https://platform.openai.com/account/api-keys
OPENAI_API_KEY = "your-openai-api-key"
# --- Entity directory and master prompts
ENTITY_DIR = "modules/basic_escordia/config/entities/"
MASTER_PROMPTS = {
    "npcs": "You are a NPC from a RPG game. Your answers should be rich but not too long, answer in one or two sentences. Do not get out of character.",
    # Add other master prompts here
}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIGenerator:
    def __init__(self, service='runpod'):
        self.service = service
        if service == 'openai':
            openai.api_key = OPENAI_API_KEY

    def generate_response(self, prompt):
        if self.service == 'runpod':
            return self._run_sync_runpod(prompt)
        elif self.service == 'openai':
            return self._run_sync_openai(prompt)
        else:
            raise ValueError("Unsupported service. Choose 'runpod' or 'openai'.")

    def _run_sync_runpod(self, prompt):
        url = f"https://api.runpod.ai/v2/{SERVERLESS_API_ID}/runsync"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {RUNPOD_API_KEY}'
        }
        payload = {
            "input": {
                "prompt": prompt,
                "max_new_tokens": 300,
                "temperature": 0.85,
                "top_k": 50,
                "top_p": 0.7,
                "repetition_penalty": 1.2,
                "batch_size": 8,
                "stop": ["</s>"]
            }
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            return response.json()
        except Exception as e:
            logger.error(f"Failed to run sync for prompt: {prompt}", exc_info=True)
            return None

    def _run_sync_openai(self, prompt):
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=500,
                temperature=0.9,
                top_p=0.7,
                frequency_penalty=1.2,
                stop=["</s>"]
            )
            return {
                "status": "COMPLETED",
                "output": response.choices[0].text.strip()
            }
        except Exception as e:
            logger.error(f"Failed to generate response with OpenAI for prompt: {prompt}", exc_info=True)
            return None

def process_entity(file_path, master_prompt, ai_generator):
    try:
        with open(file_path, 'r') as file:
            entities = json.load(file)
    except Exception as e:
        logger.error(f"Failed to load entities from {file_path}: {e}", exc_info=True)
        return

    updated_entities = {}

    for entity_name, entity_info in entities.items():
        for key, value in entity_info.items():
            if key.endswith('_prompt'):
                prompt = f"[INST] <<SYS>>{master_prompt}<</SYS>>You are a {entity_name}, from Peaceful Village and your instructions are these: {value}[/INST]"
                logger.info(f"Sending prompt for {entity_name} ({key})")
                response = ai_generator.generate_response(prompt)
                if response and response.get("status") == "COMPLETED":
                    updated_entities[entity_name] = entity_info
                    updated_entities[entity_name][key.replace('_prompt', '')] = response['output']
                else:
                    logger.warning(f"Failed to get a valid response for {entity_name}, response was: {response}")

    try:
        with open(file_path, 'w') as file:
            json.dump(updated_entities, file, indent=4)
    except Exception as e:
        logger.error(f"Failed to save updated entities to {file_path}: {e}", exc_info=True)

def main(service='runpod'):
    ai_generator = AIGenerator(service=service)
    for file_path in glob.glob(os.path.join(ENTITY_DIR, '*.json')):
        module_name = os.path.basename(file_path).split('.')[0]
        master_prompt = MASTER_PROMPTS.get(module_name, "")
        if master_prompt:
            process_entity(file_path, master_prompt, ai_generator)
        else:
            logger.warning(f"No master prompt found for {module_name}")

if __name__ == "__main__":
    service_choice = 'runpod'  # or 'openai'
    main(service=service_choice)
