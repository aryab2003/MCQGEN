import spacy
from collections import Counter
import random

nlp = spacy.load("en_core_web_sm")


def generate_mcqs(text, num_questions, num_distractors):

    doc = nlp(text)
    sel_sents = list(doc.sents)

    mcqs = []
    selected_sentences = set()

    while len(mcqs) < num_questions and len(selected_sentences) < len(sel_sents):
        sent = random.choice(sel_sents)

        if sent in selected_sentences:
            continue

        selected_sentences.add(sent)

        sent_text = sent.text.lower()
        doc = nlp(sent_text)

        nouns = [token.text for token in doc if token.pos_ == "NOUN"]

        if len(nouns) < 2:
            continue

        noun_counts = Counter(nouns)

        if noun_counts:
            subject = noun_counts.most_common(1)[0][0]
            ans = [subject]
            stem = sent_text.replace(subject, "-------")
            distractors = list(set(nouns).difference(set([subject])))

            if len(distractors) < num_distractors:
                continue

            distractor_options = random.sample(distractors, num_distractors - 1)
            ans.extend(distractor_options)
            random.shuffle(ans)
            corr_ind = chr(65 + ans.index(subject))
            mcqs.append((stem, ans, corr_ind))

    return mcqs
