import torch
from transformers import AutoModelForTokenClassification, AutoTokenizer

from phi_gateway.train import split_words

MODEL_DIR = "models/phi-model"
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForTokenClassification.from_pretrained(MODEL_DIR)
model.eval()


def model_find(text, threshold=0.5):
    words = split_words(text)
    enc = tokenizer([text[s:e] for s, e in words], is_split_into_words=True,
                    truncation=True, max_length=512, return_tensors="pt")
    with torch.no_grad():
        probs = model(**enc).logits[0].softmax(-1)

    tags = ["O"] * len(words)
    previous = None
    for i, word_id in enumerate(enc.word_ids()):
        if word_id is not None and word_id != previous:
            p = probs[i]
            if 1 - p[0] >= threshold:
                tags[word_id] = model.config.id2label[int(p[1:].argmax()) + 1]
        previous = word_id

    found = []
    prev_label = None
    for (s, e), tag in zip(words, tags):
        if tag == "O":
            prev_label = None
            continue
        label = tag[2:]
        if label == prev_label and tag.startswith("I-"):
            found[-1][1] = e
        else:
            found.append([s, e, label])
        prev_label = label
    return [(s, e, label, text[s:e]) for s, e, label in found]


if __name__ == "__main__":
    import sys

    from phi_gateway.evaluate import evaluate, load_notes, show

    path = sys.argv[1]
    threshold = float(sys.argv[2])
    notes = load_notes(path)
    stats, leaked = evaluate(notes, detector=lambda text: model_find(text, threshold))
    show(stats, leaked, len(notes))