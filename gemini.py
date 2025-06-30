import asyncio
from google import genai
from dotenv import load_dotenv
import os
from pydantic import BaseModel


class DefaultSchema(BaseModel):
    response: str


class Gemini:
    def __init__(self, api_key, model="gemini-2.5-pro"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    async def query(self, contents, schema=DefaultSchema):
        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=contents,
            # 이미지 예제
            # contents=[
            #     'Tell me a story based on this image',
            #     Image.open(image_path)
            # ]
            config={
                "response_mime_type": "application/json",
                "response_schema": schema,
            },
        )
        return response.parsed


async def main():
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    gemini = Gemini(api_key)
    for i in range(30):
        try:
            print(f"{i}: {await gemini.query('아무거나 말해봐라')}")
        except Exception as e:
            print(f"Query {i} failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
