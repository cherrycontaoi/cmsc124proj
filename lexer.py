import re

construct_regex = {
    # Keywords
    'PROGRAM_START' : r'^HAI',
    'PROGRAM_END' : r'^KTHXBYE',
    'VARIABLE_DECLARATION_PORTION_START' : r'^WAZZUP',
    'VARIABLE_DECLARATION_PORTION_END' : r'^BUHBYE',
    'COMMENT_IDENTIFIER' : r'^BTW',
    'MULTI_COMMENT_DELIM_OP' : r'^OBTW',
    'MULTI_COMMENT_DELIM_CL' : r'^TLDR',
    'VAR_DECLARATION' : r'^I HAS A',
    'VAR_INITIALIZATION' : r'^ITZ',
    'VAR_ASSIGNMENT' : r'^R',
    'ADD_OPERATION' : r'^SUM OF',
    'SUB_OPERATION' : r'^DIFF OF',
    'MUL_OPERATION' : r'^PRODUKT OF',
    'DIV_OPERATION' : r'^QUOSHUNT OF',
    'MOD_OPERATION' : r'^MOD OF',
    'MAX_OPERATION' : r'^BIGGR OF',
    'MIN_OPERATION' : r'^SMALLER OF',
    'AND_OPERATION' : r'^BOTH OF',
    'OR_OPERATION' : r'^EITHER OF',
    'XOR_OPERATION' : r'^WON OF',
    'NOT_OPERATION' : r'^NOT',
    'INF_AND' : r'^ALL OF',
    'INF_OR' : r'^ANY OF',
    'IS_EQUAL' : r'^BOTH SAEM',
    'NOT_EQUAL' : r'^DIFFRINT',
    'STRING_CONCAT' : r'^SMOOSH',
    'CAST_OPERATOR' : r'^MAEK',
    'A_KEYWORD' : r'^A',
    'TYPECAST' : r'^IS NOW A',
    'PRINT_OUTPUT' : r'^VISIBLE',
    'GIVE_INPUT': r'^GIMMEH',
    'IF_DELIMITER_OP' : r'^O RLY\?',
    'IF_STATEMENT' : r'^YA RLY',
    'ELSE_IF_STATEMENT' : r'^MEBBE',
    'ELSE_STATEMENT' : r'^NO WAI',
    'IF_SWITCH_DELIMITER_CL' : r'^OIC',
    'SWITCH_CASE_DELIM_OP' : r'^WTF\?',
    'CASE_STATEMENT' : r'^OMG',
    'DEFAULT_CASE' : r'^OMGWTF',
    'LOOP_DELIM_OP' : r'^IM IN YR',
    'INC_COUNTER' : r'^UPPIN',
    'DEC_COUNTER' : r'^NERFIN',
    'LOOP_COUNTER_KEYWORD' : r'^YR',
    'LOOP_COND_FALSE' : r'^TIL',
    'LOOP_COND_TRUE' : r'^WILE',
    'LOOP_DELIM_CL' : r'^IM OUTTA YR',
    'FUNCTION_DEFINITION_START' : r'^HOW IZ I',
    'FUNCTION_DEFINITION_END' : r'^IF U SAY SO',
    'BREAK_LOOP' : r'^GTFO',
    'RETURN_VALUE_KEYWORD' : r'^FOUND YR',
    'FUNCTION_CALLING' : r'^I IZ',
    'OPERAND_GROUP_CLOSE' : r'^MKAY',
    'SPACE' : r'^ ',
    'NEWLINE' : r'^\n',
        
    
    # Literals
    'INTEGER' : r'^-?(0|[1-9][0-9]*)$',                 # numbr
    'FLOAT' : r'^-?(0|[1-9][0-9]*)?\.[0-9]+',          # numbar
    'STRING' : r'^\"[^\"]*\"',                          # yarn
    'BOOL': r'^WIN|FAIL',                             # troof
    'TYPE' : r'^TROOF|NOOB|NUMBR|NUMBAR|YARN|TYPE',
    'COMMENTSTRING': r"(?<=BTW\s)(.*)",
    'MULTICOMMENTSTRING': r"(?<=OBTW\s)(.*)",
    # Identifier 
    'IDENTIFIER' : r'^[a-zA-Z][a-zA-Z_0-9]*',
}

def create_tokens():
    tokens = []
    with open("code.lol", "r") as f:
        in_multiline_comment = False
        multiline_comment_content = []
        for line in f:
            if in_multiline_comment:
                #case for multi comments ,, check first for the terminating keyword in multi line comments (the string before that is considered as part of the comment)
                if re.match (construct_regex['MULTI_COMMENT_DELIM_CL'], line.strip()):
                    # end of multi line comment
                    in_multiline_comment = False
                    # append the comment content to byline
                    byline.append(['\n'.join(multiline_comment_content).strip(), 'MULTILINE_COMMENT'])
                    byline.append(['TLDR', 'MULTI_COMMENT_END'])
                    multiline_comment_content = []
                    continue
                else:
                    # add the line to the comment content
                    multiline_comment_content.append(line.strip())
                    continue
            byline = []
            line = line.strip()  # remove whitespaces
            while line:
                for pattern_name, pattern in construct_regex.items():
                    match = re.match(pattern, line)
                    if match:
                        token_value = match.group()
                        if pattern_name == 'COMMENT_IDENTIFIER':  # single-line comments
                            byline.append([token_value, 'COMMENT'])
                            comment_match = re.search(construct_regex['COMMENTSTRING'], line)
                            if comment_match:
                                comment_content = comment_match.group().strip()
                                byline.append([comment_content, 'COMMENTSTRING'])
                            line = ""  
                            break
                        elif pattern_name == 'MULTI_COMMENT_DELIM_OP':  # start of multi-line comment
                            in_multiline_comment = True
                            # capture string beside obtw as well
                            comment_content = line[len(token_value):].strip()
                            if comment_content:
                                multiline_comment_content.append(comment_content)
                            byline.append([token_value, 'MULTI_COMMENT_START'])
                            line = ''  # skip the rest of the line after OBTW
                            break
                        elif pattern_name == 'SPACE':  # skip whitespace
                            line = line[len(token_value):]
                            break
                        else:
                            byline.append([token_value, pattern_name])
                            line = line[len(token_value):].lstrip()
                            break
                else:
                    line = line[1:].lstrip()  # unmatched character
            if byline:
                tokens.append(byline)
    return tokens

def print_tokens(tokens):
    for line in tokens:
        for token in line:
            print(token)
        print("")

tokens = create_tokens()
print_tokens(tokens)
