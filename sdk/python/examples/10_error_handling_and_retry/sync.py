from openai_codex import (
    Codex,
    JsonRpcError,
    ServerBusyError,
    retry_on_overload,
)
from openai_codex.types import TurnStatus


def main() -> None:
    with Codex() as codex:
        thread = codex.thread_start(model="gpt-5.4", config={"model_reasoning_effort": "high"})

        try:
            result = retry_on_overload(
                lambda: thread.turn("Summarize retry best practices in 3 bullets.").run(),
                max_attempts=3,
                initial_delay_s=0.25,
                max_delay_s=2.0,
            )
        except ServerBusyError as exc:
            print("Server overloaded after retries:", exc.message)
        except JsonRpcError as exc:
            print(f"JSON-RPC error {exc.code}: {exc.message}")
        else:
            if result.status == TurnStatus.failed:
                print("Turn failed:", result.error)
            else:
                print("Text:", result.final_response)


if __name__ == "__main__":
    main()
