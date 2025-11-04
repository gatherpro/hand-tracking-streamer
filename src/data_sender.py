"""
Data Sender Module
Agent4担当: 計測データのWEBアプリケーションへの送信

TODO for Agent4:
- DataSenderクラスの実装
- REST API / WebSocket通信
- 接続管理とリトライ処理
- エラーハンドリング
- tests/test_data_sender.py の作成

詳細はAGENTS.mdを参照してください
"""

import requests
import json
from typing import Dict, Optional
import time
from datetime import datetime


class DataSender:
    """
    計測データをWEBアプリケーションに送信するクラス

    Attributes:
        config (dict): 送信設定
        endpoint (str): 送信先エンドポイント
        method (str): 送信方法 ("POST" or "WEBSOCKET")
        retry_attempts (int): リトライ回数
        connected (bool): 接続状態
    """

    def __init__(self, config: dict):
        """
        データ送信の初期化

        Args:
            config (dict): 送信設定を含む辞書
                - endpoint: REST APIエンドポイント
                - method: 送信方法
                - websocket_url: WebSocket URL
                - retry_attempts: リトライ回数
                - retry_delay: リトライ間隔（秒）
        """
        self.endpoint = config.get("endpoint", "http://localhost:8000/api/hand-data")
        self.method = config.get("method", "POST")
        self.websocket_url = config.get("websocket_url", "ws://localhost:8000/ws/hand-data")
        self.retry_attempts = config.get("retry_attempts", 3)
        self.retry_delay = config.get("retry_delay", 1.0)
        self.connected = False
        self.timeout = 5

    def connect(self) -> bool:
        """
        WEBアプリケーションへの接続を確立

        Returns:
            bool: 接続成功でTrue
        """
        try:
            # エンドポイントにhealth checkを送信
            health_endpoint = self.endpoint.replace("/hand-data", "/health")
            response = requests.get(health_endpoint, timeout=self.timeout)
            self.connected = response.status_code == 200
            return self.connected
        except Exception as e:
            print(f"Connection failed: {e}")
            self.connected = False
            return False

    def send_data(self, data: Dict) -> bool:
        """
        データを送信

        Args:
            data (Dict): 送信するデータ
                {
                    "timestamp": str,
                    "hand_data": {
                        "hand_count": int,
                        "measurements": [...]
                    }
                }

        Returns:
            bool: 送信成功でTrue
        """
        return self._send_with_retry(data)

    def _send_with_retry(self, data: Dict) -> bool:
        """
        リトライ機能付きでデータを送信

        Args:
            data (Dict): 送信データ

        Returns:
            bool: 送信成功でTrue
        """
        for attempt in range(self.retry_attempts):
            try:
                response = requests.post(
                    self.endpoint,
                    json=data,
                    headers={"Content-Type": "application/json"},
                    timeout=self.timeout
                )

                if response.status_code == 200:
                    return True
                else:
                    print(f"Send failed with status {response.status_code} (attempt {attempt+1}/{self.retry_attempts})")

            except Exception as e:
                print(f"Send failed (attempt {attempt+1}/{self.retry_attempts}): {e}")

            if attempt < self.retry_attempts - 1:
                time.sleep(self.retry_delay)

        return False

    def disconnect(self):
        """
        接続を終了
        """
        self.connected = False
        print("Disconnected from server")

    def is_connected(self) -> bool:
        """
        接続状態を確認

        Returns:
            bool: 接続中の場合True
        """
        return self.connected


# テスト用のメイン関数
if __name__ == "__main__":
    import yaml

    # 設定ファイルを読み込んでテスト
    with open("../config.yaml", "r") as f:
        config = yaml.safe_load(f)

    sender = DataSender(config["data_sender"])
    # TODO: テストコードを追加
