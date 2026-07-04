"""
main.py
-------
專案的統一入口。使用方式:

    python main.py train                       # 開始訓練
    python main.py infer --prompt "你好"         # 用訓練好的模型生成文字
    python main.py infer                        # 進入互動模式,可連續輸入 prompt
"""

import argparse

from config import Config
from train import train
from inference import generate_text


def main():
    parser = argparse.ArgumentParser(description="小型 GPT 語言模型專案")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ---- train 子命令 ----
    subparsers.add_parser("train", help="訓練模型")

    # ---- infer 子命令 ----
    infer_parser = subparsers.add_parser("infer", help="使用模型生成文字")
    infer_parser.add_argument(
        "--prompt", type=str, default=None, help="起始文字,不提供則進入互動模式"
    )
    infer_parser.add_argument(
        "--max_new_tokens", type=int, default=None, help="要生成的 token 數量"
    )
    infer_parser.add_argument(
        "--temperature", type=float, default=None, help="取樣溫度,越高越隨機"
    )
    infer_parser.add_argument(
        "--top_k", type=int, default=None, help="只從機率最高的 k 個 token 中取樣"
    )

    args = parser.parse_args()
    config = Config()

    if args.command == "train":
        train(config)

    elif args.command == "infer":
        if args.prompt:
            result = generate_text(
                args.prompt,
                config,
                max_new_tokens=args.max_new_tokens,
                temperature=args.temperature,
                top_k=args.top_k,
            )
            print(result)
        else:
            print("進入互動模式,輸入 'exit' 離開。")
            while True:
                prompt = input("\n請輸入 prompt: ").strip()
                if prompt.lower() == "exit":
                    break
                result = generate_text(
                    prompt,
                    config,
                    max_new_tokens=args.max_new_tokens,
                    temperature=args.temperature,
                    top_k=args.top_k,
                )
                print("\n----- 生成結果 -----")
                print(result)


if __name__ == "__main__":
    main()
