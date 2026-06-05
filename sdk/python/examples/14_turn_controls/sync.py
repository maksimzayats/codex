from openai_codex import Codex


def main() -> None:
    with Codex() as codex:
        thread = codex.thread_start(model="gpt-5.4", config={"model_reasoning_effort": "high"})
        steer_turn = thread.turn("Count from 1 to 40 with commas, then one summary sentence.")
        steer_result = steer_turn.steer("Keep it brief and stop after 10 numbers.")

        steer_event_count = 0
        steer_completed_status = None
        steer_deltas = []
        for event in steer_turn.stream():
            steer_event_count += 1
            if event.method == "item/agentMessage/delta":
                steer_deltas.append(event.payload.delta)
                continue
            if event.method == "turn/completed":
                steer_completed_status = event.payload.turn.status.value

        if steer_completed_status is None:
            raise RuntimeError("stream ended without turn/completed")
        steer_preview = "".join(steer_deltas).strip()

        interrupt_turn = thread.turn("Count from 1 to 200 with commas, then one summary sentence.")
        interrupt_result = interrupt_turn.interrupt()

        interrupt_event_count = 0
        interrupt_completed_status = None
        interrupt_deltas = []
        for event in interrupt_turn.stream():
            interrupt_event_count += 1
            if event.method == "item/agentMessage/delta":
                interrupt_deltas.append(event.payload.delta)
                continue
            if event.method == "turn/completed":
                interrupt_completed_status = event.payload.turn.status.value

        if interrupt_completed_status is None:
            raise RuntimeError("stream ended without turn/completed")
        interrupt_preview = "".join(interrupt_deltas).strip()

        print("steer.result:", steer_result.model_dump(mode="json", by_alias=True))
        print("steer.final.status:", steer_completed_status)
        print("steer.events.count:", steer_event_count)
        print("steer.assistant.preview:", steer_preview)
        print("interrupt.result:", interrupt_result.model_dump(mode="json", by_alias=True))
        print("interrupt.final.status:", interrupt_completed_status)
        print("interrupt.events.count:", interrupt_event_count)
        print("interrupt.assistant.preview:", interrupt_preview)


if __name__ == "__main__":
    main()
