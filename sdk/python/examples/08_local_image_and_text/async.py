import asyncio
import base64
import contextlib
import tempfile
from pathlib import Path
from typing import Iterator

from openai_codex import AsyncCodex, LocalImageInput, TextInput

SAMPLE_IMAGE_PNG = "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAIAAABLbSncAAAAIUlEQVR4nGOo2PIfjv7fiYIjBipKRG2Jh6MtoaFwREUJAMtncrF3OVI0AAAAAElFTkSuQmCC"


@contextlib.contextmanager
def _temporary_sample_image_path() -> Iterator[Path]:
    with tempfile.TemporaryDirectory(prefix="codex-python-example-image-") as temp_root:
        image_path = Path(temp_root) / "generated_sample.png"
        image_path.write_bytes(base64.b64decode(SAMPLE_IMAGE_PNG))
        yield image_path


async def main() -> None:
    with _temporary_sample_image_path() as image_path:
        async with AsyncCodex() as codex:
            thread = await codex.thread_start(
                model="gpt-5.4", config={"model_reasoning_effort": "high"}
            )

            turn = await thread.turn(
                [
                    TextInput(
                        "Read this generated local image and summarize the colors/layout in 2 bullets."
                    ),
                    LocalImageInput(str(image_path.resolve())),
                ]
            )
            result = await turn.run()

            print("Status:", result.status)
            print(result.final_response)


if __name__ == "__main__":
    asyncio.run(main())
