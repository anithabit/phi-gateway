import re

from transformers import (
    AutoModelForTokenClassification,
    AutoTokenizer,
    DataCollatorForTokenClassification,
    Trainer,
    TrainingArguments,
)

from phi_gateway.evaluate import load_notes

MODEL_NAME = "distilbert-base-cased"
TYPES = ["NAME", "LOCATION", "DATE", "AGE", "PHONE", "EMAIL", "SSN", "MRN", "ID", "ZIP", "URL", "IP"]
LABELS = ["O"] + [f"{p}-{t}" for t in TYPES for p in ("B", "I")]
LABEL2ID = {label: i for i, label in enumerate(LABELS)}

def split_words(text):
    return [(m.start(), m.end()) for m in re.finditer(r"\w+|[^\w\s]", text)]


def word_tags(words, gold):
    tags = []
    for ws, we in words:
        tag = "O"
        for gs, ge, label in gold:
            if ws >= gs and we <= ge:
                tag = ("B-" if ws == gs else "I-") + label
        tags.append(tag)
    return tags

    def encode(text, gold, tokenizer):
    words = split_words(text)
    tags = word_tags(words, gold)
    enc = tokenizer([text[s:e] for s, e in words], is_split_into_words=True, truncation=True, max_length=256)
    labels = []
    previous = None
    for word_id in enc.word_ids():
        if word_id is None or word_id == previous:
            labels.append(-100)
        else:
            labels.append(LABEL2ID[tags[word_id]])
        previous = word_id
    enc["labels"] = labels
    return dict(enc)

    if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForTokenClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(LABELS),
        id2label=dict(enumerate(LABELS)),
        label2id=LABEL2ID,
    )
    print("Parameters:", sum(p.numel() for p in model.parameters()))

    data = [encode(text, gold, tokenizer) for text, gold in load_notes("data/train_notes.txt")]

    args = TrainingArguments(
        output_dir="models/run",
        num_train_epochs=3,
        per_device_train_batch_size=16,
        learning_rate=5e-5,
        logging_steps=50,
        save_strategy="no",
        report_to="none",
    )
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=data,
        data_collator=DataCollatorForTokenClassification(tokenizer),
    )
    trainer.train()
    trainer.save_model("models/phi-model")
    tokenizer.save_pretrained("models/phi-model")
    print("Saved to models/phi-model")