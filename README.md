# WalletWatch API 💰

A RESTful API developed with FastAPI for tracking personal expenses and income. This API provides a robust backend solution for managing financial transactions with database persistence.

## Features

- 🚀 **FastAPI Framework**: High-performance, modern Python web framework
- 💾 **PostgreSQL Database**: Reliable and scalable database using SQLModel (SQLAlchemy)
- 📊 **Transaction Management**: Track income and expenses with categories and descriptions
- 💰 **Balance Calculation**: Real-time balance calculation (Income - Expenses)
- 📄 **Pagination Support**: List transactions with skip/limit pagination
- 🔄 **Auto Database Migration**: Automatic table creation on startup
- ⚙️ **Environment Configuration**: Easy configuration via `.env` file
- 🛡️ **Data Validation**: Pydantic models for request/response validation

## Technologies

- **Python 3.10+**
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLModel** - SQL database in Python, designed for simplicity, compatibility, and robustness
- **PostgreSQL** - Advanced open-source relational database
- **psycopg2-binary** - PostgreSQL adapter for Python
- **Pydantic** - Data validation using Python type annotations
- **Pydantic Settings** - Settings management using Pydantic models
- **python-jose** - JWT implementation for Python
- **passlib** - Password hashing library with bcrypt support
- **Uvicorn** - Lightning-fast ASGI server

## Project Structure

```
WalletWatch-API/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── schemas.py              # Pydantic models for request/response validation
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Application settings and configuration
│   ├── db/
│   │   ├── __init__.py
│   │   └── session.py          # Database session management
│   ├── models/
│   │   ├── __init__.py
│   │   └── transaction.py      # Transaction SQLModel model
│   └── routers/
│       ├── __init__.py
│       └── transactions.py     # Transaction API endpoints
├── venv/                       # Virtual environment
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── LICENSE                     # MIT License
```

## Installation

### Prerequisites

- Python 3.10 or higher
- PostgreSQL database
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd WalletWatch-API
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a `.env` file**
   Create a `.env` file in the root directory with the following variables:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/walletwatch_db
PROJECT_NAME=WalletWatch API
API_V1_STR=/api/v1
   ```

   Replace `username`, `password`, `localhost`, `5432`, and `walletwatch_db` with your PostgreSQL credentials and database name.

6. **Create the database**
   Make sure PostgreSQL is running and create the database:
   ```sql
   CREATE DATABASE walletwatch_db;
   ```

## Running the Application

Start the development server with auto-reload:

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://127.0.0.1:8000
- **Interactive API Documentation**: http://127.0.0.1:8000/docs
- **Alternative API Documentation**: http://127.0.0.1:8000/redoc

## API Endpoints

### Root Endpoint
- `GET /` - Welcome message

### Transaction Endpoints

All transaction endpoints are prefixed with `/api/v1/transactions`

- `POST /api/v1/transactions/` - Create a new transaction (expense or income)
  - Request body: `TransactionCreate` (amount, category, description, is_income)
  - Response: `TransactionRead` with created transaction details

- `GET /api/v1/transactions/` - Get all transactions
  - Query parameters:
    - `skip` (int, default: 0): Number of transactions to skip
    - `limit` (int, default: 100): Maximum number of transactions to return
  - Response: List of `TransactionRead` objects

- `GET /api/v1/transactions/{transaction_id}` - Get a specific transaction by ID
  - Path parameter: `transaction_id` (int)
  - Response: `TransactionRead` object
  - Returns 404 if transaction not found

- `GET /api/v1/transactions/balance` - Calculate current balance
  - Response: `BalanceResponse` with:
    - `total_income`: Sum of all income transactions
    - `total_expense`: Sum of all expense transactions
    - `current_balance`: Total income minus total expenses

## Database Models

### Transaction Model

The `Transaction` model includes the following fields:

- `id` (int, primary key): Unique identifier
- `amount` (float): Transaction amount (must be positive)
- `category` (str): Transaction category (3-50 characters)
- `description` (str, optional): Additional transaction details
- `is_income` (bool): Whether the transaction is income (default: False)
- `created_at` (datetime): Timestamp when the transaction was created
- `updated_at` (datetime, optional): Timestamp when the transaction was last updated
- `deleted_at` (datetime, optional): Soft delete timestamp

## Configuration

The application uses Pydantic Settings to manage configuration through environment variables. The following settings are available:

- `DATABASE_URL` (required): PostgreSQL connection string
- `PROJECT_NAME` (optional): Project name (default: "WalletWatch API")
- `API_V1_STR` (optional): API version prefix (default: "/api/v1")

All settings can be configured via a `.env` file in the root directory.

## Current Implementation Status

### ✅ Implemented Features

- **Transaction CRUD Operations**:
  - ✅ Create transactions (POST)
  - ✅ Read all transactions with pagination (GET)
  - ✅ Read single transaction by ID (GET)
  - ⏳ Update transaction (TODO)
  - ⏳ Delete transaction (TODO)

- **Balance Calculation**:
  - ✅ Real-time balance calculation endpoint
  - ✅ Database-level aggregation for performance

- **Data Models**:
  - ✅ Transaction model with all fields (including soft delete support)
  - ✅ Pydantic schemas for request/response validation
  - ✅ Field validation (positive amounts, category length, etc.)

- **Database**:
  - ✅ PostgreSQL integration with SQLModel
  - ✅ Automatic table creation on startup
  - ✅ Database session management

- **API Documentation**:
  - ✅ Interactive Swagger UI at `/docs`
  - ✅ ReDoc documentation at `/redoc`

## Development

### Database Migrations

The application automatically creates database tables on startup using SQLModel's metadata. The `lifespan` context manager in `main.py` handles this:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
```

