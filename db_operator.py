import sqlite3
import os, datetime
import logger

class DBOperator:
    def __init__(self) -> None:
        self.dir_current = os.path.dirname(__file__)
        self.path_db = os.path.join(self.dir_current, 'schedule.db')
        # データベースに接続（存在しない場合は新規作成)
        self.conn = sqlite3.connect(self.path_db)
        logger.logger.info('db connected')

    # タスクを登録
    def register_task(self, data_task):
        # データベースにデータを登録
        with self.conn:
            self.conn.execute('INSERT INTO task VALUES(?, ?, ?, ?)', data_task)
        logger.logger.info('data registered')

    # アペンディクス登録
    def register_appendix(self, data_appendix):
        with self.conn:
            self.conn.execute('INSERT INTO appendix VALUES(?, ?, ?, ?)', data_appendix)
        logger.logger.info('data registered')

    # データ取得
    # 2つのテーブルを結合してデータを取得
    def select_task(self, id_task):
        with self.conn:
            cursor = self.conn.cursor()
            string_sql = 'SELECT * FROM task Inner Join appendix On task.id_schedule = appendix.id_schedule Where task.id_schedule = ?;'
            cursor.execute(string_sql, (id_task,))
            return cursor.fetchall()

    # datetimeからidを生成
    # 引数：日時
    def generate_id(self, data_date):
        # 同じ日時のデータカウント
        with self.conn:
            cursor = self.conn.cursor()
            string_date = data_date.strftime('%Y-%m-%d')
            cursor.execute(f"SELECT COUNT(*) FROM task WHERE day_start = '{string_date}';")
            count = cursor.fetchone()[0]
        id = data_date.strftime(f'%Y%m%d-{count}')
        return id

    def __del__(self):
        logger.logger.info('db operate end')
        self.conn.close()

# データ登録
def register_task():
    dt_current = datetime.datetime(year=2019, month=12, day=30, hour=14, minute=0, second=29)
    db = DBOperator()
    id_data = db.generate_id(dt_current)
    task = (id_data, dt_current.strftime('%Y-%m-%d'), 1, 60)
    db.register_task(task)
    appendix = (id_data, 1, 'test', 'tasks')
    db.register_appendix(appendix)
    del db

# データ参照
def select_task():
    db = DBOperator()
    data = db.select_task('20191230-0')
    print(data)
    del db

if __name__ == '__main__':
    # register_task()
    select_task()
    