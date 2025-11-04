"""
Hand Detection & Tracking Module
Agent2担当: MediaPipe Handsを使用した手の検出とランドマーク取得

TODO for Agent2:
- HandDetectorクラスの実装
- MediaPipe Hands初期化
- 手検出とランドマーク取得
- 複数の手への対応
- tests/test_hand_detector.py の作成

詳細はAGENTS.mdを参照してください
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime


class HandDetector:
    """
    MediaPipe Handsを使用して手を検出し、ランドマークを取得するクラス

    Attributes:
        config (dict): 手検出の設定
        mp_hands: MediaPipe Handsオブジェクト
        mp_drawing: MediaPipe描画ユーティリティ
    """

    def __init__(self, config: dict):
        """
        手検出器の初期化

        Args:
            config (dict): 手検出設定を含む辞書
                - model_complexity: モデルの複雑度 (0, 1, 2)
                - min_detection_confidence: 検出信頼度閾値
                - min_tracking_confidence: トラッキング信頼度閾値
                - max_num_hands: 最大検出手数
        """
        self.config = config
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        # MediaPipe Handsの初期化
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            model_complexity=config.get("model_complexity", 1),
            min_detection_confidence=config.get("min_detection_confidence", 0.5),
            min_tracking_confidence=config.get("min_tracking_confidence", 0.5),
            max_num_hands=config.get("max_num_hands", 2)
        )

    def detect(self, frame: np.ndarray) -> Dict:
        """
        フレームから手を検出してランドマークを取得

        Args:
            frame (np.ndarray): 入力画像フレーム

        Returns:
            Dict: 検出結果
                {
                    "hand_count": int,
                    "hands": [
                        {
                            "label": "Left" or "Right",
                            "landmarks": [[x, y, z], ...],  # 21 points
                            "confidence": float
                        }
                    ],
                    "timestamp": str
                }
        """
        # RGB変換（MediaPipeはRGBを期待）
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 手を検出
        results = self.hands.process(rgb_frame)

        # 結果を整形
        hand_count = self.get_hand_count(results)
        hands_data = []

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks, results.multi_handedness
            ):
                # 手のラベル（Left/Right）を取得
                label = handedness.classification[0].label
                confidence = handedness.classification[0].score

                # ランドマークを[[x, y, z], ...]の形式で抽出
                landmarks = [
                    [landmark.x, landmark.y, landmark.z]
                    for landmark in hand_landmarks.landmark
                ]

                hands_data.append({
                    "label": label,
                    "landmarks": landmarks,
                    "confidence": confidence
                })

        return {
            "hand_count": hand_count,
            "hands": hands_data,
            "timestamp": datetime.now().isoformat()
        }

    def draw_landmarks(self, frame: np.ndarray, landmarks) -> np.ndarray:
        """
        フレームにランドマークを描画（デバッグ用）

        Args:
            frame (np.ndarray): 入力画像フレーム
            landmarks: MediaPipe ランドマーク

        Returns:
            np.ndarray: ランドマークが描画されたフレーム
        """
        # フレームのコピーを作成（元のフレームを変更しない）
        annotated_frame = frame.copy()

        # ランドマークを描画
        self.mp_drawing.draw_landmarks(
            annotated_frame,
            landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_drawing_styles.get_default_hand_landmarks_style(),
            self.mp_drawing_styles.get_default_hand_connections_style()
        )

        return annotated_frame

    def get_hand_count(self, results) -> int:
        """
        検出された手の数を取得

        Args:
            results: MediaPipe検出結果

        Returns:
            int: 検出された手の数
        """
        if results.multi_hand_landmarks:
            return len(results.multi_hand_landmarks)
        return 0


# テスト用のメイン関数
if __name__ == "__main__":
    import yaml

    # 設定ファイルを読み込んでテスト
    with open("../config.yaml", "r") as f:
        config = yaml.safe_load(f)

    detector = HandDetector(config["hand_detection"])
    # TODO: テストコードを追加
