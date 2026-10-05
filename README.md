# ERP Order Exception Monitor

A Python and Streamlit operations tool that detects **ERP and SAP-style order exceptions**, identifies their business impact, and helps teams take corrective action.

The project simulates an ERP/SAP order management environment using synthetic data and demonstrates how deterministic business rules, SQL, and AI-generated recommendations can support supply chain and enterprise operations workflows.

## What It Does

The application follows a simple operational workflow:

**ERP/SAP Order Data → Detect Exception → Identify Impact → Recommend Fix → Take Action → Resolve Issue**

It identifies common order problems such as:

* Inventory shortages
* Delivery risks
* Supplier performance issues
* Missing ERP information

Instead of only reporting problems, the application focuses on **what should be done to fix them**.

## Key Features

### SAP and ERP-Style Exception Detection

The application simulates common operational scenarios that can occur in ERP and SAP order workflows.

Python-based business rules identify exceptions across order data, including:

* Orders where required quantity exceeds available inventory
* Orders with estimated delivery dates later than requested
* Suppliers with low on-time delivery performance
* Orders with missing required information

### Exception Prioritization

Exceptions are categorized by severity:

* High
* Medium
* Low

Severity is determined using business rules based on the potential operational impact.

### Order Investigation

Users can select an affected order and review:

* Customer
* Product
* Supplier
* Region
* Quantity
* Available inventory
* Order value
* Supplier rating
* Supplier on-time rate

This mirrors the type of operational investigation a supply chain or ERP team could perform when reviewing an order exception.

### AI Resolution Plans

The application can generate a practical resolution plan using an LLM.

The AI focuses on:

* Understanding the detected problem
* Explaining the business impact
* Recommending a corrective action
* Providing specific next steps
* Including a verification step to confirm the issue has been resolved

The AI does not determine whether an exception exists. Python business rules make that determination first, while the AI is used to help explain and resolve the issue.

If an OpenAI API key is not configured, the application automatically uses a deterministic fallback resolution plan.

### Resolution Workflow

Users can record the action taken for an exception and mark the issue as:

* Open
* In Progress
* Resolved

Resolution actions are stored in SQLite for the current application session.

### Resolution History

The application provides a history of previously recorded resolution actions, allowing users to see which issues were addressed and what action was taken.

---

## Dashboard Preview

### Main Dashboard

(main_dashboard.png)

**Screenshot:** Main ERP/SAP-style exception dashboard showing KPIs, filters, detected problems, and exception distribution.

<br>

### Order Investigation

(order_investigation.png)

**Screenshot:** Selected order with priority, order details, problem details, and recommended fix.

<br>

### AI Resolution Plan

(AI_resolution_plan.png)

**Screenshot:** AI-generated resolution summary, business impact, recommended action, and next steps.

<br>

### Resolution Workflow

(resolution_workflow.png)

**Screenshot:** Resolution workflow showing status selection and action recording.

<br>

### Resolution History

(resolution_history.png)

**Screenshot:** Resolution history showing previously recorded corrective actions.

---

## Technology Stack

| Technology    | Purpose                         |
| ------------- | ------------------------------- |
| Python        | Core application logic          |
| Pandas        | Data processing and analysis    |
| Streamlit     | Interactive web application     |
| Plotly        | Data visualization              |
| SQLite        | Resolution history storage      |
| OpenAI API    | AI-generated resolution plans   |
| python-dotenv | Environment variable management |
| Pytest        | Automated testing               |

---

## Project Structure

```text
erp-order-exception-monitor/
│
├── data/
│   ├── erp_orders.csv
│   └── erp_orders.db
│
├── src/
│   ├── __init__.py
│   ├── generate_data.py
│   ├── exception_rules.py
│   ├── database.py
│   └── ai_assistant.py
│
├── tests/
│   └── test_exception_rules.py
│
├── sql/
│   └── analysis.sql
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## How It Works

### 1. Generate ERP/SAP-Style Data

Synthetic ERP-style order data is generated with information such as:

* Order ID
* Customer
* Product
* Supplier
* Region
* Quantity
* Available inventory
* Order value
* Lead time
* Supplier rating
* Supplier on-time rate
* Delivery dates
* Payment terms

Run:

```bash
python src/generate_data.py
```

### 2. Detect Exceptions

The application evaluates each order against deterministic business rules.

For example:

```text
Required Quantity: 400
Available Inventory: 250

