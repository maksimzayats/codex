from openai_codex import Codex


def main() -> None:
    with Codex() as codex:
        # Browser login returns a live handle. Open `auth_url` and call `wait()`
        # in a real app; this example cancels immediately so it stays non-blocking.
        login = codex.login_chatgpt()
        canceled = login.cancel()
        completed = login.wait()
        account = codex.account()

        print("login.id:", login.login_id)
        print("login.auth_url:", login.auth_url)
        print("login.cancel.status:", canceled.status)
        print("login.completed.success:", completed.success)
        print("account.requires_openai_auth:", account.requires_openai_auth)


if __name__ == "__main__":
    main()
