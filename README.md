# Mnemosyne

**Mnemosyne** is a platform for managing the lifecycle of fine-tuned LLM models and the datasets that produce them.

The system is designed to make fine-tuning repeatable, inspectable, and reusable across teams and organizations. Rather than treating model training as an ad-hoc task, Mnemosyne provides a structured environment for curating datasets, launching fine-tuning jobs, evaluating results, and maintaining a persistent repository of model artifacts.

The goal is to transform model specialization from a manual workflow into a governed asset pipeline.

---

# Purpose

Organizations often discover recurring tasks that can benefit from fine-tuned language models. Examples include:

* generating structured documents
* normalizing legal or compliance text
* drafting engineering artifacts
* enforcing formatting or tone conventions
* automating repetitive editorial workflows

However, the fine-tuning process itself often becomes a barrier:

* datasets are difficult to curate and manage
* experiments are not reproducible
* model lineage becomes unclear
* successful models are difficult to reuse
* training workflows are scattered across scripts and notebooks

Mnemosyne solves this by acting as a **control plane for fine-tuning workflows**, enabling teams to manage datasets, experiments, and resulting models in a structured environment.

---

# Core Design Philosophy

Mnemosyne is built around several key principles.

### Workflow-Driven Specialization

Fine-tuning should be tied to real operational workflows, not arbitrary experimentation.

Every dataset and model should trace back to a clearly defined workflow.

Examples:

* Jira epic drafting
* legal copy normalization
* marketing content generation
* structured engineering documentation

---

### Artifact-Based Architecture

Large training datasets are **never stored directly in the relational database**.

Instead:

* the database stores metadata
* dataset artifacts are stored as files
* training jobs consume dataset artifacts
* resulting models are recorded as artifacts

This keeps the database lightweight and improves scalability.

---

### Immutable Dataset Revisions

Datasets are versioned.

Each dataset revision is treated as an immutable artifact that contains:

* normalized training examples
* validation metadata
* integrity checksums
* provenance information

Once created, dataset revisions are never modified.

---

### Explicit Model Lineage

Every model artifact must trace back to:

* a dataset revision
* a training configuration
* a fine-tuning job

This ensures reproducibility and accountability.

---

### Enterprise-Friendly Deployment

Mnemosyne is designed to be self-hostable and easy to deploy.

The stack avoids unnecessary infrastructure complexity while remaining capable of scaling to enterprise workloads.

---

# High-Level Architecture

Mnemosyne consists of several major layers.

```
Frontend
   |
Web API (Django REST Framework)
   |
Application Services
   |
Persistence + Artifact Storage
   |
External Providers (OpenAI)
```

---

# Technology Stack

## Backend

* Python 3.12
* Django
* Django REST Framework
* Celery
* RabbitMQ
* Redis
* MySQL 8.4

The backend is responsible for:

* dataset management
* training orchestration
* model artifact registry
* workflow governance
* provider integrations
* job orchestration

---

## Frontend

* Vue 3
* TypeScript
* Vite

The frontend provides a web interface for interacting with workflows, datasets, training jobs, and model artifacts.

---

## Infrastructure

* OpenResty (edge reverse proxy)
* Supervisor or systemd for process management
* Local filesystem storage for dataset artifacts

OpenResty is used primarily as a reverse proxy and TLS termination layer. Lua integration may be used later to support gateway functionality if needed.

---

# Data Architecture

Mnemosyne separates **metadata storage** from **artifact storage**.

## Metadata (Relational Database)

Stored in MySQL:

* workflows
* datasets
* dataset revisions
* training jobs
* evaluation results
* model artifacts
* promotions
* user accounts
* team permissions
* audit records

---

## Artifact Storage (Filesystem)

Large artifacts are stored outside the database.

Examples:

* dataset files
* normalized training corpora
* evaluation exports
* training logs
* job outputs

Artifacts are referenced by URI and checksum in the database.

Example storage path:

```
/var/mnemosyne/datasets/<dataset>/<revision>.jsonl
```

---

# Core Domain Objects

## Workflow

Represents a real-world task that may benefit from model specialization.

Examples:

* engineering artifact generation
* legal text normalization
* marketing copy production

Workflows provide the context that datasets and models belong to.

---

## Dataset

A logical grouping of training examples tied to a workflow.

Datasets evolve through **dataset revisions**.

---

## Dataset Revision

An immutable version of a dataset.

Contains:

* normalized training examples
* dataset metadata
* record counts
* checksums
* artifact references

Dataset revisions are stored as artifact files.

---

## Training Job

Represents a fine-tuning execution.

Tracks:

* provider job IDs
* status
* logs
* dataset revision used
* resulting checkpoints
* final model artifact

Training jobs run asynchronously through Celery workers.

---

## Model Artifact

A reusable model produced by a training job.

Each artifact includes:

* provider model identifier
* training job lineage
* dataset revision lineage
* evaluation results
* promotion status

Model artifacts are stored in the **model registry**.

---

## Evaluation Run

Represents a test suite executed against a candidate model.

Evaluation runs allow models to be compared against:

* baseline models
* previous model versions
* workflow expectations

---

# Training Workflow

A typical training workflow in Mnemosyne follows these steps.

1. Create a workflow.
2. Import or construct training examples.
3. Generate a dataset revision.
4. Validate dataset structure.
5. Launch a training job.
6. Monitor training progress.
7. Run evaluation tests.
8. Promote the model artifact.

---

# Job Orchestration

Background tasks are executed through Celery.

Typical jobs include:

* dataset validation
* dataset normalization
* training job orchestration
* evaluation runs
* artifact processing

RabbitMQ serves as the message broker.

Redis provides caching and ephemeral coordination.

---

# Storage Layout

Example filesystem layout:

```
/var/mnemosyne
    /datasets
    /artifacts
    /evaluations
    /logs
```

Each dataset revision and artifact is referenced in the database with:

* URI
* checksum
* metadata

---

# Provider Integrations

The first provider integration is OpenAI.

Responsibilities include:

* dataset upload
* training job creation
* status polling
* checkpoint tracking
* model artifact registration

Provider logic is implemented as an internal integration layer within the backend.

---

# Security Model

Mnemosyne supports enterprise-grade access control.

Entities may be scoped to:

* organizations
* teams
* individual users

Permissions govern:

* dataset visibility
* training job execution
* model promotion
* workflow ownership

---

# Deployment Model

Mnemosyne is designed for flexible deployment.

Typical deployment includes:

* OpenResty
* Django application server
* Celery worker pool
* RabbitMQ
* Redis
* MySQL
* artifact storage volume

No cloud dependencies are required.

---

# Future Roadmap

Potential future capabilities include:

* object storage backends
* dataset ingestion pipelines
* automated dataset generation
* model regression testing
* workflow automation
* multi-provider training support
* experiment tracking dashboards

---

# License

TBD
