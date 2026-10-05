import json
import os

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


def _fallback_resolution_plan(exception):
    """
    Return a deterministic fallback plan when
    the LLM is not configured or unavailable.
    """

    return {
        "summary": exception["problem"],
        "impact": exception["impact"],
        "recommended_action": exception["recommended_action"],
        "next_steps": [
            "Review the affected order details.",
            "Confirm the underlying ERP data.",
            "Take the recommended corrective action.",
            "Verify that the issue has been resolved.",
            "Update the order status and record the action taken.",
        ],
    }


def _parse_response(response):
    """
    Convert the LLM response into the dictionary
    expected by the Streamlit application.
    """

    text = response.output_text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    result = json.loads(text)

    required_fields = [
        "summary",
        "impact",
        "recommended_action",
        "next_steps",
    ]

    for field in required_fields:
        if field not in result:
            raise ValueError(
                f"LLM response is missing required field: {field}"
            )

    if not isinstance(result["next_steps"], list):
        raise ValueError("next_steps must be a list.")

    return result


def generate_resolution_plan(exception):
    """
    Use an LLM to analyze an already-detected ERP exception
    and create a practical corrective action plan.

    The business rules remain responsible for identifying
    the exception. The LLM is responsible for explaining
    the issue and recommending how to resolve it.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return _fallback_resolution_plan(exception)

    model = os.getenv(
        "OPENAI_MODEL",
        "gpt-6-luna",
    )

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are an operations analyst helping resolve ERP order exceptions.

Your job is to turn the detected problem into a practical
resolution plan that an operations, supply chain, or ERP team
could actually follow.

Do not invent information that is not provided.

Focus on fixing the problem, reducing business impact, and
verifying that the issue has been resolved.

ERP EXCEPTION
Exception type: {exception["exception_type"]}
Severity: {exception["severity"]}
Order ID: {exception["order_id"]}
Customer: {exception["customer"]}
Product: {exception["product"]}
Supplier: {exception["supplier"]}
Region: {exception["region"]}
Quantity: {exception["quantity"]}
Available inventory: {exception["available_inventory"]}
Order value: {exception["order_value"]}
Supplier rating: {exception["supplier_rating"]}
Supplier on-time rate: {exception["supplier_on_time_rate"]}

Detected problem:
{exception["problem"]}

Known business impact:
{exception["impact"]}

Existing recommended action:
{exception["recommended_action"]}

Return ONLY valid JSON using exactly this structure:

{{
    "summary": "Brief explanation of what happened.",
    "impact": "Specific business impact of the exception.",
    "recommended_action": "The primary corrective action that should be taken.",
    "next_steps": [
        "First concrete step.",
        "Second concrete step.",
        "Third concrete step.",
        "Verification step confirming the problem is resolved."
    ]
}}

Make the steps specific and operational.
Avoid generic advice such as "monitor the situation."
"""


    try:
        response = client.responses.create(
            model=model,
            input=prompt,
        )

        return _parse_response(response)

    except Exception:
        return _fallback_resolution_plan(exception)