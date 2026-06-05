from openai_codex import Codex


def main() -> None:
    with Codex() as codex:
        # Create an initial thread and turn so we have a real thread to resume.
        original = codex.thread_start(model="gpt-5.4", config={"model_reasoning_effort": "high"})
        _ = original.turn("Tell me one fact about Saturn.").run()
        print("Created thread:", original.id)

        # Resume the existing thread by ID.
        resumed = codex.thread_resume(original.id)
        second = resumed.turn("Continue with one more fact.").run()
        print(second.final_response)


if __name__ == "__main__":
    main()
