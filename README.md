# AuditFlow

AuditFlow is a text and voice chat application for auditors to extract insights from financial documents like trial balances and general ledgers. Built with an MCP Server using Supabase (PostgreSQL) and SQLAlchemy ORM, it uses Weaviate Vector Store for hybrid search combining BM25, metadata, and semantic search for data retrieval, integrated with n8n.

## Features

- **Text & Voice Chat Interface**: Interact with your financial documents through natural language queries using text or voice input
- **Financial Document Analysis**: Specialized support for trial balances and general ledger documents
- **Hybrid Search**: Combines BM25, metadata filtering, and semantic search for accurate data retrieval
- **MCP Server Architecture**: Built on Model Context Protocol for extensible AI integrations
- **Workflow Automation**: Seamless integration with n8n for automated audit workflows

## Tech Stack

- **Database**: Supabase (PostgreSQL)
- **ORM**: SQLAlchemy
- **Vector Store**: Weaviate
- **MCP Server**: Integrated with n8n
- **Workflow Automation**: n8n
- **Search**: Hybrid search (BM25 + Semantic + Metadata)

## Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) (Python package installer)
- Supabase account and project
- Weaviate instance (cloud or self-hosted)
- n8n instance (optional, for workflow automation)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/UmarEhtisham/AuditFlow-Chat.git
cd auditflow
```

2. Install dependencies using uv:

```bash
uv sync
```

Or install the package in development mode:

```bash
uv pip install -e .
```

3. Set up environment variables:

```bash
cp .env.example .env
```

Edit `.env` with your Supabase credentials:

```
SUPABASE_URL=your_supabase_direct_url
```

**Note**: Other credentials (Weaviate, n8n webhooks) are configured within n8n workflows.

4. Run the application:

```bash
python main.py
```

The database will be automatically initialized on first run.

## Usage

AuditFlow is accessed through WhatsApp integration powered by n8n workflows. All interactions (text queries, voice messages, and document uploads) are handled via WhatsApp.

### Text Queries

Send text messages to the configured WhatsApp number with your audit queries:

```
"Show me all transactions above $10,000 in the general ledger"
"Summarize the trial balance for Q4 2024"
"Find all entries related to account 1200"
```

### Voice Queries

Send voice messages to the WhatsApp number with your questions. The system will transcribe and process your audio queries automatically.

### Document Upload

Send financial documents (Excel, PDF) directly through WhatsApp:

1. Attach your trial balance or general ledger file
2. Add a caption specifying the document type (optional)
3. The system will process and index the document for querying

## Architecture

AuditFlow uses a multi-layered architecture:

1. **Data Layer**: Supabase PostgreSQL stores structured financial data
2. **Vector Layer**: Weaviate indexes document embeddings for semantic search
3. **Search Layer**: Hybrid search combining keyword (BM25), metadata, and semantic search
4. **MCP Server**: Handles AI model interactions and context management
5. **Integration Layer**: n8n workflows for automated processes

## Search Capabilities

AuditFlow's hybrid search combines three approaches:

- **BM25 Search**: Traditional keyword-based search for exact matches
- **Semantic Search**: Vector embeddings for conceptual similarity
- **Metadata Filtering**: Filter by date ranges, amounts, account types, etc.

## License

MIT License

Copyright (c) 2025 AuditFlow

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Support

For questions or support, please open an issue on GitHub or contact the maintainers.

## Roadmap

- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Real-time collaboration features
- [ ] Mobile application
- [ ] Integration with major accounting software
- [ ] Custom report generation

## Acknowledgments

- Built with [Supabase](https://supabase.com/)
- Powered by [Weaviate](https://weaviate.io/)
- Automated with [n8n](https://n8n.io/)
- Uses [SQLAlchemy](https://www.sqlalchemy.org/)

---

Made with ❤️ for auditors everywhere