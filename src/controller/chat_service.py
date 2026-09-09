from fastapi import APIRouter, Request
from pydantic import BaseModel
from ..common.prompt import system_prompt
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()


client = Groq()



def get_weather(location: str) -> str:
    # Later you can replace this with a real weather API
    return f"The weather in {location} is sunny with a temperature of 25°C."



class ChatService:

    def __init__(self):
        self.client = Groq()

    def generate_response(self, userinpt: str):

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": userinpt
            }
        ]
        response = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,  
        )
        content = response.choices[0].message.content

        try:
            ai_response = json.loads(content)
        except json.JSONDecodeError:
            return {
                "step": "final",
                "output": content
            }

        # -------------------------
        # STEP 2: Execute tool
        # -------------------------
        if ai_response["step"] == "action":
            print(ai_response)
            function_name = ai_response.get("function")
            query = ai_response.get("query")

            if function_name == "weather_search":
                tool_result = get_weather(query)


                # -------------------------
                # STEP 3: Observe
                # -------------------------

            messages.append({
                    "role": "assistant",
                    "content": content
                })

            messages.append({
                "role": "tool",
                "content": json.dumps({
                    'step': "observe",
                    'function': function_name,
                    'output': tool_result
                })
            })

            final_response = self.client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages,  
            )

            final_content = final_response.choices[0].message.content

            try:

                final_ai_response = json.loads(final_content)
                return final_ai_response

            except json.JSONDecodeError:

                return {
                    "step": "final",
                    "output": final_content
                }
        return ai_response
    
        

