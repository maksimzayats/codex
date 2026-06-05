import asyncio

from openai_codex import AsyncCodex


async def main() -> None:
    async with AsyncCodex() as codex:
        original = await codex.thread_start(
            model="gpt-5.4", config={"model_reasoning_effort": "high"}
        )

        first_turn = await original.turn("Tell me one fact about Saturn.")
        _ = await first_turn.run()
        print("Created thread:", original.id)

        resumed = await codex.thread_resume(original.id)
        second_turn = await resumed.turn("Continue with one more fact.")
        second = await second_turn.run()
        print(second.final_response)


if __name__ == "__main__":
    asyncio.run(main())
