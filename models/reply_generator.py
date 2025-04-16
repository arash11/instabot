from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class ReplyGenerator:
    def __init__(self, model_name="HooshvareLab/gpt2-fa"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def generate_reply(self, input_text, max_new_tokens=50):
        if not isinstance(input_text, str) or not input_text.strip():
            return "متوجه نشدم، لطفاً واضح‌تر بفرمایید."

        inputs = self.tokenizer.encode(input_text, return_tensors="pt")
        attention_mask = torch.ones_like(inputs)
        outputs = self.model.generate(
            inputs,
            attention_mask=attention_mask,
            max_new_tokens=max_new_tokens,
            pad_token_id=self.tokenizer.eos_token_id,
            no_repeat_ngram_size=2,
            do_sample=True,
            top_p=0.95,
            temperature=0.9
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
