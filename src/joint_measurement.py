"""
Joint Measurement & Data Processing Module
Agent3担当: 手のランドマークから関節間距離の計算とデータ処理

TODO for Agent3:
- JointMeasurementクラスの実装
- 関節間距離の計算
- データの正規化とフォーマット
- 単位変換機能
- tests/test_joint_measurement.py の作成

詳細はAGENTS.mdを参照してください
"""

import numpy as np
from typing import List, Dict, Tuple
from datetime import datetime


class JointMeasurement:
    """
    手のランドマークから関節間の距離を計算するクラス

    Attributes:
        config (dict): 計測設定
        landmarks_to_measure (List[Tuple[int, int]]): 計測する関節ペアのリスト
        scale_factor (float): 実寸への変換スケール
    """

    def __init__(self, config: dict):
        """
        関節計測の初期化

        Args:
            config (dict): 計測設定を含む辞書
                - landmarks_to_measure: 計測する関節ペアのリスト
                - unit: 単位 (cm, mm, etc.)
                - scale_factor: スケール変換係数
        """
        # TODO: 実装をここに追加
        pass

    def calculate_distances(self, landmarks: List[List[float]]) -> Dict:
        """
        ランドマーク間の距離を計算

        Args:
            landmarks (List[List[float]]): 21個のランドマーク座標 [[x, y, z], ...]

        Returns:
            Dict: 計測結果
                {
                    "measurements": {
                        "wrist_to_thumb": {"distance": float, "unit": str},
                        "wrist_to_index": {"distance": float, "unit": str},
                        ...
                    }
                }
        """
        # TODO: 実装をここに追加
        pass

    def _euclidean_distance(self, point1: List[float], point2: List[float]) -> float:
        """
        2点間のユークリッド距離を計算

        Args:
            point1 (List[float]): 座標1 [x, y, z]
            point2 (List[float]): 座標2 [x, y, z]

        Returns:
            float: ユークリッド距離
        """
        # TODO: 実装をここに追加
        pass

    def normalize_data(self, data: Dict) -> Dict:
        """
        データを正規化

        Args:
            data (Dict): 生の計測データ

        Returns:
            Dict: 正規化されたデータ
        """
        # TODO: 実装をここに追加
        pass

    def format_output(self, hand_id: int, measurements: Dict) -> Dict:
        """
        出力データをフォーマット

        Args:
            hand_id (int): 手のID
            measurements (Dict): 計測データ

        Returns:
            Dict: フォーマットされた出力
                {
                    "hand_id": int,
                    "measurements": {...},
                    "timestamp": str
                }
        """
        # TODO: 実装をここに追加
        pass


# テスト用のメイン関数
if __name__ == "__main__":
    import yaml

    # 設定ファイルを読み込んでテスト
    with open("../config.yaml", "r") as f:
        config = yaml.safe_load(f)

    measurement = JointMeasurement(config["measurement"])
    # TODO: テストコードを追加
