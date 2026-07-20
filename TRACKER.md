# Progress Tracker

Source of truth for the pipeline. Read before each run, update after.
Kept alongside the books so it travels with them.

## Reading plan

Self-paced batches. Each batch is the next unit for all four tracks (three books plus
AWS). New content only arrives once you've ticked off the current batch below, so it
never piles up. Work sequentially inside a book: finish a chapter before the next, and
a long chapter can span several batches (kept "in progress").

**Track A: Systems design (chapter by chapter)**
1. *Designing Data-Intensive Applications*: 12 chapters
2. *AI Engineering* (Chip Huyen): 10 chapters
3. *High Performance MySQL, 4th ed.*: 13 chapters

**Track B: AWS, beyond the basics (topic by topic)**
Core networking → Transit Gateway → EC2 → S3 → Lambda → Queueing/messaging → CloudWatch.
Source is the official AWS docs: https://docs.aws.amazon.com/ . These are web pages,
not PDFs, so for Track B the agent reads the relevant service docs online (fetching
the right pages for each topic) instead of pulling a PDF from Drive. Each topic is
still treated like a chapter: one digest, one carousel.

## Current batch: tick each when you've studied it

- [ ] DDIA — Ch.1: Reliable, Scalable, and Maintainable Applications (`docs/digests/ddia-ch1-reliable-scalable-maintainable.html`)
- [ ] AI Engineering — Ch.1 (Part 1 of 4): The Rise of AI Engineering (`docs/digests/ai-engineering-ch1-part1-foundation-models.html`)
- [ ] High Performance MySQL — Ch.1: MySQL Architecture (`docs/digests/mysql-ch1-architecture.html`)
- [ ] AWS — Topic 1: Core Networking (VPC, subnets, route tables, NAT, IGW) (`docs/digests/aws-topic1-core-networking.html`)

<!-- Gate is CLEAR again once all four boxes above are ticked. The next run will pick up:
     DDIA Ch.2, AI Engineering Ch.1 Part 2 (pages 40-52, "Foundation Model Use Cases"),
     HP MySQL Ch.2, and AWS Topic 2 (Transit Gateway & multi-VPC connectivity). -->

## Track A: Designing Data-Intensive Applications

| Ch | Title | Pages | Digested | Carousel | Notes |
|---:|-------|-------|----------|----------|-------|
| 1 | Reliable, Scalable, and Maintainable Applications | 25–48 | 2026-07-20 | 2026-07-20 | Full chapter covered in one digest, no split needed. Carousel idea: fault vs. failure; case study Feb 28 2017 AWS S3 outage (verified against AWS's own postmortem). |
| 2 | Data Models and Query Languages | 49–90 | | | |
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
| 1 | Introduction to Building AI Applications with Foundation Models | 25-72 | Part 1/4: 2026-07-20 (pp.25-39) | 2026-07-20 (Part 1 idea: next-token prediction) | Chapter split into 4 coherent parts (47pp is too long for one thorough digest). Part 1 = "The Rise of AI Engineering" only. Next: Part 2 "Foundation Model Use Cases", pp.40-52. Then Part 3 "Planning AI Applications" pp.52-59, Part 4 "The AI Engineering Stack" + Summary pp.59-72. |
| 2 | Understanding Foundation Models | 73-136 | | | |
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
| 1 | MySQL Architecture | 23-40 | 2026-07-20 | 2026-07-20 | Full chapter covered in one digest. Carousel idea: pluggable storage engines; case study Facebook's MyRocks (announced Aug 31 2016, verified against engineering.fb.com). Render note: run `render_carousels.py` with cwd inside `.claude/skills/book-digest-carousels/` or the relative font paths in `fonts.json` silently fail to resolve and text overflows. |
| 2 | Monitoring in a Reliability Engineering World | 41-62 | | | |
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
| 1 | Core networking (VPC, subnets, route tables, NAT, IGW) | docs.aws.amazon.com | 2026-07-20 | 2026-07-20 | Sourced from 8 fetched VPC User Guide pages (what-is-amazon-vpc, configure-subnets, VPC_Route_Tables, RouteTables, VPC_Internet_Gateway, vpc-nat-gateway, default-vpc, vpc-cidr-blocks). Carousel idea: one route-table row decides public vs private; case study Feb 28 2017 AWS S3 outage. |
| 2 | Transit Gateway & multi-VPC connectivity | docs.aws.amazon.com | | | |
| 3 | EC2 (instances, AMIs, ASGs, load balancing) | docs.aws.amazon.com | | | |
| 4 | S3 (storage classes, lifecycle, security) | docs.aws.amazon.com | | | |
| 5 | Lambda (event model, cold starts, limits) | docs.aws.amazon.com | | | |
| 6 | Queueing/messaging (SQS, SNS, EventBridge) | docs.aws.amazon.com | | | |
| 7 | CloudWatch (metrics, logs, alarms, dashboards) | docs.aws.amazon.com | | | |
