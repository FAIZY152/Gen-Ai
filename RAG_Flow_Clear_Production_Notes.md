# RAG Flow --- Clear Production Notes

## 1. Big Picture

RAG (Retrieval-Augmented Generation) can start as a simple **retrieve →
generate** pipeline and become more advanced as the user's query becomes
harder to understand or the knowledge base becomes larger.

The flow in the diagram can be understood as:

``` text
User Prompt
    ↓
Query Translation / Understanding
    ↓
Query Rewriting or Expansion
    ↓
Retrieval Strategy
    ↓
Filter / Rank / Deduplicate
    ↓
LLM Generation
    ↓
Final Answer
```

The important idea is:

> **Better RAG is not only about a better LLM. It is also about sending
> better queries to the retrieval system and selecting better evidence
> before generation.**

------------------------------------------------------------------------

# 2. Basic RAG

Basic RAG has three main stages:

``` text
Documents
   ↓
Indexing
   ↓
Vector Database

User Query
   ↓
Retrieval
   ↓
Relevant Chunks
   ↓
LLM
   ↓
Answer
```

## 2.1 Indexing

### What happens?

Before users ask questions, documents are prepared and stored for
retrieval.

Typical process:

``` text
Documents
   ↓
Load
   ↓
Clean
   ↓
Chunk
   ↓
Embedding Model
   ↓
Vector Database
```

Each chunk is converted into an embedding vector and stored with
metadata.

### Production example

A company has:

-   HR policies
-   Employee handbook
-   Leave policy
-   Benefits documentation

These documents are chunked and indexed in a vector database.

### Why it matters

Good chunking and metadata directly affect retrieval quality.

Useful metadata can include:

-   document_id
-   department
-   tenant_id
-   document_type
-   created_at
-   permissions

------------------------------------------------------------------------

# 3. Retrieval

When the user asks a question, the system converts the question into an
embedding and searches the vector database.

``` text
User Query
   ↓
Query Embedding
   ↓
Vector Search
   ↓
Top-K Chunks
```

### Example

User:

> "How many annual leaves can I take?"

The retriever searches the indexed HR documents and returns the most
relevant chunks.

### Production use case

Use basic retrieval when:

-   questions are simple
-   the knowledge base is small or well structured
-   users normally use clear terminology
-   one retrieval query is enough

------------------------------------------------------------------------

# 4. Generation

The retrieved documents are passed to the LLM together with the user's
question.

``` text
User Question
      +
Retrieved Context
      ↓
     LLM
      ↓
Final Answer
```

The LLM should answer using the retrieved context instead of relying
only on its internal knowledge.

### Production example

``` text
Question:
"What is the refund period?"

Retrieved:
"Customers can request a refund within 30 days."

LLM:
"Customers can request a refund within 30 days."
```

------------------------------------------------------------------------

# 5. Why Basic RAG Is Sometimes Not Enough

Basic RAG can fail when the user's question is:

-   ambiguous
-   too short
-   badly written
-   using different terminology from the documents
-   asking multiple things
-   requiring information from multiple sources

Example:

> "What about the refund?"

This query does not provide enough context.

The system may need to understand or rewrite the query before retrieval.

That leads to **Advanced RAG**.

------------------------------------------------------------------------

# 6. Advanced RAG

Advanced RAG adds intelligence before and after retrieval.

The main components shown in the diagram are:

1.  Query Transformation
2.  Routing
3.  Query Construction
4.  Indexing
5.  Retrieval
6.  Generation

A simplified production flow is:

``` text
User Prompt
     ↓
Query Transformation
     ↓
Routing
     ↓
Query Construction
     ↓
Retrieval
     ↓
Filtering / Ranking
     ↓
Generation
```

Not every application needs every component.

------------------------------------------------------------------------

# 7. Query Translation / Query Understanding

The first advanced step is understanding what the user actually means.

``` text
User Prompt
     ↓
Query Understanding
     ↓
Better Search Query
```

The goal is to reduce ambiguity and convert the user's language into
something useful for retrieval.

## Example

User:

> "What is the leave thing for new employees?"

The system can translate it into:

