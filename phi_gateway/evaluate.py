import re

from phi_gateway.regex_detector import find_phi

MARK = re.compile(r"\[\[([A-Z]+)\|(.+?)\]\]")


def parse_note(marked):
    text = ""
    gold = []
    last = 0
    for m in MARK.finditer(marked):
        text += marked[last:m.start()]
        start = len(text)
        text += m.group(2)
        gold.append((start, len(text), m.group(1)))
        last = m.end()
    text += marked[last:]
    return text, gold


def load_notes(path):
    with open(path, encoding="utf-8") as f:
        parts = f.read().split("---")
    return [parse_note(p.strip()) for p in parts if p.strip()]

def is_covered(g, pred):
    return any(s <= g[0] and g[1] <= e for s, e, label in pred)


def evaluate(notes, detector=find_phi):
    stats = {}
    leaked_notes = 0

    for text, gold in notes:
        pred = [(s, e, label) for s, e, label, value in detector(text)]

        for g in gold:
            stats.setdefault(g[2], [0, 0, 0])
            if g in pred:
                stats[g[2]][0] += 1
            else:
                stats[g[2]][2] += 1

        for p in pred:
            stats.setdefault(p[2], [0, 0, 0])
            if p not in gold:
                stats[p[2]][1] += 1

        if any(not is_covered(g, pred) for g in gold):
            leaked_notes += 1

    return stats, leaked_notes

def show(stats, leaked_notes, total_notes):
    print(f"{'TYPE':10}{'PREC':>7}{'RECALL':>8}{'F1':>7}{'TP':>5}{'FP':>5}{'FN':>5}")
    all_tp = all_fp = all_fn = 0
    for label, (tp, fp, fn) in sorted(stats.items()):
        p = tp / (tp + fp) if tp + fp else 0
        r = tp / (tp + fn) if tp + fn else 0
        f1 = 2 * p * r / (p + r) if p + r else 0
        print(f"{label:10}{p:7.2f}{r:8.2f}{f1:7.2f}{tp:5}{fp:5}{fn:5}")
        all_tp += tp
        all_fp += fp
        all_fn += fn

    p = all_tp / (all_tp + all_fp)
    r = all_tp / (all_tp + all_fn)
    print(f"\nOVERALL   precision {p:.2f}   recall {r:.2f}")
    print(f"LEAK RATE {leaked_notes}/{total_notes} notes = {leaked_notes / total_notes:.0%}")


if __name__ == "__main__":
    notes = load_notes("data/test_notes.txt")
    stats, leaked = evaluate(notes)
    show(stats, leaked, len(notes))