import os
import fileinput
import re

templates_dir = 'templates/fichas_clinicas/'
files_to_check = [os.path.join(templates_dir, f) for f in os.listdir(templates_dir) if f.endswith('.html')]

replacements = [
    ('{% url \'fichas_clinicas:detail\'', '{% url \'fichas_clinicas:ficha_detail\''),
    ('{% url \'sessao_detalhe\'', '{% url \'fichas_clinicas:sessao_detalhe\''),
    ('{% url \'sessao_editar\'', '{% url \'fichas_clinicas:sessao_update\''),
    ('{% url \'ficha_detalhe\'', '{% url \'fichas_clinicas:ficha_detail\'')
]

for filename in files_to_check:
    print(f'Processing {filename}...')
    changed = False
    
    with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
        for line in file:
            new_line = line
            for old, new in replacements:
                if old in new_line:
                    new_line = new_line.replace(old, new)
                    changed = True
            print(new_line, end='')
    
    if changed:
        print(f'Updated {filename}')
    else:
        print(f'No changes in {filename}') 