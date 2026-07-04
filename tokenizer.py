"""
tokenizer.py
------------
最簡單的「字元級 (character-level)」tokenizer。
每一個出現過的字元(包含中文字、英文字母、標點、空白...)都會被視為一個 token。

優點:實作簡單、不需要額外訓練詞表演算法。
缺點:序列會比 BPE/WordPiece 長很多。若之後要做更嚴謹的專案,
      可以把這個檔案替換成 HuggingFace tokenizers 或 sentencepiece。
"""

import json
import os


class CharTokenizer:
    def __init__(self, vocab: list[str] | None = None):
        self.vocab = vocab or []
        self.stoi = {ch: i for i, ch in enumerate(self.vocab)}  # string -> id
        self.itos = {i: ch for i, ch in enumerate(self.vocab)}  # id -> string

    @property
    def vocab_size(self) -> int:
        return len(self.vocab)

    @classmethod
    def build_from_text(cls, text: str) -> "CharTokenizer":
        """從語料文字中掃出所有出現過的字元,建立詞表。"""
        chars = sorted(set(text))
        return cls(vocab=chars)

    def encode(self, text: str) -> list[int]:
        """文字 -> id 序列。遇到詞表外的字元會被忽略。"""
        return [self.stoi[ch] for ch in text if ch in self.stoi]

    def decode(self, ids: list[int]) -> str:
        """id 序列 -> 文字。"""
        return "".join(self.itos[i] for i in ids)

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.vocab, f, ensure_ascii=False)

    @classmethod
    def load(cls, path: str) -> "CharTokenizer":
        if not os.path.exists(path):
            raise FileNotFoundError(f"找不到 tokenizer 檔案: {path}")
        with open(path, "r", encoding="utf-8") as f:
            vocab = json.load(f)
        return cls(vocab=vocab)


if __name__ == "__main__":
    # 簡單自我測試
    sample = "你好,世界! Hello, World!"
    tok = CharTokenizer.build_from_text(sample)
    ids = tok.encode(sample)
    print("原文:", sample)
    print("編碼:", ids)
    print("解碼還原:", tok.decode(ids))
    assert tok.decode(ids) == sample
    print("Tokenizer 自我測試通過 ✅")