> "What is the annual leave policy for newly hired employees?"

Now the retrieval query is much clearer.

## Production use cases

Useful for:

-   customer support
-   HR assistants
-   legal document search
-   medical knowledge systems
-   enterprise knowledge bases

------------------------------------------------------------------------

# 8. Query Rewriting

Query rewriting changes the original question into a better retrieval
query.

``` text
Original Query
      ↓
LLM
      ↓
Rewritten Query
      ↓
Retriever
```

### Example

Original:

> "Can I get money back after buying it?"

Rewritten:

> "What is the product refund policy and eligibility period?"

The rewritten query is more aligned with the language likely to exist in
the documents.

------------------------------------------------------------------------

# 9. Query Transformation

Query transformation is the broader concept of changing the original
query to improve retrieval.

Common techniques include:

-   Query rewriting
-   Query expansion
-   Query decomposition
-   Multi-query generation
-   HyDE
-   Query translation

The purpose is the same:

> **Create a query that retrieves better evidence than the raw user
> prompt.**

------------------------------------------------------------------------

# 10. Query Expansion

Sometimes one query does not cover all possible terminology.

Example:

``` text
Original:
"How do I reset my password?"
```

Possible expanded queries:

``` text
"How do I reset my password?"
"Forgot password recovery process"
"Account password reset procedure"
```

These queries can retrieve different relevant documents.

------------------------------------------------------------------------

# 11. Multi-Query RAG

Multi-query RAG generates multiple versions of the user's question.

``` text
                 ┌─ Query 1 ─→ Retrieval
User Question ───┼─ Query 2 ─→ Retrieval
                 └─ Query 3 ─→ Retrieval
```

This is the **fan-out** idea shown in the diagram.

### Why?

Different queries can retrieve different relevant chunks.

### Example

User:

> "How does our employee insurance work?"

Possible queries:

``` text
1. Employee health insurance policy
2. Employee insurance coverage
3. Health benefits eligibility
```

The results are combined before generation.

### Production use case

Useful when:

-   terminology varies
-   documents use different wording
-   recall is more important than retrieval speed
-   enterprise knowledge bases are large

------------------------------------------------------------------------

# 12. Parallel Query / Fan-Out Retrieval

This is the next step shown in the diagram.

Instead of executing queries one after another, multiple queries are
sent to retrieval systems in parallel.

``` text
                  ┌→ Retriever 1 → Docs
User Query → LLM ─┼→ Retriever 2 → Docs
                  └→ Retriever 3 → Docs
                              ↓
                       Merge Results
                              ↓
                         Deduplicate
```

## Why parallel?

It reduces latency compared with running every retrieval operation
sequentially.

## Production example

For a product support assistant:

``` text
Query 1 → Product documentation
Query 2 → Troubleshooting documentation
Query 3 → FAQ knowledge base
```

The system retrieves from all three paths and combines the results.

------------------------------------------------------------------------

# 13. Filtering / Unique Results

The diagram shows:

``` text
[filter_unique]
```

This means removing duplicate documents or chunks after multiple
retrieval operations.

Example:

``` text
Query 1 → Doc A, Doc B, Doc C
Query 2 → Doc B, Doc C, Doc D
Query 3 → Doc A, Doc D, Doc E
```

After deduplication:

``` text
Doc A
Doc B
Doc C
Doc D
Doc E
```

### Why?

Without deduplication, the same chunk may consume multiple positions in
the final context.

This can:

-   waste context window
-   increase token cost
-   reduce evidence diversity

------------------------------------------------------------------------

# 14. Reciprocal Rank Fusion (RRF)

The second major retrieval strategy shown in the diagram is **Reciprocal
Rank Fusion**.

RRF combines multiple ranked result lists into one ranking.

``` text
Query 1 → Ranked Results ─┐
Query 2 → Ranked Results ─┼→ RRF → Final Ranking
Query 3 → Ranked Results ─┘
```

Instead of simply joining results, RRF gives higher importance to
documents that appear near the top across multiple result lists.

A common scoring idea is:

``` text
RRF Score(d) = Σ 1 / (k + rank(d))
```

