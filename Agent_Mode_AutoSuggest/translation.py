import re
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import fasttext

# Tải mô hình phát hiện ngôn ngữ fasttext
lang_detect_model = fasttext.load_model('lid.176.bin')

# Định nghĩa bản đồ mã ngôn ngữ cho mBART
lang_code_map = {
    'ar': 'ar_AR', 'cs': 'cs_CZ', 'de': 'de_DE', 'en': 'en_XX', 'es': 'es_XX',
    'et': 'et_EE', 'fi': 'fi_FI', 'fr': 'fr_XX', 'gu': 'gu_IN', 'hi': 'hi_IN',
    'it': 'it_IT', 'ja': 'ja_XX', 'kk': 'kk_KZ', 'ko': 'ko_KR', 'lt': 'lt_LT',
    'lv': 'lv_LV', 'my': 'my_MM', 'ne': 'ne_NP', 'nl': 'nl_XX', 'ro': 'ro_RO',
    'ru': 'ru_RU', 'si': 'si_LK', 'tr': 'tr_TR', 'vi': 'vi_VN', 'zh-cn': 'zh_CN',
    'af': 'af_ZA', 'az': 'az_AZ', 'bn': 'bn_IN', 'fa': 'fa_IR', 'gl': 'gl_ES',
    'he': 'he_IL', 'hr': 'hr_HR', 'id': 'id_ID', 'ka': 'ka_GE', 'km': 'km_KH',
    'mk': 'mk_MK', 'ml': 'ml_IN', 'mn': 'mn_MN', 'mr': 'mr_IN', 'pl': 'pl_PL',
    'ps': 'ps_AF', 'pt': 'pt_XX', 'sq': 'sq_AL', 'ta': 'ta_IN', 'te': 'te_IN',
    'th': 'th_TH', 'uk': 'uk_UA', 'ur': 'ur_PK', 'xh': 'xh_ZA', 'sw': 'sw_KE'
}

def protect_code_snippets(text):
    """
    Đánh dấu các đoạn code trong văn bản bằng cách bao quanh chúng bằng thẻ.
    """
    # Bảo vệ các từ được bao quanh bởi dấu backtick
    text = re.sub(r'`([^`]*)`', r'<code>\1</code>', text)
    
    # Bảo vệ các từ có chứa các ký tự như -, ., /, _
    pattern = r'\b[a-zA-Z0-9_.-/]+\b'
    protected_text = re.sub(pattern, lambda x: f"<code>{x.group(0)}</code>", text)
    
    return protected_text

def unprotect_code_snippets(text):
    """
    Loại bỏ các thẻ bảo vệ khỏi đoạn code.
    """
    return text.replace("<code>", "").replace("</code>", "")

def detect_language_fasttext(text):
    """
    Sử dụng fasttext để phát hiện ngôn ngữ của văn bản.
    """
    predictions = lang_detect_model.predict(text, k=1)
    lang = predictions[0][0].split('__')[-1]  # Trích xuất mã ngôn ngữ từ fasttext
    return lang

def translate_to_english(input_text):
    """
    Dịch câu từ ngôn ngữ đầu vào (tự động phát hiện) sang tiếng Anh, nhưng giữ nguyên đoạn code.

    Args:
    - input_text (str): Câu cần dịch.

    Returns:
    - str: Bản dịch tiếng Anh của câu.
    """
    # Tên mô hình
    model_name = "facebook/mbart-large-50-many-to-many-mmt"
    
    # Tải tokenizer và mô hình
    tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
    model = MBartForConditionalGeneration.from_pretrained(model_name)

    # Tự động phát hiện ngôn ngữ đầu vào bằng fasttext
    detected_lang = detect_language_fasttext(input_text)

    # Tìm mã ngôn ngữ trong bản đồ
    source_language = lang_code_map.get(detected_lang)
    if not source_language:
        raise ValueError(f"Ngôn ngữ '{detected_lang}' không được hỗ trợ bởi mBART.")

    # Bảo vệ đoạn code trong văn bản
    protected_text = protect_code_snippets(input_text)

    # Đặt ngôn ngữ nguồn và ngôn ngữ đích
    tokenizer.src_lang = source_language
    tokenizer.tgt_lang = "en_XX"  # Dịch sang tiếng Anh

    # Mã hóa câu
    inputs = tokenizer(protected_text, return_tensors="pt")

    # Tạo bản dịch
    translated_tokens = model.generate(**inputs)
    translation = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

    # Loại bỏ thẻ bảo vệ từ đoạn code
    final_translation = unprotect_code_snippets(translation)

    return final_translation

# Ví dụ sử dụng
input_text = "để commit thì dùng git clone đúng không?"
english_translation = translate_to_english(input_text)
print(english_translation)
