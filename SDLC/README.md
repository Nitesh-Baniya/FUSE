# Week 2 Task: Software Development Concepts

This fellowship week is essentially teaching you a very common modern backend stack workflow:
- Containerization with Docker
- Database setup with PostgreSQL
- Backend API development using FastAPI
- ORM usage with SQLAlchemy
- Validation using Pydantic
- Async programming with asyncio
- Modular backend architecture

***

<div style="background-color: #1d3c54;
color: #f4f4f4; border:1px solid #e22a45; border-radius:12px; padding:20px;">

<h1 >Task Description Given by TA</h1>

<p>You are provided with the following files:</p>

<ul>
  <li><code>Task1_Week2.pdf</code></li>
  <li><code>Task2_Week2.pdf</code></li>
  <li><code>Task3_Week2.pdf</code></li>
  <li><code>seed.sql</code> (PostgreSQL-compatible SQL script)</li>
</ul>

<p>The <code>seed.sql</code> file contains scripts to:</p>

<ul>
  <li>Create the database</li>
  <li>Create tables</li>
  <li>Insert data into those tables</li>
</ul>

<hr>

<h2>Important Guidelines</h2>

<p>Tasks must be completed sequentially:</p>

<ul>
  <li>✅ Complete Task 1 before starting Task 2</li>
  <li>✅ Complete Task 2 before starting Task 3</li>
  <li>❌ You cannot skip ahead or work on tasks out of order</li>
</ul>

<p>Carefully review each task document for detailed instructions.</p>

<hr>

<h2>Task Breakdown</h2>

<h3>🔹 Task 1: PostgreSQL Setup with Docker</h3>

<p>Set up a PostgreSQL database using Docker Compose.</p>

<p>Use the provided <code>seed.sql</code> file to:</p>

<ul>
  <li>Initialize the database</li>
  <li>Create required tables</li>
  <li>Populate tables with data</li>
</ul>

<hr>

<h3>🔹 Task 2: Build API Endpoint (Customers Table)</h3>

<p>Develop an API using FastAPI.</p>

<p>Focus on the <code>customers</code> table.</p>

<h4>Requirements:</h4>

<ul>
  <li>Create endpoint(s) to fetch data from the table</li>
  <li>Use ORM (Object Relational Mapping) for database interaction</li>
  <li>Use Pydantic for:
    <ul>
      <li>Data validation</li>
      <li>Request/response schemas</li>
    </ul>
  </li>
  <li>Handle user input via FastAPI</li>
</ul>

<hr>

<h3>🔹 Task 3: Modularity & Concurrency</h3>

<p>Design separate API endpoints for each table to:</p>

<ul>
  <li>Fetch the count of records in each table</li>
</ul>

<p>Implement concurrency using <code>asyncio</code> to:</p>

<ul>
  <li>Gather counts from all tables efficiently</li>
  <li>Return aggregated statistics</li>
</ul>

<hr>

<h2>Final Note</h2>

<p>
Make sure to carefully read each task document for detailed instructions and requirements before starting.
</p>

<hr>

<h2>Best of Luck!</h2>

<p>
We hope you enjoy working through these tasks and gain valuable hands-on experience.
</p>

</div>

***