### Adding New Models

1. Create a new model in `app/models/`
2. Import it in `app/models/__init__.py`
3. Import the model in `app/main.py` to ensure it's registered with SQLModel

### Adding New Endpoints

1. Create router functions in `app/routers/`
2. Include the router in `app/main.py` using `app.include_router()`

## Dependencies

All project dependencies are listed in `requirements.txt`:

- `fastapi` - Web framework
- `uvicorn[standard]` - ASGI server
- `pydantic` - Data validation
- `pydantic-settings` - Settings management
- `sqlmodel` - Database ORM
- `psycopg2-binary` - PostgreSQL driver
- `python-jose[cryptography]` - JWT support
- `passlib[bcrypt]` - Password hashing

## TODO List

### 🔐 Authentication & Authorization
- [ ] Implement OAuth2 with JWT authentication
- [ ] Create User model and authentication endpoints
- [ ] Add user registration and login endpoints
- [ ] Protect transaction endpoints with authentication
- [ ] Implement user-specific transaction filtering (users can only see their own transactions)
- [ ] Add role-based access control (if needed)

### 🔄 CRUD Operations
- [ ] Implement UPDATE endpoint (`PUT /api/v1/transactions/{transaction_id}`)
- [ ] Implement DELETE endpoint (`DELETE /api/v1/transactions/{transaction_id}`)
- [ ] Implement soft delete functionality (use `deleted_at` field)
- [ ] Add hard delete option (admin only)

### 🔍 Filtering & Search
- [ ] Add filtering by category
- [ ] Add filtering by transaction type (income/expense)
- [ ] Add date range filtering (by `created_at`)
- [ ] Add search by description (text search)
- [ ] Add sorting options (by date, amount, category)
- [ ] Exclude soft-deleted transactions from queries by default

### 📊 Advanced Features
- [ ] Add transaction statistics endpoint (monthly/yearly summaries)
- [ ] Add category-wise expense breakdown
- [ ] Add date-based grouping (daily, weekly, monthly)
- [ ] Add export functionality (CSV, JSON)
- [ ] Add transaction tags/labels system
- [ ] Add recurring transactions support

### 🛡️ Validation & Error Handling
- [ ] Add comprehensive input validation
- [ ] Improve error messages and error handling
- [ ] Add request rate limiting
- [ ] Add input sanitization

### 🧪 Testing
- [ ] Set up pytest testing framework
- [ ] Add unit tests for models and schemas
- [ ] Add integration tests for API endpoints
- [ ] Add database transaction tests
- [ ] Add authentication tests
- [ ] Set up CI/CD pipeline

### 📚 Documentation
- [ ] Add API usage examples
- [ ] Add authentication flow documentation
- [ ] Add deployment guide
- [ ] Add contribution guidelines

### 🚀 Performance & Optimization
- [ ] Add database indexing for frequently queried fields
- [ ] Implement caching for balance calculations
- [ ] Add database query optimization
- [ ] Add pagination metadata (total count, page info)

### 🔧 Infrastructure
- [ ] Add database migration system (Alembic)
- [ ] Add logging configuration
- [ ] Add monitoring and health check endpoints
- [ ] Add Docker containerization
- [ ] Add environment-specific configurations (dev, staging, prod)

## Author

Fernando Herrera

## License

MIT License - see LICENSE file for details
