from botbuilder.core import ActivityHandler, TurnContext
import pandas as pd
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class CyberBot(ActivityHandler):
    def __init__(self):
        self.faq = {}
        try:
            df = pd.read_excel("MSMEs_qns.xlsx")
            for _, row in df.iterrows():
                self.faq[row["Keyword"].lower()] = row["Answers"]
        except Exception as e:
            print(f"[ERROR] Failed to load Excel file: {e}")

    async def on_message_activity(self, turn_context: TurnContext):
        user_message = turn_context.activity.text.lower()

        # Match FAQ from Excel
        for keyword, answer in self.faq.items():
            if keyword in user_message:
                await turn_context.send_activity(answer)
                return

        # Fallback to OpenAI
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_message}]
            )
            reply = response.choices[0].message.content.strip()
            await turn_context.send_activity(reply)
        except Exception as e:
            await turn_context.send_activity("Sorry, I had trouble finding an answer.")
            print(f"[ERROR] OpenAI API failed: {e}")
