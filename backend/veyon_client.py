import requests

class VeyonClient:
    def __init__(self, base_url: str = "http://localhost:8080"):
        # Initialize the Veyon API client 初始化Veyon API client
        self.base_url = base_url
        self.connection_uid = None

    def authenticate(self, auth_method: str, credentials: dict) -> dict:
        # Authenticate with the Veyon Server 与服务器验证
        response = requests.post(
            f"{self.base_url}/api/v1/authentication/localhost",
            json={"method": auth_method, "credentials": credentials}
        )
        response.raise_for_status()
        self.connection_uid = response.json()["connection-uid"]
        return response.json()

    def get_screenshot(self) -> bytes:
        # Get current screenshot from remote computer as PNG image 从远程电脑中获取屏幕截图
        response = requests.get(
            f"{self.base_url}/api/v1/framebuffer?format=png",
            headers={"Connection-Uid": self.connection_uid}
        )
        response.raise_for_status()
        return response.content

    def lock_screens(self):
        # Lock all screens on remote computers 锁定所有远程电脑的屏幕
        response = requests.put(
            f"{self.base_url}/api/v1/feature/ccb535a2-1d24-4cc1-a709-8b47d2b2ac79",
            headers={"Connection-Uid": self.connection_uid},
            json={"active": True}
        )
        response.raise_for_status()
        return True