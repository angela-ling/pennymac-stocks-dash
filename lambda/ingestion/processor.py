
def calculate_highest_mover(stock_data_list):
    """
    Inputs: A list of dicts with 'symbol', 'open', and 'close'.
    Output: The single dictionary with the highest percentage change.
    """
    # Calculate the percent change for every stock in the list
    for stock in stock_data_list:
        # Formula: ((Close - Open) / Open) * 100
        change = ((stock['close'] - stock['open']) / stock['open']) * 100
        stock['percent_change'] = round(change, 2)

    # Use max() with a lambda key to find the dictionary with the highest change
    winner = max(stock_data_list, key=lambda x: abs(x['percent_change']))
    
    return winner

if __name__ == "__main__":
    test_data = [
        {"symbol": "AAPL", "open": 100, "close": 105}, # +5.0%
        {"symbol": "TSLA", "open": 100, "close": 85},  # -15.0% (Should Win!)
        {"symbol": "NVDA", "open": 100, "close": 112}  # +12.0%
    ]
    
    winner = calculate_highest_mover(test_data)
    print(f"Winner: {winner['symbol']} with a {winner['percent_change']}% move.")
    
    # Validation
    assert winner['symbol'] == "TSLA", "Logic failed: TSLA should have won with the largest move."