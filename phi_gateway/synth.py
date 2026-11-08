import random

from faker import Faker

random.seed(42)
Faker.seed(42)
fake = Faker(["en_US", "en_IN"])

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
    "Mr. {NAME} stays at {LOCATION}, {LOCATION} {ZIP}.",
    "Mrs. {NAME} came in from {LOCATION} on {DATE}.",
    "Referred to Dr. {NAME} at {LOCATION}.",
    "Spoke with the son, {NAME}, regarding {NAME}.",
    "Plan {ID}, billing ref {ID}.",
    "Policy number {ID}. Licence {ID} on file.",
    "Sent to {LOCATION}. Sodium 138, potassium 4.1.",
    "Seen with her husband {NAME}. She is 72.",
    "Scan performed {DATE}; read by Dr. {NAME}.",
    "History of Addison's disease. Reviewed by Dr. {NAME} on {DATE}.",
    "Sample taken on {DATE} at {LOCATION}.",
    "Bed 12. Pain score 3/10. Ambulating with a frame.",
]

PLACE_WORDS = ["Hospital", "Medical Center", "Clinic", "Health Centre", "Infirmary",
               "Nursing Home", "Surgical Center", "Rehab Unit", "Heart Center", "Care Home"]


def make_location():
    return random.choice([
        fake.city(),
        fake.street_address(),
        fake.last_name() + " " + random.choice(PLACE_WORDS),
        fake.city() + " " + random.choice(PLACE_WORDS),
    ])


VALUES = {
    "NAME": lambda: random.choice([fake.name(), fake.first_name(), fake.last_name(),
                                   fake.first_name() + " Parkinson", fake.first_name() + " Addison"]),
    "DATE": lambda: fake.date(pattern=random.choice(["%m/%d/%Y", "%m/%d/%y", "%B %d, %Y", "%d %b %Y",
                                                     "%Y-%m-%d", "%d-%b-%Y", "%b %d, %Y", "%B %d"])),
    "PHONE": lambda: fake.numerify(random.choice(["###-###-####", "(###) ###-####", "##########", "###.###.####"])),
    "EMAIL": lambda: fake.email(safe=True),
    "LOCATION": make_location,
    "AGE": lambda: str(random.randint(90, 105)),
    "MRN": lambda: fake.numerify("########"),
    "ZIP": lambda: fake.numerify(random.choice(["#####", "#####-####"])),
    "SSN": lambda: fake.ssn(),
    "URL": lambda: "https://portal.example.org/p/" + fake.numerify("####"),
    "IP": lambda: fake.ipv4_private(),
    "ID": lambda: random.choice(["INS", "PLN-", "A", "LC"]) + fake.numerify(random.choice(["######", "########"])),
}


def fill(sentence):
    for label, make in VALUES.items():
        while "{" + label + "}" in sentence:
            sentence = sentence.replace("{" + label + "}", f"[[{label}|{make().strip()}]]", 1)
    return sentence


def make_note():
    chosen = random.sample(SENTENCES, 5)
    return "\n".join(fill(s) for s in chosen)


if __name__ == "__main__":
    notes = [make_note() for _ in range(3000)]
    with open("data/train_notes.txt", "w", encoding="utf-8") as f:
        f.write("\n---\n".join(notes))
    print("Wrote", len(notes), "notes. First one:\n")
    print(notes[0])