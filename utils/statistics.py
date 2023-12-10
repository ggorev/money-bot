def get_statistics(expenses: list):
    total_amount = sum(amount for category, amount in expenses)
    text = f"\n<b>Общая сумма: {total_amount}</b>₽\n\n"
    for category, amount in expenses:
        percentage = (amount / total_amount) * 100
        text += f"{category}: <b>{amount}</b>₽ ({round(percentage)}%)\n"
    return text
