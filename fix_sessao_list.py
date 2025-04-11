with open('templates/fichas_clinicas/sessao_list.html', 'r', encoding='utf-8') as file:
    content = file.read()

# Substituir url 'sessao_detalhe' por 'fichas_clinicas:sessao_detalhe'
content = content.replace("'fichas_clinicas:sessao_detalhe'", "'fichas_clinicas:sessao_detalhe'")

with open('templates/fichas_clinicas/sessao_list.html', 'w', encoding='utf-8') as file:
    file.write(content)

print("Arquivo templates/fichas_clinicas/sessao_list.html foi atualizado com sucesso.") 