from models import ProductOpportunity


def test_product_opportunity():
    opportunity = ProductOpportunity(
        title="AI Productivity",
        target_audience="Managers",
        problem="Low productivity",
        solution="AI workflow",
        demand_score=80,
        suggested_price="$50",
        reasoning="Strong demand",
    )

    assert opportunity.demand_score == 80
