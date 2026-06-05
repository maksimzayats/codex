from openai_codex import Codex


def main() -> None:
    with Codex() as codex:
        thread = codex.thread_start(model="gpt-5.4", config={"model_reasoning_effort": "high"})
        result = thread.turn("Give 3 bullets about SIMD.").run()

        print("thread_id:", thread.id)
        print("turn_id:", result.id)
        print("status:", result.status)
        if result.error is not None:
            print("error:", result.error)
        print("text:", result.final_response)
        print("items.count:", len(result.items))


if __name__ == "__main__":
    main()
