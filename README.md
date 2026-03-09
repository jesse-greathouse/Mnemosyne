# Mnemosyne

**Mnemosyne** is a platform for managing the lifecycle of fine-tuned LLM models and the datasets that produce them.

The system is designed to make fine-tuning repeatable, inspectable, and reusable across teams and organizations. Rather than treating model training as an ad-hoc task, Mnemosyne provides a structured environment for curating datasets, launching fine-tuning jobs, evaluating results, and maintaining a persistent repository of model artifacts.

The goal is to transform model specialization from a manual workflow into a governed asset pipeline.

---

# Purpose

Organizations often discover recurring tasks that can benefit from fine-tuned language models. Examples include:

- generating structured documents
- normalizing legal or compliance text
- drafting engineering artifacts
- enforcing formatting or tone conventions
- automating repetitive editorial workflows

However, the fine-tuning process itself often becomes a barrier:

- datasets are difficult to curate and manage
- experiments are not reproducible
- model lineage becomes unclear
- successful models are difficult to reuse
- training workflows are scattered across scripts and notebooks

Mnemosyne solves this by acting as a **control plane for fine-tuning workflows**, enabling teams to manage datasets, experiments, and resulting models in a structured environment.

---

# Core Design Philosophy

Mnemosyne is built around several key principles.

### Workflow-Driven Specialization

Fine-tuning should be tied to real operational workflows, not arbitrary experimentation.

Every dataset and model should trace back to a clearly defined workflow.

Examples:

- Jira epic drafting
- legal copy normalization
- marketing content generation
- structured engineering documentation

---

### Artifact-Based Architecture

Large training datasets are **never stored directly in the relational database**.

Instead:

- the database stores metadata
- dataset artifacts are stored as files
- training jobs consume dataset artifacts
- resulting models are recorded as artifacts

This keeps the database lightweight and improves scalability.

---

### Immutable Dataset Revisions

Datasets are versioned.

Each dataset revision is treated as an immutable artifact that contains:

- normalized training examples
- validation metadata
- integrity checksums
- provenance information

Once created, dataset revisions are never modified.

---

### Explicit Model Lineage

Every model artifact must trace back to:

- a dataset revision
- a training configuration
- a fine-tuning job

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

- Python 3.12
- Django
- Django REST Framework
- Celery
- RabbitMQ
- Redis
- MySQL 8.4

The backend is responsible for:

- dataset management
- training orchestration
- model artifact registry
- workflow governance
- provider integrations
- job orchestration

---

## Frontend

- Vue 3
- TypeScript
- Vite

The frontend provides a web interface for interacting with workflows, datasets, training jobs, and model artifacts.

---

## Infrastructure

- OpenResty (edge reverse proxy)
- Supervisor or systemd for process management
- Local filesystem storage for dataset artifacts

OpenResty is used primarily as a reverse proxy and TLS termination layer.

---

# Data Architecture

Mnemosyne separates **metadata storage** from **artifact storage**.

## Metadata (Relational Database)

Stored in MySQL:

- workflows
- datasets
- dataset revisions
- training jobs
- evaluation results
- model artifacts
- promotions
- user accounts
- team permissions
- audit records

---

## Artifact Storage (Filesystem)

Large artifacts are stored outside the database.

Examples:

- dataset files
- normalized training corpora
- evaluation exports
- training logs
- job outputs

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

- engineering artifact generation
- legal text normalization
- marketing copy production

---

## Dataset

A logical grouping of training examples tied to a workflow.

Datasets evolve through **dataset revisions**.

---

## Dataset Revision

An immutable version of a dataset.

Contains:

- normalized training examples
- dataset metadata
- record counts
- checksums
- artifact references

---

## Training Job

Represents a fine-tuning execution.

Tracks:

- provider job IDs
- status
- logs
- dataset revision used
- resulting checkpoints
- final model artifact

Training jobs run asynchronously through Celery workers.

---

## Model Artifact

A reusable model produced by a training job.

Each artifact includes:

