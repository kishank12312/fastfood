def PriceList(SeparateOrders):
    result = []
    for order in SeparateOrders:
        currentPrice = 0
        for obj in order:
            currentPrice += obj.ItemPrice
        result.append(currentPrice)
    
    return result