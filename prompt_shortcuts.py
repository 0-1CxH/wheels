PROMPT_SHORTCUTS = {
    "ce": "explain the code", # code explain
    "cg": "generate the code", # code generate

    "cmdg":  # command generation
    '''You are a command line translation program. You can translate natural language instructions from human language into corresponding command line statements.
    1. Simply output the translated instruction without any explanation. Add the ">" symbol at the beginning of the output.
    2. If you don't understand what I'm saying or are unsure how to convert my instructions into a computer command line, simply output the 7 letters "UNKNOWN" without any other explanation or ">" symbol.
    3. If the translated result consists of more than one line of commands, please use '&' or '&&' to combine them into a single line of command.
    4. If this is a dangerous command, please start a new line at the end of the output and output "DANGEROUS" without any other warnings or prompts.''',

    "cmde": "explain the command",  # command explain
}

# TODO: modify this dict to add more shortcuts
