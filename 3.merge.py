from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

base_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("./lora_adapter")

# LoRAの統合
model = PeftModel.from_pretrained(base_model, "./lora_adapter")
merged_model = model.merge_and_unload()

# マージ済みモデルの保存
merged_model.save_pretrained("./merged_model")
tokenizer.save_pretrained("./merged_model")