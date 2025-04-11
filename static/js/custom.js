// Espera o documento ser carregado
document.addEventListener('DOMContentLoaded', function() {
    // Efeito de fade out para alertas após 5 segundos
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    if (alerts.length > 0) {
        setTimeout(function() {
            alerts.forEach(function(alert) {
                alert.classList.add('fade');
                setTimeout(function() {
                    alert.remove();
                }, 500);
            });
        }, 5000);
    }

    // Adiciona a classe "active" ao link de navegação atual
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(function(link) {
        const href = link.getAttribute('href');
        if (href && currentPath.indexOf(href) === 0) {
            link.classList.add('active');
            // Se estiver em um dropdown, também ativa o dropdown
            const dropdown = link.closest('.dropdown-menu');
            if (dropdown) {
                const toggle = dropdown.previousElementSibling;
                if (toggle && toggle.classList.contains('dropdown-toggle')) {
                    toggle.classList.add('active');
                }
            }
        }
    });

    // Inicializa tooltips para botões de ação
    const actionButtons = document.querySelectorAll('.btn-action');
    actionButtons.forEach(function(button) {
        if (button.title || button.dataset.bsTitle) {
            new bootstrap.Tooltip(button);
        }
    });

    // Adiciona classes de estilo a elementos específicos
    styleSpecificElements();
    
    // Melhora a experiência em formulários
    enhanceFormExperience();
    
    // Adiciona interatividade a tabelas
    enhanceTableExperience();
    
    // Novas funções para mobile
    transformTablesToCardsMobile();
    initBackToTopButton();
    enhanceMobileNavigation();
    makeTablesResponsive();
    
    // Refazer transformações quando a janela for redimensionada
    window.addEventListener('resize', function() {
        // Limpar visualizações existentes
        document.querySelectorAll('.mobile-card-view').forEach(function(container) {
            container.remove();
        });
        
        // Restaurar visibilidade das tabelas
        document.querySelectorAll('table.d-none.d-md-table').forEach(function(table) {
            table.classList.remove('d-none', 'd-md-table');
        });
        
        // Reaplicar transformações
        transformTablesToCardsMobile();
        makeTablesResponsive();
    });
});

// Função para estilizar elementos específicos
function styleSpecificElements() {
    // Adiciona a classe 'sessao-card' aos cards de sessão de atendimento na página de detalhes da ficha
    const sessaoCards = document.querySelectorAll('#sessoes .card');
    sessaoCards.forEach(function(card) {
        card.classList.add('sessao-card');
    });
    
    // Adiciona ícones aos badges de status
    const statusBadges = document.querySelectorAll('.badge');
    statusBadges.forEach(function(badge) {
        if (badge.textContent.trim() === 'Aberta') {
            badge.innerHTML = '<i class="fas fa-folder-open me-1"></i> Aberta';
        } else if (badge.textContent.trim() === 'Em Andamento') {
            badge.innerHTML = '<i class="fas fa-sync-alt me-1"></i> Em Andamento';
        } else if (badge.textContent.trim() === 'Finalizada') {
            badge.innerHTML = '<i class="fas fa-check-circle me-1"></i> Finalizada';
        }
    });
    
    // Adiciona classes de hover aos cards do dashboard
    const dashboardCards = document.querySelectorAll('.col-md-4 .card');
    dashboardCards.forEach(function(card) {
        card.classList.add('dashboard-card');
    });
}

// Função para melhorar a experiência em formulários
function enhanceFormExperience() {
    // Destaca o campo atual quando em foco
    const formInputs = document.querySelectorAll('.form-control, .form-select');
    formInputs.forEach(function(input) {
        input.addEventListener('focus', function() {
            this.closest('.form-group, .mb-3').classList.add('is-focused');
        });
        
        input.addEventListener('blur', function() {
            this.closest('.form-group, .mb-3').classList.remove('is-focused');
        });
    });
    
    // Suaviza a exibição de mensagens de erro em formulários
    const formErrors = document.querySelectorAll('.invalid-feedback, .errorlist');
    formErrors.forEach(function(error) {
        error.style.opacity = '0';
        setTimeout(function() {
            error.style.transition = 'opacity 0.3s ease';
            error.style.opacity = '1';
        }, 100);
    });
    
    // Adiciona contador de caracteres em campos textarea
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(function(textarea) {
        if (!textarea.hasAttribute('maxlength')) return;
        
        const maxLength = parseInt(textarea.getAttribute('maxlength'));
        const wrapper = document.createElement('div');
        wrapper.className = 'textarea-counter-wrapper position-relative';
        
        const counter = document.createElement('small');
        counter.className = 'textarea-counter text-muted position-absolute end-0 bottom-0 pe-2 pb-1';
        counter.textContent = textarea.value.length + '/' + maxLength;
        
        textarea.parentNode.insertBefore(wrapper, textarea);
        wrapper.appendChild(textarea);
        wrapper.appendChild(counter);
        
        textarea.addEventListener('input', function() {
            counter.textContent = this.value.length + '/' + maxLength;
        });
    });
}

