
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from typing import List
from database.models import TrailBalanceCurrentYear, TrailBalancePreviousYear


# Import models from the models module
def get_model_by_name(table_name: str):
    
    if table_name == 'current_year':
        return TrailBalanceCurrentYear
    elif table_name == 'previous_year':
        return TrailBalancePreviousYear
    else:
        raise ValueError(f"Unknown table: {table_name}")


async def get_total(db: AsyncSession, table_name: str, column: str) -> float:
    """
    Returns the total of either the debit, credit, or balance column from a given table.
    This is a read-only operation that does not modify the database.
    
    Args:
        db: Async database session (read-only)
        table_name: Name of the table ('current_year' or 'previous_year')
        column: Column name to sum ('debit', 'credit', or 'balance')
    
    Returns:
        float: The total value of the specified column
    """
    # Validate column name
    if column not in ['debit', 'credit', 'balance']:
        raise ValueError(f"Invalid column: {column}. Must be one of 'debit', 'credit', 'balance'")
    
    model_class = get_model_by_name(table_name)
    col_attr = getattr(model_class, column)
    
    # Calculate and return the sum using correct SQLAlchemy 2.0 async syntax
    stmt = select(func.sum(col_attr))
    result = await db.execute(stmt)
    total = result.scalar_one_or_none()
    return total if total is not None else 0.0


async def get_account_names(db: AsyncSession, table_name: str) -> List[str]:
    """
    Retrieves all account names from the specified table.
    This is a read-only operation that does not modify the database.
    
    Args:
        db: Async database session (read-only)
        table_name: Name of the table ('current_year' or 'previous_year')
    
    Returns:
        List[str]: List of account names
    """
    model_class = get_model_by_name(table_name)
    
    # Query all distinct account names (using the account_name column)
    stmt = select(model_class.account_name).distinct()
    result = await db.execute(stmt)
    results = result.all()
    
    # Extract names from tuples and return as list
    return [name for name, in results]


async def get_gl_accounts(db: AsyncSession, table_name: str) -> List[str]:
    """
    Retrieves all GL account numbers from the specified table.
    This is a read-only operation that does not modify the database.
    
    Args:
        db: Async database session (read-only)
        table_name: Name of the table ('current_year' or 'previous_year')
    
    Returns:
        List[str]: List of GL account numbers
    """
    model_class = get_model_by_name(table_name)
    
    # Query all distinct GL account numbers
    stmt = select(model_class.gl_account).distinct()
    result = await db.execute(stmt)
    results = result.all()
    
    # Extract GL accounts from tuples and return as list
    return [gl_account for gl_account, in results]


async def check_total_match(db: AsyncSession, table_name: str) -> dict:
    """
    Compares the total debit and total credit of a given table to check if they match.
    This is a read-only operation that does not modify the database.
    
    Args:
        db: Async database session (read-only)
        table_name: Name of the table ('current_year' or 'previous_year')
    
    Returns:
        dict: Contains debit_total, credit_total, and is_balanced status
    """
    model_class = get_model_by_name(table_name)
    
    # Get total debit and credit values using correct SQLAlchemy 2.0 syntax
    debit_stmt = select(func.sum(model_class.debit))
    credit_stmt = select(func.sum(model_class.credit))
    
    debit_result = await db.execute(debit_stmt)
    credit_result = await db.execute(credit_stmt)
    
    debit_total = debit_result.scalar_one_or_none() or 0.0
    credit_total = credit_result.scalar_one_or_none() or 0.0
    
    # Check if they match (with a small tolerance for floating point precision)
    is_balanced = abs(debit_total - credit_total) < 0.01
    
    return {
        "debit_total": debit_total,
        "credit_total": credit_total,
        "is_balanced": is_balanced
    }


async def get_variance_analysis(db: AsyncSession, threshold: float = 5.0) -> dict:
    """
    Performs variance analysis between current year and previous year balance columns.
    This is a read-only operation that does not modify the database.

    Args:
        db: Async database session (read-only)
        threshold: Percentage threshold for variance detection (default 5%)

    Returns:
        dict: Contains variance analysis results with accounts exceeding threshold
    """
    current_year_model = TrailBalanceCurrentYear
    previous_year_model = TrailBalancePreviousYear
    
    # Get all accounts with their balances from both tables
    current_stmt = select(current_year_model.account_name, current_year_model.balance).distinct()
    previous_stmt = select(previous_year_model.account_name, previous_year_model.balance).distinct()
    
    current_result = await db.execute(current_stmt)
    previous_result = await db.execute(previous_stmt)
    
    current_accounts = {row.account_name: row.balance for row in current_result.fetchall()}
    previous_accounts = {row.account_name: row.balance for row in previous_result.fetchall()}
    
    # Calculate variances for accounts that exist in both tables
    variance_results = []
    all_account_names = set(current_accounts.keys()) | set(previous_accounts.keys())
    
    for account_name in all_account_names:
        current_balance = current_accounts.get(account_name, 0.0)
        previous_balance = previous_accounts.get(account_name, 0.0)
        
        # Calculate variance percentage 
        if previous_balance != 0:
            variance_percentage = round(abs((current_balance - previous_balance) / previous_balance) * 100, 2)
        else:
            variance_percentage = 100.0 if current_balance != 0 else 0.0  # When previous is 0, set to 100% if current is non-zero
        
        if variance_percentage != 0.0:  # Only include accounts with actual change
            variance_results.append({
                'account_name': account_name,
                'current_balance': current_balance,
                'previous_balance': previous_balance,
                'variance_amount': current_balance - previous_balance,
                'variance_percentage': variance_percentage,
                'exceeds_threshold': variance_percentage >= threshold
            })
    
    # Filter only accounts that exceed the threshold
    significant_variances = [v for v in variance_results if v['exceeds_threshold']]
    
    return {
        'total_accounts': len(all_account_names),
        'variance_count': len(significant_variances),
        'threshold_used': threshold,
        'variances_exceeding_threshold': significant_variances
    }