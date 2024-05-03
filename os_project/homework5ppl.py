def evaluate_expression(tokens, memory):
    if len(tokens) == 1:
        try:
            return int(tokens[0])
        except ValueError:
            return memory[-1]  # Handling 'LAST'
    elif 'IF' in tokens:
        if_index = tokens.index('IF')
        cond = evaluate_expression(tokens[if_index+1:if_index+4], memory)
        true_expr = evaluate_expression(tokens[if_index+4:if_index+7], memory)
        false_expr = evaluate_expression(tokens[if_index+7:if_index+10], memory)
        return true_expr if cond > 0 else false_expr
    elif '+' in tokens:
        plus_index = tokens.index('+')
        left = evaluate_expression(tokens[:plus_index], memory)
        right = evaluate_expression(tokens[plus_index+1:], memory)
        return left + right

def parse_sequence(tokens, memory):
    results = []
    while tokens:
        if 'TOTAL' in tokens:
            total_index = tokens.index('TOTAL')
            expr_result = evaluate_expression(tokens[:total_index], memory)
            results.append(expr_result)
            memory.append(expr_result)  # Update memory with the last result
            tokens = tokens[total_index+1:]
            if tokens and tokens[0] == 'OFF':
                break
        else:
            break
    return results

def parse_program(tokens):
    if tokens[0] == 'ON':
        return parse_sequence(tokens[1:], [])

def execute_calculator_program(program):
    tokens = program.replace(',', '').split()
    results = parse_program(tokens)
    for result in results:
        print(result)

# Example program, formatted as in your problem statement
program = """
ON
3 + 4
TOTAL
1 + LAST
TOTAL
IF LAST + 1, 2 + 3, 4 + 5
TOTAL
OFF
"""

execute_calculator_program(program)
