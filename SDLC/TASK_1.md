<h1>Task 1: PostgreSQL Setup Using Docker</h1>

<h2>Objective</h2>

<p>
The objective of this task was to create and run a PostgreSQL database inside a Docker container and automatically initialize the database using the provided <code>seed.sql</code> file. The setup ensures that all required tables and sample data are created automatically when the container starts for the first time.
</p>

<p>This task demonstrates the use of:</p>

<ul>
  <li>Docker containerization</li>
  <li>PostgreSQL database setup</li>
  <li>Environment variable configuration using <code>.env</code></li>
  <li>Automatic database initialization using SQL scripts</li>
</ul>

<hr>

<h1>Project Structure</h1>

<p>The project was organized with the following files:</p>

<pre><code>project/
│
├── docker-compose.yml
├── .env
├── seed.sql
└── README.md
</code></pre>

<h3>File Descriptions</h3>

<table>
  <thead>
    <tr>
      <th>File</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>.env</code></td>
      <td>Stores database credentials and configuration variables</td>
    </tr>
    <tr>
      <td><code>docker-compose.yml</code></td>
      <td>Defines the PostgreSQL Docker service</td>
    </tr>
    <tr>
      <td><code>seed.sql</code></td>
      <td>Contains SQL commands to create tables and insert sample data</td>
    </tr>
  </tbody>
</table>

<hr>

<h1>Step 1: Setting Up Environment Variables</h1>

<p>
A <code>.env</code> file was created to securely store database configuration values such as username, password, database name, and port number.
</p>

<p>Example configuration:</p>

<pre><code>POSTGRES_USER=fuseadmin
POSTGRES_PASSWORD=fusepassword
POSTGRES_DB=fusedb
POSTGRES_PORT=5432
</code></pre>

<h2>Purpose of Using <code>.env</code></h2>

<p>
Using a <code>.env</code> file improves security and maintainability because sensitive credentials are not directly written inside the application or Docker configuration files. This also makes it easier to modify configurations without changing the source code.
</p>

<hr>

<h1>Step 2: Creating Docker Compose Configuration</h1>

<p>
A <code>docker-compose.yml</code> file was created to define the PostgreSQL service.
</p>

<p>The configuration:</p>

<ul>
  <li>Uses the official PostgreSQL Docker image</li>
  <li>Loads environment variables from <code>.env</code></li>
  <li>Maps the PostgreSQL port</li>
  <li>Automatically executes <code>seed.sql</code></li>
</ul>

<p>Example configuration:</p>

<pre><code>version: '3.9'

services:
  db:
    image: postgres:16

    container_name: fuse_postgres

    restart: always

    env_file:
      - .env

    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}

    ports:
      - "${POSTGRES_PORT}:5432"

    volumes:
      - ./seed.sql:/docker-entrypoint-initdb.d/seed.sql
</code></pre>

<h2>Understanding Each Part</h2>

<h3><code>image: postgres:16</code></h3>

<p>
Uses the official PostgreSQL Docker image.
</p>

<h3><code>env_file</code></h3>

<p>
Loads variables from the <code>.env</code> file.
</p>

<h3><code>environment</code></h3>

<p>
Passes environment variables into the container.
</p>

<h3><code>ports</code></h3>

<pre><code>"${POSTGRES_PORT}:5432"
</code></pre>

<p><strong>Meaning:</strong></p>

<p>
Your computer port → Container port
</p>

<h3><code>volumes</code></h3>

<p>
Most important part:
</p>

<pre><code>- ./seed.sql:/docker-entrypoint-initdb.d/seed.sql
</code></pre>

<p>
This mounts your local SQL file into PostgreSQL’s special initialization folder.
</p>

<p>
When PostgreSQL starts for the first time:
</p>

<ul>
  <li>It checks <code>/docker-entrypoint-initdb.d/</code></li>
  <li>Finds <code>seed.sql</code></li>
  <li>Runs all SQL commands automatically</li>
</ul>

<p>
That is the core idea of this assignment.
</p>

<hr>

<h1>Step 3: Connecting the SQL Initialization File</h1>

<p>
The <code>seed.sql</code> file was linked to the special PostgreSQL initialization directory:
</p>

<pre><code>/docker-entrypoint-initdb.d/
</code></pre>

<p>
This directory is automatically checked by PostgreSQL during the first container startup.
</p>

<p>When the container starts:</p>

<ol>
  <li>PostgreSQL initializes the database</li>
  <li>It searches the initialization directory</li>
  <li>It detects <code>seed.sql</code></li>
  <li>The SQL commands are executed automatically</li>
  <li>Tables and sample data are created</li>
</ol>

<p>
This process eliminates the need for manual database setup.
</p>

<hr>

<h1>Step 4: Running the Docker Container</h1>

<p>
The PostgreSQL container was started using the following command:
</p>

<pre><code>docker compose up -d
</code></pre>

<h2>Explanation</h2>

<ul>
  <li><code>docker compose up</code> starts the services defined in <code>docker-compose.yml</code></li>
  <li><code>-d</code> runs the container in detached mode (background)</li>
</ul>

<p>
After successful execution, Docker downloaded the PostgreSQL image and started the database container.
</p>

<hr>

<h1>Step 5: Verifying Running Containers</h1>

<p>
The running container was verified using:
</p>

<pre><code>docker ps
</code></pre>

<p>
This command displays all currently running Docker containers.
</p>

<p>Expected output includes:</p>

<ul>
  <li>PostgreSQL image</li>
  <li>Container name</li>
  <li>Port mapping</li>
  <li>Running status</li>
