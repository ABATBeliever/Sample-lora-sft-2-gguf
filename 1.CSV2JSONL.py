import json
import re

import pandas as pd

# data.csv という名前で、以下の構造のCSV学習データを用意してください
# システムプロンプト,プロンプト,回答

# ChatGPTなどのAIに作ってもらった場合、「利用規約違反の蒸留」に該当する可能性があります。ご注意ください
# (詳細については、それこそAIに聞いてください)

# ===== 設定 =====
CSV_PATH = 'data.csv'             # 入力CSV
OUTPUT_PATH = 'train_data.jsonl'  # 出力JSONL
COLUMNS = ['system', 'input', 'output']

read_options = dict(
    header=None,
    names=COLUMNS,
    dtype=str,
    keep_default_na=False,
    encoding='utf-8-sig',
)

try:
    df = pd.read_csv(CSV_PATH, **read_options)
except Exception as e:
    print(f"Failed to Load: {e}")
    print("列数が合わない行をスキップします...")
    df = pd.read_csv(CSV_PATH, on_bad_lines='skip', **read_options)

df = df.fillna('')
for col in COLUMNS:
    df[col] = df[col].astype(str).str.strip()

print("--- CSVについて ---")
print(f"件数: {len(df)} 件")
empty_counts = {col: int((df[col] == '').sum()) for col in COLUMNS}
print(f"空欄: {empty_counts}")

if len(df) > 0 and (df['output'] == '').all():
    print("\n[警告] 模範解答の列がすべて空です。"
          "3列（システムプロンプト,質問,模範解答）にしてください。")

print("\n--- システムプロンプトの種類 ---")
sys_counts = df['system'].replace('', '(空)').value_counts()
print(f"種類数: {len(sys_counts)}")
for text, n in sys_counts.head(5).items():
    short = text if len(text) <= 40 else text[:40] + '...'
    print(f"{n:>6} 件: {short}")

df['kw_count'] = df['output'].apply(lambda x: len(x.split()))
print("\n--- 模範解答の単語数（空白区切り） ---")
print(df['kw_count'].value_counts().sort_index().to_string())

print("\n--- 質問の文頭の上位 ---")
df['first_word'] = df['input'].apply(lambda x: re.split(r'[、\s]', x)[0])
print(df['first_word'].value_counts().head(5).to_string())

jsonl_lines = []
skipped = 0
no_system = 0

for _, row in df.iterrows():
    system, inp, out = row['system'], row['input'], row['output']

    if not inp or not out:
        skipped += 1
        continue

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    else:
        no_system += 1
    messages.append({"role": "user", "content": inp})
    messages.append({"role": "assistant", "content": out})

    jsonl_lines.append(json.dumps({"messages": messages}, ensure_ascii=False))

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(jsonl_lines) + '\n')

print(f"\n{len(jsonl_lines)} 件のデータ(CSV)を '{OUTPUT_PATH}' (JSONL) に変換しました。")
if skipped:
    print(f"除外: {skipped} 件")
if no_system:
    print(f"システムプロンプトなし: {no_system} 件")
