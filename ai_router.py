# -*- coding: utf-8 -*-
"""Gemini-first AI router with OpenRouter fallback and key rotation."""
from __future__ import annotations
import json, os, random, time
import requests
from gemini_client import get_client

class AIRouter:
    def __init__(self):
        self.keys=[k.strip() for k in os.getenv('OPENROUTER_API_KEYS','').split(',') if k.strip()]
        self.models=[m.strip() for m in os.getenv('OPENROUTER_MODELS','google/gemini-2.5-flash,openai/gpt-4o-mini').split(',') if m.strip()]
        self.timeout=max(10,int(os.getenv('AI_REQUEST_TIMEOUT','60')))
        self.retries=max(1,min(3,int(os.getenv('AI_RETRIES','2'))))
    def generate(self,prompt:str,generation_config:dict|None=None)->str:
        errors=[]
        try:
            return get_client().generate_text(prompt,generation_config=generation_config or {})
        except Exception as exc:
            errors.append(f'Gemini: {exc}')
        keys=self.keys[:]; random.shuffle(keys)
        for key in keys:
            for model in self.models:
                for attempt in range(self.retries):
                    try:
                        payload={'model':model,'messages':[{'role':'user','content':prompt}], 'temperature':0.7, 'response_format':{'type':'json_object'}}
                        response=requests.post('https://openrouter.ai/api/v1/chat/completions',headers={'Authorization':f'Bearer {key}','Content-Type':'application/json','X-Title':'Thanawiyah_Quiz'},json=payload,timeout=self.timeout)
                        response.raise_for_status()
                        data=response.json()
                        return data['choices'][0]['message']['content']
                    except Exception as exc:
                        errors.append(f'OpenRouter/{model}: {exc}')
                        if attempt+1<self.retries: time.sleep(0.5*(2**attempt))
        raise RuntimeError('فشل جميع مزودي الذكاء الاصطناعي: ' + ' | '.join(errors[-4:]))

_router=None
def get_router():
    global _router
    if _router is None: _router=AIRouter()
    return _router
