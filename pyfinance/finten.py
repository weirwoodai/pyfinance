import requests


class FinTen:
    def __init__(self):
        self.URI = "https://finten.weirwood.ai"

    def _is_reachable(self) -> bool:
        response = requests.get(self.URI)

        if response.status_code == 200:
            try:
                if response.json()["greeting"] == "You reached the FinTen API! 🥳":
                    return True
            except Exception as e:
                print(f"Unable to reach FinTen API {e}")
                return False
        return False

