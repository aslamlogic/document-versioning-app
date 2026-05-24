# Document Versioning Workflow App
## Objective: Generate a full-stack app (React + FastAPI + Postgres) for document versioning.

---

## Functional Requirements
### Step 1: Upload
- Drag-and-drop interface for `.docx`/`.pdf` files (<50MB).
- Progress bar for upload status.
- Store uploaded files in `/uploads` (server-side).
- Validate file type and size before upload.

### Step 2: Diff View
- Side-by-side comparison of current vs. previous version.
- Highlight changes:
  - Green for additions.
  - Red for deletions.
- Support for:
  - Text-based files (e.g., `.docx`).
  - PDFs (rendered as images for comparison).
- Allow users to toggle between "Inline" and "Side-by-Side" views.

### Step 3: Structured Notes
- Rich text editor (TipTap) for annotations.
- Support for:
  - Text formatting (bold, italic, lists, etc.).
  - Embedding images/links.
- Save notes to the database, linked to the specific document version.
- Allow editing/deleting notes.

### Step 4: Sign-Off
- Role-based status pills:
  - **Draft** (Yellow): Default status for new uploads.
  - **Review** (Blue): After initial review.
  - **Approved** (Green): Final approval.
- "Publish" button:
  - Only visible to **Admin** users.
  - Changes document status to "Published" and locks it from further edits.

### Step 5: New Version
- "Create New Version" button:
  - Archives the current draft as a new version in the database.
  - Resets the workflow to Step 1 (empty upload interface).
  - Preserves all previous versions for auditing.

---

## Non-Functional Requirements
### Roles and Permissions (RBAC)
| Role      | Permissions                                                                 |
|-----------|-----------------------------------------------------------------------------|
| **Editor** | Upload, edit notes, create new versions, submit for review.               |
| **Reviewer** | View documents, add notes, approve/reject (change status to Review/Approved). |
| **Admin**   | All permissions + publish, manage users, delete documents/versions.       |

### Audit Logs
- Log **all actions** to PostgreSQL:
  - Upload, diff view, note creation/edit, status change, publish, version creation.
- Store:
  - User ID (email or username).
  - Action type (e.g., "upload", "approve").
  - Timestamp.
  - Metadata (e.g., file name, version ID).

### Accessibility
- WCAG 2.1 AA compliant:
  - Color contrast (minimum 4.5:1 for text).
  - Keyboard navigation support.
  - ARIA labels for interactive elements.

### Availability
- Dockerized deployment:
  - Containers for frontend, backend, and PostgreSQL.
  - Coolify auto-restart for 99.9% uptime.
- Health checks for all services.

### Database
- **PostgreSQL** with the following schema:

```sql
-- Documents table: Stores metadata for each document.
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    current_version_id INT REFERENCES versions(id),
    created_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(255) NOT NULL
);

-- Versions table: Tracks all versions of a document.
CREATE TABLE versions (
    id SERIAL PRIMARY KEY,
    document_id INT REFERENCES documents(id) ON DELETE CASCADE,
    file_path VARCHAR(255) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('draft', 'review', 'approved', 'published')),
    created_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(255) NOT NULL
);

-- Notes table: Stores annotations for each version.
CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    version_id INT REFERENCES versions(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_by VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Audit logs table: Tracks all user actions.
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    action VARCHAR(50) NOT NULL, -- e.g., 'upload', 'approve', 'publish'
    entity_type VARCHAR(20) NOT NULL, -- 'document', 'version', 'note'
    entity_id INT NOT NULL,
    metadata JSONB, -- Additional context (e.g., old/new status)
    created_at TIMESTAMP DEFAULT NOW()
);

-- Users table: Stores role information.
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(20) CHECK (role IN ('editor', 'reviewer', 'admin')),
    created_at TIMESTAMP DEFAULT NOW()
);
