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
        self.landmarks_to_measure = config.get("landmarks_to_measure", [])
        self.scale_factor = config.get("scale_factor", 1.0)
        self.unit = config.get("unit", "cm")

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
        measurements = {}

        for pair in self.landmarks_to_measure:
            idx1, idx2 = pair
            point1 = landmarks[idx1]
            point2 = landmarks[idx2]

            # 距離計算
            distance = self._euclidean_distance(point1, point2)

            # スケール変換（ピクセル → cm）
            distance_scaled = distance * self.scale_factor

            # 関節名を決定
            name = self._get_joint_name(idx1, idx2)
            measurements[name] = {
                "distance": round(distance_scaled, 2),
                "unit": self.unit
            }

        return {"measurements": measurements}

    def _get_joint_name(self, idx1: int, idx2: int) -> str:
        """
        ランドマークインデックスから関節名を生成

        Args:
            idx1 (int): 最初のランドマークインデックス
            idx2 (int): 2番目のランドマークインデックス

        Returns:
            str: 関節名（例: "wrist_to_thumb"）
        """
        landmark_names = {
            0: "wrist",
            4: "thumb",
            8: "index",
            12: "middle",
            16: "ring",
            20: "pinky"
        }

        name1 = landmark_names.get(idx1, f"landmark_{idx1}")
        name2 = landmark_names.get(idx2, f"landmark_{idx2}")
        return f"{name1}_to_{name2}"

    def _euclidean_distance(self, point1: List[float], point2: List[float]) -> float:
        """
        2点間のユークリッド距離を計算

        Args:
            point1 (List[float]): 座標1 [x, y, z]
            point2 (List[float]): 座標2 [x, y, z]

        Returns:
            float: ユークリッド距離
        """
        return np.linalg.norm(np.array(point1) - np.array(point2))

    def normalize_data(self, data: Dict) -> Dict:
        """
        データを正規化

        Args:
            data (Dict): 生の計測データ

        Returns:
            Dict: 正規化されたデータ
        """
        # 異常値のフィルタリング（距離が負の値や極端に大きい値をチェック）
        normalized = {"measurements": {}}

        if "measurements" in data:
            for joint_name, measurement in data["measurements"].items():
                distance = measurement.get("distance", 0)

                # 異常値チェック（0 < distance < 1000 cm）
                if 0 < distance < 1000:
                    normalized["measurements"][joint_name] = measurement

        return normalized

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
        return {
            "hand_id": hand_id,
            "measurements": measurements.get("measurements", {}),
            "timestamp": datetime.now().isoformat()
        }


# テスト用のメイン関数
if __name__ == "__main__":
    import yaml

    # 設定ファイルを読み込んでテスト
    with open("../config.yaml", "r") as f:
        config = yaml.safe_load(f)

    measurement = JointMeasurement(config["measurement"])
    # TODO: テストコードを追加
