import os

def type_R(name, bits, format_res):
    bits = bits[6:]

    rs = bits[:5]
    bits = bits[5:]

    rt = bits[:5]
    bits = bits[5:]

    rd = bits[:5]
    bits = bits[5:]

    shamt = bits[:5]
    bits = bits[5:]

    func = bits[:6]

    format_res = r_instructions[func]['format_func']
    name = r_instructions[func]['mnemonic']

    return format_res(rs, rt, rd, shamt, name)


def type_I(name, bits, format_res):
    bits = bits[6:]

    rs = bits[:5]
    bits = bits[5:]

    rt = bits[:5]
    bits = bits[5:]

    immediate = bits[:16]

    return format_res(name, rt, rs, immediate)


def type_J(name, bits, format_res):
    bits = bits[6:]
    address = bits[:26]
    return format_J(address)


# Formatters
def format_R_default(rs, rt, rd, shamt, func_name):
    return f'{func_name} {registers[rd]}, {registers[rs]}, {registers[rt]}'


def format_R_shift(rs, rt, rd, shamt, func_name):
    return f'{func_name} {registers[rt]}, {registers[rd]}, {convert_binary_to_decimal(shamt)}'


def format_R_jump(rs, rt, rd, shamt, func_name):
    return f'{func_name} {registers[rs]}'


def format_J(immediate):
    return f'j {convert_binary_to_decimal(immediate)}'


def format_I_load_store(name, rt, rs, immediate):
    return f'{name}, {registers[rt]}, {convert_binary_to_decimal(immediate)}({registers[rs]})'


def format_I_logic_arithmetic(name, rt, rs, immediate):
    return f'{name}, {registers[rt]}, {registers[rs]}, {convert_binary_to_decimal(immediate)}'


def format_I_branch(name, rt, rs, immediate):
    return f'{name}, {registers[rs]}, {registers[rt]}, {convert_binary_to_decimal(immediate)}'


def format_I_branch_single(name, rt, rs, immediate):
    return f'{name} {registers[rs]}, {convert_binary_to_decimal(immediate)}'


# Helper functions
def convert_binary_to_decimal(binary):
    value = int(binary, 2)
    if binary[0] == '1' and len(binary) == 16:
        value -= (1 << 16)
    return str(value)


def process_file(input_path):
    output_lines = []

    try:
        with open(input_path, 'r') as file:
            for line in file:
                line = line.strip()
                if len(line) != 32:
                    continue

                opcode = line[:6]
                if opcode not in instruction_types:
                    output_lines.append("Invalid opcode")
                    continue

                method = instruction_types[opcode]['method']
                name = instruction_types[opcode]['name']
                format_func = instruction_types[opcode]['format_func']

                result = method(name, line, format_func)
                output_lines.append(result)
    except FileNotFoundError:
        print(f"File not found: {input_path}")

    return output_lines


# Instruction tables
r_instructions = {
    '100000': {'mnemonic': 'add', 'format_func': format_R_default},
    '100010': {'mnemonic': 'sub', 'format_func': format_R_default},
    '100100': {'mnemonic': 'and', 'format_func': format_R_default},
    '100101': {'mnemonic': 'or', 'format_func': format_R_default},
    '100110': {'mnemonic': 'xor', 'format_func': format_R_default},
    '000000': {'mnemonic': 'sll', 'format_func': format_R_shift},
    '000010': {'mnemonic': 'srl', 'format_func': format_R_shift},
    '001000': {'mnemonic': 'jr', 'format_func': format_R_jump},
}

instruction_types = {
    # R-type
    '000000': {'method': type_R, 'name': '', 'format_func': None},

    # load/store
    '100000': {'method': type_I, 'name': 'lb', 'format_func': format_I_load_store},
    '100001': {'method': type_I, 'name': 'lh', 'format_func': format_I_load_store},
    '100011': {'method': type_I, 'name': 'lw', 'format_func': format_I_load_store},
    '101000': {'method': type_I, 'name': 'sb', 'format_func': format_I_load_store},
    '101001': {'method': type_I, 'name': 'sh', 'format_func': format_I_load_store},
    '101011': {'method': type_I, 'name': 'sw', 'format_func': format_I_load_store},

    # immediate arithmetic/logical
    '001000': {'method': type_I, 'name': 'addi', 'format_func': format_I_logic_arithmetic},
    '001100': {'method': type_I, 'name': 'andi', 'format_func': format_I_logic_arithmetic},
    '001101': {'method': type_I, 'name': 'ori', 'format_func': format_I_logic_arithmetic},
    '001110': {'method': type_I, 'name': 'xori', 'format_func': format_I_logic_arithmetic},
    '001111': {'method': type_I, 'name': 'liu', 'format_func': format_I_logic_arithmetic},

    # branches
    '000100': {'method': type_I, 'name': 'beq', 'format_func': format_I_branch},
    '000101': {'method': type_I, 'name': 'bne', 'format_func': format_I_branch},
    '000110': {'method': type_I, 'name': 'blez', 'format_func': format_I_branch_single},
    '000111': {'method': type_I, 'name': 'bgtz', 'format_func': format_I_branch_single},

    # jump
    '000010': {'method': type_J, 'name': '', 'format_func': format_J},
}

registers = {
    '00000': '$zero',
    '01000': '$t0', '01001': '$t1', '01010': '$t2', '01011': '$t3',
    '01100': '$t4', '01101': '$t5', '01110': '$t6', '01111': '$t7',
    '10000': '$s0', '10001': '$s1', '10010': '$s2', '10011': '$s3',
    '10100': '$s4', '10101': '$s5', '10110': '$s6', '10111': '$s7',
}


# Main execution
if __name__ == '__main__':
    FILE_PATH = 'D:\\Faculdade\\ArquiteturaComputadores'

    for i in range(1, 11):  # TESTE-01.txt to TESTE-10.txt
        current_file = f'{i:02}'
        input_file = os.path.join(FILE_PATH, f'TESTE-{current_file}.txt')
        output_file = os.path.join(FILE_PATH, f'TESTE-{current_file}-RESULTADO.txt')

        results = process_file(input_file)

        with open(output_file, 'w') as out:
            for line in results:
                out.write(line + '\n')

        print(f'✅ Generated: {output_file}')
