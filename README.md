# LoRAで教師あり微調整(SFT)をして.ggufにするやつ
Sample-lora-sft-2-gguf

小さな言語モデル [Qwen2.5-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct) を、  
自分のデータで LoRA ファインチューニングし、[llama.cpp](https://github.com/ggml-org/llama.cpp)や[LLMTextCore](https://github.com/ABATBeliever/LLMTextCore)で動く **GGUF** 形式にするまでの  
手順とスクリプトをまとめたものです。

Qwen 2.5-0.5B-Instruct は小さいモデルなので簡単に作れます。  
ただし、実用性はあまりないかもしれません。

学習したいデータとGoogleアカウント、多少のマシンリソースがあれば、**GPU不要**で動きます。

```
[ 1 ] 学習データをCSVで用意する
 ↓
[ 2 ] Colab で LoRA 学習
 ↓
[ 3 ] ベースモデルにマージ
 ↓
[ 4 ] GGUF 変換 + 量子化
 ↓
[END] *.gguf ゲット！
```

---

## ディレクトリ構成

```
.
├── README.md                     # これ
├── LICENSE
├── 0.環境.txt                    # 環境構築
├── 1.CSV2JSONL.py                # 学習データセットを整形
├── 2.LoRA_Colab.txt              # Google Colab (T4 GPU) で LoRA 学習 を実行
├── 3.merge.py                    # LoRA アダプタをベースモデルに統合
└── 4.Conv2GGUF.txt               # GGUF 変換、量子化
```

---

## 動作環境

| 項目 | 内容 |
|---|---|
| OS（ローカル作業） | Windows 10 / 11（x64） |
| Python | 3.11.8 |
| パッケージ管理 | [uv](https://docs.astral.sh/uv/) |
| 学習 | Google Colab（無料枠の T4 GPU で動作確認） |
| ベースモデル | `Qwen/Qwen2.5-0.5B-Instruct` |

---

## 使い方
基本的に、ファイル名の数字が小さい順に読んだり実行したりします。

### 環境構築
0.環境.txt に従ってください

### 学習データセットを整形
```
uv run python 1.CSV2JSONL.py
```

### Google Colab (T4 GPU) で LoRA 学習 を実行
2.LoRA_Colab.txt に従ってください。  
> ※この処理だけはくそ重いのでGoogle Colabで行ってください。  
　終わるとダウンロードされるzipを、このリポジトリを置いたパスに展開した状態で配置します。  
　ちなみに、ローカルのCPU(13世代i7)で行うと約18時間かかります。Colab無料枠なら3分。

### LoRA アダプタをベースモデルに統合
```
uv run python 3.merge.py
```

### GGUF 変換、量子化
4.Conv2GGUF.txt に従ってください

## ライセンス・第三者ソフトウェアについて

このキットはABATBelieverが制作したもので、[MIT License](./LICENSE) で公開します。

### Llama-cpp

このキットは llama.cpp そのものは含んでいませんが、作業中に利用します。  
ほとんどはMITLicenseですが、**libomp.dllは Apache-2.0 with LLVM exceptions です**。

### ベースモデル（Qwen2.5-0.5B-Instruct）

- 提供: Alibaba Cloud（Qwen Team）
- ライセンス: **Apache License 2.0**（ https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct ）
- このリポジトリにはモデルの重みを含みません。学習・マージ時に Hugging Face から自動ダウンロードされます。
- このキットで作った `lora_adapter` / `merged_model` / `.gguf` を **公開・配布する場合** は、Apache-2.0 の条件（ライセンス文の添付、改変の明示、元の著作権表示の保持など）に従ってください。
- **違うモデルを使った場合、例えば同じQwenの世代違いやサイズ違いでも、ライセンスが違うかもしれません。**

### 依存ライブラリ (同梱されていないPythonライブラリ)

- PyTorch
- Transformers
- PEFT
- TRL
- Datasets
- SentencePiece
- Pandas

`uv pip install` で各自の環境に取得されます。各ライブラリのライセンスは、それぞれの配布元を参照してください。

### 学習データについて

`train_data.jsonl` は各自でCSVを用意し、`1.CSV2JSONL.py`で変換して生成するものです。  
他人の著作物や個人情報を含むデータを学習に使う場合は、その利用条件に注意してください。  
このリポジトリには学習データは含まれていません。  

※ChatGPTなどのAIに学習データを作ってもらう場合、「利用規約違反の蒸留」にご注意ください。

## 免責

- 本キットは Alibaba Cloud（Qwen）・llama.cpp / ggml プロジェクト・Google・Hugging Face とは **一切無関係の非公式なものであり、承認や保証を受けていません**。  
　商標は各権利者に帰属します。
- 本キットは無保証（AS IS）で提供されます。利用によって生じたいかなる損害についても、作者は責任を負いません。