Where:

-   `d` = document
-   `rank(d)` = document's position in a result list
-   `k` = constant used to smooth the ranking

You do not normally need to manually implement this formula if your
retrieval framework already provides RRF.

------------------------------------------------------------------------

# 15. Why RRF Is Useful

Imagine:

``` text
Query 1:
A
B
C
D

Query 2:
C
A
E
F

Query 3:
A
C
B
G
```

Document `A` appears near the top multiple times.

Document `C` also appears consistently.

RRF can therefore rank:

``` text
A
C
B
...
```

The key idea:

> **Documents supported by multiple retrieval perspectives become
> stronger candidates.**

------------------------------------------------------------------------

# 16. Multi-Query + RRF

These two techniques work especially well together.

``` text
                 ┌→ Query 1 → Retrieval ─┐
User Question →  ├→ Query 2 → Retrieval ─┼→ RRF → Top Results
                 └→ Query 3 → Retrieval ─┘
```

### Production use case

Suppose an enterprise user asks:

> "What are the security requirements for deploying our application?"

The system can create:

``` text
1. Application security requirements
2. Production deployment security policy
3. Infrastructure security controls
```

Each query retrieves its own ranked results.

RRF combines those rankings.

The final top documents are passed to the LLM.

------------------------------------------------------------------------

# 17. Query Routing

Routing decides **where the query should go**.

``` text
                 ┌→ Vector Search
User Query → Router ├→ SQL
                 ├→ Knowledge Graph
                 └→ API / Search Engine
```

### Example

User asks:

> "Show me all invoices from January."

This is structured data.

A router can send it to SQL instead of vector search.

Another question:

> "Explain our refund policy."

This can go to document retrieval.

### Production use case

Very useful in enterprise systems where information exists in different
sources:

-   PostgreSQL
-   Elasticsearch / OpenSearch
-   Vector database
-   APIs
-   Knowledge graph
-   File storage

------------------------------------------------------------------------

# 18. Query Construction

Query construction converts natural language into a query format
understood by a specific data source.

Examples:

``` text
Natural Language
      ↓
Query Constructor
      ↓
SQL / Metadata Filter / Search Query / API Query
```

### Example

User:

> "Find all support documents for the billing team from 2026."

The system could construct:

``` text
department = "billing"
year = 2026
```

and combine those filters with semantic search.

### Production use case

Useful when retrieval needs:

-   metadata filters
-   SQL queries
-   search-engine syntax
-   structured APIs
-   tenant-specific filtering

------------------------------------------------------------------------

# 19. Indexing Is Still Important in Advanced RAG

Advanced retrieval does not remove the need for good indexing.

A production index may contain:

``` text
Document
 ├── Chunk
 ├── Embedding
 ├── Metadata
 ├── Tenant ID
 ├── Permissions
 └── Source information
```

Possible indexes:

-   Vector index
-   Keyword index
-   Metadata index
-   Search-engine index

A strong production system can combine these approaches.

------------------------------------------------------------------------

# 20. Hybrid Retrieval

A production RAG system often combines:

``` text
Semantic Search
      +
Keyword Search
      ↓
Combined Results
```

Semantic search understands meaning.

Keyword search is strong for exact terms such as:

-   product IDs
-   error codes
-   policy names
-   ticket numbers
-   technical terms

### Example

User:

> "What does error ERR-402 mean?"

Keyword search can be very important because `ERR-402` is an exact
identifier.

------------------------------------------------------------------------

# 21. End-to-End Advanced RAG Example

Consider an enterprise customer-support assistant.

### Step 1 --- User

``` text
"Why can't I process the payment?"
```

### Step 2 --- Query understanding

The system identifies:

``` text
Payment failure / payment processing issue
```

### Step 3 --- Query transformation

Generate:

``` text
Payment processing failure
Payment transaction declined
Payment troubleshooting
```

### Step 4 --- Parallel retrieval

``` text
Query 1 → Vector Search
Query 2 → Keyword Search
Query 3 → Vector Search
```

### Step 5 --- Combine results

``` text
All retrieved documents
        ↓
Deduplicate
        ↓
RRF / Ranking
```

