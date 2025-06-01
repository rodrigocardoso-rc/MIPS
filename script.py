import os

# ========== Utility ==========
def convert_binary_to_decimal(binary: str):
    value = int(binary, 2)
    if binary[0] == '1' and len(binary) == 16:
        value -= (1 << 16)
    return str(value)

# ========== Instruction Parsers ==========
def parse_r_type(_, bits, _format):
    rs = bits[6:11]
    rt = bits[11:16]
    rd = bits[16:21]
    shamt = bits[21:26]
    func = bits[26:32]

    fmt = r_instructions[func]
    return fmt['format'](rs, rt, rd, shamt, fmt['mnemonic'])

def parse_i_type(name, bits, fmt):
    rs = bits[6:11]
    rt = bits[11:16]
    imm = bits[16:32]

    return fmt(name, rt, rs, imm)

def parse_j_type(_, bits, fmt):
    return fmt(bits[6:32])

# ========== Formatters ==========
def fmt_r_default(rs, rt, rd, _, name):
    return f"{name} {registers[rd]}, {registers[rs]}, {registers[rt]}"

def fmt_r_shift(_, rt, rd, shamt, name):
    return f"{name} {registers[rt]}, {registers[rd]}, {convert_binary_to_decimal(shamt)}"

def fmt_r_jump(rs, *_):
    return f"jr {registers[rs]}"

def fmt_j_target(address):
    return f"j {convert_binary_to_decimal(address)}"

def fmt_i_mem(name, rt, rs, imm):
    return f"{name}, {registers[rt]}, {convert_binary_to_decimal(imm)}({registers[rs]})"

def fmt_i_arith(name, rt, rs, imm):
    return f"{name}, {registers[rt]}, {registers[rs]}, {convert_binary_to_decimal(imm)}"

def fmt_i_branch(name, rt, rs, imm):
    return f"{name}, {registers[rs]}, {registers[rt]}, {convert_binary_to_decimal(imm)}"

def fmt_i_branch_single(name, _, rs, imm):
    return f"{name} {registers[rs]}, {convert_binary_to_decimal(imm)}"

# ========== Decoding ==========
def decode_instruction(binary_line):
    opcode = binary_line[:6]
    instruction = instruction_set.get(opcode)
    if not instruction:
        return "Invalid opcode"

    return instruction['parser'](instruction['name'], binary_line, instruction['format'])

# ========== Processing ==========
def process_file(path):
    results = []
    try:
        with open(path, 'r') as file:
            for line in file:
                line = line.strip()
                if len(line) == 32:
                    results.append(decode_instruction(line))
    except FileNotFoundError:
        print(f"❌ File not found: {path}")
    return results

# ========== Instruction Tables ==========
r_instructions = {
    '100000': {'mnemonic': 'add',  'format': fmt_r_default},
    '100010': {'mnemonic': 'sub',  'format': fmt_r_default},
    '100100': {'mnemonic': 'and',  'format': fmt_r_default},
    '100101': {'mnemonic': 'or',   'format': fmt_r_default},
    '100110': {'mnemonic': 'xor',  'format': fmt_r_default},
    '000000': {'mnemonic': 'sll',  'format': fmt_r_shift},
    '000010': {'mnemonic': 'srl',  'format': fmt_r_shift},
    '001000': {'mnemonic': 'jr',   'format': fmt_r_jump},
}

instruction_set = {
    '000000': {'parser': parse_r_type, 'name': '',     'format': None},

    # Memory
    '100000': {'parser': parse_i_type, 'name': 'lb',   'format': fmt_i_mem},
    '100001': {'parser': parse_i_type, 'name': 'lh',   'format': fmt_i_mem},
    '100011': {'parser': parse_i_type, 'name': 'lw',   'format': fmt_i_mem},
    '101000': {'parser': parse_i_type, 'name': 'sb',   'format': fmt_i_mem},
    '101001': {'parser': parse_i_type, 'name': 'sh',   'format': fmt_i_mem},
    '101011': {'parser': parse_i_type, 'name': 'sw',   'format': fmt_i_mem},

    # Arithmetic / Logic
    '001000': {'parser': parse_i_type, 'name': 'addi', 'format': fmt_i_arith},
    '001100': {'parser': parse_i_type, 'name': 'andi', 'format': fmt_i_arith},
    '001101': {'parser': parse_i_type, 'name': 'ori',  'format': fmt_i_arith},
    '001110': {'parser': parse_i_type, 'name': 'xori', 'format': fmt_i_arith},
    '001111': {'parser': parse_i_type, 'name': 'liu',  'format': fmt_i_arith},

    # Branches
    '000100': {'parser': parse_i_type, 'name': 'beq',  'format': fmt_i_branch},
    '000101': {'parser': parse_i_type, 'name': 'bne',  'format': fmt_i_branch},
    '000110': {'parser': parse_i_type, 'name': 'blez', 'format': fmt_i_branch_single},
    '000111': {'parser': parse_i_type, 'name': 'bgtz', 'format': fmt_i_branch_single},

    # Jump
    '000010': {'parser': parse_j_type, 'name': '',     'format': fmt_j_target},
}

registers = {
    '00000': '$zero',

    '01000': '$t0',
    '01001': '$t1',
    '01010': '$t2',
    '01011': '$t3',
    '01100': '$t4',
    '01101': '$t5',
    '01110': '$t6',
    '01111': '$t7',

    '10000': '$s0',
    '10001': '$s1',
    '10010': '$s2',
    '10011': '$s3',
    '10100': '$s4',
    '10101': '$s5',
    '10110': '$s6',
    '10111': '$s7',
}

# ========== Main ==========
if __name__ == '__main__':
    base_path = 'D:\\Faculdade\\ArquiteturaComputadores'

    for i in range(1, 11):  # TESTE-01.txt to TESTE-10.txt
        filename = f'TESTE-{i:02}'
        input_file = os.path.join(base_path, f'{filename}.txt')
        output_file = os.path.join(base_path, f'{filename}-RESULTADO.txt')

        decoded = process_file(input_file)

        with open(output_file, 'w') as out:
            out.write('\n'.join(decoded))

        print(f'✅ Output generated: {output_file}')