// Função para melhorar a experiência em tabelas
function enhanceTableExperience() {
    // Adiciona classe 'table-hover' a todas as tabelas
    const tables = document.querySelectorAll('table:not(.table-hover)');
    tables.forEach(function(table) {
        table.classList.add('table-hover');
    });
    
    // Adiciona tooltip aos botões de ação nas tabelas
    const tableActionButtons = document.querySelectorAll('.table .btn-sm');
    tableActionButtons.forEach(function(button) {
        // Detecta a ação pelo ícone
        if (button.innerHTML.includes('bi-eye') || button.innerHTML.includes('fa-eye')) {
            button.setAttribute('title', 'Visualizar');
            button.classList.add('btn-action');
        } else if (button.innerHTML.includes('bi-pencil') || button.innerHTML.includes('fa-edit')) {
            button.setAttribute('title', 'Editar');
            button.classList.add('btn-action');
        } else if (button.innerHTML.includes('bi-trash') || button.innerHTML.includes('fa-trash')) {
            button.setAttribute('title', 'Excluir');
            button.classList.add('btn-action');
        } else if (button.innerHTML.includes('bi-plus-circle') || button.innerHTML.includes('fa-plus-circle')) {
            button.setAttribute('title', 'Nova Sessão');
            button.classList.add('btn-action');
        } else if (button.innerHTML.includes('bi-folder-open') || button.innerHTML.includes('fa-folder-open')) {
            button.setAttribute('title', 'Ver Ficha');
            button.classList.add('btn-action');
        }
    });
    
    // Adiciona efeito de hover na linha quando o mouse passa por cima
    const tableRows = document.querySelectorAll('.table-hover tbody tr');
    tableRows.forEach(function(row) {
        row.addEventListener('mouseenter', function() {
            this.style.transition = 'background-color 0.2s ease';
        });
    });
}

// Função para transformar tabelas em cards para visualização mobile
function transformTablesToCardsMobile() {
    // Somente executa em telas menores que 768px
    if (window.innerWidth <= 768) {
        document.querySelectorAll('table.table').forEach(function(table) {
            // Não transformar tabelas que já têm uma classe específica
            if (table.classList.contains('no-transform')) return;
            
            // Criar container para cards
            const cardContainer = document.createElement('div');
            cardContainer.className = 'mobile-card-view d-md-none';
            
            // Obter cabeçalhos
            const headers = [];
            table.querySelectorAll('thead th').forEach(function(th) {
                headers.push(th.textContent.trim());
            });
            
            // Criar um card para cada linha
            table.querySelectorAll('tbody tr').forEach(function(row) {
                const card = document.createElement('div');
                card.className = 'card mb-3';
                
                const cardBody = document.createElement('div');
                cardBody.className = 'card-body p-3';
                
                // Variável para armazenar botões encontrados
                const buttonsFound = [];
                
                // Para cada célula, criar um item com label baseado no cabeçalho
                row.querySelectorAll('td').forEach(function(cell, index) {
                    if (headers[index] && !cell.classList.contains('table-mobile-hide')) {
                        // Se a célula contém botões, coletá-los para adicionar ao final
                        if (cell.querySelector('.btn')) {
                            const buttons = cell.querySelectorAll('.btn');
                            buttons.forEach(function(button) {
                                buttonsFound.push(button.cloneNode(true));
                            });
                            
                            // Se a célula só tem botões, não criar o item de texto
                            if (cell.textContent.trim() === '') return;
                        }
                        
                        const item = document.createElement('div');
                        item.className = 'mb-2';
                        
                        const label = document.createElement('strong');
                        label.className = 'text-muted me-2';
                        label.textContent = headers[index] + ':';
                        
                        item.appendChild(label);
                        item.appendChild(document.createTextNode(' ' + cell.textContent.trim()));
                        
                        cardBody.appendChild(item);
                    }
                });
                
                // Se encontramos botões, adicionar ao final do card
                if (buttonsFound.length > 0) {
                    const buttonContainer = document.createElement('div');
                    buttonContainer.className = 'mt-3 d-flex gap-2 justify-content-end';
                    
                    buttonsFound.forEach(function(button) {
                        buttonContainer.appendChild(button);
                    });
                    
                    cardBody.appendChild(buttonContainer);
                }
                
                card.appendChild(cardBody);
                cardContainer.appendChild(card);
            });
            
            // Inserir a visualização em cards após a tabela
            table.parentNode.insertBefore(cardContainer, table.nextSibling);
            
            // Esconder a tabela original em telas pequenas
            table.classList.add('d-none', 'd-md-table');
        });
    }
}

// Função para implementar botão "Voltar ao topo"
function initBackToTopButton() {
    // Criar botão dinamicamente se não existir
    let backToTopButton = document.getElementById('backToTop');
    
    if (!backToTopButton) {
        backToTopButton = document.createElement('button');
        backToTopButton.id = 'backToTop';
        backToTopButton.className = 'btn btn-primary rounded-circle position-fixed d-md-none';
        backToTopButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
        backToTopButton.style.cssText = 'bottom: 20px; right: 20px; width: 50px; height: 50px; display: none; z-index: 1000;';
        document.body.appendChild(backToTopButton);
    }
    
    // Mostrar o botão quando rolar 300px
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.style.display = 'flex';
            backToTopButton.style.justifyContent = 'center';
            backToTopButton.style.alignItems = 'center';
        } else {
            backToTopButton.style.display = 'none';
        }
    });
    
    // Scrollar para o topo quando clicado
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Função para otimizar navegação mobile
function enhanceMobileNavigation() {
    // Fechar menu ao clicar em um item de navegação
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const navbarToggler = document.querySelector('.navbar-toggler');
    
    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            if (window.innerWidth < 992 && navbarCollapse.classList.contains('show')) {
                navbarToggler.click();
            }
        });
    });
}

// Função para tornar tabelas responsivas automaticamente
function makeTablesResponsive() {
    document.querySelectorAll('table:not(.table-responsive)').forEach(function(table) {
        if (!table.parentElement.classList.contains('table-responsive')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'table-responsive';
            table.parentNode.insertBefore(wrapper, table);
            wrapper.appendChild(table);
        }
    });
} 