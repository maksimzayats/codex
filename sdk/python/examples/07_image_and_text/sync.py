from openai_codex import Codex, ImageInput, TextInput

REMOTE_IMAGE_URL = "https://raw.githubusercontent.com/github/explore/main/topics/python/python.png"


def main() -> None:
    with Codex() as codex:
        thread = codex.thread_start(model="gpt-5.4", config={"model_reasoning_effort": "high"})
        result = thread.turn(
            [
                TextInput("What is in this image? Give 3 bullets."),
                ImageInput(REMOTE_IMAGE_URL),
            ]
        ).run()

        print("Status:", result.status)
        print(result.final_response)


if __name__ == "__main__":
    main()
