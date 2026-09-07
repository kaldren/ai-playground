---
name: create-architecture-doc
description: Create a concise Markdown architecture document from a project description, following the organization's required Overview, Architecture, and Implementation structure. Use when a user asks for an architecture document and provides project context in a Markdown file.
---

Create the architecture document from the supplied project-description Markdown file. Preserve the facts in the source and do not invent requirements, stakeholders, technologies, or implementation decisions that it does not support.

# Create Architecture Document

Write the company name as the first content line when it is available, followed by a title that identifies the project. Then include exactly these top-level sections:

1. **Overview**: Summarize the purpose, scope, goals, and stakeholders supported by the source.
2. **Architecture**: Describe supported components and interactions and include at least one valid Mermaid diagram when enough architecture can be derived from the source.
3. **Implementation**: Give implementation guidance grounded in technologies and constraints named in the source.

# Rules

1. Return only the finished Markdown document unless the user asks for commentary.
2. Keep the document at or below 100 lines, including Mermaid source.
3. Use fenced `mermaid` blocks for every diagram.
4. If the source does not support meaningful content for a required section, write `N/A` in that section instead of guessing.
5. Prefer explicit assumptions or open questions over presenting inferred details as facts.
