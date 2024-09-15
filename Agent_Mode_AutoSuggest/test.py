from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

# Tải tokenizer và mô hình
tokenizer = AutoTokenizer.from_pretrained('distilbert-base-cased-distilled-squad')
model = AutoModelForQuestionAnswering.from_pretrained('distilbert-base-cased-distilled-squad')

# Văn bản và câu hỏi
context = "git clone is used to clone a repo on github to local."
question = "what should i do to get a repo on github to my machine?"

# Tokenize văn bản và câu hỏi
inputs = tokenizer(question, context, return_tensors='pt')

# Dự đoán điểm bắt đầu và kết thúc của câu trả lời trong văn bản
with torch.no_grad():
    outputs = model(**inputs)

start_scores = outputs.start_logits
end_scores = outputs.end_logits

# Xác định vị trí bắt đầu và kết thúc của câu trả lời
start_index = torch.argmax(start_scores)
end_index = torch.argmax(end_scores) + 1

# Giải mã câu trả lời từ vị trí trong văn bản
answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs.input_ids[0][start_index:end_index]))
print(f"Answer: {answer}")
