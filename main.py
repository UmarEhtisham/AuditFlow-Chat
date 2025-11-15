from fastmcp import FastMCP
from typing import Literal
from database.queries import get_total, get_account_names, get_gl_accounts, check_total_match, get_variance_analysis
from database.database import get_db_session
from database.schema import TotalResponse, AccountNamesResponse, GlAccountsResponse, TotalMatchResponse, VarianceAnalysisResponse

# Initialize the MCP server
mcp = FastMCP(name="AuditFlow")


@mcp.tool()
async def totalTool(
    table_name: Literal['current_year', 'previous_year'],
    column: Literal['debit', 'credit', 'balance'],
    toolCallId: str = ""

) -> TotalResponse:
    """
    Calculates the total value of a specified column from the given table.
    This is a read-only operation that does not modify the database.
    """
    async with get_db_session() as db:
        total_value = await get_total(db, table_name, column)

    return TotalResponse(
        table_name=table_name,
        column=column,
        total=total_value
    )


@mcp.tool()
async def accountNameTool(
    table_name: Literal['current_year', 'previous_year'],
    toolCallId: str = ""
    ) -> AccountNamesResponse:

    """
    Retrieves all account names from the specified table.
    This is a read-only operation that does not modify the database.
    """
    async with get_db_session() as db:
        account_names = await get_account_names(db, table_name)
        return AccountNamesResponse(account_names=account_names, table_name=table_name)


@mcp.tool()
async def glAccountTool(
    table_name: Literal['current_year', 'previous_year'],
    toolCallId: str = ""
    ) -> GlAccountsResponse:
    """
    Retrieves all GL account numbers from the specified table.
    This is a read-only operation that does not modify the database.
    """
    async with get_db_session() as db:
        gl_accounts = await get_gl_accounts(db, table_name)
        return GlAccountsResponse(gl_accounts=gl_accounts, table_name=table_name)


@mcp.tool()
async def totalMatchTool(
    table_name: Literal['current_year', 'previous_year'],
    toolCallId: str = ""
    ) -> TotalMatchResponse:
    """
    Compares the total debit and total credit of a given table to check if they match.
    This is a read-only operation that does not modify the database.
    """
    async with get_db_session() as db:
        result = await check_total_match(db, table_name)
        return TotalMatchResponse(
            debit_total=result["debit_total"],
            credit_total=result["credit_total"],
            is_balanced=result["is_balanced"],
            table_name=table_name
        )


@mcp.tool()
async def varianceAnalysisTool(
    threshold: float = 5.0,  # Default 5% threshold
    toolCallId: str = ""
    ) -> VarianceAnalysisResponse:
    """
    Performs variance analysis between current year and previous year balance columns.
    This is a read-only operation that does not modify the database.
    """
    async with get_db_session() as db:
        result = await get_variance_analysis(db, threshold)
        return VarianceAnalysisResponse(
            total_accounts=result["total_accounts"],
            variance_count=result["variance_count"],
            threshold_used=result["threshold_used"],
            variances_exceeding_threshold=result["variances_exceeding_threshold"]
        )

if __name__ == "__main__":

    # Run the MCP server
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)