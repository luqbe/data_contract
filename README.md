# soda_Data_Contract Demo

This project demonstrates the use of data contracts in a Databricks environment using Delta Live Tables (DLT). It includes a sample pipeline that ingests raw order data, applies data quality rules based on a defined contract, and produces cleaned silver-layer data.

## Project Structure

- `databricks.yml`: Databricks bundle configuration for deployment.
- `contract/datacontract.yml`: Data contract specification defining the schema and expectations for the `orders_bronze` table.
- `resources/`: Contains Databricks resources like the DLT pipeline (`demo_pipeline.yml`) and a data generator job (`generator.yml`).
- `src/contract/transformations/`: Python modules for DLT transformations.
  - `bronze.py`: Ingests raw CSV data from a volume into the `orders_bronze` table.
  - `silver.py`: Cleans and validates data from `orders_bronze` into `orders_silver`, enforcing contract rules (e.g., non-null order IDs, positive amounts, valid email formats).

## Prerequisites

- Databricks workspace with DLT enabled.
- Access to a catalog named `data_contract_demo` and schema `orders_data`.
- Raw data in CSV format uploaded to `/Volumes/data_contract_demo/orders_data/orders_raw/raw_data/`.

## Setup and Deployment

1. **Clone or download the project** to your local machine.

2. **Configure the bundle**:
   - Update `databricks.yml` with your workspace details if needed.
   - Ensure the `catalog` and `schema` variables match your Databricks environment.

3. **Deploy the bundle**:
   - Use the Databricks CLI: `databricks bundle deploy --target lab`.
   - This deploys the DLT pipeline and data generator job.

4. **Run the data generator job** (optional, to populate sample data):
   - Trigger the `data_generator` job from the Databricks UI or CLI.

5. **Execute the DLT pipeline**:
   - Start the `demo_contract` pipeline from the Databricks UI.
   - Monitor for data quality expectations (e.g., failures on missing IDs, dropped rows for negative amounts).

## Data Contract Details

The contract in `contract/datacontract.yml` specifies:
- **Model**: `orders_bronze` with fields for `order_id` (string, required, primary), `total_amount` (string, required), and `customer_email` (string, email format).
- **Server**: Points to a Databricks SQL warehouse for validation.

Quality rules in `silver.py` enforce:
- Critical failure if `order_id` is null.
- Row drops for non-positive `total_amount`.
- Warnings for invalid email formats.

## Usage

- View pipeline results in the Databricks UI under the `data_contract_demo.orders_data` schema.
- Query tables like `orders_bronze` and `orders_silver` via SQL or notebooks.
- Update the contract or transformations as needed for your use case.


### Linting and Validation

To ensure the data contract is valid and adheres to the specification:

1. **Install the Data Contract CLI**:
   - Run: `pip install data-contracts`.

2. **Lint the Contract** (checks syntax and structure):
   - Navigate to the project root and execute: `datacontract lint contract/datacontract.yml`.
   - This flags issues like missing required fields or invalid types.

3. **Validate Against Data** (optional, requires server access):
   - For full validation against the Databricks server defined in the contract:
     - Set environment variables for authentication (e.g., `DATABRICKS_TOKEN`).
     - Run: `datacontract test contract/datacontract.yml`.
   - This verifies schema compliance, data types, and expectations against the actual `orders_bronze` table.

4. **Automate in CI/CD**:
   - Integrate linting into your deployment pipeline (e.g., via GitHub Actions) to catch contract issues early.

