# long_term_memory の中身を眺めて，いらなそうなファイルを消す
# 一旦手動で対応するが，いつかSeLaにやってほしい

import os
import shutil
from glob import glob

os.makedirs("tmp/long_term_memory_removed", exist_ok=True)

rm_list = []

for p in glob("tmp/long_term_memory/*.txt"):
    with open(p, encoding="utf-8_sig") as f:
        print(f.read())
    if input("remove?: yN [N] > ") == "y":
        rm_list.append(os.path.basename(p))

for p in rm_list:
    shutil.move(
        os.path.join("tmp", "long_term_memory", p),
        os.path.join("tmp", "long_term_memory_removed", p),
    )
