# Digest email template

The reader is **new to the material**. The goal is to teach the chapter so they
walk away understanding it — not just a list of bullet points. Define jargon,
explain each idea with a concrete example, and keep the detail that matters.

## Required structure

Write the digest in exactly this shape. The first line is the email subject.

```
Subject: 📘 <Book short title> — Ch.<N>: <Chapter title>

**In one line:** <what this chapter is really about, in plain English>

**The big idea**
2–4 sentences. No jargon. If you must use a term, define it in the same breath.

**Key terms** (define every term a newcomer wouldn't know)
- <Term> — <one plain-language line>. e.g. <tiny example>
- <Term> — <one plain-language line>.

**How it works** (the core of the chapter — do not thin this out)
Open with a short **grounding paragraph** that orients the beginner before the details:
what the chapter's subject actually *is* and why it exists (e.g. a "What 'data-intensive'
actually means" opener). Then explain each main concept in turn, each in its own labelled
sub-section. For every concept:
- State it simply.
- Give a concrete example the reader can picture.
- Note the "why" — what problem it solves or where it shows up.
- Add a small inline-SVG schematic where a picture explains faster than words.
This is the heaviest section of the digest and where a beginner actually learns: be
**thorough and complete**, define every term as it appears, and never compress it to save
space. Match the depth of a full teaching write-up — several sub-sections, real detail in
each. If in doubt, longer and clearer beats shorter.

**Why it matters**
Where this shows up in the real world / how it connects to what they'll do next.

**Remember this**
- 3 to 5 crisp takeaways they could recall from memory tomorrow.

**Try it yourself** (always include)
- 4 to 6 **micro-projects**: small things to build, not just reflect on. Each should be
  doable in an hour or two in any language (a fault injector, a percentile meter, a mini
  load test, a tiny redundancy demo). Building is what broadens understanding. Keep them
  beginner-friendly and low-setup, and tie each one to a concept from the chapter.

**Go deeper (optional)**
One pointer, like a section to reread or a natural next question to explore.

**Sources & verify** (always include, last section)
- The primary source this digest is grounded in: book title, chapter, and page range
  where known (for the AWS track, the specific docs.aws.amazon.com pages, as links).
- A one-line reminder that the digest is a teaching draft, not a substitute for the
  source, and that the reader should verify anything they'll rely on against it.
- If any claim was uncertain or the source was thin, say so plainly here.
```

## Style rules

- Warm, encouraging, second person ("you'll notice…"), written as a fellow learner
  sharing what clicked, not a lecturing expert.
- Write like a person: no em dashes (use commas, periods, or parentheses), avoid
  "it's not X, it's Y" and forced rule-of-three phrasing, use contractions.
- Short paragraphs. Prefer a clear sentence over a clever one.
- Never assume prior knowledge; when in doubt, define it.
- **Err on the side of thoroughness.** A full teaching digest runs long (multiple
  screens) and that's correct; completeness beats brevity. Never drop important detail
  to be concise, and never shorten a digest below the depth a beginner needs to actually
  understand the chapter.
- Don't copy sentences from the book; explain in your own words.

## Worked example (abridged)

```
Subject: 📘 Designing Data-Intensive Apps — Ch.1: Reliable, Scalable, Maintainable

**In one line:** What we actually mean when we call a system "good", and the three
qualities worth designing for.

**The big idea**
Before building anything, it helps to agree on what "working well" means. This
chapter breaks it into three goals — reliability, scalability, and
maintainability — and shows they're choices you design for, not luck.

**Key terms**
- Fault — one component going wrong (a disk dies). Different from a failure.
- Failure — the whole system stops doing its job for the user.
- Fault-tolerant — the system keeps working even when a fault happens.

**How it works**
*Reliability* means the system keeps doing the right thing even when things go
wrong. Example: a hard drive in a data center dies roughly once every few years,
so with 10,000 drives you should expect one to die most days — a reliable system
plans for that instead of hoping. …
```
