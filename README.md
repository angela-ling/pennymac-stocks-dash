# Serverless Stock Winners Pipeline
**Pennymac Tech Rotational Engineer Program Project**

A full-stack serverless application that automatically identifies and displays the daily "Top Moving" stock from a select group of high-volume tickers (AAPL, MSFT, GOOGL, AMZN, TSLA).

Link to dashboard: http://datastack-stockappbucketa91b76cd-opjzru0uybwn.s3-website-us-east-1.amazonaws.com/

---

## System Architecture ##
The project follows a decoupled, event-driven architecture built entirely with the **AWS Cloud Development Kit (CDK)**.

* **Frontend:** A responsive Single Page Application (SPA) hosted on **Amazon S3**. It utilizes the Fetch API to retrieve data from the backend and renders a color-coded "Winning Stocks" table.
* **API Layer:** **Amazon API Gateway** serves as the entry point. It features a custom **Usage Plan** with rate-limiting (2 req/sec) to ensure service stability and cost control.
* **Compute:** Two **AWS Lambda** functions (Python 3.12):
    * `IngestionFunction`: Triggered on a schedule to fetch data from the Massive API and identify the winner.
    * `RetrievalFunction`: A REST API backend that queries history for the user interface.
* **Database:** **Amazon DynamoDB** serves as the persistent store for historical winners, indexed by date for fast lookups.



---

## Key Technical Features

### 1. Robust Data Ingestion & Pacing
The ingestion pipeline implements a **12-second pacing strategy** between API calls. This proactive rate-limiting ensures the application stays within third-party API constraints without triggering `429 Too Many Requests` errors.

### 2. Infrastructure as Code (IaC)
The project is managed via a multi-stack CDK approach:
* **`DataStack`**: Manages persistent resources with an independent lifecycle (S3, DynamoDB).
* **`ServicesStack`**: Manages rapidly iterable compute and networking layers (Lambda, API Gateway).

### 3. Security & Cost Management
* **Block Public Access (BPA)**: Configured S3 to block all public ACLs, enforcing modern policy-based security over legacy file-level permissions.
* **API Usage Plan**: Implemented a throttling limit of 2 requests per second to protect the account from excessive API calls to ensure usage stays within the AWS Free Tier.
* **CORS Management**: Configured granular Cross-Origin Resource Sharing headers to allow secure communication between the S3 frontend and the API Gateway.

### 4. Financial Data Logic
To meet the "Last 7 Days" requirement, the retrieval logic uses a **12-day lookback window**. This specifically accounts for weekend market closures, ensuring the UI always displays a complete history.

---

## Getting Started

### Prerequisites
* AWS CLI & CDK Toolkit installed and configured.
* Python 3.12+
* A valid API Key from Massive API.

### Installation & Deployment
1.  **Clone and Install**
    ```bash
    git clone https://github.com/angela-ling/pennymac-stocks-dash.git
    cd pennymac-stocks-dash
    pip install -r requirements.txt
    ```

2.  **Deploy the Infrastructure**
    ```bash
    cdk deploy --all
    ```

---

## Cleanup
To avoid ongoing AWS costs, run:
```bash
cdk destroy --all