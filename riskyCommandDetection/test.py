from transformers import pipeline

# Tạo pipeline cho hỏi đáp sử dụng mô hình BERT
qa_pipeline = pipeline('question-answering', model='bert-large-uncased-whole-word-masking-finetuned-squad')

# Đoạn văn bản để tìm câu trả lời
context = """
Paris is the capital and most populous city of France. The city has a population of over 2 million residents.
Paris is known for its cafe culture, and landmarks such as the Eiffel Tower, the Louvre, Notre-Dame Cathedral, 
and the Arc de Triomphe.
"""

# Câu hỏi cần trả lời
question = "Nhà Trắng ở đâu?"

# Sử dụng pipeline để tìm câu trả lời
result = qa_pipeline(question=question, context=context)

# In kết quả
print(f"Answer: {result['answer']}")
