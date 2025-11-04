"""
Unit tests for Data Sender Module
Agent4が実装してください
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.data_sender import DataSender


@pytest.fixture
def config():
    """テスト用の設定"""
    return {
        "endpoint": "http://localhost:8000/api/hand-data",
        "method": "POST",
        "websocket_url": "ws://localhost:8000/ws/hand-data",
        "retry_attempts": 3,
        "retry_delay": 0.1  # テストでは短めに設定
    }


@pytest.fixture
def sample_data():
    """テスト用のサンプルデータ"""
    return {
        "timestamp": "2025-11-05T00:00:00",
        "hand_data": {
            "hand_count": 1,
            "measurements": [
                {
                    "hand_id": 0,
                    "label": "Right",
                    "joints": {
                        "wrist_to_thumb": 12.5,
                        "wrist_to_index": 15.3,
                        "wrist_to_middle": 16.8,
                        "wrist_to_ring": 15.1,
                        "wrist_to_pinky": 13.2
                    }
                }
            ]
        }
    }


def test_initialization(config):
    """初期化テスト"""
    sender = DataSender(config)
    assert sender.endpoint == "http://localhost:8000/api/hand-data"
    assert sender.method == "POST"
    assert sender.retry_attempts == 3
    assert sender.retry_delay == 0.1
    assert sender.connected == False


def test_connection_success(config):
    """接続成功テスト"""
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        sender = DataSender(config)
        result = sender.connect()

        assert result == True
        assert sender.is_connected() == True
        mock_get.assert_called_once_with("http://localhost:8000/api/health", timeout=5)


def test_connection_failure(config):
    """接続失敗テスト"""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("Connection error")

        sender = DataSender(config)
        result = sender.connect()

        assert result == False
        assert sender.is_connected() == False


def test_data_sending_success(config, sample_data):
    """データ送信成功テスト"""
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        sender = DataSender(config)
        result = sender.send_data(sample_data)

        assert result == True
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args.kwargs['json'] == sample_data
        assert call_args.kwargs['headers'] == {"Content-Type": "application/json"}


def test_data_sending_failure(config, sample_data):
    """データ送信失敗テスト"""
    with patch('requests.post') as mock_post:
        mock_post.side_effect = Exception("Send error")

        sender = DataSender(config)
        result = sender.send_data(sample_data)

        assert result == False
        assert mock_post.call_count == 3  # retry_attempts回試行される


def test_retry_logic_success_on_second_attempt(config, sample_data):
    """リトライ処理テスト - 2回目で成功"""
    with patch('requests.post') as mock_post:
        # 1回目は失敗、2回目は成功
        mock_response_fail = Mock()
        mock_response_fail.status_code = 500
        mock_response_success = Mock()
        mock_response_success.status_code = 200
        mock_post.side_effect = [mock_response_fail, mock_response_success]

        sender = DataSender(config)
        result = sender.send_data(sample_data)

        assert result == True
        assert mock_post.call_count == 2


def test_retry_logic_all_failures(config, sample_data):
    """リトライ処理テスト - 全て失敗"""
    with patch('requests.post') as mock_post, patch('time.sleep'):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        sender = DataSender(config)
        result = sender.send_data(sample_data)

        assert result == False
        assert mock_post.call_count == 3  # retry_attempts回試行される


def test_disconnect(config):
    """切断テスト"""
    sender = DataSender(config)
    sender.connected = True
    sender.disconnect()

    assert sender.is_connected() == False


def test_is_connected_initial_state(config):
    """接続状態確認テスト - 初期状態"""
    sender = DataSender(config)
    assert sender.is_connected() == False


def test_timeout_configuration(config):
    """タイムアウト設定テスト"""
    sender = DataSender(config)
    assert sender.timeout == 5
