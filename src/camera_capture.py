"""
Camera Capture Module
Agent1担当: カメラからのリアルタイム映像取得

TODO for Agent1:
- CameraCaptureクラスの実装
- カメラ初期化処理
- フレーム取得メソッド
- エラーハンドリング
- tests/test_camera_capture.py の作成

詳細はAGENTS.mdを参照してください
"""

import cv2
import yaml
from typing import Optional, Tuple
import numpy as np


class CameraCapture:
    """
    固定カメラからのビデオキャプチャを管理するクラス

    Attributes:
        config (dict): カメラ設定
        cap (cv2.VideoCapture): OpenCVのVideoCaptureオブジェクト
    """

    def __init__(self, config: dict):
        """
        カメラキャプチャの初期化

        Args:
            config (dict): カメラ設定を含む辞書
                - device_id: カメラデバイスID
                - width: フレーム幅
                - height: フレーム高さ
                - fps: フレームレート
        """
        self.config = config
        self.device_id = config.get('device_id', 0)
        self.width = config.get('width', 1280)
        self.height = config.get('height', 720)
        self.fps = config.get('fps', 30)
        self.cap: Optional[cv2.VideoCapture] = None

    def start(self) -> bool:
        """
        カメラキャプチャを開始

        Returns:
            bool: 成功した場合True
        """
        try:
            self.cap = cv2.VideoCapture(self.device_id)

            if not self.cap.isOpened():
                print(f"Error: Could not open camera with device_id {self.device_id}")
                return False

            # カメラ設定を適用
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)

            # 設定が正しく適用されたか確認
            actual_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            actual_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            actual_fps = self.cap.get(cv2.CAP_PROP_FPS)

            print(f"Camera started: {actual_width}x{actual_height} @ {actual_fps}fps")
            return True

        except Exception as e:
            print(f"Error starting camera: {e}")
            return False

    def get_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        カメラから1フレームを取得

        Returns:
            Tuple[bool, Optional[np.ndarray]]: (成功フラグ, フレーム画像)
        """
        if self.cap is None or not self.cap.isOpened():
            print("Error: Camera is not opened. Call start() first.")
            return False, None

        try:
            ret, frame = self.cap.read()

            if not ret:
                print("Error: Failed to capture frame")
                return False, None

            return True, frame

        except Exception as e:
            print(f"Error capturing frame: {e}")
            return False, None

    def stop(self):
        """
        カメラを停止してリソースを解放
        """
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            print("Camera stopped and released")

    def is_opened(self) -> bool:
        """
        カメラが開いているか確認

        Returns:
            bool: カメラが開いている場合True
        """
        return self.cap is not None and self.cap.isOpened()


# テスト用のメイン関数
if __name__ == "__main__":
    # 設定ファイルを読み込んでテスト
    with open("../config.yaml", "r") as f:
        config = yaml.safe_load(f)

    camera = CameraCapture(config["camera"])
    # TODO: テストコードを追加
