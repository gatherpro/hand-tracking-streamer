"""
Main Controller & Integration
Agent5担当: 全モジュールの統合とメインループ実装

このモジュールは全てのコンポーネントを統合し、
手追跡システムのメインループを実装します。
"""

import yaml
import logging
from pythonjsonlogger import jsonlogger
import signal
import sys
from typing import Optional
from datetime import datetime
import os

# 他のモジュールをインポート
try:
    from camera_capture import CameraCapture
    from hand_detector import HandDetector
    from joint_measurement import JointMeasurement
    from data_sender import DataSender
except ImportError as e:
    # モジュールが未実装の場合は警告を出すが、続行する（テスト用）
    logging.warning(f"Some modules not available: {e}")
    # テスト用にNoneで定義
    CameraCapture = None
    HandDetector = None
    JointMeasurement = None
    DataSender = None


class HandTrackingApp:
    """
    手追跡アプリケーションのメインコントローラー

    全モジュールを統合し、メインループを実行します。
    カメラからのフレーム取得 → 手検出 → 距離計測 → データ送信の
    パイプラインを管理します。

    Attributes:
        config (dict): アプリケーション設定
        camera: カメラキャプチャインスタンス
        detector: 手検出器インスタンス
        measurement: 関節計測インスタンス
        sender: データ送信インスタンス
        running (bool): アプリケーション実行状態
        logger: ロガーインスタンス
    """

    def __init__(self, config_path: str = "config.yaml"):
        """
        アプリケーションの初期化

        Args:
            config_path (str): 設定ファイルのパス
        """
        self.config = self.load_config(config_path)
        self.setup_logging()
        self.running = False
        self.logger = logging.getLogger(__name__)

        # 各モジュールのインスタンスを初期化
        # 他のAgentが実装完了したらコメントを外す
        try:
            if CameraCapture is not None:
                self.camera = CameraCapture(self.config["camera"])
            else:
                self.camera = None

            if HandDetector is not None:
                self.detector = HandDetector(self.config["hand_detection"])
            else:
                self.detector = None

            if JointMeasurement is not None:
                self.measurement = JointMeasurement(self.config["measurement"])
            else:
                self.measurement = None

            if DataSender is not None:
                self.sender = DataSender(self.config["data_sender"])
            else:
                self.sender = None
        except (NameError, AttributeError, TypeError) as e:
            self.logger.warning(f"Modules not fully implemented yet: {e}")
            self.camera = None
            self.detector = None
            self.measurement = None
            self.sender = None

        # シグナルハンドラの設定
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)

    def load_config(self, config_path: str) -> dict:
        """
        設定ファイルを読み込む

        Args:
            config_path (str): 設定ファイルのパス

        Returns:
            dict: 設定辞書

        Raises:
            FileNotFoundError: 設定ファイルが見つからない場合
            yaml.YAMLError: YAMLパースエラーの場合
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config
        except FileNotFoundError:
            print(f"Error: Config file not found: {config_path}")
            raise
        except yaml.YAMLError as e:
            print(f"Error: Failed to parse config file: {e}")
            raise

    def setup_logging(self):
        """
        ロギングを設定

        config.yamlの設定に基づいてロギングを初期化します。
        JSONフォーマットでファイルとコンソールに出力します。
        """
        log_config = self.config.get("logging", {})
        log_level = log_config.get("level", "INFO")
        log_format = log_config.get("format", "json")
        log_file = log_config.get("file", "hand_tracker.log")

        # ログレベルの設定
        level = getattr(logging, log_level.upper(), logging.INFO)

        # ログフォーマットの設定
        if log_format == "json":
            formatter = jsonlogger.JsonFormatter(
                '%(timestamp)s %(name)s %(levelname)s %(message)s'
            )
        else:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )

        # ルートロガーの設定
        root_logger = logging.getLogger()
        root_logger.setLevel(level)

        # 既存のハンドラをクリア
        root_logger.handlers = []

        # ファイルハンドラ
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

        # コンソールハンドラ
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    def initialize(self) -> bool:
        """
        全モジュールを初期化

        各モジュールの起動と接続を確立します。

        Returns:
            bool: 初期化成功でTrue、失敗でFalse
        """
        self.logger.info("Initializing Hand Tracking System...")

        # モジュールが利用可能かチェック
        if not all([self.camera, self.detector, self.measurement, self.sender]):
            self.logger.error("Not all modules are available")
            return False

        # カメラ起動
        try:
            if not self.camera.start():
                self.logger.error("Failed to start camera")
                return False
            self.logger.info("Camera started successfully")
        except Exception as e:
            self.logger.error(f"Exception while starting camera: {e}")
            return False

        # データ送信先に接続
        try:
            if not self.sender.connect():
                self.logger.warning("Failed to connect to data endpoint")
                # データ送信は必須ではないので、続行
        except Exception as e:
            self.logger.warning(f"Exception while connecting to sender: {e}")

        self.logger.info("Initialization complete")
        return True

    def main_loop(self):
        """
        メインループ

        処理フロー:
        1. カメラからフレーム取得
        2. 手の検出とランドマーク取得
        3. 関節距離の計測
        4. データの送信
        5. 次のフレームへ

        Ctrl+C (SIGINT) またはSIGTERMで終了します。
        """
        self.logger.info("Starting main loop...")
        self.running = True

        frame_count = 0

        while self.running:
            try:
                # 1. フレーム取得
                success, frame = self.camera.get_frame()
                if not success:
                    self.logger.warning("Failed to get frame")
                    continue

                frame_count += 1

                # 2. 手検出
                detection_result = self.detector.detect(frame)

                if detection_result["hand_count"] == 0:
                    # 手が検出されなければスキップ
                    continue

                self.logger.debug(
                    f"Detected {detection_result['hand_count']} hand(s)"
                )

                # 3. 各手について距離計測
                all_measurements = []
                for hand in detection_result["hands"]:
                    landmarks = hand["landmarks"]

                    # 距離計算
                    measurements = self.measurement.calculate_distances(landmarks)

                    all_measurements.append({
                        "hand_id": len(all_measurements),
                        "label": hand["label"],
                        "joints": measurements["measurements"]
                    })

                # 4. データ送信
                data = {
                    "timestamp": datetime.now().isoformat(),
                    "frame_number": frame_count,
                    "hand_data": {
                        "hand_count": detection_result["hand_count"],
                        "measurements": all_measurements
                    }
                }

                if not self.sender.send_data(data):
                    self.logger.warning("Failed to send data")
                else:
                    self.logger.debug("Data sent successfully")

            except KeyboardInterrupt:
                # Ctrl+Cでの終了
                self.logger.info("Keyboard interrupt received")
                break
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}", exc_info=True)
                # エラーが発生しても続行
                continue

        self.logger.info("Main loop ended")

    def run(self):
        """
        アプリケーションを実行

        初期化 → メインループ → クリーンアップの流れを管理します。
        """
        self.logger.info("Starting Hand Tracking Application...")

        if not self.initialize():
            self.logger.error("Initialization failed, exiting")
            sys.exit(1)

        try:
            self.main_loop()
        except Exception as e:
            self.logger.error(f"Fatal error in main loop: {e}", exc_info=True)
        finally:
            self.cleanup()

        self.logger.info("Application stopped")

    def handle_shutdown(self, signum, frame):
        """
        シャットダウン処理

        シグナルを受信したときに呼ばれます。

        Args:
            signum: シグナル番号
            frame: フレーム情報
        """
        self.logger.info(f"Shutdown signal received: {signum}")
        self.running = False

    def cleanup(self):
        """
        リソースのクリーンアップ

        カメラの停止とデータ送信の切断を行います。
        """
        self.logger.info("Cleaning up resources...")

        if self.camera:
            try:
                self.camera.stop()
                self.logger.info("Camera stopped")
            except Exception as e:
                self.logger.error(f"Error stopping camera: {e}")

        if self.sender:
            try:
                self.sender.disconnect()
                self.logger.info("Data sender disconnected")
            except Exception as e:
                self.logger.error(f"Error disconnecting sender: {e}")

        self.logger.info("Cleanup complete")


def main():
    """
    エントリーポイント

    コマンドライン引数で設定ファイルのパスを指定できます。
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Hand Tracking System - Main Controller"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)"
    )
    args = parser.parse_args()

    # 設定ファイルの存在確認
    if not os.path.exists(args.config):
        print(f"Error: Configuration file not found: {args.config}")
        sys.exit(1)

    # アプリケーション起動
    app = HandTrackingApp(config_path=args.config)
    app.run()


if __name__ == "__main__":
    main()