</ul>


<hr>

<h1>Step 6: Accessing the Docker Container</h1>

<p>
To interact with the PostgreSQL server directly, a terminal session was opened inside the running container using:
</p>

<pre><code>docker exec -it fuse_postgres /bin/bash
</code></pre>

<h2>Explanation</h2>

<table>
  <thead>
    <tr>
      <th>Command Part</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>docker exec</code></td>
      <td>Executes commands inside a running container</td>
    </tr>
    <tr>
      <td><code>-it</code></td>
      <td>Opens an interactive terminal</td>
    </tr>
    <tr>
      <td><code>fuse_postgres</code></td>
      <td>Name of the running container</td>
    </tr>
    <tr>
      <td><code>/bin/bash</code></td>
      <td>Opens bash shell inside the container</td>
    </tr>
  </tbody>
</table>

<hr>

<h1>Step 7: Connecting to PostgreSQL</h1>

<p>
After entering the container, PostgreSQL was accessed using:
</p>

<pre><code>psql -U fuseadmin -d fusedb
</code></pre>

<h2>Explanation</h2>

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>-U</code></td>
      <td>PostgreSQL username</td>
    </tr>
    <tr>
      <td><code>-d</code></td>
      <td>Database name</td>
    </tr>
  </tbody>
</table>

<p>
Successful connection opens the PostgreSQL command-line interface.
</p>

<hr>

<h1>Step 8: Verifying Database Tables</h1>

<p>
The following command was used to display all tables inside the database:
</p>

<pre><code>\dt
</code></pre>

<p>
The database successfully contained the following tables:
</p>

<ul>
  <li>customers</li>
  <li>orders</li>
  <li>products</li>
  <li>offices</li>
  <li>employees</li>
  <li>productlines</li>
  <li>payments</li>
  <li>orderdetails</li>
</ul>

<p>
This confirmed that the <code>seed.sql</code> file executed successfully.
</p>

<hr>

<h1>Step 9: Running SQL Queries</h1>

<p>
A sample SQL query was executed to verify that the tables contained data.
</p>

<p>Example:</p>

<pre><code>SELECT COUNT(*) FROM customers;
</code></pre>

<p>
This query returns the total number of rows in the <code>customers</code> table.
</p>

<p>Additional verification queries can also be executed, such as:</p>

<pre><code>SELECT * FROM customers LIMIT 5;
</code></pre>

<hr>

<h1>Challenges Faced</h1>

<p>
During the setup process, some common issues that may occur include:
</p>

<ul>
  <li>Port conflicts if PostgreSQL is already running locally</li>
  <li>Incorrect environment variable configuration</li>
  <li>Docker volume caching preventing SQL reinitialization</li>
  <li>Incorrect file mounting paths</li>
</ul>

<p>These issues can typically be resolved by:</p>

<ul>
  <li>Changing ports</li>
  <li>Rechecking <code>.env</code> values</li>
  <li>Restarting containers</li>
  <li>Removing old Docker volumes using:</li>
</ul>

<pre><code>docker compose down -v
</code></pre>

<h2>VERY IMPORTANT CONCEPT</h2>

<p>
<code>seed.sql</code> only runs during the <strong>first database creation</strong>.
</p>

<p>
If you later modify <code>seed.sql</code>, Docker may <strong>NOT rerun it</strong> because PostgreSQL data already exists in the container volume.
</p>

<h3>To reset everything:</h3>

<pre><code>docker compose down -v</code></pre>

<h3>Then run again:</h3>

<pre><code>docker compose up</code></pre>

<p>
The <code>-v</code> flag removes the old database volume completely.
</p>

<p>
This is a very common beginner issue.
</p>

<hr>

<h1>Conclusion</h1>

<p>
In this task, PostgreSQL was successfully deployed using Docker Compose and automatically initialized using the provided <code>seed.sql</code> file. The setup demonstrated how Docker containers can simplify database deployment while maintaining consistent environments across development and production systems.
</p>

<p>
The use of <code>.env</code> improved configuration management and security, while Docker Compose simplified service orchestration. Automatic database initialization reduced manual setup effort and ensured reproducibility of the database environment.
</p>


<hr>
<h2>Short Reflection</h2>

<h3>Config (Factor III)</h3>
<p><strong>Question:</strong> Why is .env better than writing passwords in code?</p>

<p>
Using a <code>.env</code> file is better than writing passwords directly in the code because it keeps sensitive information such as database usernames and passwords separate from the application logic. This improves security since credentials are not exposed inside the source code. It also makes the application easier to manage because configuration values can be changed without modifying the code itself. Additionally, it reduces the risk of accidentally pushing sensitive data to public repositories like GitHub.
</p>

<h3>Backing Services (Factor IV)</h3>
<p><strong>Question:</strong> Why is treating the database as a separate service useful?</p>

<p>
Treating the database as a separate service is useful because it decouples the database from the main application. This means the database can be updated, replaced, or scaled independently without affecting the application code. It also improves flexibility and maintainability, as the application does not depend on a tightly integrated database system. This separation follows modern architecture practices and makes deployment more reliable.
</p>

<h3>Dev/Prod Parity (Factor X)</h3>
<p><strong>Question:</strong> Why does Docker make development and production similar?</p>

<p>
Docker makes development and production environments similar by packaging the application and its dependencies into containers. This ensures that the same PostgreSQL setup used in development can also run in production without changes. As a result, it reduces environment-related issues such as configuration mismatches and “works on my machine” problems. This consistency improves reliability and makes deployment smoother.
</p>