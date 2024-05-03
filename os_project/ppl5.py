def parse_expression(tokens, memory):
    if len(tokens) == 1:
        try:
            return int(tokens[0])
        except ValueError:
            return memory[-1]  # Handling 'LAST'
    elif 'IF' in tokens:
        token = ",".join(str(ele) for ele in tokens)
        exp = token.split(",")
        print(exp)
        cond = parse_expression(exp[0][3:].replace(',', '').split(), memory)
        if cond>0:
            return parse_expression(exp[1].replace(',', '').split(), memory)
        else:
            return parse_expression(exp[2].replace(',', '').split(), memory)

    elif '+' in tokens:
        plus_index = tokens.index('+')
        left = parse_expression(tokens[:plus_index], memory)
        right = parse_expression(tokens[plus_index+1:], memory)
        return left + right

def parse_sequence(tokens, memory):
    results = []
    while tokens:
        if 'TOTAL' in tokens:
            total_index = tokens.index('TOTAL')
            expr_result = parse_expression(tokens[:total_index], memory)
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
