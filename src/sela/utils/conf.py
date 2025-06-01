import os
from os.path import abspath, dirname, join

import yaml


class Conf:
    def __init__(self, conf_path: str | None = None):
        if not conf_path:
            dir_path = dirname(abspath(__file__))
            tmp_path = join(dirname(dirname(dirname(dir_path))), "tmp")
            conf_path = join(tmp_path, "conf.yaml")

        with open(conf_path) as f:
            self.conf = yaml.safe_load(f.read())
            for k, v in self.conf.items():
                if k.upper() == k:  # 大文字変数は環境変数としてロード
                    os.environ[k] = v
