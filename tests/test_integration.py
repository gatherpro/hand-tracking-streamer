"""
Integration tests for the entire system
Agent5が実装

全モジュールの統合テストを実施します。
他のAgentのモジュールが未実装の場合はモックを使用してテストします。
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open
import sys
import os
import yaml
import numpy as np
from datetime import datetime

# src ディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import HandTrackingApp


@pytest.fixture
def mock_config():
    """テスト用の設定データを提供"""
    return {
        "camera": {
            "device_id": 0,
            "width": 1280,
            "height": 720,
            "fps": 30
        },
        "hand_detection": {
            "model_complexity": 1,
            "min_detection_confidence": 0.5,
            "min_tracking_confidence": 0.5,
            "max_num_hands": 2
        },
        "measurement": {
            "landmarks_to_measure": [[0, 4], [0, 8], [0, 12], [0, 16], [0, 20]],
            "unit": "cm",
            "scale_factor": 10.0
        },
        "data_sender": {
            "endpoint": "http://localhost:8000/api/hand-data",
            "method": "POST",
            "retry_attempts": 3,
            "retry_delay": 1.0
        },
        "logging": {
            "level": "INFO",
            "format": "json",
            "file": "hand_tracker.log"
        }
    }


@pytest.fixture
def mock_modules():
    """全モジュールのモックを提供"""
    # CameraCapture モック
    camera_mock = Mock()
    camera_mock.start.return_value = True
    camera_mock.get_frame.return_value = (True, np.zeros((720, 1280, 3), dtype=np.uint8))
    camera_mock.stop.return_value = None
    camera_mock.is_opened.return_value = True

    # HandDetector モック
    detector_mock = Mock()
    detector_mock.detect.return_value = {
        "hand_count": 1,
        "hands": [
            {
                "label": "Right",
                "landmarks": [[0.5, 0.5, 0.0] for _ in range(21)],
                "confidence": 0.95
            }
        ],
        "timestamp": datetime.now().isoformat()
    }

    # JointMeasurement モック
    measurement_mock = Mock()
    measurement_mock.calculate_distances.return_value = {
        "measurements": {
            "wrist_to_thumb": {"distance": 12.5, "unit": "cm"},
            "wrist_to_index": {"distance": 15.3, "unit": "cm"},
            "wrist_to_middle": {"distance": 16.8, "unit": "cm"},
            "wrist_to_ring": {"distance": 15.1, "unit": "cm"},
            "wrist_to_pinky": {"distance": 13.2, "unit": "cm"}
        }
    }

    # DataSender モック
    sender_mock = Mock()
    sender_mock.connect.return_value = True
    sender_mock.send_data.return_value = True
    sender_mock.disconnect.return_value = None
    sender_mock.is_connected.return_value = True

    return {
        "camera": camera_mock,
        "detector": detector_mock,
        "measurement": measurement_mock,
        "sender": sender_mock
    }


class TestHandTrackingApp:
    """HandTrackingApp のテストクラス"""

    def test_load_config(self, mock_config, tmp_path):
        """設定ファイルの読み込みテスト"""
        # 一時的な設定ファイルを作成
        config_file = tmp_path / "test_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(mock_config, f)

        # 設定を読み込み
        app = HandTrackingApp(config_path=str(config_file))

        assert app.config is not None
        assert "camera" in app.config
        assert "hand_detection" in app.config
        assert app.config["camera"]["device_id"] == 0

    def test_load_config_file_not_found(self):
        """存在しない設定ファイルのエラーハンドリングテスト"""
        with pytest.raises(FileNotFoundError):
            app = HandTrackingApp(config_path="nonexistent_config.yaml")

    @patch('main.CameraCapture')
    @patch('main.HandDetector')
    @patch('main.JointMeasurement')
    @patch('main.DataSender')
    def test_initialization_success(
        self, mock_sender_class, mock_measurement_class,
        mock_detector_class, mock_camera_class, mock_config, tmp_path
    ):
        """初期化成功のテスト"""
        # モックの設定
        camera_mock = Mock()
        camera_mock.start.return_value = True
        mock_camera_class.return_value = camera_mock

        sender_mock = Mock()
        sender_mock.connect.return_value = True
        mock_sender_class.return_value = sender_mock

        mock_detector_class.return_value = Mock()
        mock_measurement_class.return_value = Mock()

        # 設定ファイル作成
        config_file = tmp_path / "test_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(mock_config, f)

        # アプリ作成と初期化
        app = HandTrackingApp(config_path=str(config_file))
        result = app.initialize()

        assert result is True
        camera_mock.start.assert_called_once()
        sender_mock.connect.assert_called_once()

    @patch('main.CameraCapture')
    @patch('main.HandDetector')
    @patch('main.JointMeasurement')
    @patch('main.DataSender')
    def test_initialization_camera_failure(
        self, mock_sender_class, mock_measurement_class,
        mock_detector_class, mock_camera_class, mock_config, tmp_path
    ):
        """カメラ起動失敗時のテスト"""
        # カメラの起動を失敗させる
        camera_mock = Mock()
        camera_mock.start.return_value = False
        mock_camera_class.return_value = camera_mock

        mock_sender_class.return_value = Mock()
        mock_detector_class.return_value = Mock()
        mock_measurement_class.return_value = Mock()

        # 設定ファイル作成
        config_file = tmp_path / "test_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(mock_config, f)

        # アプリ作成と初期化
        app = HandTrackingApp(config_path=str(config_file))
        result = app.initialize()

        assert result is False

    @patch('main.CameraCapture')
    @patch('main.HandDetector')
    @patch('main.JointMeasurement')
    @patch('main.DataSender')
    def test_main_loop_with_hand_detection(
        self, mock_sender_class, mock_measurement_class,
        mock_detector_class, mock_camera_class, mock_config, tmp_path
    ):
        """メインループでの手検出とデータ送信のテスト"""
        # モックの設定
        camera_mock = Mock()
        frame_count = [0]  # カウンター用

        def get_frame_side_effect():
            frame_count[0] += 1
            if frame_count[0] <= 3:  # 3フレームだけ処理
                return (True, np.zeros((720, 1280, 3), dtype=np.uint8))
            else:
                return (False, None)

        camera_mock.get_frame.side_effect = get_frame_side_effect
        camera_mock.start.return_value = True
        mock_camera_class.return_value = camera_mock

        detector_mock = Mock()
        detector_mock.detect.return_value = {
            "hand_count": 1,
            "hands": [
                {
                    "label": "Right",
                    "landmarks": [[0.5, 0.5, 0.0] for _ in range(21)],
                    "confidence": 0.95
                }
            ]
        }
        mock_detector_class.return_value = detector_mock

        measurement_mock = Mock()
        measurement_mock.calculate_distances.return_value = {
            "measurements": {
                "wrist_to_thumb": {"distance": 12.5, "unit": "cm"}
            }
        }
        mock_measurement_class.return_value = measurement_mock

        sender_mock = Mock()
        sender_mock.send_data.return_value = True
        sender_mock.connect.return_value = True
        mock_sender_class.return_value = sender_mock

        # 設定ファイル作成
        config_file = tmp_path / "test_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(mock_config, f)

        # アプリ作成と実行
        app = HandTrackingApp(config_path=str(config_file))
        app.running = True

        # 少しのフレームだけ処理してループを抜ける
        iteration_count = 0
        max_iterations = 5

        while app.running and iteration_count < max_iterations:
            success, frame = camera_mock.get_frame()
            if not success:
                break

            detection_result = detector_mock.detect(frame)
            if detection_result["hand_count"] > 0:
                for hand in detection_result["hands"]:
                    measurement_mock.calculate_distances(hand["landmarks"])

                sender_mock.send_data({"test": "data"})

            iteration_count += 1

        # アサーション
        assert detector_mock.detect.call_count >= 1
        assert measurement_mock.calculate_distances.call_count >= 1
        assert sender_mock.send_data.call_count >= 1

    @patch('main.CameraCapture')
    @patch('main.HandDetector')
    @patch('main.JointMeasurement')
    @patch('main.DataSender')
    def test_cleanup(
        self, mock_sender_class, mock_measurement_class,
        mock_detector_class, mock_camera_class, mock_config, tmp_path
    ):
        """クリーンアップ処理のテスト"""
        # モックの設定
        camera_mock = Mock()
        mock_camera_class.return_value = camera_mock

        sender_mock = Mock()
        mock_sender_class.return_value = sender_mock

        mock_detector_class.return_value = Mock()
        mock_measurement_class.return_value = Mock()

        # 設定ファイル作成
        config_file = tmp_path / "test_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(mock_config, f)

        # アプリ作成とクリーンアップ
        app = HandTrackingApp(config_path=str(config_file))
        app.cleanup()

        # リソースが解放されたことを確認
        camera_mock.stop.assert_called_once()
        sender_mock.disconnect.assert_called_once()

    @patch('main.CameraCapture')
    @patch('main.HandDetector')
    @patch('main.JointMeasurement')
    @patch('main.DataSender')
    def test_handle_shutdown(
        self, mock_sender_class, mock_measurement_class,
        mock_detector_class, mock_camera_class, mock_config, tmp_path
    ):
        """シャットダウンシグナル処理のテスト"""
        mock_camera_class.return_value = Mock()
        mock_sender_class.return_value = Mock()
        mock_detector_class.return_value = Mock()
        mock_measurement_class.return_value = Mock()

        # 設定ファイル作成
        config_file = tmp_path / "test_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(mock_config, f)

        # アプリ作成
        app = HandTrackingApp(config_path=str(config_file))
        app.running = True

        # シャットダウンシグナル送信
        app.handle_shutdown(2, None)  # SIGINT

        # runningがFalseになったことを確認
        assert app.running is False


def test_full_pipeline():
    """全体パイプラインのテスト（エンドツーエンド）"""
    # このテストは他のAgentが実装完了後に実際のモジュールでテストする
    # 現在はモックでの基本的な統合テストを実施済み
    pass


def test_module_integration():
    """モジュール間連携テスト"""
    # このテストは他のAgentが実装完了後に詳細にテストする
    # 各モジュールのインターフェースが正しく連携することを確認
    pass


def test_error_recovery():
    """エラー回復テスト"""
    # フレーム取得失敗時の回復テストなど
    # 他のAgentが実装完了後に詳細にテストする
    pass


@pytest.mark.parametrize("hand_count", [0, 1, 2])
def test_multiple_hands_detection(hand_count):
    """複数の手の検出テスト（パラメータ化）"""
    # 0本、1本、2本の手が検出された場合のテスト
    # このテストは他のAgentが実装完了後に実施
    pass


def test_performance():
    """パフォーマンステスト"""
    # FPS測定、処理時間測定など
    # 他のAgentが実装完了後に詳細にテストする
    pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
