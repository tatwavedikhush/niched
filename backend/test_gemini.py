from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents="Say hello to Niched in one sentence."
)

print(response.text)