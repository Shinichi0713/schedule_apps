import logging
import os

logger = None
def set_logger():
    global logger
    # ロガーの作成
    logger = logging.getLogger('example_logger')

    # ログレベルの設定
    logger.setLevel(logging.DEBUG)

    # ログの出力形式の設定
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # ログの出力先の設定
    dir_current = os.path.dirname(__file__)
    handler = logging.FileHandler(os.path.join(dir_current, 'application.log'))  # ここでファイル名を指定
    handler.setFormatter(formatter)

    # ロガーにハンドラを追加
    logger.addHandler(handler)

    # # ログの出力
    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warning('warning message')
    # logger.error('error message')
    # logger.critical('critical message')

if logger is None:
    set_logger()