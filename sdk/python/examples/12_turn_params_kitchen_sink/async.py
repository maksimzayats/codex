import asyncio
import json

from openai_codex import (
    AsyncCodex,
)
from openai_codex.types import (
    Personality,
    ReasoningSummary,
)

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "actions": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": ["summary", "actions"],
    "additionalProperties": False,
}

SUMMARY = ReasoningSummary.model_validate("concise")

PROMPT = (
    "Analyze a safe rollout plan for enabling a feature flag in production. "
    "Return JSON matching the requested schema."
)


async def main() -> None:
    async with AsyncCodex() as codex:
        thread = await codex.thread_start(
            model="gpt-5.4", config={"model_reasoning_effort": "high"}
        )

        turn = await thread.turn(
            PROMPT,
            output_schema=OUTPUT_SCHEMA,
            personality=Personality.pragmatic,
            summary=SUMMARY,
        )
        result = await turn.run()
        structured_text = result.final_response.strip()
        try:
            structured = json.loads(structured_text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Expected JSON matching OUTPUT_SCHEMA, got: {structured_text!r}"
            ) from exc

        summary = structured["summary"]
        actions = structured["actions"]
        if (
            not isinstance(summary, str)
            or not isinstance(actions, list)
            or not all(isinstance(action, str) for action in actions)
        ):
            raise RuntimeError(
                f"Expected structured output with string summary/actions, got: {structured!r}"
            )

        print("Status:", result.status)
        print("summary:", summary)
        print("actions:")
        for action in actions:
            print("-", action)
        print("Items:", len(result.items))


if __name__ == "__main__":
    asyncio.run(main())
