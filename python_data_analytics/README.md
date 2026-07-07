# Introduction
London Gift Shop (LGS) is a UK-based online store that sells giftware. Many customers of the company are wholesalers. 
The company has been running online shops for more than 10 years to customers across the UK and internationally. 
This project analyzes two years of transactional data (2009–2011) to find actionable insights that LGS can use to protect and increase revenue. 
The analytics results will allow LGS to:

- Identify and retain their highest-value customers through targeted loyalty programs
- Design win-back campaigns for at-risk customers before revenue is permanently lost
- Optimize inventory planning and marketing spend around predictable seasonal peaks
- Monitor customer health over time to detect early signs of churn

**Technologies used:**

**Data Analysis & Visualization**
- **Python** — core programming language
- **pandas** — data wrangling, transformation, and aggregation
- **numpy** — numerical computations
- **matplotlib / seaborn** — data visualization and charting

**Database & Connectivity**
- **PostgreSQL** — data warehouse storing raw retail transaction data
- **sqlalchemy** — ORM layer for connecting Python to PostgreSQL
- **psycopg2** — PostgreSQL database driver

**Development Environment**
- **Jupyter Notebook** — interactive data wrangling and visualization
- **Docker** — containerized Jupyter and PostgreSQL environments

**Analytics Methodology**
- **RFM Analysis** — industry-standard customer segmentation framework (Recency, Frequency, Monetary)

# Implementation
## Project Architecture
**LGS Web Application**

**Frontend** - a browser-facing application served via Content Delivery Network (CDN), in an azure storage that stores HTML/CSS/JavaScript and images.

**Backend** — browser requests hit Azure API Management, which routes to an AKS Kubernetes cluster running microservices, which persist transactional data to an Azure SQL Server (OLTP) database

**Jarvis Consulting PoC Environment**
Jarvis team does not have access to the LGS environment, the LGS IT team extracted transactional data from Azure SQL Server via ETL (JDBC/ODBC) in a `retail.sql` file.
The Jarvis PoC environment consists of:

**PostgreSQL Data Warehouse** — stores the raw retail transaction data containing 1,067,371 rows ranging December 2009 to December 2011. Data was loaded from the provided `retail.sql` file.

**Jupyter Notebook Analytics** — connects to PostgreSQL via SQLAlchemy, performs data wrangling, cleaning, transformation, and produces visual analytics insights.

![Project Architecture](assets/Project_Architecture.png)

Both PostgreSQL and Jupyter run in Docker containers connected through a shared **Docker bridge network**.

The dataset contains the following attributes:

| Column | Type | Description |
|---|---|---|
| `invoice_no` | Nominal | 6-digit invoice number. Starts with 'C' if canceled |
| `stock_code` | Nominal | 5-digit product code uniquely assigned to each product |
| `description` | Nominal | Product name |
| `quantity` | Numeric | Quantity of each product per transaction |
| `invoice_date` | Numeric | Date and time the transaction was generated |
| `unit_price` | Numeric | Product price per unit in sterling (£) |
| `customer_id` | Nominal | 5-digit number uniquely assigned to each customer |
| `country` | Nominal | Country where the customer resides |

## Data Analytics and Wrangling
 
Notebook can be found here: [retail_data_analytics_wrangling.ipynb](./retail_data_analytics_wrangling.ipynb)

The following analyses were performed to help LGS increase revenue:
 
### 1. Monthly Sales and Growth
 
Monthly sales data reveals a clear Q4 holiday peak, with October through December consistently generating the highest revenue each year. Month-over-month growth rates show volatility but a general upward trend into Q4. This gives LGS a predictable window to proactively plan inventory restocking and targeted promotions ahead of peak season.
 
Note: December 2009 and December 2011 appear lower due to incomplete data at the start and end of the dataset.
 
### 2. Top Products by Season
 
Top 10 products were analyzed separately for Q4 (Oct–Dec) versus the rest of the year (Jan–Sep). Products unique to the Q4 top 10 (highlighted in the charts) are seasonal items that appear only during the holiday period. LGS can use this to stock seasonal products ahead of Q4 and distinguish evergreen products from seasonal ones in inventory planning.
 
### 3. New vs. Existing Customer Revenue Split
 
Customers were classified as new (first purchase in the current month) or existing (purchased in a prior month). Existing customers consistently contributed approximately 80% or more of monthly revenue throughout the dataset. This tells LGS that investing in customer retention yields a higher ROI than acquiring new customers.
 
### 4. RFM Customer Segmentation
 
Customers were scored and segmented into 11 groups using Recency, Frequency, and Monetary analysis, scored on a 1–5 scale across each dimension. Segments include Champions, Loyal, Potential Loyalists, New Customers, Promising, Need Attention, About to Sleep, Can't Lose Them, At Risk, Hibernating, and Lost.
 
Segments were further grouped into three retention priority tiers:
 
| Priority | Segments | Customers | Revenue Share |
|---|---|---|---|
| High Priority | Champions, Loyal, At Risk, Can't Lose Them | 2,428 | 88.2% |
| Medium Priority | Potential Loyalists, Need Attention, New Customers | 1,766 | 8.2% |
| Low Priority | Promising, About to Sleep, Hibernating, Lost | 1,684 | 3.6% |
 
LGS can use this to reward Champions with loyalty programs, target At Risk customers with win-back campaigns, and avoid spending marketing budget on Lost customers.
 
### 5. Revenue by Country
 
Revenue and customer counts were analyzed by country. The UK dominates volume, but Germany, France, Ireland, and the Netherlands show meaningful international demand. LGS can use this to prioritize geographic expansion and tailor international marketing efforts.
 
## Improvements
 
- **Product-level Analysis** — Identify top and bottom performing products by revenue to help optimize inventory decisions.
- **Cohort Retention Tracking** — Track how groups of new customers behave over time to better measure retention and lifetime value.
