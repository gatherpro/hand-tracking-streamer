"""
Unit tests for Joint Measurement Module
Agent3が実装してください
"""

import pytest
import numpy as np
from src.joint_measurement import JointMeasurement


def test_init():
    """初期化テスト"""
    config = {
        "landmarks_to_measure": [[0, 4], [0, 8]],
        "unit": "cm",
        "scale_factor": 10.0
    }
    measurement = JointMeasurement(config)

    assert measurement.landmarks_to_measure == [[0, 4], [0, 8]]
    assert measurement.unit == "cm"
    assert measurement.scale_factor == 10.0


def test_euclidean_distance():
    """ユークリッド距離計算テスト"""
    config = {
        "landmarks_to_measure": [[0, 4]],
        "unit": "cm",
        "scale_factor": 1.0
    }
    measurement = JointMeasurement(config)

    point1 = [0.0, 0.0, 0.0]
    point2 = [3.0, 4.0, 0.0]

    distance = measurement._euclidean_distance(point1, point2)
    assert distance == 5.0  # 3-4-5三角形


def test_distance_calculation():
    """距離計算テスト"""
    config = {
        "landmarks_to_measure": [[0, 4], [0, 8]],
        "unit": "cm",
        "scale_factor": 10.0
    }
    measurement = JointMeasurement(config)

    # サンプルランドマークデータ（21個）
    landmarks = [
        [0.0, 0.0, 0.0],  # 0: Wrist
        [0.1, 0.1, 0.0],  # 1
        [0.2, 0.2, 0.0],  # 2
        [0.3, 0.3, 0.0],  # 3
        [0.4, 0.4, 0.0],  # 4: Thumb tip
        [0.5, 0.5, 0.0],  # 5
        [0.6, 0.6, 0.0],  # 6
        [0.7, 0.7, 0.0],  # 7
        [0.8, 0.8, 0.0],  # 8: Index tip
        [0.9, 0.9, 0.0],  # 9
        [1.0, 1.0, 0.0],  # 10
        [1.1, 1.1, 0.0],  # 11
        [1.2, 1.2, 0.0],  # 12: Middle tip
        [1.3, 1.3, 0.0],  # 13
        [1.4, 1.4, 0.0],  # 14
        [1.5, 1.5, 0.0],  # 15
        [1.6, 1.6, 0.0],  # 16: Ring tip
        [1.7, 1.7, 0.0],  # 17
        [1.8, 1.8, 0.0],  # 18
        [1.9, 1.9, 0.0],  # 19
        [2.0, 2.0, 0.0],  # 20: Pinky tip
    ]

    result = measurement.calculate_distances(landmarks)

    assert "measurements" in result
    assert "wrist_to_thumb" in result["measurements"]
    assert "wrist_to_index" in result["measurements"]

    # 距離の検証（0,0,0 から 0.4,0.4,0 の距離は sqrt(0.32) * 10）
    expected_distance = round(np.sqrt(0.4**2 + 0.4**2) * 10, 2)
    assert result["measurements"]["wrist_to_thumb"]["distance"] == expected_distance
    assert result["measurements"]["wrist_to_thumb"]["unit"] == "cm"


def test_data_normalization():
    """データ正規化テスト"""
    config = {
        "landmarks_to_measure": [[0, 4]],
        "unit": "cm",
        "scale_factor": 1.0
    }
    measurement = JointMeasurement(config)

    # 正常なデータ
    data = {
        "measurements": {
            "wrist_to_thumb": {"distance": 12.5, "unit": "cm"},
            "wrist_to_index": {"distance": 15.3, "unit": "cm"}
        }
    }

    normalized = measurement.normalize_data(data)
    assert len(normalized["measurements"]) == 2

    # 異常値を含むデータ
    data_with_outliers = {
        "measurements": {
            "wrist_to_thumb": {"distance": 12.5, "unit": "cm"},
            "bad_measurement_1": {"distance": -5.0, "unit": "cm"},  # 負の値
            "bad_measurement_2": {"distance": 1500.0, "unit": "cm"},  # 極端に大きい
            "wrist_to_index": {"distance": 15.3, "unit": "cm"}
        }
    }

    normalized = measurement.normalize_data(data_with_outliers)
    assert len(normalized["measurements"]) == 2  # 正常な2つだけ残る
    assert "bad_measurement_1" not in normalized["measurements"]
    assert "bad_measurement_2" not in normalized["measurements"]


def test_output_format():
    """出力フォーマットテスト"""
    config = {
        "landmarks_to_measure": [[0, 4]],
        "unit": "cm",
        "scale_factor": 1.0
    }
    measurement = JointMeasurement(config)

    measurements = {
        "measurements": {
            "wrist_to_thumb": {"distance": 12.5, "unit": "cm"}
        }
    }

    output = measurement.format_output(0, measurements)

    assert "hand_id" in output
    assert "measurements" in output
    assert "timestamp" in output
    assert output["hand_id"] == 0
    assert output["measurements"]["wrist_to_thumb"]["distance"] == 12.5


def test_get_joint_name():
    """関節名生成テスト"""
    config = {
        "landmarks_to_measure": [[0, 4]],
        "unit": "cm",
        "scale_factor": 1.0
    }
    measurement = JointMeasurement(config)

    assert measurement._get_joint_name(0, 4) == "wrist_to_thumb"
    assert measurement._get_joint_name(0, 8) == "wrist_to_index"
    assert measurement._get_joint_name(0, 12) == "wrist_to_middle"
    assert measurement._get_joint_name(0, 16) == "wrist_to_ring"
    assert measurement._get_joint_name(0, 20) == "wrist_to_pinky"
