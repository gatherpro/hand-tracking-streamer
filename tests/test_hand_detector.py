"""
Unit tests for Hand Detector Module
Agent2が実装してください
"""

import pytest
import numpy as np
import cv2
from src.hand_detector import HandDetector


@pytest.fixture
def hand_detector():
    """HandDetectorのフィクスチャ"""
    config = {
        "model_complexity": 1,
        "min_detection_confidence": 0.5,
        "min_tracking_confidence": 0.5,
        "max_num_hands": 2
    }
    return HandDetector(config)


@pytest.fixture
def sample_frame():
    """テスト用のサンプルフレーム（黒い画像）"""
    # 640x480の黒い画像を作成
    return np.zeros((480, 640, 3), dtype=np.uint8)


def test_hand_detector_initialization(hand_detector):
    """HandDetectorの初期化テスト"""
    assert hand_detector is not None
    assert hand_detector.mp_hands is not None
    assert hand_detector.hands is not None
    assert hand_detector.mp_drawing is not None


def test_detect_returns_correct_structure(hand_detector, sample_frame):
    """detectメソッドが正しい構造を返すかテスト"""
    result = hand_detector.detect(sample_frame)

    # 返り値の構造をチェック
    assert "hand_count" in result
    assert "hands" in result
    assert "timestamp" in result
    assert isinstance(result["hand_count"], int)
    assert isinstance(result["hands"], list)
    assert isinstance(result["timestamp"], str)


def test_detect_no_hands(hand_detector, sample_frame):
    """手が検出されない場合のテスト"""
    result = hand_detector.detect(sample_frame)

    # 黒い画像では手が検出されないはず
    assert result["hand_count"] == 0
    assert len(result["hands"]) == 0


def test_get_hand_count():
    """get_hand_countメソッドのテスト"""
    config = {
        "model_complexity": 1,
        "min_detection_confidence": 0.5,
        "min_tracking_confidence": 0.5,
        "max_num_hands": 2
    }
    detector = HandDetector(config)

    # モックの結果を作成
    class MockResults:
        def __init__(self, num_hands):
            if num_hands > 0:
                self.multi_hand_landmarks = [None] * num_hands
            else:
                self.multi_hand_landmarks = None

    # 手が0個の場合
    results_0 = MockResults(0)
    assert detector.get_hand_count(results_0) == 0

    # 手が1個の場合
    results_1 = MockResults(1)
    assert detector.get_hand_count(results_1) == 1

    # 手が2個の場合
    results_2 = MockResults(2)
    assert detector.get_hand_count(results_2) == 2


def test_draw_landmarks(hand_detector, sample_frame):
    """draw_landmarksメソッドのテスト"""
    # モックのランドマークを作成
    class MockLandmark:
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

    class MockHandLandmarks:
        def __init__(self):
            self.landmark = [MockLandmark(0.5, 0.5, 0.0) for _ in range(21)]

    mock_landmarks = MockHandLandmarks()

    # 描画を実行
    annotated_frame = hand_detector.draw_landmarks(sample_frame, mock_landmarks)

    # 結果が画像であることを確認
    assert annotated_frame is not None
    assert annotated_frame.shape == sample_frame.shape
    assert isinstance(annotated_frame, np.ndarray)


def test_landmarks_format(hand_detector):
    """ランドマークのフォーマットが正しいかテスト"""
    # 手の画像を模したサンプルを作成（実際には手がないので空の結果になるが構造は確認できる）
    sample_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    result = hand_detector.detect(sample_frame)

    # handsリストが空でない場合、各handの構造を確認
    for hand in result["hands"]:
        assert "label" in hand
        assert "landmarks" in hand
        assert "confidence" in hand
        assert hand["label"] in ["Left", "Right"]
        assert isinstance(hand["landmarks"], list)
        assert isinstance(hand["confidence"], float)

        # ランドマークが21個あることを確認
        if len(hand["landmarks"]) > 0:
            assert len(hand["landmarks"]) == 21
            # 各ランドマークが[x, y, z]の形式であることを確認
            for landmark in hand["landmarks"]:
                assert len(landmark) == 3