Exception:
Inventory Shortage

Impact:
150 units are unavailable for fulfillment.
```

### 3. Investigate the Problem

Users select an exception from the dashboard to review the affected order and understand the underlying issue.

This represents a simplified version of an operational workflow that could be used alongside an ERP or SAP environment.

### 4. Generate a Resolution Plan

The AI assistant takes the detected exception and generates a business-focused resolution plan.

The AI does not determine whether an exception exists. That decision is handled by deterministic Python rules.

This keeps exception detection predictable while using AI where it provides the most value: **explaining the issue and recommending practical next steps.**

### 5. Record the Resolution

After taking action, the user can record:

* Resolution status
* Action taken
* Resolution timestamp

The information is stored in SQLite.

---

## AI and ERP Approach

The project uses a hybrid approach combining traditional business logic with AI:

```text
                  ERP / SAP-Style Order Data
                            │
                            ▼
                   Deterministic Rules
                            │
                            ▼
                    Exception Detected
                            │
                            ▼
                       LLM Assistant
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
           Summary        Impact       Corrective
                                        Action
                            │
                            ▼
                       Next Steps
                            │
                            ▼
                     Resolution Record
```

This approach separates **business rule detection** from **AI-assisted resolution**.

The application does not rely on the LLM to decide whether an order violates a business rule.

---

## Example Exceptions

### Inventory Shortage

An order requires more inventory than is currently available.

**Possible actions:**

* Check alternate warehouse inventory
* Review replenishment options
* Split the shipment
* Confirm the customer delivery requirement

### Delivery Risk

The estimated delivery date is later than the requested delivery date.

**Possible actions:**

* Review supplier lead time
* Check alternate fulfillment options
* Confirm a revised delivery date
* Update the customer commitment

### Supplier Performance

A supplier has a low historical on-time delivery rate.

**Possible actions:**

* Review supplier performance
* Confirm the current order commitment
* Evaluate alternate suppliers
* Adjust sourcing decisions if necessary

### Data Quality

Required ERP information is missing.

**Possible actions:**

* Identify the missing fields
* Confirm the information with the responsible team
* Update the order
* Recheck the order before processing

---

## Running the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/yaminik03/erp-order-exception-monitor.git
cd erp-order-exception-monitor
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate the Data

```bash
python src/generate_data.py
```

### 5. Configure the AI Assistant

Create a `.env` file:

```text
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-6-luna
```

The `.env` file is intentionally excluded from Git.

If no API key is configured, the application uses the built-in fallback resolution logic.

### 6. Run the Application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

---

## Testing

Run the automated tests with:

```bash
python -m pytest
```

The tests verify the core exception detection rules, including inventory, delivery, supplier, and data quality exceptions.

---

## SQL Analysis

The project also includes SQL queries in:

```text
sql/analysis.sql
```

These queries can be used to analyze operational trends such as:

* Exception frequency
* Supplier performance
* Order value
* Inventory shortages
* Delivery risks

---

## SAP Integration Context

This project is **not connected to a live SAP system**.

Instead, it uses synthetic ERP-style data to demonstrate concepts relevant to SAP and enterprise operations, including:

* Order exception management
* Inventory availability
* Supplier performance
* Delivery commitments
* Operational prioritization
* Resolution tracking
* AI-assisted business workflows

A future version could connect these workflows to SAP data through appropriate APIs or enterprise integration services.

---

## Important Note

This project uses **synthetic ERP-style data** and is not connected to a live SAP or ERP system.

The project demonstrates how an ERP operations workflow could be structured using Python, SQL, data analysis, and AI-assisted resolution recommendations.

---

## Skills Demonstrated

* Python
* SQL
* Pandas
* Streamlit
* Plotly
* SQLite
* LLM integration
* API integration
* SAP/ERP workflow concepts
* Data analysis
* Business rule development
* Exception management
* Supply chain analytics
* Enterprise operations
* Automated testing
* Operational problem solving

---

## Future Improvements

Potential next steps include:

* SAP API integration
* Real-time ERP data ingestion
* User authentication and role-based access
* Email or Slack notifications for critical exceptions
* Supplier performance trend analysis
* Automated resolution actions
* Resolution effectiveness tracking
* Integration with enterprise workflow systems

---

## Author

**Yamini Kattelu**

Information Technology graduate focused on AI engineering, data analysis, supply chain technology, and intelligent enterprise applications.

GitHub: `github.com/yaminik03`