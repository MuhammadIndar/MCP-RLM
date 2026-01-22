import os
from openai import OpenAI
from anthropic import Anthropic

class LLMBackend:
    def __init__(self, agent_config, providers_config):
        self.model = agent_config['model']
        self.temp = agent_config.get('temperature', 0)
        self.max_tokens = agent_config.get('max_tokens', 1024)
        ref = agent_config['provider_ref']
        if ref not in providers_config:
            raise ValueError(f"Provider '{ref}' tidak ditemukan di config.yaml")
        
        prov_conf = providers_config[ref]
        self.type = prov_conf.get('type', 'openai_compatible')
        env_var = prov_conf.get('api_key_env')
        self.api_key = os.getenv(env_var)
        
        if not self.api_key and self.type != 'openai_compatible':
            print(f"WARNING: API Key {env_var} kosong/tidak ditemukan.")

        if self.type == 'openai_compatible':
            base_url = prov_conf.get('base_url')
            if not base_url:
                raise ValueError(f"Provider '{ref}' butuh 'base_url'")
            
            self.client = OpenAI(
                base_url=base_url,
                api_key=self.api_key if self.api_key else "dummy"
            )
            
        elif self.type == 'anthropic':
            self.client = Anthropic(api_key=self.api_key)
        
        else:
            raise ValueError(f"Tipe provider '{self.type}' belum didukung.")

    def generate(self, system_prompt, user_prompt):
        try:
            if self.type == 'openai_compatible':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=self.temp,
                    max_tokens=self.max_tokens
                )
                return response.choices[0].message.content

            elif self.type == 'anthropic':
                response = self.client.messages.create(
                    model=self.model,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}],
                    temperature=self.temp,
                    max_tokens=self.max_tokens
                )
                return response.content[0].text
                
        except Exception as e:
            return f"[ERROR LLM CALL]: {str(e)}"