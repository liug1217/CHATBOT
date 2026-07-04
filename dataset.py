"""
dataset.py
----------
負責:
1. 讀取語料文字檔
2. 切分成 train / validation
3. 提供 get_batch() 隨機取出訓練用的 (輸入, 標籤) 配對

這裡不使用 torch.utils.data.Dataset + DataLoader 的完整寫法,
而是採用「語言模型訓練最常見」的隨機取樣方式,直接從長序列中裁切片段,
效能更好、程式碼也更精簡。
"""

import os
import glob
import torch
from config import Config
from tokenizer import CharTokenizer


def load_corpus_text(data_dir: str) -> str:
    """
    讀取 data_dir 底下所有 .txt 檔案,依檔名排序後合併成一份完整文字。
    這樣可以把語料依用途拆成多個檔案管理(例如 chat.txt、story.txt、
    qa.txt、code.txt),彼此互不影響,之後要增減某一類語料也很清楚。
    """
    if not os.path.isdir(data_dir):
        raise FileNotFoundError(
            f"找不到語料資料夾: {data_dir}\n"
            "請建立這個資料夾,並在裡面放入至少一個 .txt 檔案。"
        )

    txt_files = sorted(glob.glob(os.path.join(data_dir, "*.txt")))
    if not txt_files:
        raise FileNotFoundError(
            f"{data_dir} 資料夾底下沒有任何 .txt 檔案,請至少放入一個語料檔。"
        )

    texts = []
    for path in txt_files:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        texts.append(content)
        print(f"[dataset] 已讀取語料檔: {path} ({len(content)} 字元)")

    # 用換行分隔不同檔案的內容,避免前一個檔案的結尾和下一個檔案的開頭黏在一起
    return "\n".join(texts)


class TextDataset:
    def __init__(self, config: Config, tokenizer: CharTokenizer):
        self.config = config
        self.tokenizer = tokenizer

        text = load_corpus_text(config.data_dir)

        data = torch.tensor(tokenizer.encode(text), dtype=torch.long)

        split_idx = int(len(data) * config.train_split)
        self.train_data = data[:split_idx]
        self.val_data = data[split_idx:]

        print(f"[dataset] 全文長度: {len(text)} 字元")
        print(f"[dataset] 訓練集: {len(self.train_data)} tokens, "
              f"驗證集: {len(self.val_data)} tokens")

    def get_batch(self, split: str = "train"):
        """
        隨機取出一個 batch。
        split: "train" 或 "val"
        回傳: x, y,兩者形狀皆為 (batch_size, block_size)
              y 是 x 往右移一位(下一個字元預測任務的標籤)
        """
        data = self.train_data if split == "train" else self.val_data
        block_size = self.config.block_size
        batch_size = self.config.batch_size

        if len(data) <= block_size:
            raise ValueError(
                f"資料長度({len(data)})小於 block_size({block_size}),"
                "請提供更長的語料或調小 block_size。"
            )

        # 隨機選取 batch_size 個起始點
        ix = torch.randint(0, len(data) - block_size - 1, (batch_size,))
        x = torch.stack([data[i: i + block_size] for i in ix])
        y = torch.stack([data[i + 1: i + block_size + 1] for i in ix])

        x, y = x.to(self.config.device), y.to(self.config.device)
        return x, y


if __name__ == "__main__":
    # 簡單自我測試:需要先有一個 data/ 資料夾,裡面至少一個 .txt 檔案
    cfg = Config()
    os.makedirs(cfg.data_dir, exist_ok=True)
    sample_path = os.path.join(cfg.data_dir, "_sample.txt")
    if not any(glob.glob(os.path.join(cfg.data_dir, "*.txt"))):
        # 若資料夾是空的,先建立一份小範例方便測試
        with open(sample_path, "w", encoding="utf-8") as f:
            f.write("你好世界" * 200)

    text = load_corpus_text(cfg.data_dir)
    tok = CharTokenizer.build_from_text(text)
    ds = TextDataset(cfg, tok)
    x, y = ds.get_batch("train")
    print("x shape:", x.shape, "y shape:", y.shape)