- provider model identifier
- training job lineage
- dataset revision lineage
- evaluation results
- promotion status

---

## Evaluation Run

Represents a test suite executed against a candidate model.

---

# Installation

## System Requirements

Recommended minimum environment:

- Linux (Ubuntu or Debian recommended)
- 4 CPU cores
- 8 GB RAM
- MySQL 8+
- RabbitMQ
- Redis

External services are **not automatically provisioned**. Mnemosyne connects to existing infrastructure.

---

## Clone the Repository

```
git clone https://github.com/jesse-greathouse/Mnemosyne.git
cd Mnemosyne
```

---

## Install Dependencies

Run the installer:

```
bin/install
```

This installs:

- system packages
- Python runtime
- virtual environment
- Python dependencies
- Node.js
- frontend build dependencies
- OpenResty

---

## Build the Frontend

If needed manually:

```
bin/install --build
```

---

# Configuration

After installation, configure the application.

```
bin/configure
```

This interactive setup will:

- generate a Django secret key
- configure database connection
- configure RabbitMQ connection
- configure Redis connection
- configure web server settings
- create `.env` configuration
- generate runtime configuration files

---

## Configuration Files

Primary configuration files:

```
.mnemosyne-cfg.yml   # Application configuration
src/.env             # Runtime environment variables
etc/nginx/           # Web server configuration
etc/supervisor/      # Process management
```

---

## External Services

The following services must be available:

### MySQL

Example configuration:

```
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=mnemosyne
DATABASE_USER=mnemosyne
DATABASE_PASSWORD=secret
```

---

### RabbitMQ

RabbitMQ is used as the Celery message broker.

Example:

```
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=mnemosyne
RABBITMQ_PASSWORD=secret
RABBITMQ_VHOST=mnemosyne
```

---

### Redis

Redis is used for caching and coordination.

Example:

```
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

---

# Database Setup

Apply migrations:

```
bin/migrate
```

---

# Create Admin User

Create the Django admin account:

```
bin/adminuser
```

---

# Seed Initial Data

Optional initialization:

```
bin/seed
```

This creates default groups and permissions.

---

# Running the Application

Mnemosyne runs two primary process groups.

### Web Services

```
bin/web start
```

This launches:

- OpenResty
- Gunicorn
- Supervisor processes

Stop:

```
bin/web stop
```

Restart:

```
bin/web restart
```

---

### Background Workers

Celery workers handle asynchronous jobs.

Start workers:

```
bin/queue start
```

Stop workers:

```
bin/queue stop
```

Restart workers:

```
bin/queue restart
```

---

# Application Access

Default URL:

```
http://localhost:8282
```

API endpoint example:

```
http://localhost:8282/api/ping
```

---

# Storage Layout

Example filesystem layout:

```
Mnemosyne/
    bin/
    etc/
    opt/
    src/
    var/
        cache/
        log/
        static/
        www/
```

Artifacts are typically stored under:

```
/var/mnemosyne/
```

---

# Training Workflow

Typical model lifecycle:

1. Create a workflow
2. Import training data
3. Generate dataset revision
4. Validate dataset
5. Launch training job
6. Monitor training progress
7. Run evaluation tests
8. Promote model artifact

---

# Job Orchestration

Background tasks include:

- dataset validation
- dataset normalization
- training orchestration
- evaluation runs
- artifact processing

Celery workers process jobs from RabbitMQ.

---

# Security Model

Access control supports:

- users
- teams
- organizations

Permissions govern:

- dataset visibility
- training job execution
- model promotion
- workflow ownership

---

# Deployment Model

Typical deployment:

```
OpenResty
Gunicorn
Celery Workers
RabbitMQ
Redis
MySQL
Filesystem Storage
```

The platform is fully **self-hostable**.

---

# Future Roadmap

Potential future capabilities include:

- object storage backends
- dataset ingestion pipelines
- automated dataset generation
- model regression testing
- workflow automation
- multi-provider training support
- experiment tracking dashboards

---

# License

See the `LICENSE` file included with this project.
