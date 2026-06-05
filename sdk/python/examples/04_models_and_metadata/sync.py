from openai_codex import Codex
from openai_codex.types import InitializeResponse


def _server_label(metadata: InitializeResponse) -> str:
    server = metadata.serverInfo
    if server is None:
        return "unknown"
    return " ".join(part for part in (server.name, server.version) if part) or "unknown"


def main() -> None:
    with Codex() as codex:
        print("server:", _server_label(codex.metadata))
        models = codex.models()
        print("models.count:", len(models.data))
        print("models:", ", ".join(model.id for model in models.data[:5]))


if __name__ == "__main__":
    main()
