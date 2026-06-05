import asyncio

from openai_codex import AsyncCodex
from openai_codex.types import InitializeResponse


def _server_label(metadata: InitializeResponse) -> str:
    server = metadata.serverInfo
    if server is None:
        return "unknown"
    return " ".join(part for part in (server.name, server.version) if part) or "unknown"


async def main() -> None:
    async with AsyncCodex() as codex:
        print("Server:", _server_label(codex.metadata))

        thread = await codex.thread_start(
            model="gpt-5.4", config={"model_reasoning_effort": "high"}
        )
        result = await thread.run("Say hello in one sentence.")
        print("Items:", len(result.items))
        print("Text:", result.final_response)


if __name__ == "__main__":
    asyncio.run(main())
