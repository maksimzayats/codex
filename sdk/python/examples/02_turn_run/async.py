import asyncio

from openai_codex import AsyncCodex


async def main() -> None:
    async with AsyncCodex() as codex:
        thread = await codex.thread_start(
            model="gpt-5.4", config={"model_reasoning_effort": "high"}
        )
        turn = await thread.turn("Give 3 bullets about SIMD.")
        result = await turn.run()

        print("thread_id:", thread.id)
        print("turn_id:", result.id)
        print("status:", result.status)
        if result.error is not None:
            print("error:", result.error)
        print("text:", result.final_response)
        print("items.count:", len(result.items))


if __name__ == "__main__":
    asyncio.run(main())