### Step 6 --- Filter

Apply:

``` text
tenant_id
product
user permissions
document type
```

### Step 7 --- Generation

Pass the best evidence to the LLM.

### Step 8 --- Final answer

The assistant gives a grounded response with citations or source
references.

------------------------------------------------------------------------

# 22. Production Architecture

A practical production architecture can look like:

``` text
                    User
                      ↓
                Query Service
                      ↓
             Query Understanding
                      ↓
                 Query Router
                      ↓
             Query Transformation
                      ↓
          ┌───────────┴───────────┐
          ↓                       ↓
     Vector Search           Keyword Search
          ↓                       ↓
       Results                  Results
          └───────────┬───────────┘
                      ↓
               Deduplication
                      ↓
                Reranking / RRF
                      ↓
               Context Builder
                      ↓
                    LLM
                      ↓
              Grounded Response
```

------------------------------------------------------------------------

# 23. When to Use Which RAG Strategy

  Situation                         Recommended approach
  --------------------------------- ---------------------------------
  Simple FAQ                        Basic RAG
  Clear user queries                Basic RAG
  Ambiguous questions               Query rewriting
  Different terminology             Multi-query
  Multiple information sources      Query routing
  Structured database data          Query construction + SQL
  Multiple retrieval systems        RRF
  Duplicate results                 Deduplication
  Exact IDs / error codes           Keyword or hybrid search
  Large enterprise knowledge base   Hybrid + reranking
  Strict access control             Metadata / permission filtering

------------------------------------------------------------------------

# 24. Important Production Rule

Do not automatically use every advanced RAG technique.

More complexity does **not** automatically mean better RAG.

For example:

``` text
Basic RAG
  ↓
Measure quality
  ↓
Identify failure
  ↓
Add the technique that solves that failure
```

If basic retrieval already works well, adding multi-query, RRF, routing,
and multiple LLM calls can unnecessarily increase:

-   latency
-   token cost
-   infrastructure complexity
-   debugging difficulty

------------------------------------------------------------------------

# 25. Practical RAG Progression

A good way to build a production RAG system is:

``` text
Level 1
Basic RAG
Index → Retrieve → Generate

        ↓

Level 2
Query Rewriting
Improve the user's query

        ↓

Level 3
Multi-Query
Generate multiple retrieval perspectives

        ↓

Level 4
Parallel Retrieval
Retrieve from multiple queries/sources

        ↓

Level 5
Deduplication + Ranking
Clean and rank the combined results

        ↓

Level 6
RRF / Reranking
Improve final document ordering

        ↓

Level 7
Routing + Query Construction
Choose the correct data source

        ↓

Level 8
Hybrid Enterprise RAG
Vector + Keyword + SQL + APIs + permissions
```

------------------------------------------------------------------------

# 26. The Main Concept Behind Your Diagram

Your diagram is essentially showing **increasing retrieval
intelligence**:

``` text
Basic RAG
   ↓
Understand the query
   ↓
Rewrite the query
   ↓
Create multiple queries
   ↓
Retrieve in parallel
   ↓
Remove duplicates
   ↓
Fuse / rank results
   ↓
Generate grounded answer
```

The most important mental model is:

> **RAG quality depends heavily on Retrieval Quality.**

The LLM can only generate a reliable answer if the right evidence
reaches it.

So in production, think about RAG as:

``` text
Query Quality
      +
Retrieval Quality
      +
Context Quality
      +
Generation Quality
      =
Good RAG System
```

------------------------------------------------------------------------

# 27. Simple Interview Explanation

If you need to explain this flow in an interview:

> "Basic RAG embeds the user query and retrieves relevant chunks before
> sending them to the LLM. When basic retrieval is not enough we can
> transform the query through rewriting or multi-query generation.
> Multiple queries can run in parallel and their results can be
> deduplicated and combined using techniques like Reciprocal Rank
> Fusion. In enterprise systems we can also add routing and query
> construction to decide whether the query should go to vector search
> SQL keyword search or another data source. The final ranked and
> filtered context is then passed to the LLM for grounded generation."
