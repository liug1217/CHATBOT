"""
inference.py
------------
載入訓練好的模型與 tokenizer,根據使用者輸入的 prompt 生成後續文字。
"""

import os
import torch

from config import Config
from tokenizer import CharTokenizer
from model import GPTModel


def load_model(config: Config):
    if not os.path.exists(config.checkpoint_path):
        raise FileNotFoundError(
            f"找不到模型權重: {config.checkpoint_path},請先執行 train.py 訓練模型。"
        )
    if not os.path.exists(config.tokenizer_path):
        raise FileNotFoundError(
            f"找不到 tokenizer 檔案: {config.tokenizer_path},請先執行 train.py 訓練模型。"
        )

    tokenizer = CharTokenizer.load(config.tokenizer_path)

    checkpoint = torch.load(config.checkpoint_path, map_location=config.device)
    model = GPTModel(config, vocab_size=checkpoint["vocab_size"]).to(config.device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    return model, tokenizer


def generate_text(
    prompt: str,
    config: Config | None = None,
    max_new_tokens: int | None = None,
    temperature: float | None = None,
    top_k: int | None = None,
) -> str:
    """
    給定 prompt,回傳「prompt + 模型生成的後續文字」。
    未指定的參數會採用 config.py 裡的預設值。
    """
    config = config or Config()
    model, tokenizer = load_model(config)

    max_new_tokens = max_new_tokens or config.max_new_tokens
    temperature = temperature if temperature is not None else config.temperature
    top_k = top_k if top_k is not None else config.top_k

    idx = torch.tensor(
        [tokenizer.encode(prompt)], dtype=torch.long, device=config.device
    )
    if idx.shape[1] == 0:
        raise ValueError("prompt 編碼後長度為 0,可能包含詞表以外的字元。")

    out_idx = model.generate(
        idx, max_new_tokens=max_new_tokens, temperature=temperature, top_k=top_k
    )
    return tokenizer.decode(out_idx[0].tolist())


if __name__ == "__main__":
    cfg = Config()
    prompt = input("請輸入 prompt: ").strip() or "你好"
    result = generate_text(prompt, cfg)
    print("\n----- 生成結果 -----")
    print(result)
