# Wilson Vuu . Jarvis Consulting

With over a year of software development experience building applications end to end, I am currently a Software Developer/Data Engineer at Jarvis, where I build backend applications in Java while designing Python data pipelines that transform raw data into actionable business insights. This spans everything from application development to an end-to-end Azure Databricks pipeline built with PySpark and the Medallion Architecture. Previously at Cardata, I built Laravel and Node.js APIs for financial workflows while improving the React.js/TypeScript frontend with reusable components, and at Lowe-Martin, I automated data sanitization with Python and VBA to improve mailing accuracy and speed up bulk mail batches. Most recently, I earned the Databricks Certified Data Engineer Associate certification, validating my ability to build production-grade pipelines on modern cloud platforms.
What draws me to software is that there's always something new to learn or a better way to build something, whether it's using a new technology or implementing a cleaner solution to an old problem.

## Skills

**Proficient:** Java, Python, SQL/RDBMS, REST APIs, ETL Pipelines, Spark

**Competent:** Spring Boot, React.js, Linux/Bash, Node.js, Git, Docker

**Familiar:** PHP (Laravel), Hibernate, Agile/Scrum, HTML/CSS, Unit Testing (JUnit)

## Jarvis Projects

Project source code: [https://github.com/jarviscanada/jarvis_data_eng_WilsonVuu](https://github.com/jarviscanada/jarvis_data_eng_WilsonVuu)


**Cluster Monitor** [[GitHub](https://github.com/jarviscanada/jarvis_data_eng_WilsonVuu/tree/master/linux_sql)]: The Linux Cluster Monitoring project is a system designed to track hardware specifications and resource usage across a networked Linux cluster. Each node collects its hardware profile on initialization and continuously logs CPU, memory, and disk metrics at scheduled intervals using crontab, with all data stored in a centralized PostgreSQL database managed through Docker. The data is organized into two tables covering hardware specifications and ongoing resource usage, giving the LCA team at Jarvis the visibility to monitor system performance over time and make informed decisions around resource allocation.

**Java Grep App** [[GitHub](https://github.com/jarviscanada/jarvis_data_eng_WilsonVuu/tree/master/core_java/grep)]: Implemented a Java application that replicates the Unix grep command, taking a regex pattern, a root directory, and an output file as arguments. The app recursively searches all files in the directory and writes matching lines to the output. Built using Java's Streams API with a lazy pipeline using Java NIO's Files.walk() for file traversal, flatMap to flatten each file's lines into a single stream, and filter to match the regex, ensuring memory stays low regardless of file or directory size. Used Maven for dependency and build management, packaging the app into a fat jar with all dependencies bundled. Containerized the application with Docker and pushed the image to DockerHub. Verified behavior with unit tests across edge cases.

**Python Data Analytics** [[GitHub](https://github.com/jarviscanada/jarvis_data_eng_WilsonVuu/tree/master/python_data_analytics)]: Analyzed two years of transactional data (2009-2011) for London Gift Shop (LGS), a UK-based wholesale retailer, to find actionable insights around customer retention and revenue growth. Applied RFM segmentation to identify high-value customers, quantify at-risk revenue, and support targeted win-back campaigns. Explored monthly sales trends, new vs. existing customer revenue splits, and customer health status over time to inform marketing and inventory decisions. Built using Python (pandas, NumPy, matplotlib, seaborn) in a Jupyter Notebook environment, with data stored in a PostgreSQL data warehouse, both running in Docker containers connected via a shared bridge network.

**Databricks Data Engineering Project** [[GitHub](https://github.com/jarviscanada/jarvis_data_eng_WilsonVuu/tree/master/spark)]: Designed and implemented end-to-end data pipelines in Azure Databricks using PySpark and the Medallion Architecture (Bronze, Silver, Gold) to process transactional, customer, and stock market data from multiple sources. Built scalable ETL and DLT pipelines to ingest, cleanse, transform, and model data into Delta tables optimized for analytics. Delivered datasets and interactive dashboards that identified fraud patterns, customer behavior trends, and stock performance metrics.


## Highlighted Projects
**Inventory Management System**: The Inventory Management System is a Spring Boot application with a React frontend, designed to help businesses organize their catalog and track stock levels. It models the relationships between items, categories, and suppliers through a relational schema using Spring Data JPA/Hibernate, and exposes a RESTful API to create, update, and query inventory data across the catalog, delivering a clear, maintainable foundation for keeping stock accurate and operations running smoothly.

**Smart Investors**: Smart Investors is a web application with a JavaScript frontend that lets users practice investment strategies in a risk-free environment. It tracks each user's portfolio and transaction history through a relational database, and integrates the Yahoo Finance API to feed live market data into the platform for accurate portfolio valuations.


## Professional Experiences

**Software Developer/Data Engineer, Jarvis (2026-present)**: Developed and delivered a range of software and data engineering projects including a Linux cluster monitoring system, a Java grep application, and performed data analytics using Python in an Agile environment. Built backend services and data pipelines across Java and Python, working in Linux environments with tools such as Docker, PostgreSQL, and Bash.

**Full Stack Software Engineer, Cardata (Nov 2021-Jul 2022)**: Integrated React.js and TypeScript frontends with Laravel and Node.js backend services to improve system scalability and the user experience of daily payment processing. Engineered a dynamic PDF export system to automate report generation and introduced a localization pipeline to the application, achieving 93% translation coverage.

**Data/Programmer Analyst Intern, Lowe-Martin (May 2019-Sep 2019)**: Used VBA and Python to automate the sanitization of CSV data, resulting in an increase in shipping accuracy. Built custom report generation tools in Microsoft Access and Excel to display and present shipping and address data for internal review and validation. Built a prototype of the corporate website using HTML/CSS and JavaScript as a visual mockup for leadership to review and approve.


## Education
**Wilfrid Laurier University (2017-2022)**, Bachelor of Science, Computer Science


## Miscellaneous
- Databricks Certified Data Engineer Associate (July 2026)
- Badminton player: Still a beginner, but I play in weekly recreational sessions. It’s a fun way to stay active, and I really enjoy the quick pace and the social side of the game.
- Hiking enthusiast: I love hitting local trails and getting lost in conservation areas for a few hours. For me, it's a good way to clear my mind and recharge.