import random

from faker import Faker

random.seed(42)
Faker.seed(42)
fake = Faker()

SENTENCES = [
    "Patient {NAME} was seen on {DATE}.",
    "{NAME} is a 45-year-old woman with asthma.",
    "{NAME}, a {AGE}-year-old man, was admitted to {LOCATION}.",
    "Pain started 3 days ago. BP 120/80, HR 92.",
    "Call {PHONE} or email {EMAIL}.",
    "MRN: {MRN}. Seen by Dr. {NAME}.",
    "Lives in {LOCATION}, ZIP {ZIP}.",
    "Dr. {NAME} confirmed Parkinson's disease.",
    "Follow up in 2 weeks. Fax {PHONE}.",
    "SSN {SSN}. Discharged on {DATE}.",
    "Aged 67, diabetic since 2015.",
    "Portal link {URL} opened from {IP}.",
]

VALUES = {
    "NAME": lambda: random.choice([fake.name(), fake.first_name(), fake.last_name(), fake.first_name() + " Parkinson"]),
    "DATE": lambda: fake.date(pattern=random.choice(["%m/%d/%Y", "%B %d, %Y", "%d %b %Y", "%Y-%m-%d"])),
    "PHONE": lambda: fake.numerify(random.choice(["###-###-####", "(###) ###-####", "##########"])),
    "EMAIL": lambda: fake.email(safe=True),
    "LOCATION": lambda: random.choice([fake.city(), fake.street_address(), fake.last_name() + " Hospital"]),
    "AGE": lambda: str(random.randint(90, 105)),
    "MRN": lambda: fake.numerify("########"),
    "ZIP": lambda: fake.zipcode(),
    "SSN": lambda: fake.ssn(),
    "URL": lambda: "https://portal.example.org/p/" + fake.numerify("####"),
    "IP": lambda: fake.ipv4_private(),
}

def fill(sentence):
    for label, make in VALUES.items():
        while "{" + label + "}" in sentence:
            sentence = sentence.replace("{" + label + "}", f"[[{label}|{make()}]]", 1)
    return sentence


def make_note():
    chosen = random.sample(SENTENCES, 4)
    return "\n".join(fill(s) for s in chosen)


if __name__ == "__main__":
    notes = [make_note() for _ in range(2000)]
    with open("data/train_notes.txt", "w", encoding="utf-8") as f:
        f.write("\n---\n".join(notes))
    print("Wrote", len(notes), "notes. First one:\n")
    print(notes[0])