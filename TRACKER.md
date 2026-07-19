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

- [ ] DDIA — Ch.1: Reliable, Scalable, and Maintainable Applications (full chapter)
- [ ] AI Engineering — Ch.1, Part 1 of 2: The Rise of AI Engineering + Foundation Model Use Cases (pp.25-51)
- [ ] High Performance MySQL — Ch.1: MySQL Architecture (full chapter)
- [ ] AWS — Topic 1: Core networking (VPC, subnets, route tables, IGW, NAT gateway)

<!-- Gate: next run is blocked until every box above is checked. Once cleared, the next
     run finishes AI Engineering Ch.1 Part 2 (pp.52-72, cached below) and starts DDIA Ch.2,
     High Performance MySQL Ch.2, and AWS Topic 2. -->

## Track A: Designing Data-Intensive Applications

| Ch | Title | Pages | Digested | Carousel | Notes |
|---:|-------|-------|----------|----------|-------|
| 1 | Reliable, Scalable, and Maintainable Applications | 25–48 | 2026-07-19 | 2026-07-19 | Fault vs failure, load parameters/percentiles (Twitter fan-out), operability/simplicity/evolvability. Case study: AWS S3 Feb 2017 outage. Digest: `ddia-ch1-reliable-scalable-maintainable` |
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
| 1 | Introduction to Building AI Applications with Foundation Models | 25-72 | in progress (Part 1: 2026-07-19) | 2026-07-19 (Part 1) | Split 2 parts (dense chapter, depth over speed). Part 1 done: pp.25-51, "The Rise of AI Engineering" + "Foundation Model Use Cases". **Next: Part 2, pp.52-72** — "Planning AI Applications" + "The AI Engineering Stack". Case study: Getty Images v. Stability AI. Digest: `ai-engineering-ch1-part1-introduction-foundation-models` |
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
| 1 | MySQL Architecture | 23-40 | 2026-07-19 | 2026-07-19 | Source/replica single-writer model, storage engine layer, transactions/ACID/MVCC. Case study: GitHub Oct 21-22 2018 incident. Digest: `high-performance-mysql-ch1-architecture` |
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
| 1 | Core networking (VPC, subnets, route tables, NAT, IGW) | docs.aws.amazon.com | 2026-07-19 | 2026-07-19 | Grounded in 11 fetched AWS doc pages (VPC, subnets, route tables, IGW, NAT gateway). NAT throughput/connection numbers flagged as time-sensitive. Case study: Dec 7 2021 AWS US-EAST-1 event. Digest: `aws-01-core-networking` |
| 2 | Transit Gateway & multi-VPC connectivity | docs.aws.amazon.com | | | |
| 3 | EC2 (instances, AMIs, ASGs, load balancing) | docs.aws.amazon.com | | | |
| 4 | S3 (storage classes, lifecycle, security) | docs.aws.amazon.com | | | |
| 5 | Lambda (event model, cold starts, limits) | docs.aws.amazon.com | | | |
| 6 | Queueing/messaging (SQS, SNS, EventBridge) | docs.aws.amazon.com | | | |
| 7 | CloudWatch (metrics, logs, alarms, dashboards) | docs.aws.amazon.com | | | |
