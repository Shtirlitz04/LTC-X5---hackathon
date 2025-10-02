# model.py
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
from typing import List, Dict, Any
import os

MODEL_PATH = "./model/Model"

_device = "cuda" if torch.cuda.is_available() else "cpu"
_model = None
_tokenizer = None

_labels = ['O', 'B-BRAND', 'I-BRAND', 'B-TYPE', 'I-TYPE',
           'B-PERCENT', 'I-PERCENT', 'B-VOLUME', 'I-VOLUME']

_id2label = {i: l for i, l in enumerate(_labels)}

def load_model():
    """Загружает модель и токенайзер один раз при старте."""
    global _model, _tokenizer
    print(f"📥 Загрузка модели из {MODEL_PATH}...")

    _tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    _model = AutoModelForTokenClassification.from_pretrained(MODEL_PATH)

    # Переводим в eval-режим (важно!)
    _model.eval()

    # Если есть GPU — перемещаем на него
    if torch.cuda.is_available():
        _model.to("cuda")
        print("✅ Модель загружена на GPU")
    else:
        print("⚠️  GPU недоступен, используется CPU")

    return _predict_batch

def _predict_batch(texts):
    """
    Приватная функция для выполнения предсказания NER для батча текстов.
    """

    global _tokenizer, _model, _device, _id2label

    if not texts:
        return []

    inputs = _tokenizer(
        texts,
        return_tensors="pt",
        return_offsets_mapping=True,
        padding=True,
        truncation=True
    )

    offset_mappings = inputs.pop("offset_mapping")
    inputs = {k: v.to(_device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = _model(**inputs)

    logits = outputs.logits
    pred_ids = torch.argmax(logits, dim=-1).cpu().numpy()

    all_batch_results = []

    for i in range(len(texts)):
        input_ids = inputs["input_ids"][i].cpu()
        attention_mask = inputs["attention_mask"][i].cpu()
        offset_mapping = offset_mappings[i]
        preds = pred_ids[i]

        valid_indices = attention_mask == 1
        input_ids = input_ids[valid_indices]
        offset_mapping = offset_mapping[valid_indices]
        preds = preds[:len(input_ids)]

        tokens = _tokenizer.convert_ids_to_tokens(input_ids)
        labels_pred = [_id2label[pred] for pred in preds]
        offsets = offset_mapping.tolist()

        tokens_data = []
        for tok, lab, (s, e) in zip(tokens, labels_pred, offsets):
            if tok not in ("[CLS]", "[SEP]"):
                tokens_data.append((tok, lab, (s, e)))

        merged_tokens_data = []
        if tokens_data:
            current_token, current_label, (current_start, current_end) = tokens_data[0]
            for j in range(1, len(tokens_data)):
                tok, lab, (s, e) = tokens_data[j]
                # Объединяем subword-токены (например, "привет" -> "при", "##вет")
                if tok.startswith("##") or \
                   (tok in [".", ",", "!", "?", ";", ":", "-", "—", "–", "..."] and merged_tokens_data):
                    current_token += tok.replace("##", "")
                    current_end = e
                else:
                    merged_tokens_data.append((current_token, current_label, (current_start, current_end)))
                    current_token, current_label, (current_start, current_end) = tok, lab, (s, e)
            merged_tokens_data.append((current_token, current_label, (current_start, current_end)))

        result_for_text = []
        for _, label, (start_char, end_char) in merged_tokens_data:
            result_for_text.append({
                "start_index": start_char,
                "end_index": end_char,
                "entity": label
            })
        
        all_batch_results.append(result_for_text)

    return all_batch_results
