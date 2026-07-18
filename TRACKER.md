# Progress Tracker

Source of truth for the pipeline. Read before each run, update after.
Kept alongside the books so it travels with them.

## Reading plan

Self-paced batches. Each batch is the next unit for all four tracks (three books plus
AWS). New content only arrives once you've ticked off the current batch below, so it
never piles up. Work sequentially inside a book: finish a chapter before the next, and
a long chapter can span several batches (kept "in progress").

**Track A: Systems design (chapter by chapter)**
1. *Designing Data-Intensive Applications*: 12 chapters (in progress)
2. *AI Engineering* (Chip Huyen): 10 chapters
3. *High Performance MySQL, 4th ed.*: 13 chapters

**Track B: AWS, beyond the basics (topic by topic)**
Core networking → Transit Gateway → EC2 → S3 → Lambda → Queueing/messaging → CloudWatch.
Source is the official AWS docs: https://docs.aws.amazon.com/ . These are web pages,
not PDFs, so for Track B the agent reads the relevant service docs online (fetching
the right pages for each topic) instead of pulling a PDF from Drive. Each topic is
still treated like a chapter: one digest, one carousel.

## Current batch: tick each when you've studied it

<!-- The twice-daily cron (00:00 and 18:00 GMT+1) only sends the NEXT batch once every
     box below is checked. Tick a box by editing this file, e.g. in GitHub's web editor,
     after you've read the digest and built its micro-project. Nothing new arrives, and
     GitHub Pages is not updated, until this batch is fully checked. -->

- [ ] DDIA - Ch.2 (Part 1 of 2) - Data Models and Query Languages: Relational vs. Document
- [ ] AI Engineering - Ch.2 (Part 1 of 2) - Understanding Foundation Models: Training Data & Modeling
- [ ] High Performance MySQL - Ch.2 - Monitoring in a Reliability Engineering World
- [ ] AWS - Transit Gateway & multi-VPC connectivity

## Track A: Designing Data-Intensive Applications

| Ch | Title | Pages | Digested | Carousel | Notes |
|---:|-------|-------|----------|----------|-------|
| 1 | Reliable, Scalable, and Maintainable Applications | 25–48 | 2026-07-18 | 2026-07-18 | reliability / scalability / maintainability |
| 2 | Data Models and Query Languages | 49–90 | 2026-07-18 | 2026-07-18 | in progress — part 1 of 2 done (pages 49–70: relational vs. document, query languages, MapReduce). Resume at page 71 (Graph-Like Data Models) for part 2 |
| 3 | Storage and Retrieval | 91–132 | | | |
| 4 | Encoding and Evolution | 133–166 | | | |
| 5 | Replication | 173–220 | | | |
| 6 | Partitioning | 221–242 | | | |
| 7 | Transactions | 243–294 | | | |
| 8 | The Trouble with Distributed Systems | 295–342 | | | |
| 9 | Consistency and Consensus | 343–406 | | | |
| 10 | Batch Processing | 411–460 | | | |
| 11 | Stream Processing | 461–510 | | | |
| 12 | The Future of Data Systems | 511–574 | | | |


## Track A: AI Engineering (Chip Huyen)

| Ch | Title | Pages | Digested | Carousel | Notes |
|---:|-------|-------|----------|----------|-------|
| 1 | Introduction to Building AI Applications with Foundation Models | 25-72 | | | |
| 2 | Understanding Foundation Models | 73-136 | 2026-07-18 | 2026-07-18 | in progress — part 1 of 2 done (pages 73–101: training data, model architecture, model size). Resume at page 102 (Post-Training) for part 2 |
| 3 | Evaluation Methodology | 137-182 | | | |
| 4 | Evaluate AI Systems | 183-234 | | | |
| 5 | Prompt Engineering | 235-276 | | | |
| 6 | RAG and Agents | 277-330 | | | |
| 7 | Finetuning | 331-386 | | | |
| 8 | Dataset Engineering | 387-428 | | | |
| 9 | Inference Optimization | 429-472 | | | |
| 10 | AI Engineering Architecture and User Feedback | 473-518 | | | |

## Track A: High Performance MySQL (4th ed.)

| Ch | Title | Pages | Digested | Carousel | Notes |
|---:|-------|-------|----------|----------|-------|
| 1 | MySQL Architecture | 23-40 | | | |
| 2 | Monitoring in a Reliability Engineering World | 41-62 | 2026-07-18 | 2026-07-18 | SLIs/SLOs/SLAs, proactive monitoring, percentiles vs. averages |
| 3 | Performance Schema | 63-96 | | | |
| 4 | Operating System and Hardware Optimization | 97-120 | | | |
| 5 | Optimizing Server Settings | 121-146 | | | |
| 6 | Schema Design and Management | 147-176 | | | |
| 7 | Indexing for High Performance | 177-212 | | | |
| 8 | Query Performance Optimization | 213-248 | | | |
| 9 | Replication | 249-278 | | | |
| 10 | Backup and Recovery | 279-308 | | | |
| 11 | Scaling MySQL | 309-334 | | | |
| 12 | MySQL in the Cloud | 335-346 | | | |
| 13 | Compliance with MySQL | 347-364 | | | |

## Track B: AWS beyond the basics

| # | Topic | Source | Digested | Carousel | Notes |
|--:|-------|--------|----------|----------|-------|
| 1 | Core networking (VPC, subnets, route tables, NAT, IGW) | docs.aws.amazon.com | | | |
| 2 | Transit Gateway & multi-VPC connectivity | docs.aws.amazon.com | 2026-07-18 | 2026-07-18 | full-mesh peering math, attachments/route tables, association vs. propagation, segmentation |
| 3 | EC2 (instances, AMIs, ASGs, load balancing) | docs.aws.amazon.com | | | |
| 4 | S3 (storage classes, lifecycle, security) | docs.aws.amazon.com | | | |
| 5 | Lambda (event model, cold starts, limits) | docs.aws.amazon.com | | | |
| 6 | Queueing/messaging (SQS, SNS, EventBridge) | docs.aws.amazon.com | | | |
| 7 | CloudWatch (metrics, logs, alarms, dashboards) | docs.aws.amazon.com | | | |
