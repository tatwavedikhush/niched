from models import ProductOpportunity
from product_generator import generate_product

opportunity = ProductOpportunity(
    title="AI Productivity Optimization",
    target_audience="Business Executives and Managers",
    problem="Executives struggle to turn AI adoption into measurable productivity gains",
    solution="A practical system for identifying AI opportunities and improving team productivity",
    demand_score=80,
    suggested_price="$50-$100/user/month",
    reasoning="Strong pain point around AI adoption and productivity",
)


product = generate_product(opportunity)

print("\n===== GENERATED PRODUCT =====")
print(product.model_dump_json(indent=2))
print("===== END =====")
