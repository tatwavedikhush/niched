from pydantic import BaseModel
import ollama


class ProductSection(BaseModel):
    title: str
    content: str


class DigitalProduct(BaseModel):
    title: str
    introduction: str
    sections: list[ProductSection]
    checklist: list[str]
    conclusion: str


def generate_product(opportunity):
    prompt = f"""
You are an expert digital product creator.

Create a useful, practical digital product based on this opportunity:

Title: {opportunity.title}
Target audience: {opportunity.target_audience}
Problem: {opportunity.problem}
Solution: {opportunity.solution}

Create a product that genuinely helps the target audience solve the problem.

Include:
- A clear introduction
- 4 to 6 detailed sections
- Practical and actionable advice
- A useful checklist
- A concise conclusion

Return ONLY valid JSON matching the provided schema.
"""

    response = ollama.chat(
        model="llama3.1:8b",
        messages=[{"role": "user", "content": prompt}],
        format=DigitalProduct.model_json_schema(),
    )

    return DigitalProduct.model_validate_json(response["message"]["content"])
