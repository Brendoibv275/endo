// Configuração global para o DataTables
document.addEventListener('DOMContentLoaded', function() {
    // Verifica se o DataTables está carregado
    if (typeof $.fn.DataTable !== 'undefined') {
        // Configura DataTables para todas as tabelas com a classe 'datatable'
        $('.datatable').each(function() {
            $(this).DataTable({
                responsive: true,
                language: {
                    url: '//cdn.datatables.net/plug-ins/1.10.25/i18n/Portuguese-Brasil.json',
                    search: "_INPUT_",
                    searchPlaceholder: "Buscar..."
                },
                dom: '<"top d-flex justify-content-between align-items-center mb-3"fl>rt<"bottom d-flex justify-content-between align-items-center"ip>',
                lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "Todos"]],
                pageLength: 25,
                ordering: true,
                stateSave: true,
                stateDuration: 60 * 60 * 24 * 7, // 1 semana
                columnDefs: [
                    { responsivePriority: 1, targets: 0 }, // ID
                    { responsivePriority: 2, targets: -1 } // Ações (última coluna)
                ],
                initComplete: function() {
                    // Adiciona a classe de estilo do Bootstrap aos elementos do DataTables
                    $('.dataTables_length select').addClass('form-select form-select-sm');
                    $('.dataTables_filter input').addClass('form-control form-control-sm ms-2');
                    $('.dataTables_info').addClass('text-muted');
                    
                    // Personaliza os botões de paginação
                    $('.dataTables_paginate .paginate_button').addClass('page-link');
                    $('.dataTables_paginate').addClass('pagination');
                }
            });
        });
        
        // Configura DataTables para a tabela de pacientes (personalização específica)
        if ($('#pacientes-table').length) {
            $('#pacientes-table').DataTable({
                responsive: true,
                language: {
                    url: '//cdn.datatables.net/plug-ins/1.10.25/i18n/Portuguese-Brasil.json',
                    search: "_INPUT_",
                    searchPlaceholder: "Buscar paciente..."
                },
                dom: '<"top d-flex justify-content-between align-items-center mb-3"fl>rt<"bottom d-flex justify-content-between align-items-center"ip>',
                lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "Todos"]],
                pageLength: 25,
                columnDefs: [
                    { responsivePriority: 1, targets: 1 }, // Nome
                    { responsivePriority: 2, targets: -1 } // Ações
                ],
                ordering: true,
                order: [[1, 'asc']] // Ordenar por nome
            });
        }

        // Configura DataTables para a tabela de fichas clínicas (personalização específica)
        if ($('#fichas-table').length) {
            $('#fichas-table').DataTable({
                responsive: true,
                language: {
                    url: '//cdn.datatables.net/plug-ins/1.10.25/i18n/Portuguese-Brasil.json',
                    search: "_INPUT_",
                    searchPlaceholder: "Buscar ficha..."
                },
                dom: '<"top d-flex justify-content-between align-items-center mb-3"fl>rt<"bottom d-flex justify-content-between align-items-center"ip>',
                lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "Todos"]],
                pageLength: 25,
                columnDefs: [
                    { responsivePriority: 1, targets: 1 }, // Paciente
                    { responsivePriority: 2, targets: 5 }, // Status
                    { responsivePriority: 3, targets: -1 } // Ações
                ],
                ordering: true,
                order: [[3, 'desc']] // Ordenar por data de abertura (decrescente)
            });
        }

        // Configura DataTables para a tabela de sessões (personalização específica)
        if ($('#sessoes-table').length) {
            $('#sessoes-table').DataTable({
                responsive: true,
                language: {
                    url: '//cdn.datatables.net/plug-ins/1.10.25/i18n/Portuguese-Brasil.json',
                    search: "_INPUT_",
                    searchPlaceholder: "Buscar sessão..."
                },
                dom: '<"top d-flex justify-content-between align-items-center mb-3"fl>rt<"bottom d-flex justify-content-between align-items-center"ip>',
                lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "Todos"]],
                pageLength: 25,
                columnDefs: [
                    { responsivePriority: 1, targets: 1 }, // Data
                    { responsivePriority: 2, targets: 2 }, // Paciente
                    { responsivePriority: 3, targets: -1 } // Ações
                ],
                ordering: true,
                order: [[1, 'desc']] // Ordenar por data da sessão (decrescente)
            });
        }
    }
}); 